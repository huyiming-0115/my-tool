<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">←</text>
        <text class="nav-title">猜数字</text>
        <text class="nav-icon" @click="resetGame">↻</text>
      </view>
    </view>
    <view class="content">
      <view class="info-card">
        <text class="info-text">数字范围: 1 - 100</text>
      </view>
      <view class="input-area">
        <input class="guess-input" type="number" v-model="currentGuess" placeholder="输入你的猜测..." />
        <view class="btn guess-btn" @click="submitGuess"><text class="btn-text">确定</text></view>
      </view>
      <view class="status-card">
        <text class="status-text">{{ statusText }}</text>
      </view>
      <view class="stats-row">
        <view class="stat-item">
          <text class="stat-label">尝试次数</text>
          <text class="stat-value">{{ attempts }}</text>
        </view>
        <view class="stat-item">
          <text class="stat-label">最佳记志</text>
          <text class="stat-value">{{ bestScore || '-' }}</text>
        </view>
      </view>
      <view class="history-card">
        <text class="history-title">历史记志</text>
        <view class="history-list">
          <view v-for="(item, idx) in history" :key="idx" class="history-item">
            <text class="history-num">#{{ idx + 1 }}</text>
            <text class="history-guess">{{ item.guess }}</text>
            <text class="history-hint":class="item.hintClass">{{ item.hint }}</text>
          </view>
          <view v-if="history.length === 0" class="history-empty">
            <text>输入数字开始挑戏！</text>
          </view>
        </view>
      </view>
      <view class="btn-area">
        <view class="btn" @click="resetGame"><text class="btn-text">新游戏</text></view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, computed, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
function goBack() { uni.navigateBack() }

const target = ref(0)
const currentGuess = ref("")
const attempts = ref(0)
const history = ref([])
const gameWon = ref(false)
const bestScore = ref(0)

const statusText = computed(() => {
  if (gameWon.value) {

const statusText = computed(() => {
  if (gameWon.value) {

const statusText = computed(() => {
  if (gameWon.value) {
    return '恭喜！你用了 '+attempts.value+' 次猜中！'
  }
  if (attempts.value === 0) {
    return '请输入一个 1-100 的数字'
  }
  const last = history.value[history.value.length - 1]
  return last ? last.hint : '继续挑戏...'
})

function submitGuess() {
  const guess = parseInt(currentGuess.value)
  if (isNaN(guess) || guess < 1 || guess > 100) {
    uni.showToast({ title: '请输入1-100的数字!', icon: 'none' })
    return
  }
  attempts.value++
  let hint = ''  let hintClass = ''  if (guess === target.value) {
    hint = '正确！'
    hintClass = 'hint-correct'    gameWon.value = true
    if (!bestScore.value || attempts.value < bestScore.value) {
      bestScore.value = attempts.value
      uni.setStorageSync('guessnum_best', bestScore.value)
    }
  } else if (guess < target.value) {
    hint = '太小了！'
    hintClass = 'hint-low'  } else {
    hint = '太大了！'
    hintClass = 'hint-high'  }
  history.value.push({ guess, hint, hintClass })
  currentGuess.value = ''}

function resetGame() {
  target.value = Math.floor(Math.random() * 100) + 1
  currentGuess.value = ''  attempts.value = 0
  history.value = []
  gameWon.value = false
}

onMounted(function() {
  if (!uni.getStorageSync("isLoggedIn")) {
    uni.reLaunch({ url: "/pages/login/login" })
    return
  }
  bestScore.value = uni.getStorageSync('guessnum_best') || 0
  resetGame()
})
</script>
<style scoped>
.page { min-height: 100vh; background: #f5f7fb }
.custom-nav { background: linear-gradient(135deg, #10b981, #34d399); width: 100% }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx }
.nav-icon { width: 72rpx; text-align: center; font-size: 44rpx; color: #fff; font-weight: 700; flex-shrink: 0 }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600 }
.content { padding: 24rpx }
.info-card { background: #fff; border-radius: 16rpx; padding: 24rpx; margin-bottom: 24rpx; text-align: center; box-shadow: 0 2rpx 12rpx rgba(0,0,0,0.06) }
.info-text { font-size: 28rpx; color: #333; font-weight: 600 }
.input-area { display: flex; gap: 16rpx; margin-bottom: 24rpx }
.guess-input { flex: 1; background: #fff; border-radius: 12rpx; padding: 20rpx 24rpx; font-size: 32rpx; border: 2rpx solid #e2e8f0 }
.guess-btn { padding: 20rpx 32rpx }
.status-card { background: #fff; border-radius: 16rpx; padding: 24rpx; margin-bottom: 24rpx; text-align: center; box-shadow: 0 2rpx 12rpx rgba(0,0,0,0.06) }
.status-text { font-size: 32rpx; font-weight: 600; color: #333 }
.stats-row { display: flex; gap: 24rpx; margin-bottom: 24rpx }
.stat-item { flex: 1; background: #fff; border-radius: 16rpx; padding: 20rpx; text-align: center; box-shadow: 0 2rpx 12rpx rgba(0,0,0,0.06) }
.stat-label { font-size: 24rpx; color: #888; margin-bottom: 8rpx }
.stat-value { font-size: 36rpx; font-weight: 700; color: #10b981 }
.history-card { background: #fff; border-radius: 16rpx; padding: 24rpx; margin-bottom: 24rpx; box-shadow: 0 2rpx 12rpx rgba(0,0,0,0.06) }
.history-title { font-size: 28rpx; font-weight: 600; color: #333; margin-bottom: 16rpx }
.history-list { max-height: 400rpx; overflow-y: auto }
.history-item { display: flex; align-items: center; padding: 12rpx 0; border-bottom: 1rpx solid #f0f0f0 }
.history-num { font-size: 24rpx; color: #888; width: 60rpx }
.history-guess { font-size: 32rpx; font-weight: 700; color: #333; width: 100rpx; text-align: center }
.history-hint { flex: 1; font-size: 26rpx; text-align: right }
.hint-low { color: #3b82f6 }
.hint-high { color: #ef4444 }
.hint-correct { color: #10b981; font-weight: 700 }
.history-empty { text-align: center; padding: 32rpx; color: #888; font-size: 26rpx }
.btn-area { margin-top: 24rpx }
.btn { background: linear-gradient(135deg, #10b981, #34d399); border-radius: 16rpx; padding: 24rpx; text-align: center }
.btn-text { color: #fff; font-size: 28rpx; font-weight: 600 }
</style>
