<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">水平仪</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="level-area">
        <view class="level-circle" :class="{ level: isLevel }">
          <view class="level-bubble" :style="{ transform: 'translate(' + bubbleX + 'px, ' + bubbleY + 'px)' }"></view>
        </view>
      </view>
      <view class="level-info">
        <view class="info-row"><text>角度: {{ angleX.toFixed(1) }}° / {{ angleY.toFixed(1) }}°</text></view>
        <view class="info-row"><text class="level-status" :class="{ active: isLevel }">{{ isLevel ? "✅ 水平" : "❌ 不平" }}</text></view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onUnmounted, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const angleX = ref(0)
const angleY = ref(0)
const bubbleX = ref(0)
const bubbleY = ref(0)
const isLevel = ref(false)
var watcher = null
onMounted(function() {
  if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }
  if (uni.onAccelerometerChange) {
    uni.startAccelerometer()
    watcher = function(res) {
      angleX.value = Math.atan2(res.y, res.z) * 180 / Math.PI
      angleY.value = Math.atan2(-res.x, Math.sqrt(res.y * res.y + res.z * res.z)) * 180 / Math.PI
      bubbleX.value = Math.max(-60, Math.min(60, angleX.value * 2))
      bubbleY.value = Math.max(-60, Math.min(60, angleY.value * 2))
      isLevel.value = Math.abs(angleX.value) < 3 && Math.abs(angleY.value) < 3
    }
    uni.onAccelerometerChange(watcher)
  }
})
onUnmounted(function() { if (uni.stopAccelerometer) uni.stopAccelerometer() })
function goBack() { uni.navigateBack() }
</script>
<style scoped>
.page { min-height: 100vh; background: #2d3436; }
.custom-nav { background: linear-gradient(135deg, #00b894, #00cec9); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; display: flex; flex-direction: column; align-items: center; }
.level-area { margin-bottom: 40rpx; }
.level-circle { width: 300rpx; height: 300rpx; border-radius: 50%; border: 4rpx solid #00b894; background: rgba(0,184,148,0.1); position: relative; display: flex; align-items: center; justify-content: center; }
.level-circle.level { border-color: #00cec9; box-shadow: 0 0 30rpx rgba(0,206,201,0.3); }
.level-bubble { width: 40rpx; height: 40rpx; border-radius: 50%; background: #00cec9; transition: transform 0.1s; }
.level-info { text-align: center; }
.info-row { margin-bottom: 16rpx; font-size: 28rpx; color: #fff; }
.level-status { font-weight: 700; }
.level-status.active { color: #00cec9; }
</style>