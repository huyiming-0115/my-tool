
<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">手持弹幕</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="input-bar"><input class="ls-input" v-model="text" placeholder="输入弹幕文字" maxlength="50" /></view>
      <view class="opts-row"><text class="opt-label">字体颜色:</text><view class="color-dot" v-for="c in colors" :key="c" :style="{background:c, border: fontColor===c?'4rpx solid #333':'none'}" @click="fontColor=c"></view></view>
      <view class="opts-row"><text class="opt-label">背景:</text><view class="color-dot" v-for="c in bgColors" :key="c" :style="{background:c, border: bgColor===c?'4rpx solid #333':'none'}" @click="bgColor=c"></view></view>
      <view class="opts-row"><text class="opt-label">速度:</text><slider class="ls-slider" :value="speed" min="1" max="10" show-value @change="speed=$event.detail.value"/></view>
      <view class="ls-btn" @click="startScroll"><text>开始滚动</text></view>
    </view>
    <view class="led-fullscreen" v-if="showLed" :style="{background: bgColor}">
      <view class="led-scroll-container" :style="{animationDuration: (11-speed)*0.3+'s'}">
        <text class="led-text" :style="{color: fontColor, textShadow: '0 0 20rpx '+fontColor}">{{ text || '欢迎使用' }}</text>
      </view>
      <view class="led-close" @click="showLed=false">×</view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const text = ref("")
const speed = ref(5)
const fontColor = ref("#00ff00")
const bgColor = ref("#000000")
const showLed = ref(false)
const colors = ["#00ff00","#ff0000","#ffff00","#00ffff","#ff00ff","#ffffff","#ff8800"]
const bgColors = ["#000000","#000088","#008800","#880000","#440044"]
function startScroll() { showLed.value = true }
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #0f0c29, #302b63); }
.custom-nav { background: linear-gradient(135deg, #0f0c29, #302b63); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.input-bar { margin-bottom: 24rpx; }
.ls-input { background: rgba(255,255,255,0.1); border-radius: 16rpx; padding: 20rpx 24rpx; font-size: 28rpx; color: #fff; }
.opts-row { display: flex; align-items: center; gap: 16rpx; margin-bottom: 20rpx; flex-wrap: wrap; }
.opt-label { color: rgba(255,255,255,0.7); font-size: 26rpx; }
.color-dot { width: 48rpx; height: 48rpx; border-radius: 50%; }
.ls-slider { flex: 1; }
.ls-btn { background: linear-gradient(135deg, #00b894, #00cec9); border-radius: 16rpx; padding: 24rpx; text-align: center; margin-top: 32rpx; }
.ls-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.led-fullscreen { position: fixed; inset: 0; z-index: 9999; display: flex; align-items: center; justify-content: center; overflow: hidden; }
.led-scroll-container { animation: ledScroll linear infinite; white-space: nowrap; }
.led-text { font-size: 80rpx; font-weight: 900; letter-spacing: 8rpx; }
@keyframes ledScroll { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
.led-close { position: absolute; top: 40rpx; right: 40rpx; font-size: 60rpx; color: rgba(255,255,255,0.5); z-index: 10000; }
</style>
