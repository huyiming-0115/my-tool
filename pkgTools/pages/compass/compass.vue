<template>
  <view class="cp-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">指南针</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="compass-dial">
        <view class="dial-ring" :style="{ transform: 'rotate(' + (-heading) + 'deg)' }">
          <text class="dir-n">N</text><text class="dir-e">E</text><text class="dir-s">S</text><text class="dir-w">W</text>
        </view>
        <view class="dial-center"><text class="dial-degree">{{ Math.round(heading) }}°</text><text class="dial-dir">{{ direction }}</text></view>
      </view>
      <view class="compass-info">
        <view class="info-item"><text class="info-l">角度</text><text class="info-v">{{ heading.toFixed(1) }}°</text></view>
        <view class="info-item"><text class="info-l">方位</text><text class="info-v">{{ direction }}</text></view>
      </view>
      <view class="compass-tip" v-if="!supported"><text>⚠️ 设备不支持电子罗盘，显示模拟数据</text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted, onUnmounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const heading = ref(0)
const direction = ref("北")
const supported = ref(true)
let watcher = null
const dirs = ["北", "东北", "东", "东南", "南", "西南", "西", "西北"]
onMounted(() => {
  if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }
  if (uni.onCompassChange) {
    uni.startCompass()
    watcher = (res) => { heading.value = res.direction; direction.value = dirs[Math.round(res.direction / 45) % 8] }
    uni.onCompassChange(watcher)
  } else {
    supported.value = false
    let h = 0
    watcher = setInterval(() => { h = (h + 2) % 360; heading.value = h; direction.value = dirs[Math.round(h / 45) % 8] }, 200)
  }
})
onUnmounted(() => { if (uni.stopCompass) uni.stopCompass(); if (typeof watcher === 'number') clearInterval(watcher) })
function goBack() { uni.navigateBack() }
</script>
<style scoped>
.cp-page { min-height: 100vh; background: #2d3436; display: flex; flex-direction: column; }
.custom-nav { background: linear-gradient(135deg, #0984e3, #74b9ff); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { flex: 1; display: flex; flex-direction: column; align-items: center; padding: 40rpx; }
.compass-dial { position: relative; width: 480rpx; height: 480rpx; margin-bottom: 40rpx; }
.dial-ring { width: 100%; height: 100%; border-radius: 50%; border: 6rpx solid #74b9ff; background: rgba(116, 185, 255, 0.1); position: relative; transition: transform 0.3s; }
.dir-n, .dir-e, .dir-s, .dir-w { position: absolute; font-size: 36rpx; font-weight: 700; }
.dir-n { top: 16rpx; left: 50%; transform: translateX(-50%); color: #ff6b6b; }
.dir-e { right: 16rpx; top: 50%; transform: translateY(-50%); color: #fff; }
.dir-s { bottom: 16rpx; left: 50%; transform: translateX(-50%); color: #fff; }
.dir-w { left: 16rpx; top: 50%; transform: translateY(-50%); color: #fff; }
.dial-center { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; }
.dial-degree { font-size: 56rpx; color: #fff; font-weight: 700; display: block; }
.dial-dir { font-size: 28rpx; color: #74b9ff; display: block; }
.compass-info { display: flex; gap: 40rpx; margin-bottom: 32rpx; }
.info-item { text-align: center; background: rgba(255,255,255,0.1); padding: 20rpx 40rpx; border-radius: 16rpx; }
.info-l { font-size: 24rpx; color: rgba(255,255,255,0.6); display: block; }
.info-v { font-size: 32rpx; color: #fff; font-weight: 600; display: block; margin-top: 4rpx; }
.compass-tip { font-size: 24rpx; color: #ffeaa7; }
</style>
