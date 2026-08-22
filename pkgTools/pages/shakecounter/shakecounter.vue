<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">摇一摇计数</text><text class="nav-icon" @click="count = 0">🔄</text></view>
    </view>
    <view class="content">
      <view class="shake-display"><text class="shake-count">{{ count }}</text><text class="shake-label">摇动次数</text></view>
      <view class="shake-icon" :class="{ shaking: shaking }">📱</view>
      <view class="shake-status">{{ monitoring ? "监测中..." : "点击开始" }}</view>
      <view class="shake-btn" @click="toggle"><text>{{ monitoring ? "停止" : "开始" }}</text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onUnmounted, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const count = ref(0)
const monitoring = ref(false)
const shaking = ref(false)
var lastX = 0, lastY = 0, lastZ = 0, lastTime = 0
var watcher = null
function toggle() {
  if (monitoring.value) {
    uni.stopAccelerometer()
    if (watcher) uni.offAccelerometerChange(watcher)
    monitoring.value = false
  } else {
    uni.startAccelerometer()
    watcher = function(res) {
      var now = Date.now()
      if (now - lastTime > 100) {
        var diff = Math.abs(res.x - lastX) + Math.abs(res.y - lastY) + Math.abs(res.z - lastZ)
        if (diff > 15) { count.value++; shaking.value = true; setTimeout(function() { shaking.value = false }, 200) }
        lastX = res.x; lastY = res.y; lastZ = res.z; lastTime = now
      }
    }
    uni.onAccelerometerChange(watcher)
    monitoring.value = true
  }
}
onUnmounted(function() { if (monitoring.value) uni.stopAccelerometer() })
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #636e72, #2d3436); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 44rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; display: flex; flex-direction: column; align-items: center; }
.shake-display { text-align: center; margin-bottom: 32rpx; }
.shake-count { font-size: 96rpx; font-weight: 700; color: #2d3436; display: block; }
.shake-label { font-size: 24rpx; color: #999; }
.shake-icon { font-size: 120rpx; margin-bottom: 24rpx; }
.shake-icon.shaking { animation: shake 0.2s; }
@keyframes shake { 0%, 100% { transform: rotate(0); } 25% { transform: rotate(-15deg); } 75% { transform: rotate(15deg); } }
.shake-status { font-size: 26rpx; color: #999; margin-bottom: 32rpx; }
.shake-btn { width: 80%; background: linear-gradient(135deg, #636e72, #2d3436); border-radius: 16rpx; padding: 28rpx; text-align: center; }
.shake-btn text { font-size: 32rpx; color: #fff; font-weight: 600; }
</style>