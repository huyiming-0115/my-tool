<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">←</text>
        <text class="nav-title">2048游戏</text>
        <text class="nav-icon" @click="resetGame">↻</text>
      </view>
    </view>
    <view class="content">
      <view class="scoreboard">
        <view class="score-box">
          <text class="score-label">分数</text>
          <text class="score-value">{{ score }}</text>
        </view>
        <view class="score-box">
          <text class="score-label">最佳</text>
          <text class="score-value">{{ bestScore }}</text>
        </view>
      </view>
      <view class="status-bar">{{ statusText }}</view>
      <view class="grid" @touchstart="onTouchStart" @touchend="onTouchEnd">
        <view
          v-for="(tile, index) in tiles"          :key="index"          class="tile"          :class="['tile-' + (tile.value || 0), { 'tile-new': tile.isNew }]"        >
          <text class="tile-text">{{ tile.value || '' }}</text>
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

const SIZE = 4
const tiles = ref([])
const score = ref(0)
const bestScore = ref(0)
const gameOver = ref(false)
const won = ref(false)

const statusText = computed(() => {
  if (gameOver.value) return '游戏结束!'
  if (won.value) return '你赢了! ！'
  return '用滚动向发！'
})

function initGrid() {
  tiles.value = []
  for (let i = 0; i < SIZE * SIZE; i++) {
    tiles.value.push({ value: 0, isNew: false, merged: false })
  }
}

function addRandomTile() {
  const empty = []
  tiles.value.forEach((t, i) => { if (t.value === 0) empty.push(i) })
  if (empty.length === 0) return false
  const idx = empty[Math.floor(Math.random() * empty.length)]
  tiles.value[idx] = { value: Math.random() < 0.9 ? 2 : 4, isNew: true, merged: false }
  return true
}

function getGrid() {
  const grid = []
  for (let r = 0; r < SIZE; r++) {
    grid[r] = []
    for (let c = 0; c < SIZE; c++) {
      grid[r][c] = tiles.value[r * SIZE + c].value
    }
  }
  return grid
}

function slideRow(row) {
  let arr = row.filter(v => v !== 0)
  let gained = 0
  for (let i = 0; i < arr.length - 1; i++) {
    if (arr[i] === arr[i + 1]) {
      arr[i] *= 2
      gained += arr[i]
      if (arr[i] === 2048) won.value = true
      arr.splice(i + 1, 1)
    }
  }
  while (arr.length < SIZE) arr.push(0)
  return { result: arr, gained }
}

function move(direction) {
  if (gameOver.value) return
  const grid = getGrid()
  let newGrid = []
  let totalGained = 0
  let moved = false
  for (let i = 0; i < SIZE; i++) {
    let row
    if (direction === 'left') {
      row = [...grid[i]]
    } else if (direction === 'right') {
      row = [...grid[i]].reverse()
    } else if (direction === 'up') {
      row = []
      for (let j = 0; j < SIZE; j++) row.push(grid[j][i])
    } else {
      row = []
      for (let j = 0; j < SIZE; j++) row.push(grid[SIZE - 1 - j][i])
    }
    const { result, gained } = slideRow(row)
    totalGained += gained
    let finalRow
    if (direction === 'left') {
      finalRow = result
    } else if (direction === 'right') {
      finalRow = result.reverse()
    } else if (direction === 'up') {
      for (let j = 0; j < SIZE; j++) {
        if (grid[j][i] !== finalRow ? (grid[j][i] !== (result[j] || 0)) : false) moved = true
      }
      newGrid[i] = finalRow
    } else {
      finalRow = result.reverse()
    }
    if (direction === 'left' || direction === 'right') {
      if (grid[i].join(',') !== result.join(',')) moved = true
      newGrid[i] = result
    }
  }
  if (!moved) {
    for (let i = 0; i < SIZE; i++) {
      for (let j = 0; j < SIZE; j++) {
        let v
        if (direction === 'up') v = newGrid[j] ? newGrid[j][i] : -1
        else if (direction === 'down') v = newGrid[SIZE-1-j] ? newGrid[SIZE-1-j][i] : -1
        else v = newGrid[i] ? newGrid[i][j] : -1
        if (grid[i][j] !== v) { moved = true; break }
      }
      if (moved) break
    }
  }
  if (!moved) return
  score.value += totalGained
  if (score.value > bestScore.value) {
    bestScore.value = score.value
    uni.setStorageSync('game2048_best', bestScore.value)
  }
  const newTiles = []
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      newTiles.push({ value: newGrid[i][j], isNew: false, merged: false })
    }
  }
  tiles.value = newTiles
  addRandomTile()
  if (isGameOver()) {
    gameOver.value = true
  }
}

