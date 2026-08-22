<template>
  <view class="running-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">←</text>
        <text class="nav-title">跑步记录</text>
        <text class="nav-icon empty"> </text>
      </view>
    </view>
    <view class="content">
      <view class="stats-card">
        <view class="stat-item"><text class="s-num">{{ totalRuns }}</text><text class="s-label">总次数</text></view>
        <view class="stat-item"><text class="s-num">{{ totalDistance }}</text><text class="s-label">总里程(km)</text></view>
        <view class="stat-item"><text class="s-num">{{ totalDuration }}</text><text class="s-label">总时长(分)</text></view>
      </view>
      <view class="start-btn" @click="startRun" v-if="!isRunning">
        <text class="start-text">🏃 开始跑步</text>
      </view>
      <view class="running-card" v-if="isRunning">
        <text class="run-timer">{{ formatTime(runTimer) }}</text>
        <text class="run-dist">距离: {{ currentDistance }} km</text>
        <view class="run-actions">
          <button class="run-btn stop" @click="stopRun">结束</button>
        </view>
      </view>
      <view class="section-title">历史记录</view>
      <view class="record-list">
        <view class="record-item" v-for="(r, idx) in records" :key="idx">
          <view class="r-left"><text class="r-date">{{ r.date }}</text><text class="r-pace">配速 {{ r.pace }}</text></view>
          <view class="r-right"><text class="r-dist">{{ r.distance }}km</text><text class="r-dur">{{ r.duration }}分</text></view>
        </view>
      </view>
      <view class="empty-mini" v-if="records.length === 0"><text>还没有跑步记录</text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const records = ref([])
const isRunning = ref(false)
const runTimer = ref(0)
const currentDistance = ref(0)
let timer = null
let locations = []
const totalRuns = computed(() => records.value.length)
const totalDistance = computed(() => records.value.reduce((s, r) => s + r.distance, 0).toFixed(1))
const totalDuration = computed(() => records.value.reduce((s, r) => s + r.duration, 0))
function goBack() { uni.navigateBack() }
function formatTime(s) { return String(Math.floor(s / 60)).padStart(2, "0") + ":" + String(s % 60).padStart(2, "0") }
function startRun() {
  isRunning.value = true; runTimer.value = 0; currentDistance.value = 0; locations = []
  timer = setInterval(() => { runTimer.value++ }, 1000)
  uni.getLocation({ type: "gcj02", success: (res) => { locations.push({ lat: res.latitude, lng: res.longitude }) } })
}
function stopRun() {
  clearInterval(timer); isRunning.value = false
  if (locations.length >= 2) {
    let dist = 0
    for (let i = 1; i < locations.length; i++) {
      const dx = (locations[i].lng - locations[i - 1].lng) * 111000
      const dy = (locations[i].lat - locations[i - 1].lat) * 111000
      dist += Math.sqrt(dx * dx + dy * dy)
    }
    currentDistance.value = (dist / 1000).toFixed(2)
  }
  const dur = Math.max(1, Math.round(runTimer.value / 60))
  records.value.unshift({ date: new Date().toISOString().slice(0, 10), distance: parseFloat(currentDistance.value) || 0.5, duration: dur, pace: dur > 0 ? Math.floor(runTimer.value / 60 / (parseFloat(currentDistance.value) || 0.5)) + ":" + String(Math.round((runTimer.value % 60) / 10) * 10).padStart(2, "0") : "0:00" })
  saveData()
}
function saveData() { uni.setStorageSync("running_records", JSON.stringify(records.value)) }
onUnmounted(() => { clearInterval(timer) })
onMounted(() => {
  if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }
  const saved = uni.getStorageSync("running_records"); if (saved) { try { records.value = JSON.parse(saved) } catch (e) {} }
})
</script>
<style lang="scss" scoped>
.running-page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #ef4444, #dc2626); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.stats-card { background: linear-gradient(135deg, #ef4444, #dc2626); border-radius: 24rpx; padding: 32rpx; display: flex; justify-content: space-between; margin-bottom: 24rpx; }
.stat-item { text-align: center; flex: 1; }
.s-num { font-size: 36rpx; color: #fff; font-weight: 700; display: block; }
.s-label { font-size: 20rpx; color: rgba(255,255,255,0.7); margin-top: 4rpx; display: block; }
.start-btn { background: #fff; border-radius: 24rpx; padding: 40rpx; text-align: center; margin-bottom: 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.start-text { font-size: 32rpx; font-weight: 600; color: #ef4444; }
.running-card { background: #fff; border-radius: 24rpx; padding: 40rpx; text-align: center; margin-bottom: 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.run-timer { font-size: 72rpx; font-weight: 700; color: #ef4444; display: block; font-variant-numeric: tabular-nums; }
.run-dist { font-size: 28rpx; color: #666; margin-top: 16rpx; display: block; }
.run-actions { margin-top: 24rpx; }
.run-btn.stop { background: #ef4444; color: #fff; border-radius: 50rpx; font-size: 28rpx; }
.section-title { font-size: 28rpx; font-weight: 600; color: #333; margin: 24rpx 0 16rpx; }
.record-list { background: #fff; border-radius: 24rpx; padding: 8rpx 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.record-item { display: flex; justify-content: space-between; padding: 20rpx 0; border-bottom: 2rpx solid #f9f9f9; }
.r-left, .r-right { display: flex; flex-direction: column; }
.r-date { font-size: 24rpx; color: #333; font-weight: 600; }
.r-pace { font-size: 20rpx; color: #999; margin-top: 4rpx; }
.r-dist { font-size: 26rpx; color: #ef4444; font-weight: 600; }
.r-dur { font-size: 20rpx; color: #999; margin-top: 4rpx; }
.empty-mini { text-align: center; padding: 32rpx; font-size: 24rpx; color: #999; }
</style>
