<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u82f1\u8bed\u8bcd\u6c47\u6d4b\u8bd5</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="score-row"><text>\u5f97\u5206: {{ score }}</text><text>{{ current+1 }}/{{ total }}</text></view>
      <view class="question-card" v-if="current < total">
        <text class="question-word">{{ words[current].en }}</text>
        <view class="options-grid">
          <text class="opt-btn" v-for="(opt, i) in words[current].opts" :key="i" :class="{correct: showAnswer && opt===words[current].cn, wrong: showAnswer && selected===i && opt!==words[current].cn}" @click="answer(i)">{{ opt }}</text>
        </view>
        <text class="next-btn" v-if="showAnswer" @click="next">\u4e0b\u4e00\u9898 \u2192</text>
      </view>
      <view class="result-card" v-else>
        <text class="result-title">\u6d4b\u8bd5\u5b8c\u6210!</text>
        <text class="result-score">{{ score }} / {{ total }}</text>
        <text class="result-msg">{{ score >= total*0.8 ? '\u4f18\u79c0!' : score >= total*0.6 ? '\u4e0d\u9519!' : '\u7ee7\u7eed\u52aa\u529b!' }}</text>
        <text class="restart-btn" @click="restart">\u91cd\u65b0\u5f00\u59cb</text>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const score = ref(0)
const current = ref(0)
const total = ref(10)
const selected = ref(-1)
const showAnswer = ref(false)
const allWords = [
  {en:"apple", cn:"\u82f9\u679c"}, {en:"banana", cn:"\u9999\u8549"}, {en:"cat", cn:"\u732b"},
  {en:"dog", cn:"\u72d7"}, {en:"elephant", cn:"\u5927\u8c61"}, {en:"fish", cn:"\u9c7c"},
  {en:"good", cn:"\u597d"}, {en:"happy", cn:"\u5feb\u4e50"}, {en:"internet", cn:"\u4e92\u8054\u7f51"},
  {en:"jump", cn:"\u8df3"}, {en:"king", cn:"\u56fd\u738b"}, {en:"love", cn:"\u7231"},
  {en:"money", cn:"\u94b1"}, {en:"name", cn:"\u540d\u5b57"}, {en:"open", cn:"\u6253\u5f00"},
  {en:"pen", cn:"\u7b14"}, {en:"queen", cn:"\u738b\u540e"}, {en:"run", cn:"\u8dd1"},
  {en:"sun", cn:"\u592a\u9633"}, {en:"time", cn:"\u65f6\u95f4"}
]
const words = ref([])
function shuffle(a) { return a.sort(function() { return Math.random() - 0.5 }) }
function genWords() {
  var picked = shuffle(allWords.slice()).slice(0, total.value)
  words.value = picked.map(function(w) {
    var opts = [w.cn]
    while (opts.length < 4) { var r = allWords[Math.floor(Math.random()*allWords.length)].cn; if (opts.indexOf(r) === -1) opts.push(r) }
    return { en: w.en, cn: w.cn, opts: shuffle(opts) }
  })
}
function answer(i) {
  if (showAnswer.value) return
  selected.value = i
  showAnswer.value = true
  if (words.value[current.value].opts[i] === words.value[current.value].cn) score.value++
}
function next() { current.value++; selected.value = -1; showAnswer.value = false }
function restart() { score.value = 0; current.value = 0; selected.value = -1; showAnswer.value = false; genWords() }
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }; genWords() })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #f093fb, #f5576c); }
.custom-nav { background: linear-gradient(135deg, #e84393, #fd79a8); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.score-row { display: flex; justify-content: space-between; color: #fff; font-size: 28rpx; margin-bottom: 24rpx; }
.question-card { background: #fff; border-radius: 24rpx; padding: 40rpx; text-align: center; }
.question-word { font-size: 48rpx; font-weight: 700; color: #333; display: block; margin-bottom: 32rpx; }
.options-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16rpx; }
.opt-btn { padding: 24rpx; border-radius: 16rpx; background: #f8f8f8; font-size: 28rpx; color: #333; }
.opt-btn.correct { background: #00b894; color: #fff; }
.opt-btn.wrong { background: #e17055; color: #fff; }
.next-btn { display: inline-block; margin-top: 24rpx; padding: 16rpx 32rpx; background: #e84393; color: #fff; border-radius: 12rpx; font-size: 26rpx; }
.result-card { background: #fff; border-radius: 24rpx; padding: 60rpx; text-align: center; }
.result-title { font-size: 36rpx; font-weight: 700; color: #333; display: block; }
.result-score { font-size: 64rpx; font-weight: 700; color: #e84393; display: block; margin: 16rpx 0; }
.result-msg { font-size: 28rpx; color: #666; display: block; margin-bottom: 24rpx; }
.restart-btn { display: inline-block; padding: 20rpx 40rpx; background: #e84393; color: #fff; border-radius: 12rpx; font-size: 28rpx; }
</style>
