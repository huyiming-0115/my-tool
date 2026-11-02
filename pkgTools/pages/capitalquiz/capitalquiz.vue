<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u4e16\u754c\u9996\u90fd\u6311\u6218</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="score-row"><text>\u5f97\u5206: {{ score }}</text><text>{{ current+1 }}/{{ total }}</text></view>
      <view class="question-card" v-if="current < total">
        <text class="question-country">{{ countries[current].country }}</text>
        <text class="question-label">\u9996\u90fd\u662f\uff1f</text>
        <view class="options-grid">
          <text class="opt-btn" v-for="(opt, i) in countries[current].opts" :key="i" :class="{correct: showAnswer && opt===countries[current].capital, wrong: showAnswer && selected===i && opt!==countries[current].capital}" @click="answer(i)">{{ opt }}</text>
        </view>
        <text class="next-btn" v-if="showAnswer" @click="next">\u4e0b\u4e00\u9898 \u2192</text>
      </view>
      <view class="result-card" v-else>
        <text class="result-title">\u6311\u6218\u5b8c\u6210!</text>
        <text class="result-score">{{ score }} / {{ total }}</text>
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
const allCountries = [
  {country:"\u4e2d\u56fd", capital:"\u5317\u4eac"}, {country:"\u7f8e\u56fd", capital:"\u534e\u76db\u987f"},
  {country:"\u65e5\u672c", capital:"\u4e1c\u4eac"}, {country:"\u97e9\u56fd", capital:"\u9996\u5c14"},
  {country:"\u82f1\u56fd", capital:"\u4f26\u6566"}, {country:"\u6cd5\u56fd", capital:"\u5df4\u9ece"},
  {country:"\u5fb7\u56fd", capital:"\u67cf\u6797"}, {country:"\u610f\u5927\u5229", capital:"\u7f57\u9a6c"},
  {country:"\u4fc4\u7f57\u65af", capital:"\u83ab\u65af\u79d1"}, {country:"\u52a0\u62ff\u5927", capital:"\u6e25\u592a\u534e"},
  {country:"\u6fb3\u5927\u5229\u4e9a", capital:"\u585e\u5c14\u5361"}, {country:"\u5df4\u897f", capital:"\u5df4\u897f\u5229\u4e9a"},
  {country:"\u5370\u5ea6", capital:"\u65b0\u5fb7\u91cc"}, {country:"\u897f\u73ed\u7259", capital:"\u9a6c\u5fb7\u91cc"},
  {country:"\u571f\u8033\u5176", capital:"\u5b89\u5361\u62c9"}, {country:"\u8377\u5170", capital:"\u963f\u59c6\u65af\u7279\u4e39"}
]
const countries = ref([])
function shuffle(a) { return a.sort(function() { return Math.random() - 0.5 }) }
function genQuiz() {
  var picked = shuffle(allCountries.slice()).slice(0, total.value)
  countries.value = picked.map(function(c) {
    var opts = [c.capital]
    while (opts.length < 4) { var r = allCountries[Math.floor(Math.random()*allCountries.length)].capital; if (opts.indexOf(r) === -1) opts.push(r) }
    return { country: c.country, capital: c.capital, opts: shuffle(opts) }
  })
}
function answer(i) {
  if (showAnswer.value) return
  selected.value = i
  showAnswer.value = true
  if (countries.value[current.value].opts[i] === countries.value[current.value].capital) score.value++
}
function next() { current.value++; selected.value = -1; showAnswer.value = false }
function restart() { score.value = 0; current.value = 0; selected.value = -1; showAnswer.value = false; genQuiz() }
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }; genQuiz() })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #667eea, #764ba2); }
.custom-nav { background: linear-gradient(135deg, #5a67d8, #6b46c1); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.score-row { display: flex; justify-content: space-between; color: #fff; font-size: 28rpx; margin-bottom: 24rpx; }
.question-card { background: #fff; border-radius: 24rpx; padding: 40rpx; text-align: center; }
.question-country { font-size: 48rpx; font-weight: 700; color: #333; display: block; }
.question-label { font-size: 26rpx; color: #999; display: block; margin-bottom: 24rpx; }
.options-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16rpx; }
.opt-btn { padding: 24rpx; border-radius: 16rpx; background: #f8f8f8; font-size: 28rpx; }
.opt-btn.correct { background: #00b894; color: #fff; }
.opt-btn.wrong { background: #e17055; color: #fff; }
.next-btn { display: inline-block; margin-top: 24rpx; padding: 16rpx 32rpx; background: #5a67d8; color: #fff; border-radius: 12rpx; font-size: 26rpx; }
.result-card { background: #fff; border-radius: 24rpx; padding: 60rpx; text-align: center; }
.result-title { font-size: 36rpx; color: #333; display: block; }
.result-score { font-size: 64rpx; font-weight: 700; color: #5a67d8; display: block; margin: 16rpx 0; }
.restart-btn { display: inline-block; padding: 20rpx 40rpx; background: #5a67d8; color: #fff; border-radius: 12rpx; font-size: 28rpx; }
</style>
