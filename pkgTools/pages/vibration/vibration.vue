<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">震动马达</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="vb-presets">
        <text class="vb-section-title">预设模式</text>
        <view class="vb-preset-grid">
          <view class="vb-preset-card" v-for="(p, i) in presets" :key="i" @click="runPattern(p)">
            <text class="vb-preset-icon">{{p.icon}}</text>
            <text class="vb-preset-name">{{p.name}}</text>
          </view>
        </view>
      </view>
      <view class="vb-custom">
        <text class="vb-section-title">自定义震动</text>
        <view class="vb-custom-row">
          <text class="vb-label">震动时长(ms)</text>
          <input class="vb-input" type="number" v-model="customDuration" placeholder="200" />
        </view>
        <view class="vb-btn" @click="vibrateCustom"><text>震动一次</text></view>
      </view>
      <view class="vb-pattern-builder">
        <text class="vb-section-title">自定义模式</text>
        <text class="vb-hint">输入震动间隔序列，如: 100,200,100,200</text>
        <input class="vb-input" v-model="patternInput" placeholder="100,200,100,200" />
        <view class="vb-btn" @click="vibratePattern"><text>执行模式</text></view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const customDuration = ref(200)
const patternInput = ref("100,200,100,200")
const presets = [
  { name: "短震", icon: "⚡", pattern: function() { uni.vibrateShort({}) } },
  { name: "长震", icon: "📱", pattern: function() { uni.vibrateLong({}) } },
  { name: "心跳", icon: "❤️", pattern: function() { var t = setInterval(function() { uni.vibrateShort({}) }, 300); setTimeout(function() { clearInterval(t) }, 1500) } },
  { name: "警报", icon: "🚨", pattern: function() { var arr = [100,50,100,50,100]; var i = 0; var t = setInterval(function() { if (i >= arr.length) { clearInterval(t); return } uni.vibrateShort({}); i++ }, arr[i] || 100) } },
  { name: "渐强", icon: "📈", pattern: function() { var d = 50; var t = setInterval(function() { uni.vibrateShort({}); d += 30; if (d > 400) clearInterval(t) }, d) } },
  { name: "节奏", icon: "🎵", pattern: function() { var arr = [200,100,200,100,400]; var i = 0; var t = setInterval(function() { if (i >= arr.length) { clearInterval(t); return } uni.vibrateShort({}); i++ }, arr[i] || 200) } }
]
function runPattern(preset) {
  preset.pattern()
}
function vibrateCustom() {
  var d = parseInt(customDuration.value) || 200
  if (d < 100) { uni.vibrateShort({}); return }
  if (d > 10000) d = 10000
  uni.vibrateLong({})
}
function vibratePattern() {
  var parts = patternInput.value.split(",").map(function(s) { return parseInt(s.trim()) || 100 })
  if (parts.length === 0) return
  var i = 0
  var t = setInterval(function() {
    if (i >= parts.length) { clearInterval(t); return }
    if (parts[i] > 0) { uni.vibrateShort({}) }
    i++
  }, parts[i] || 100)
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #2c3e50, #4ca1af); }
.custom-nav { background: linear-gradient(135deg, #2c3e50, #4ca1af); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 32rpx; }
.vb-section-title { color: rgba(255,255,255,0.8); font-size: 28rpx; font-weight: 600; display: block; margin-bottom: 16rpx; }
.vb-preset-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16rpx; margin-bottom: 32rpx; }
.vb-preset-card { background: rgba(255,255,255,0.15); border-radius: 20rpx; padding: 24rpx; text-align: center; }
.vb-preset-icon { font-size: 48rpx; display: block; margin-bottom: 8rpx; }
.vb-preset-name { color: #fff; font-size: 26rpx; font-weight: 600; }
.vb-custom, .vb-pattern-builder { background: rgba(255,255,255,0.1); border-radius: 20rpx; padding: 24rpx; margin-bottom: 20rpx; }
.vb-custom-row { margin-bottom: 16rpx; }
.vb-label { color: rgba(255,255,255,0.7); font-size: 26rpx; display: block; margin-bottom: 12rpx; }
.vb-input { background: rgba(255,255,255,0.2); border-radius: 12rpx; padding: 16rpx 20rpx; font-size: 28rpx; color: #fff; margin-bottom: 16rpx; }
.vb-hint { color: rgba(255,255,255,0.5); font-size: 24rpx; display: block; margin-bottom: 12rpx; }
.vb-btn { background: rgba(255,255,255,0.3); border-radius: 16rpx; padding: 20rpx; text-align: center; }
.vb-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
</style>
