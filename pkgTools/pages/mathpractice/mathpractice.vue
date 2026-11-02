<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u6570\u5b66\u53e3\u7b97\u7ec3\u4e60</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="setting-row">
        <text class="set-item" :class="{active: level===1}" @click="level=1">\u7b97\u672f</text>
        <text class="set-item" :class="{active: level===2}" @click="level=2">\u52a0\u51cf</text>
        <text class="set-item" :class="{active: level===3}" @click="level=3">\u4e58\u9664</text>
        <text class="set-item" :class="{active: level===4}" @click="level=4">\u6df7\u5408</text>
      </view>
      <view class="score-row"><text>\u5f97\u5206: {{ score }}</text><text>\u65f6\u95f4: {{ timeLeft }}s</text></view>
      <view class="question-card" v-if="timeLeft > 0">
        <text class="question-text">{{ num1 }} {{ op }} {{ num2 }} = ?</text>
        <input class="answer-input" type="number" v-model="userAnswer" @confirm="submit" />
        <text class="submit-btn" @click="submit">\u786e\u5b9a</text>
      </view>
      <view class="result-card" v-else>
        <text class="result-title">\u65f6\u95f4\u5230!</text>
        <text class="result-score">{{ score }} \u5206</text>
        <text class="restart-btn" @click="start">\u518d\u6765\u4e00\u8f6e</text>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const level = ref(2)
const score = ref(0)
const timeLeft = ref(60)
const num1 = ref(0)
const num2 = ref(0)
const op = ref("+")
const userAnswer = ref("")
let timer = null
function genQuestion() {
  var ops = ["+","-","\u00d7","\u00f7"]
  var o = level.value === 1 ? (Math.random()>0.5?"+":"-") : level.value === 2 ? (Math.random()>0.5?"+":"-") : level.value === 3 ? (Math.random()>0.5?"\u00d7":"\u00f7") : ops[Math.floor(Math.random()*4)]
  op.value = o
  var a = Math.floor(Math.random()*50+1)
  var b = Math.floor(Math.random()*50+1)
  if (o === "\u00d7") { a = Math.floor(Math.random()*12+1); b = Math.floor(Math.random()*12+1) }
  if (o === "\u00f7") { b = Math.floor(Math.random()*12+1); a = b * Math.floor(Math.random()*12+1) }
  if (o === "-" && a < b) { var t = a; a = b; b = t }
  num1.value = a; num2.value = b
}
function submit() {
  var ans = 0
  if (op.value === "+") ans = num1.value + num2.value
  else if (op.value === "-") ans = num1.value - num2.value
  else if (op.value === "\u00d7") ans = num1.value * num2.value
  else ans = num1.value / num2.value
  if (parseFloat(userAnswer.value) === ans) score.value += 10
  userAnswer.value = ""
  genQuestion()
}
function start() {
  score.value = 0; timeLeft.value = 60
  genQuestion()
  timer = setInterval(function() { timeLeft.value--; if (timeLeft.value <= 0) clearInterval(timer) }, 1000)
}
function goBack() { clearInterval(timer); uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }; start() })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #4facfe, #00f2fe); }
.custom-nav { background: linear-gradient(135deg, #0984e3, #00cec9); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.setting-row { display: flex; gap: 12rpx; margin-bottom: 24rpx; }
.set-item { flex: 1; text-align: center; padding: 16rpx; border-radius: 12rpx; background: rgba(255,255,255,0.3); color: #fff; font-size: 24rpx; }
.set-item.active { background: #fff; color: #0984e3; }
.score-row { display: flex; justify-content: space-between; color: #fff; font-size: 28rpx; margin-bottom: 24rpx; font-weight: 600; }
.question-card { background: #fff; border-radius: 24rpx; padding: 60rpx 40rpx; text-align: center; }
.question-text { font-size: 60rpx; font-weight: 700; color: #333; display: block; margin-bottom: 32rpx; }
.answer-input { width: 100%; background: #f8f8f8; border-radius: 16rpx; padding: 24rpx; font-size: 36rpx; text-align: center; margin-bottom: 24rpx; }
.submit-btn { display: inline-block; padding: 20rpx 60rpx; background: #0984e3; color: #fff; border-radius: 12rpx; font-size: 28rpx; }
.result-card { background: #fff; border-radius: 24rpx; padding: 60rpx; text-align: center; }
.result-title { font-size: 36rpx; color: #333; display: block; }
.result-score { font-size: 80rpx; font-weight: 700; color: #0984e3; display: block; margin: 16rpx 0; }
.restart-btn { display: inline-block; padding: 20rpx 40rpx; background: #0984e3; color: #fff; border-radius: 12rpx; font-size: 28rpx; }
</style>
