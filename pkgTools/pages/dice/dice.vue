<template>
  <view class="dice-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">骰子</text><text class="nav-icon" @click="diceCount = diceCount >= 6 ? 1 : diceCount + 1">{{ diceCount }}</text></view>
    </view>
    <view class="content">
      <view class="dice-area">
        <view class="dice-item" v-for="(d, idx) in diceResults" :key="idx">
          <view class="dice-cube" :class="{ rolling: rolling }">
            <text class="dice-dot" v-if="!rolling">{{ d }}</text>
            <text class="dice-rolling" v-rolling>?</text>
          </view>
        </view>
      </view>
      <view class="total-score" v-if="diceResults.length > 1 && !rolling"><text>总分: {{ diceResults.reduce((s, d) => s + d, 0) }}</text></view>
      <view class="roll-btn" :class="{ disabled: rolling }" @click="roll"><text>{{ rolling ? '抛出中...' : '抛骰子' }}</text></view>
      <view class="dice-options"><text class="opt-label">选择数量:</text><view class="opt-btns"><text class="opt-btn" :class="{ active: diceCount === 1 }" @click="diceCount = 1">1</text><text class="opt-btn" :class="{ active: diceCount === 2 }" @click="diceCount = 2">2</text><text class="opt-btn" :class="{ active: diceCount === 3 }" @click="diceCount = 3">3</text><text class="opt-btn" :class="{ active: diceCount === 5 }" @click="diceCount = 5">5</text></view></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const diceCount = ref(2)
const diceResults = ref([1, 1])
const rolling = ref(false)
function roll() {
  if (rolling.value) return
  rolling.value = true
  let count = 0
  const timer = setInterval(() => { diceResults.value = Array(diceCount.value).fill(0).map(() => Math.floor(Math.random() * 6) + 1); count++ }, 100)
  setTimeout(() => { clearInterval(timer); rolling.value = false; uni.vibrateShort({}) }, 1000)
}
function goBack() { uni.navigateBack() }
onMounted(() => { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.dice-page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #e17055, #d63031); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 44rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; display: flex; flex-direction: column; align-items: center; }
.dice-area { display: flex; gap: 24rpx; justify-content: center; flex-wrap: wrap; margin-bottom: 32rpx; }
.dice-cube { width: 140rpx; height: 140rpx; background: #fff; border-radius: 24rpx; display: flex; align-items: center; justify-content: center; box-shadow: 0 8rpx 24rpx rgba(0,0,0,0.1); }
.dice-cube.rolling { animation: shake 0.1s infinite; }
@keyframes shake { 0%, 100% { transform: rotate(0deg); } 25% { transform: rotate(-10deg); } 75% { transform: rotate(10deg); } }
.dice-dot { font-size: 80rpx; color: #d63031; font-weight: 700; }
.dice-rolling { font-size: 60rpx; color: #999; }
.total-score { font-size: 32rpx; color: #333; font-weight: 700; margin-bottom: 32rpx; }
.roll-btn { width: 80%; background: linear-gradient(135deg, #e17055, #d63031); border-radius: 16rpx; padding: 28rpx; text-align: center; margin-bottom: 32rpx; }
.roll-btn text { font-size: 32rpx; color: #fff; font-weight: 600; }
.roll-btn.disabled { opacity: 0.4; }
.dice-options { display: flex; align-items: center; gap: 16rpx; }
.opt-label { font-size: 26rpx; color: #666; }
.opt-btns { display: flex; gap: 12rpx; }
.opt-btn { width: 64rpx; height: 64rpx; line-height: 64rpx; text-align: center; background: #fff; border-radius: 12rpx; font-size: 28rpx; color: #666; }
.opt-btn.active { background: #d63031; color: #fff; }
</style>
