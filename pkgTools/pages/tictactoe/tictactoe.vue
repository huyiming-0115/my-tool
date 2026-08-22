<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">←</text>
        <text class="nav-title">井字棋</text>
        <text class="nav-icon" @click="resetGame">↻</text>
      </view>
    </view>
    <view class="content">
      <view class="scoreboard">
        <view class="score-item">
      <view class="scoreboard">
        <view class="score-item">
          <text class="score-label">X 胜</text>
          <text class="score-value">{{ scores.X }}</text>
        </view>
        <view class="score-item">
          <text class="score-label">平局</text>
          <text class="score-value">{{ scores.draw }}</text>
        </view>
        <view class="score-item">
          <text class="score-label">O 胜</text>
          <text class="score-value">{{ scores.O }}</text>
        </view>
      </view>
      <view class="status-bar">
        <text class="status-text">{{ statusText }}</text>
      </view>
      <view class="grid">
        <view
          v-for="(cell, index) in board"          :key="index"          class="cell"          :class="{ 'win-cell': winningLine.includes(index) }"          @click="makeMove(index)"        >
          <text class="cell-text" :class="{ 'text-x': cell === 'X', 'text-o': cell === 'O' }">{{ cell }}</text>
        </view>
      </view>
      <view class="btn-area">
      <view class="btn-area">
        <view class="btn" @click="resetGame"><text class="btn-text">重新开始</text></view>
        <view class="btn btn-reset" @click="resetScores"><text class="btn-text">重置比分</text></view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, computed, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
function goBack() { uni.navigateBack() }

const board = ref(['', '', '', '', '', '', '', '', ''])
const currentPlayer = ref('X')
const gameOver = ref(false)
const winningLine = ref([])
const scores = ref({ X: 0, O: 0, draw: 0 })

const winPatterns = [
  [0, 1, 2], [3, 4, 5], [6, 7, 8],
  [0, 3, 6], [1, 4, 7], [2, 5, 8],
  [0, 4, 8], [2, 4, 6]
]

const statusText = computed(() => {
  if (gameOver.value) {
    if (winningLine.value.length) {

const statusText = computed(() => {
  if (gameOver.value) {
    if (winningLine.value.length) {
      return currentPlayer.value + ' 获丞!'
    }
    return '平局!'
  }
  return '当前玩家: ' + currentPlayer.value
})

function makeMove(index) {
  if (board.value[index] || gameOver.value) return
  board.value[index] = currentPlayer.value
  if (checkWin()) {
    gameOver.value = true
    scores.value[currentPlayer.value]++
    saveScores()
    return
  }
  if (board.value.every(c => c !== '')) {
    gameOver.value = true
    scores.value.draw++
    saveScores()
    return
  }
  currentPlayer.value = currentPlayer.value === 'X' ? 'O' : 'X'
}

function checkWin() {
  for (const pattern of winPatterns) {
    const [a, b, c] = pattern
    if (board.value[a] && board.value[a] === board.value[b] && board.value[a] === board.value[c]) {
      winningLine.value = pattern
      return true
    }
  }
  return false
}

function resetGame() {
  board.value = ['', '', '', '', '', '', '', '', '']
  currentPlayer.value = 'X'  gameOver.value = false
  winningLine.value = []
}

function resetScores() {
  scores.value = { X: 0, O: 0, draw: 0 }
  saveScores()
}

function saveScores() {
  uni.setStorageSync('tictactoe_scores', scores.value)
}

function loadScores() {
  const saved = uni.getStorageSync('tictactoe_scores')
  if (saved) scores.value = saved
}

onMounted(function() {
  if (!uni.getStorageSync("isLoggedIn")) {
    uni.reLaunch({ url: "/pages/login/login" })
    return
  }
  loadScores()
})
</script>
<style scoped>
.page { min-height: 100vh; background: #f5f7fb }
.custom-nav { background: linear-gradient(135deg, #4a6cf7, #7c3aed); width: 100% }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx }
.nav-icon { width: 72rpx; text-align: center; font-size: 44rpx; color: #fff; font-weight: 700; flex-shrink: 0 }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600 }
.content { padding: 24rpx }
.scoreboard { display: flex; justify-content: space-around; background: #fff; border-radius: 16rpx; padding: 24rpx; margin-bottom: 24rpx; box-shadow: 0 2rpx 12rpx rgba(0,0,0,0.06) }
.score-item { display: flex; flex-direction: column; align-items: center }
.score-label { font-size: 24rpx; color: #888; margin-bottom: 8rpx }
.score-value { font-size: 40rpx; font-weight: 700; color: #333 }
.status-bar { text-align: center; margin-bottom: 24rpx }
.status-text { font-size: 32rpx; font-weight: 600; color: #333 }
.grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12rpx; background: #e2e8f0; border-radius: 16rpx; padding: 12rpx }
.cell { aspect-ratio: 1; background: #fff; border-radius: 12rpx; display: flex; align-items: center; justify-content: center; min-height: 180rpx }
.cell:active { background: #f0f0f0 }
.win-cell { background: #fef08a }
.cell-text { font-size: 80rpx; font-weight: 700 }
.text-x { color: #4a6cf7 }
.text-o { color: #7c3aed }
.btn-area { display: flex; gap: 24rpx; margin-top: 32rpx }
.btn { flex: 1; background: linear-gradient(135deg, #4a6cf7, #7c3aed); border-radius: 16rpx; padding: 24rpx; text-align: center }
.btn-reset { background: linear-gradient(135deg, #64748b, #475569) }
.btn-text { color: #fff; font-size: 28rpx; font-weight: 600 }
</style>
