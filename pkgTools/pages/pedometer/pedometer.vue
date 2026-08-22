<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">计步器</text><text class="nav-icon" @click="steps = 0">🔄</text></view>
    </view>
    <view class="content">
      <view class="step-ring">
        <text class="step-count">{{ steps }}</text>
        <text class="step-label">步</text>
      </view>
      <view class="step-stats">
        <view class="stat-item"><text class="stat-v">{{ (steps * 0.04).toFixed(1) }}</text><text class="stat-l">千卡</text></view>
        <view class="stat-item"><text class="stat-v">{{ (steps * 0.0007).toFixed(2) }}</text><text class="stat-l">公里</text></view>
      </view>
      <view class="step-btn" @click="simulate"><text>模拟走路</text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const steps = ref(0)
function simulate() { steps.value += Math.floor(Math.random() * 500) + 100 }
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #00b894, #55efc4); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; display: flex; flex-direction: column; align-items: center; }
.step-ring { width: 300rpx; height: 300rpx; border-radius: 50%; border: 8rpx solid #00b894; display: flex; flex-direction: column; align-items: center; justify-content: center; margin-bottom: 32rpx; }
.step-count { font-size: 72rpx; font-weight: 700; color: #00b894; }
.step-label { font-size: 28rpx; color: #999; }
.step-stats { display: flex; gap: 40rpx; margin-bottom: 32rpx; }
.stat-item { text-align: center; background: #fff; padding: 24rpx 40rpx; border-radius: 16rpx; }
.stat-v { font-size: 36rpx; font-weight: 700; color: #333; display: block; }
.stat-l { font-size: 22rpx; color: #999; display: block; margin-top: 4rpx; }
.step-btn { width: 80%; background: linear-gradient(135deg, #00b894, #55efc4); border-radius: 16rpx; padding: 28rpx; text-align: center; }
.step-btn text { font-size: 32rpx; color: #fff; font-weight: 600; }
</style>