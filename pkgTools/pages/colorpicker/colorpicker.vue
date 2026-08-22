<template>
  <view class="cl-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">颜色拾取</text><text class="nav-icon" @click="copyHex">📋</text></view>
    </view>
    <view class="content">
      <view class="preview-box" :style="{ background: currentColor }">
        <text class="preview-text">{{ currentColor }}</text>
      </view>
      <view class="sliders">
        <view class="slider-row"><text class="s-label">R</text><slider class="s-bar" :value="r" min="0" max="255" block-size="20" activeColor="#ff6b6b" @change="r = $event.detail.value; updateColor()" /><text class="s-val">{{ r }}</text></view>
        <view class="slider-row"><text class="s-label">G</text><slider class="s-bar" :value="g" min="0" max="255" block-size="20" activeColor="#2ed573" @change="g = $event.detail.value; updateColor()" /><text class="s-val">{{ g }}</text></view>
        <view class="slider-row"><text class="s-label">B</text><slider class="s-bar" :value="b" min="0" max="255" block-size="20" activeColor="#4a90d9" @change="b = $event.detail.value; updateColor()" /><text class="s-val">{{ b }}</text></view>
      </view>
      <view class="color-values">
        <view class="cv-item" @click="copyHex"><text class="cv-label">HEX</text><text class="cv-val">{{ hexVal }}</text></view>
        <view class="cv-item" @click="copyRgb"><text class="cv-label">RGB</text><text class="cv-val">rgb({{ r }},{{ g }},{{ b }})</text></view>
      </view>
      <view class="palette">
        <text class="palette-title">常用色</text>
        <view class="palette-grid">
          <view class="palette-item" v-for="(c, idx) in palette" :key="idx" :style="{ background: c }" @click="setColor(c)"></view>
        </view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const r = ref(102)
const g = ref(126)
const b = ref(234)
const currentColor = ref("#667eea")
const hexVal = ref("#667EEA")
const palette = ["#ff6b6b", "#feca57", "#48dbfb", "#ff9ff3", "#54a0ff", "#5f27cd", "#00d2d3", "#ff9f43", "#ee5a24", "#6ab04c", "#be2edd", "#22a6b3", "#667eea", "#ed6663", "#2c3e50", "#95a5a6"]
function updateColor() { hexVal.value = "#" + [r.value, g.value, b.value].map(v => Number(v).toString(16).padStart(2, "0").toUpperCase()).join(""); currentColor.value = hexVal.value.toLowerCase() }
function setColor(hex) { const m = hex.match(/\w/g); r.value = parseInt(m[0] + m[1], 16); g.value = parseInt(m[2] + m[3], 16); b.value = parseInt(m[4] + m[5], 16); updateColor() }
function copyHex() { uni.setClipboardData({ data: hexVal.value, success: () => uni.showToast({ title: "已复制", icon: "success" }) }) }
function copyRgb() { uni.setClipboardData({ data: `rgb(${r.value},${g.value},${b.value})`, success: () => uni.showToast({ title: "已复制", icon: "success" }) }) }
function goBack() { uni.navigateBack() }
onMounted(() => { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.cl-page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #667eea, #764ba2); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 44rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.preview-box { height: 240rpx; border-radius: 24rpx; display: flex; align-items: center; justify-content: center; margin-bottom: 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.preview-text { font-size: 36rpx; color: #fff; font-weight: 700; text-shadow: 0 2rpx 8rpx rgba(0,0,0,0.3); }
.sliders { background: #fff; border-radius: 24rpx; padding: 16rpx 24rpx; margin-bottom: 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.slider-row { display: flex; align-items: center; padding: 16rpx 0; }
.s-label { font-size: 28rpx; font-weight: 700; width: 50rpx; }
.s-bar { flex: 1; }
.s-val { font-size: 26rpx; color: #666; width: 70rpx; text-align: right; }
.color-values { display: flex; gap: 24rpx; margin-bottom: 24rpx; }
.cv-item { flex: 1; background: #fff; border-radius: 16rpx; padding: 24rpx; text-align: center; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.cv-label { font-size: 24rpx; color: #999; display: block; }
.cv-val { font-size: 28rpx; color: #333; font-weight: 600; font-family: monospace; display: block; margin-top: 8rpx; }
.palette { background: #fff; border-radius: 24rpx; padding: 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.palette-title { font-size: 26rpx; color: #999; margin-bottom: 16rpx; display: block; }
.palette-grid { display: grid; grid-template-columns: repeat(8, 1fr); gap: 16rpx; }
.palette-item { width: 100%; height: 64rpx; border-radius: 12rpx; }
</style>
