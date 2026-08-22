<template>
  <view class="cd-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">←</text>
        <text class="nav-title">倒计时</text>
        <text class="nav-icon empty"> </text>
      </view>
    </view>

    <view class="content">
      <view class="timer-display" v-if="!finished">
        <text class="timer-text">{{ displayTime }}</text>
        <text class="timer-label">{{ mode === "stopwatch" ? "经过时间" : "剩余时间" }}</text>
      </view>
      <view class="timer-finished" v-else>
        <text class="finished-text">时间到!</text>
      </view>

      <view class="input-card" v-if="!running && mode === 'countdown'">
        <view class="preset-row">
          <text class="preset-btn" @click="setPreset(1)">1分钟</text>
          <text class="preset-btn" @click="setPreset(3)">3分钟</text>
          <text class="preset-btn" @click="setPreset(5)">5分钟</text>
          <text class="preset-btn" @click="setPreset(10)">10分钟</text>
          <text class="preset-btn" @click="setPreset(25)">25分钟</text>
        </view>
        <view class="custom-row">
          <input class="time-input" v-model="inputMin" type="number" placeholder="分" />
          <text class="time-sep">:</text>
          <input class="time-input" v-model="inputSec" type="number" placeholder="秒" />
        </view>
      </view>

      <view class="mode-tabs">
        <text class="mode-tab" :class="{ active: mode === 'countdown' }" @click="mode = 'countdown'">倒计时</text>
        <text class="mode-tab" :class="{ active: mode === 'stopwatch' }" @click="mode = 'stopwatch'">正计时</text>
      </view>

      <view class="controls">
        <button class="ctrl-btn start" @click="toggleTimer">{{ running ? "暂停" : "开始" }}</button>
        <button class="ctrl-btn reset" @click="resetTimer">重置</button>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue"

const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const mode = ref("countdown")
const totalSeconds = ref(0)
const remainingSeconds = ref(0)
const running = ref(false)
const finished = ref(false)
const inputMin = ref("")
const inputSec = ref("")
let timer = null

const displayTime = computed(() => {
  const s = remainingSeconds.value
  const h = Math.floor(s / 3600)
  const m = Math.floor((s % 3600) / 60)
  const sec = s % 60
  if (h > 0) return String(h).padStart(2, "0") + ":" + String(m).padStart(2, "0") + ":" + String(sec).padStart(2, "0")
  return String(m).padStart(2, "0") + ":" + String(sec).padStart(2, "0")
})

function setPreset(min) {
  totalSeconds.value = min * 60
  remainingSeconds.value = min * 60
  finished.value = false
}

function toggleTimer() {
  if (mode.value === "countdown" && !running.value && remainingSeconds.value === 0) {
    const m = parseInt(inputMin.value) || 0
    const s = parseInt(inputSec.value) || 0
    if (m === 0 && s === 0) { uni.showToast({ title: "请设置时间", icon: "none" }); return }
    totalSeconds.value = m * 60 + s
    remainingSeconds.value = totalSeconds.value
    finished.value = false
  }
  if (running.value) {
    clearInterval(timer)
    running.value = false
  } else {
    if (remainingSeconds.value <= 0 && mode.value === "countdown") return
    running.value = true
    finished.value = false
    timer = setInterval(() => {
      if (mode.value === "countdown") {
        remainingSeconds.value--
        if (remainingSeconds.value <= 0) {
          remainingSeconds.value = 0
          clearInterval(timer)
          running.value = false
          finished.value = true
          uni.vibrateLong({})
        }
      } else {
        remainingSeconds.value++
      }
    }, 1000)
  }
}

function resetTimer() {
  clearInterval(timer)
  running.value = false
  finished.value = false
  if (mode.value === "countdown") {
    remainingSeconds.value = totalSeconds.value
  } else {
    remainingSeconds.value = 0
  }
}

function goBack() { uni.navigateBack() }

onUnmounted(() => { clearInterval(timer) })

onMounted(() => {
  if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }
})
</script>

<style lang="scss" scoped>
.cd-page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #f43f5e, #e11d48); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 32rpx; }
.timer-display { background: #fff; border-radius: 32rpx; padding: 60rpx 40rpx; text-align: center; margin-bottom: 32rpx; }
.timer-text { font-size: 96rpx; font-weight: 700; color: #333; display: block; font-variant-numeric: tabular-nums; }
.timer-label { font-size: 26rpx; color: #999; margin-top: 16rpx; display: block; }
.timer-finished { background: linear-gradient(135deg, #f43f5e, #e11d48); border-radius: 32rpx; padding: 80rpx 40rpx; text-align: center; margin-bottom: 32rpx; }
.finished-text { font-size: 60rpx; font-weight: 700; color: #fff; }
.input-card { background: #fff; border-radius: 24rpx; padding: 32rpx; margin-bottom: 24rpx; }
.preset-row { display: flex; gap: 12rpx; margin-bottom: 24rpx; flex-wrap: wrap; }
.preset-btn { padding: 12rpx 24rpx; background: #f5f5f5; border-radius: 30rpx; font-size: 24rpx; color: #666; }
.custom-row { display: flex; align-items: center; gap: 16rpx; }
.time-input { flex: 1; height: 80rpx; border: 2rpx solid #e5e7eb; border-radius: 12rpx; text-align: center; font-size: 32rpx; }
.time-sep { font-size: 40rpx; font-weight: 700; color: #333; }
.mode-tabs { display: flex; gap: 16rpx; margin-bottom: 24rpx; }
.mode-tab { flex: 1; text-align: center; padding: 16rpx; background: #fff; border-radius: 16rpx; font-size: 28rpx; color: #666; }
.mode-tab.active { background: linear-gradient(135deg, #f43f5e, #e11d48); color: #fff; }
.controls { display: flex; gap: 24rpx; }
.ctrl-btn { flex: 1; height: 88rpx; line-height: 88rpx; text-align: center; border-radius: 16rpx; font-size: 30rpx; font-weight: 600; }
.ctrl-btn.start { background: linear-gradient(135deg, #f43f5e, #e11d48); color: #fff; }
.ctrl-btn.reset { background: #fff; color: #666; border: 2rpx solid #e5e7eb; }
</style>
