<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u756a\u8304\u949f</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="timer-display">
        <text class="timer-text">{{ displayTime }}</text>
        <text class="timer-phase">{{ isBreak ? '\u4f11\u606f\u4e2d' : '\u4e13\u6ce8\u4e2d' }}</text>
      </view>
      <view class="timer-controls">
        <text class="ctrl-btn start" @click="toggleTimer">{{ running ? '\u6682\u505c' : '\u5f00\u59cb' }}</text>
        <text class="ctrl-btn reset" @click="resetTimer">\u91cd\u7f6e</text>
      </view>
      <view class="timer-stats">
        <text class="stat-item">\u5faa\u73af: {{ cycles }}/4</text>
        <text class="stat-item">\u5b8c\u6210: {{ completed }} \u4e2a\u756a\u8304</text>
      </view>
      <view class="timer-settings">
        <text class="set-title">\u65f6\u957f\u8bbe\u7f6e (\u5206\u949f)</text>
        <view class="set-row"><text class="set-label">\u4e13\u6ce8:</text><input class="set-input" type="number" v-model="workMin" :disabled="running" /></view>
        <view class="set-row"><text class="set-label">\u4f11\u606f:</text><input class="set-input" type="number" v-model="breakMin" :disabled="running" /></view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, computed, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const workMin = ref(25)
const breakMin = ref(5)
const totalSec = ref(25 * 60)
const running = ref(false)
const isBreak = ref(false)
const cycles = ref(0)
const completed = ref(0)
let timer = null
const displayTime = computed(function() {
  const m = Math.floor(totalSec.value / 60)
  const s = totalSec.value % 60
  return (m<10?"0":"") + m + ":" + (s<10?"0":"") + s
})
function toggleTimer() {
  if (running.value) { clearInterval(timer); running.value = false; return }
  running.value = true
  timer = setInterval(function() {
    if (totalSec.value <= 0) {
      clearInterval(timer); running.value = false
      uni.vibrateShort({})
      if (isBreak.value) { isBreak.value = false; totalSec.value = workMin.value * 60 }
      else { isBreak.value = true; totalSec.value = breakMin.value * 60; completed.value++; cycles.value++ }
    } else totalSec.value--
  }, 1000)
}
function resetTimer() { clearInterval(timer); running.value = false; isBreak.value = false; totalSec.value = workMin.value * 60 }
function goBack() { clearInterval(timer); uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #ff6b6b, #ee5a24); }
.custom-nav { background: linear-gradient(135deg, #e17055, #d63031); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; display: flex; flex-direction: column; align-items: center; }
.timer-display { text-align: center; margin: 40rpx 0; }
.timer-text { font-size: 120rpx; font-weight: 200; color: #fff; display: block; font-family: monospace; }
.timer-phase { font-size: 28rpx; color: rgba(255,255,255,0.8); }
.timer-controls { display: flex; gap: 24rpx; margin-bottom: 40rpx; }
.ctrl-btn { padding: 24rpx 48rpx; border-radius: 16rpx; font-size: 28rpx; font-weight: 600; }
.ctrl-btn.start { background: #fff; color: #e17055; }
.ctrl-btn.reset { background: rgba(255,255,255,0.2); color: #fff; }
.timer-stats { display: flex; gap: 32rpx; margin-bottom: 40rpx; }
.stat-item { color: rgba(255,255,255,0.8); font-size: 24rpx; }
.timer-settings { width: 100%; background: rgba(255,255,255,0.1); border-radius: 20rpx; padding: 24rpx; }
.set-title { font-size: 26rpx; color: #fff; display: block; margin-bottom: 16rpx; }
.set-row { display: flex; align-items: center; gap: 16rpx; margin-bottom: 12rpx; }
.set-label { color: rgba(255,255,255,0.8); font-size: 26rpx; min-width: 100rpx; }
.set-input { flex: 1; background: #fff; border-radius: 12rpx; padding: 12rpx 16rpx; font-size: 28rpx; }
</style>
