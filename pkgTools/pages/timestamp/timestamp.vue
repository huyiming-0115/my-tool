<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">时间戳转换</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="ts-card"><text class="ts-label">Unix 时间戳 (秒)</text><text class="ts-val">{{ ts }}</text><view class="ts-row"><text class="ts-btn" @click="setNow">当前</text></view></view>
      <view class="ts-card"><text class="ts-label">日期时间</text><text class="ts-val">{{ dateStr }}</text></view>
      <view class="ts-card"><text class="ts-label">毫秒时间戳</text><text class="ts-val">{{ ts * 1000 }}</text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const ts = ref(Math.floor(Date.now() / 1000))
const dateStr = ref(new Date().toLocaleString())
function setNow() { ts.value = Math.floor(Date.now() / 1000); updateDate() }
function updateDate() { dateStr.value = new Date(ts.value * 1000).toLocaleString() }
setInterval(() => { ts.value = Math.floor(Date.now() / 1000); updateDate() }, 1000)
function goBack() { uni.navigateBack() }
onMounted(() => { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #00b894, #55efc4); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.ts-card { background: #fff; border-radius: 24rpx; padding: 24rpx; margin-bottom: 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.ts-label { font-size: 26rpx; color: #999; display: block; margin-bottom: 12rpx; }
.ts-val { font-size: 36rpx; font-weight: 700; color: #00b894; display: block; font-family: monospace; word-break: break-all; }
.ts-row { display: flex; gap: 16rpx; margin-top: 16rpx; }
.ts-btn { flex: 1; text-align: center; padding: 16rpx; background: #f5f5f5; border-radius: 12rpx; font-size: 24rpx; color: #666; }
.ts-btn:active { background: #00b894; color: #fff; }
</style>