function isGameOver() {
  for (let i = 0; i < SIZE * SIZE; i++) {
    if (tiles.value[i].value === 0) return false
  }
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const v = tiles.value[i * SIZE + j].value
      if (j < SIZE - 1 && v === tiles.value[i * SIZE + j + 1].value) return false
      if (i < SIZE - 1 && v === tiles.value[(i + 1) * SIZE + j].value) return false
    }
  }
  return true
}

function resetGame() {
  gameOver.value = false
  won.value = false
  score.value = 0
  initGrid()
  addRandomTile()
  addRandomTile()
}

let touchStartX = 0
let touchStartY = 0
function onTouchStart(e) {
  touchStartX = e.touches[0].clientX
  touchStartY = e.touches[0].clientY
}
function onTouchEnd(e) {
  const dx = e.changedTouches[0].clientX - touchStartX
  const dy = e.changedTouches[0].clientY - touchStartY
  const absDx = Math.abs(dx)
  const absDy = Math.abs(dy)
  if (Math.max(absDx, absDy) < 30) return
  if (absDx > absDy) {
    move(dx > 0 ? 'right' : 'left')
  } else {
    move(dy > 0 ? 'down' : 'up')
  }
}

onMounted(function() {
  if (!uni.getStorageSync("isLoggedIn")) {
    uni.reLaunch({ url: "/pages/login/login" })
    return
  }
  bestScore.value = uni.getStorageSync('game2048_best') || 0
  resetGame()
  const gridEl = document ? null : null
})
</script>
<style scoped>
.page { min-height: 100vh; background: #f5f7fb }
.custom-nav { background: linear-gradient(135deg, #f59e0b, #f97316); width: 100% }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx }
.nav-icon { width: 72rpx; text-align: center; font-size: 44rpx; color: #fff; font-weight: 700; flex-shrink: 0 }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600 }
.content { padding: 24rpx }
.scoreboard { display: flex; gap: 24rpx; margin-bottom: 24rpx }
.score-box { flex: 1; background: linear-gradient(135deg, #f59e0b, #f97316); border-radius: 16rpx; padding: 20rpx; text-align: center }
.score-label { font-size: 24rpx; color: rgba(255,255,255,0.9); margin-bottom: 8rpx }
.score-value { font-size: 40rpx; font-weight: 700; color: #fff }
.status-bar { text-align: center; margin-bottom: 24rpx; font-size: 28rpx; color: #666 }
.grid { background: #b8c6db; border-radius: 16rpx; padding: 12rpx; display: grid; grid-template-columns: repeat(4, 1fr); gap: 12rpx; touch-action: none }
.tile { aspect-ratio: 1; background: rgba(255,255,255,0.35); border-radius: 12rpx; display: flex; align-items: center; justify-content: center; transition: all 0.15s ease }
.tile-new { animation: pop 0.2s ease }
@keyframes pop { 0% { transform: scale(0); } 100% { transform: scale(1); } }
.tile-text { font-size: 48rpx; font-weight: 700; color: #333 }
.tile-2 { background: #eee4da }
.tile-4 { background: #ede0c8 }
.tile-8 { background: #f2b179; color: #fff }
.tile-16 { background: #f59563; color: #fff }
.tile-32 { background: #f67c5f; color: #fff }
.tile-64 { background: #f65e3b; color: #fff }
.tile-128 { background: #edcf72; color: #fff; font-size: 40rpx }
.tile-256 { background: #edcc61; color: #fff; font-size: 40rpx }
.tile-512 { background: #edc850; color: #fff; font-size: 40rpx }
.tile-1024 { background: #edc53f; color: #fff; font-size: 32rpx }
.tile-2048 { background: #edc22e; color: #fff; font-size: 32rpx }
.tile-text { font-size: 48rpx; font-weight: 700 }
.tile-2 .tile-text, .tile-4 .tile-text { color: #776e65 }
.tile-8 .tile-text, .tile-16 .tile-text, .tile-32 .tile-text, .tile-64 .tile-text { color: #fff }
.btn-area { margin-top: 32rpx }
.btn { background: linear-gradient(135deg, #f59e0b, #f97316); border-radius: 16rpx; padding: 24rpx; text-align: center }
.btn-text { color: #fff; font-size: 28rpx; font-weight: 600 }
</style>
