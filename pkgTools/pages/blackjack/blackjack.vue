<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">←</text>
        <text class="nav-title">21点</text>
        <text class="nav-icon" @click="resetGame">↻</text>
      </view>
    </view>
    <view class="content">
      <view class="scoreboard">
        <view class="score-item">
          <text class="score-label">胜别数</text>
          <text class="score-value">{{ scores.wins }}</text>
        </view>
        <view class="score-item">
          <text class="score-label">平局</text>
          <text class="score-value">{{ scores.pushes }}</text>
        </view>
        <view class="score-item">
          <text class="score-label">败别数</text>
          <text class="score-value">{{ scores.losses }}</text>
        </view>
      </view>
      <view class="status-bar">{{ statusText }}</view>
      <view class="table">
        <view class="hand-section">
          <view class="hand-header">
            <text class="hand-title">普家（总数:{{ dealerScore }}）</text>
          </view>
          <view class="cards">
            <view v-for="(card, idx) in dealerHand" :key="idx" class="card" :class="{ 'card-hidden': idx === 0 && !gameOver }">
              <text class="card-text">{{ idx === 0 && !gameOver ? '?' : cardDisplay(card) }}</text>
            </view>
          </view>
        </view>
        <view class="hand-section">
          <view class="hand-header">
            <text class="hand-title">你（总数:{{ playerScore }}）</text>
          </view>
          <view class="cards">
            <view v-for="(card, idx) in playerHand" :key="idx" class="card">
              <text class="card-text">{{ cardDisplay(card) }}</text>
            </view>
          </view>
        </view>
      </view>
      <view class="actions">
        <view class="btn hit-btn" @click="hit" :class="{ 'btn-disabled': gameOver }"><text class="btn-text">拼牌</text></view>
        <view class="btn stand-btn" @click="stand" :class="{ 'btn-disabled': gameOver }"><text class="btn-text">停拼</text></view>
        <view class="btn new-btn" @click="resetGame"><text class="btn-text">新局展</text></view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, computed, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
function goBack() { uni.navigateBack() }

const playerHand = ref([])
const dealerHand = ref([])
const gameOver = ref(false)
const scores = ref({ wins: 0, losses: 0, pushes: 0 })

const playerScore = computed(() => calcHand(playerHand.value))
const dealerScore = computed(() => {
  if (!gameOver.value && dealerHand.value.length > 0) {
    return calcHand([dealerHand.value[1]])
  }
  return calcHand(dealerHand.value)
})

const statusText = computed(() => {
  if (!gameOver.value) return '选择拼牌或停拼'
  if (playerScore.value > 21) return '你爆了！'
  if (dealerScore.value > 21) return '普家爆了！你赢！'
  if (playerScore.value > dealerScore.value) return '你赢了！'
  if (playerScore.value < dealerScore.value) return '你输了！'
  return '平局！'
})

function drawCard() {
  return Math.floor(Math.random() * 11) + 1
}

function calcHand(hand) {
  let total = 0
  for (const card of hand) {
    total += card
  }
  return total
}

function cardDisplay(card) {
  if (card === 1 || card === 11) return 'A'  return String(card)
}

function deal() {
  playerHand.value = [drawCard(), drawCard()]
  dealerHand.value = [drawCard(), drawCard()]
  if (playerScore.value === 21) {
    gameOver.value = true
    scores.value.wins++
    saveScores()
  }
}

function hit() {
  if (gameOver.value) return
  playerHand.value.push(drawCard())
  if (playerScore.value > 21) {
    gameOver.value = true
    scores.value.losses++
    saveScores()
  }
}

function stand() {
  if (gameOver.value) return
  while (calcHand(dealerHand.value) < 17) {
    dealerHand.value.push(drawCard())
  }
  gameOver.value = true
  const ps = playerScore.value
  const ds = calcHand(dealerHand.value)
  if (ds > 21 || ps > ds) {
    scores.value.wins++
  } else if (ps < ds) {
    scores.value.losses++
  } else {
    scores.value.pushes++
  }
  saveScores()
}

function resetGame() {
  gameOver.value = false
  deal()
}

function saveScores() {
  uni.setStorageSync('blackjack_scores', scores.value)
}

function loadScores() {
  const saved = uni.getStorageSync('blackjack_scores')
  if (saved) scores.value = saved
}

onMounted(function() {
  if (!uni.getStorageSync("isLoggedIn")) {
    uni.reLaunch({ url: "/pages/login/login" })
    return
  }
  loadScores()
  deal()
})
</script>
<style scoped>
.page { min-height: 100vh; background: #f5f7fb }
.custom-nav { background: linear-gradient(135deg, #ef4444, #dc2626); width: 100% }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx }
.nav-icon { width: 72rpx; text-align: center; font-size: 44rpx; color: #fff; font-weight: 700; flex-shrink: 0 }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600 }
.content { padding: 24rpx }
.scoreboard { display: flex; justify-content: space-around; background: #fff; border-radius: 16rpx; padding: 24rpx; margin-bottom: 24rpx; box-shadow: 0 2rpx 12rpx rgba(0,0,0,0.06) }
.score-item { display: flex; flex-direction: column; align-items: center }
.score-label { font-size: 24rpx; color: #888; margin-bottom: 8rpx }
.score-value { font-size: 40rpx; font-weight: 700; color: #333 }
.status-bar { text-align: center; margin-bottom: 24rpx; font-size: 32rpx; font-weight: 600; color: #333; background: #fff; border-radius: 16rpx; padding: 20rpx; box-shadow: 0 2rpx 12rpx rgba(0,0,0,0.06) }
.table { background: #166534; border-radius: 24rpx; padding: 32rpx; margin-bottom: 24rpx; box-shadow: 0 4rpx 20rpx rgba(0,0,0,0.15) }
.hand-section { margin-bottom: 32rpx }
.hand-header { margin-bottom: 16rpx }
.hand-title { font-size: 28rpx; color: rgba(255,255,255,0.9); font-weight: 600 }
.cards { display: flex; gap: 16rpx; flex-wrap: wrap }
.card { width: 100rpx; height: 140rpx; background: #fff; border-radius: 12rpx; display: flex; align-items: center; justify-content: center; box-shadow: 0 2rpx 8rpx rgba(0,0,0,0.2) }
.card-hidden { background: #b91c1c }
.card-text { font-size: 40rpx; font-weight: 700; color: #333 }
.card-hidden .card-text { color: #fff }
.actions { display: flex; gap: 16rpx }
.btn { flex: 1; border-radius: 16rpx; padding: 24rpx; text-align: center }
.hit-btn { background: linear-gradient(135deg, #22c55e, #16a34a) }
.stand-btn { background: linear-gradient(135deg, #f59e0b, #d97706) }
.new-btn { background: linear-gradient(135deg, #ef4444, #dc2626) }
.btn-disabled { opacity: 0.5 }
.btn-text { color: #fff; font-size: 28rpx; font-weight: 600 }
</style>
