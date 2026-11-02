<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u521d\u6563\u5f15\u5bfc</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="meditation-display">
        <view class="breath-circle" :class="{inhaling: phase==='\u5438\u606f', exhaling: phase==='\u547c\u606f'}">
          <text class="breath-text">{{ phase }}</text>
        </view>
        <text class="breath-timer">{{ breathSec }}s</text>
      </view>
      <view class="form-card"><text class="form-label">\u65f6\u957f (\u5206\u949f)</text><view class="time-options"><text class="time-opt" :class="{active: duration===1}" @click="duration=1">1</text><text class="time-opt" :class="{active: duration===3}" @click="duration=3">3</text><text class="time-opt" :class="{active: duration===5}" @click="duration=5">5</text><text class="time-opt" :class="{active: duration===10}" @click="duration=10">10</text></view></view>
      <view class="start-btn" @click="toggleMeditate"><text>{{ running ? '\u7ed3\u675f' : '\u5f00\u59cb\u521d\u6563' }}</text></view>
      <view class="tips-card"><text class="tips-title">\u547c\u5438\u8282\u594f</text><text class="tips-text">\u5438\u606f 4 \u79d2 \u2192 \u5438\u606f 4 \u79d2 \u2192 \u547c\u606f 4 \u79d2 \u2192 \u5438\u606f 4 \u79d2</text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const duration = ref(3)
const phase = ref("\u51c6\u5907")
const breathSec = ref(4)
const running = ref(false)
let timer = null
let totalTime = 0
function toggleMeditate() {
  if (running.value) { clearInterval(timer); running.value = false; phase.value = "\u51c6\u5907"; return }
  running.value = true
  totalTime = duration.value * 60
  var step = 0
  timer = setInterval(function() {
    step++
    breathSec.value = step % 4 === 0 ? 4 : breathSec.value - 1
    if (breathSec.value <= 0) { breathSec.value = 4; step = 0 }
    phase.value = step < 4 ? "\u5438\u606f" : "\u547c\u606f"
    totalTime--
    if (totalTime <= 0) { clearInterval(timer); running.value = false; phase.value = "\u5b8c\u6210"; uni.showToast({ title: "\u521d\u6563\u5b8c\u6210", icon: "success" }) }
  }, 1000)
}
function goBack() { clearInterval(timer); uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #2d3436, #636e72); }
.custom-nav { background: linear-gradient(135deg, #2d3436, #636e72); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; display: flex; flex-direction: column; align-items: center; }
.meditation-display { text-align: center; margin: 40rpx 0; }
.breath-circle { width: 300rpx; height: 300rpx; border-radius: 50%; border: 4rpx solid rgba(255,255,255,0.3); display: flex; align-items: center; justify-content: center; margin: 0 auto 24rpx; transition: 4s; }
.breath-circle.inhaling { transform: scale(1.3); border-color: #00b894; }
.breath-circle.exhaling { transform: scale(0.9); border-color: #74b9ff; }
.breath-text { font-size: 36rpx; color: #fff; font-weight: 600; }
.breath-timer { font-size: 48rpx; color: #fff; font-weight: 200; }
.form-card { width: 100%; background: rgba(255,255,255,0.1); border-radius: 20rpx; padding: 24rpx; margin-bottom: 24rpx; }
.form-label { font-size: 26rpx; color: rgba(255,255,255,0.7); display: block; margin-bottom: 16rpx; }
.time-options { display: flex; gap: 16rpx; }
.time-opt { flex: 1; text-align: center; padding: 20rpx; border-radius: 12rpx; background: rgba(255,255,255,0.1); color: #fff; font-size: 28rpx; }
.time-opt.active { background: #00b894; }
.start-btn { width: 80%; background: linear-gradient(135deg, #00b894, #00cec9); border-radius: 16rpx; padding: 28rpx; text-align: center; margin-bottom: 32rpx; }
.start-btn text { color: #fff; font-size: 32rpx; font-weight: 600; }
.tips-card { width: 100%; background: rgba(255,255,255,0.05); border-radius: 16rpx; padding: 24rpx; text-align: center; }
.tips-title { font-size: 26rpx; color: rgba(255,255,255,0.6); display: block; margin-bottom: 12rpx; }
.tips-text { font-size: 24rpx; color: rgba(255,255,255,0.5); }
</style>
