<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">二维码扫描</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="scan-area"><text class="scan-icon">📷</text><button class="scan-btn" @click="scan"><text>开始扫描</text></button></view>
      <view class="result-box" v-if="result"><text class="result-label">扫描结果</text><text class="result-text">{{ result }}</text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const result = ref("")
function scan() { uni.scanCode({ success: (res) => { result.value = res.result }, fail: () => { uni.showToast({ title: "扫描失败", icon: "none" }) } }) }
function goBack() { uni.navigateBack() }
onMounted(() => { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #0984e3, #74b9ff); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.scan-area { height: 400rpx; border: 4rpx dashed #74b9ff; border-radius: 24rpx; display: flex; flex-direction: column; align-items: center; justify-content: center; background: #fff; margin-bottom: 24rpx; }
.scan-icon { font-size: 100rpx; margin-bottom: 16rpx; }
.scan-btn { background: linear-gradient(135deg, #0984e3, #74b9ff); border-radius: 16rpx; padding: 24rpx 60rpx; border: none; }
.scan-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.scan-btn::after { border: none; }
.result-box { background: #fff; border-radius: 24rpx; padding: 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.result-label { font-size: 24rpx; color: #999; display: block; margin-bottom: 8rpx; }
.result-text { font-size: 28rpx; color: #333; word-break: break-all; }
</style>
