<template>
  <view class="lottery-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">←</text>
        <text class="nav-title">随机决策</text>
        <text class="nav-icon empty"> </text>
      </view>
    </view>

    <view class="content">
      <view class="mode-tabs">
        <text class="mode-tab" :class="{ active: mode === 'dice' }" @click="mode = 'dice'">掷骰子</text>
        <text class="mode-tab" :class="{ active: mode === 'coin' }" @click="mode = 'coin'">抛硬币</text>
        <text class="mode-tab" :class="{ active: mode === 'wheel' }" @click="mode = 'wheel'">转盘</text>
        <text class="mode-tab" :class="{ active: mode === 'number' }" @click="mode = 'number'">随机数</text>
      </view>

      <!-- Dice -->
      <view class="result-card" v-if="mode === 'dice'">
        <text class="dice-display">{{ diceValue }}</text>
        <button class="roll-btn" @click="rollDice">掷骰子</button>
      </view>

      <!-- Coin -->
      <view class="result-card" v-if="mode === 'coin'">
        <text class="coin-display">{{ coinValue }}</text>
        <button class="roll-btn" @click="flipCoin">抛硬币</button>
      </view>

      <!-- Wheel -->
      <view class="wheel-card" v-if="mode === 'wheel'">
        <view class="wheel-container">
          <view class="wheel-pointer">▼</view>
          <view class="wheel-display">{{ wheelResult || "点击开始" }}</view>
        </view>
        <view class="wheel-input-row">
          <input class="wheel-input" v-model="wheelInput" placeholder="输入选项(用逗号分隔)" />
          <button class="wheel-btn" @click="spinWheel">开始</button>
        </view>
        <text class="wheel-hint">例如: 火锅,烧烤,寿司,面条</text>
      </view>

      <!-- Random Number -->
      <view class="result-card" v-if="mode === 'number'">
        <view class="num-row">
          <input class="num-input" v-model="minNum" type="number" placeholder="最小值" />
          <text class="num-sep">~</text>
          <input class="num-input" v-model="maxNum" type="number" placeholder="最大值" />
        </view>
        <text class="number-display">{{ numberResult }}</text>
        <button class="roll-btn" @click="randomNumber">生成</button>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from "vue"

const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const mode = ref("dice")
const diceValue = ref("⚀")
const coinValue = ref("?")
const wheelResult = ref("")
const wheelInput = ref("")
const numberResult = ref("?")
const minNum = ref(1)
const maxNum = ref(100)

const diceFaces = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]

function goBack() { uni.navigateBack() }

function rollDice() {
  let count = 0
  const interval = setInterval(() => {
    diceValue.value = diceFaces[Math.floor(Math.random() * 6)]
    count++
    if (count > 10) {
      clearInterval(interval)
      diceValue.value = diceFaces[Math.floor(Math.random() * 6)]
    }
  }, 80)
}

function flipCoin() {
  let count = 0
  const interval = setInterval(() => {
    coinValue.value = count % 2 === 0 ? "🪙" : "🏆"
    count++
    if (count > 10) {
      clearInterval(interval)
      coinValue.value = Math.random() > 0.5 ? "🪙" : "🏆"
    }
  }, 80)
}

function spinWheel() {
  const options = wheelInput.value.split(/[,，]/).map(s => s.trim()).filter(s => s)
  if (options.length < 2) { uni.showToast({ title: "请至少输入2个选项", icon: "none" }); return }
  let count = 0
  const total = 20 + Math.floor(Math.random() * 10)
  const interval = setInterval(() => {
    wheelResult.value = options[count % options.length]
    count++
    if (count > total) {
      clearInterval(interval)
      wheelResult.value = options[Math.floor(Math.random() * options.length)]
    }
  }, 100)
}

function randomNumber() {
  const min = parseInt(minNum.value) || 0
  const max = parseInt(maxNum.value) || 100
  if (min >= max) { uni.showToast({ title: "最小值应小于最大值", icon: "none" }); return }
  numberResult.value = Math.floor(Math.random() * (max - min + 1)) + min
}

onMounted(() => {
  if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }
})
</script>

<style lang="scss" scoped>
.lottery-page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #a855f7, #7c3aed); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.mode-tabs { display: flex; gap: 12rpx; margin-bottom: 24rpx; }
.mode-tab { flex: 1; text-align: center; padding: 16rpx 8rpx; background: #fff; border-radius: 16rpx; font-size: 26rpx; color: #666; }
.mode-tab.active { background: linear-gradient(135deg, #a855f7, #7c3aed); color: #fff; }
.result-card { background: #fff; border-radius: 24rpx; padding: 60rpx 40rpx; text-align: center; }
.dice-display { font-size: 120rpx; display: block; margin-bottom: 40rpx; }
.coin-display { font-size: 100rpx; display: block; margin-bottom: 40rpx; }
.number-display { font-size: 80rpx; font-weight: 700; color: #a855f7; display: block; margin: 32rpx 0; }
.roll-btn { background: linear-gradient(135deg, #a855f7, #7c3aed); color: #fff; border-radius: 50rpx; font-size: 28rpx; padding: 16rpx 60rpx; }
.wheel-card { background: #fff; border-radius: 24rpx; padding: 40rpx 32rpx; text-align: center; }
.wheel-container { margin-bottom: 32rpx; }
.wheel-pointer { font-size: 40rpx; color: #a855f7; }
.wheel-display { font-size: 48rpx; font-weight: 700; color: #333; margin-top: 16rpx; min-height: 80rpx; }
.wheel-input-row { display: flex; gap: 16rpx; margin-bottom: 16rpx; }
.wheel-input { flex: 1; height: 72rpx; border: 2rpx solid #e5e7eb; border-radius: 12rpx; padding: 0 20rpx; font-size: 26rpx; }
.wheel-btn { background: linear-gradient(135deg, #a855f7, #7c3aed); color: #fff; border-radius: 12rpx; font-size: 26rpx; padding: 0 32rpx; }
.wheel-hint { font-size: 22rpx; color: #999; }
.num-row { display: flex; align-items: center; gap: 16rpx; }
.num-input { flex: 1; height: 80rpx; border: 2rpx solid #e5e7eb; border-radius: 12rpx; text-align: center; font-size: 32rpx; }
.num-sep { font-size: 40rpx; font-weight: 700; color: #333; }
</style>
