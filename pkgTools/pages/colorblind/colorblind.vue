
<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">色盲测试</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="cb-intro">
        <text class="cb-intro-text">石原氏色盲检测图是最常用的色盲检测方法。观察下图中的数字或图案。</text>
      </view>
      <view class="cb-plate" :style="{background: currentPlate.bg}">
        <text class="cb-number" :style="{color: currentPlate.fg}">{{currentPlate.text}}</text>
      </view>
      <view class="cb-answer">
        <text class="cb-answer-label">你看到的数字是？</text>
        <input class="cb-input" type="number" v-model="userAnswer" placeholder="输入数字" />
      </view>
      <view class="cb-btn" @click="checkAnswer"><text>确认</text></view>
      <view class="cb-result" v-if="showResult">
        <text class="cb-result-text" :class="{correct: isCorrect}">{{resultText}}</text>
      </view>
      <view class="cb-nav">
        <view class="cb-nav-btn" @click="prevPlate"><text>上一题</text></view>
        <view class="cb-nav-btn" @click="nextPlate"><text>下一题</text></view>
      </view>
      <view class="cb-score">得分: {{score}} / {{totalAnswered}}</view>
    </view>
  </view>
</template>
<script setup>
import { ref, reactive, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const plates = [
  {text:"8", bg:"radial-gradient(circle, #e74c3c 30%, #27ae60 30%)", answer:"8", fg:"#e74c3c"},
  {text:"6", bg:"radial-gradient(circle, #3498db 30%, #f39c12 30%)", answer:"6", fg:"#3498db"},
  {text:"29", bg:"radial-gradient(circle, #e67e22 25%, #1abc9c 25%)", answer:"29", fg:"#e67e22"},
  {text:"5", bg:"radial-gradient(circle, #9b59b6 30%, #2ecc71 30%)", answer:"5", fg:"#9b59b6"},
  {text:"74", bg:"radial-gradient(circle, #16a085 25%, #c0392b 25%)", answer:"74", fg:"#16a085"}
]
const currentIdx = ref(0)
const currentPlate = ref(plates[0])
const userAnswer = ref("")
const showResult = ref(false)
const isCorrect = ref(false)
const resultText = ref("")
const score = ref(0)
const totalAnswered = ref(0)
function checkAnswer() {
  if (!userAnswer.value) return
  totalAnswered.value++
  isCorrect.value = userAnswer.value === currentPlate.value.answer
  if (isCorrect.value) score.value++
  resultText.value = isCorrect.value ? "回答正确!" : "正确答案: " + currentPlate.value.answer
  showResult.value = true
}
function nextPlate() {
  currentIdx.value = (currentIdx.value + 1) % plates.length
  currentPlate.value = plates[currentIdx.value]
  reset()
}
function prevPlate() {
  currentIdx.value = (currentIdx.value - 1 + plates.length) % plates.length
  currentPlate.value = plates[currentIdx.value]
  reset()
}
function reset() {
  userAnswer.value = ""
  showResult.value = false
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #ff6b6b, #feca57); }
.custom-nav { background: linear-gradient(135deg, #ff6b6b, #feca57); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 32rpx; }
.cb-intro { background: rgba(255,255,255,0.2); border-radius: 16rpx; padding: 20rpx; margin-bottom: 24rpx; }
.cb-intro-text { color: rgba(255,255,255,0.9); font-size: 26rpx; line-height: 1.6; }
.cb-plate { width: 400rpx; height: 400rpx; border-radius: 50%; margin: 0 auto 32rpx; display: flex; align-items: center; justify-content: center; box-shadow: 0 8rpx 32rpx rgba(0,0,0,0.2); }
.cb-number { font-size: 120rpx; font-weight: 900; }
.cb-answer { margin-bottom: 20rpx; }
.cb-answer-label { color: rgba(255,255,255,0.8); font-size: 26rpx; display: block; margin-bottom: 12rpx; }
.cb-input { background: rgba(255,255,255,0.3); border-radius: 12rpx; padding: 16rpx 24rpx; font-size: 32rpx; color: #fff; font-weight: 600; }
.cb-btn { background: #fff; border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 20rpx; }
.cb-btn text { color: #ff6b6b; font-size: 32rpx; font-weight: 700; }
.cb-result { text-align: center; margin-bottom: 20rpx; }
.cb-result-text { color: #fff; font-size: 30rpx; font-weight: 600; }
.cb-result-text.correct { color: #2ecc71; }
.cb-nav { display: flex; gap: 20rpx; margin-bottom: 20rpx; }
.cb-nav-btn { flex: 1; text-align: center; padding: 16rpx; background: rgba(255,255,255,0.2); border-radius: 16rpx; }
.cb-nav-btn text { color: #fff; font-size: 28rpx; }
.cb-score { text-align: center; color: #fff; font-size: 28rpx; font-weight: 600; }
</style>
