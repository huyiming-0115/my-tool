<template>
  <view class="study-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">←</text>
        <text class="nav-title">学习计时</text>
        <text class="nav-icon empty"> </text>
      </view>
    </view>
    <view class="content">
      <view class="today-card">
        <text class="today-hours">{{ todayMinutes }}</text>
        <text class="today-label">今日学习(分钟)</text>
      </view>
      <view class="subject-select">
        <text class="section-title">选择学科</text>
        <view class="subject-grid">
          <view class="subject-item" :class="{ active: currentSubject === s }" v-for="s in subjects" :key="s" @click="currentSubject = s">{{ s }}</view>
        </view>
      </view>
      <view class="timer-card">
        <text class="timer-display">{{ formatTime(timer) }}</text>
        <view class="timer-actions">
          <button class="timer-btn" @click="toggleTimer">{{ isRunning ? "暂停" : "开始" }}</button>
          <button class="timer-btn reset" @click="resetTimer">重置</button>
        </view>
      </view>
      <view class="section-title">本周统计</view>
      <view class="week-chart">
        <view class="w-bar" v-for="(d, idx) in weekData" :key="idx">
          <view class="w-fill" :style="{ height: getBarHeight(d.minutes) + '%' }"></view>
          <text class="w-label">{{ d.label }}</text>
        </view>
      </view>
      <view class="section-title">学科分布</view>
      <view class="subject-stats">
        <view class="subj-item" v-for="(s, idx) in subjectStats" :key="idx">
          <text class="subj-name">{{ s.name }}</text>
          <view class="subj-bar"><view class="subj-fill" :style="{ width: s.pct + '%' }"></view></view>
          <text class="subj-min">{{ s.minutes }}分</text>
        </view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const records = ref([])
const subjects = ["数学", "英语", "物理", "化学", "语文", "编程", "其他"]
const currentSubject = ref("数学")
const timer = ref(25 * 60)
const isRunning = ref(false)
let timerInterval = null
const todayMinutes = computed(() => {
  const today = new Date().toISOString().slice(0, 10)
  return records.value.filter(r => r.date === today).reduce((s, r) => s + r.minutes, 0)
})
const weekData = computed(() => {
  const days = ["日", "一", "二", "三", "四", "五", "六"]
  const result = []; const today = new Date()
  for (let i = 6; i >= 0; i--) {
    const d = new Date(today); d.setDate(d.getDate() - i)
    const dateStr = d.toISOString().slice(0, 10)
    const minutes = records.value.filter(r => r.date === dateStr).reduce((s, r) => s + r.minutes, 0)
    result.push({ label: days[d.getDay()], minutes })
  }
  return result
})
const subjectStats = computed(() => {
  const today = new Date().toISOString().slice(0, 10)
  const todayRecords = records.value.filter(r => r.date === today)
  const total = todayRecords.reduce((s, r) => s + r.minutes, 0) || 1
  return subjects.map(s => {
    const minutes = todayRecords.filter(r => r.subject === s).reduce((sum, r) => sum + r.minutes, 0)
    return { name: s, minutes, pct: (minutes / total) * 100 }
  }).filter(s => s.minutes > 0)
})
function getBarHeight(minutes) { const max = Math.max(...weekData.value.map(d => d.minutes), 60); return (minutes / max) * 100 }
function formatTime(s) { return String(Math.floor(s / 60)).padStart(2, "0") + ":" + String(s % 60).padStart(2, "0") }
function goBack() { uni.navigateBack() }
function toggleTimer() {
  if (isRunning.value) {
    clearInterval(timerInterval); isRunning.value = false
    if (timer.value < 25 * 60) {
      const elapsed = 25 * 60 - timer.value
      records.value.push({ date: new Date().toISOString().slice(0, 10), subject: currentSubject.value, minutes: Math.round(elapsed / 60) })
      saveData()
    }
  } else {
    isRunning.value = true
    timerInterval = setInterval(() => {
      timer.value--
      if (timer.value <= 0) { clearInterval(timerInterval); isRunning.value = false; timer.value = 25 * 60 }
    }, 1000)
  }
}
function resetTimer() { clearInterval(timerInterval); isRunning.value = false; timer.value = 25 * 60 }
function saveData() { uni.setStorageSync("study_records", JSON.stringify(records.value)) }
onUnmounted(() => { clearInterval(timerInterval) })
onMounted(() => {
  if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }
  const saved = uni.getStorageSync("study_records"); if (saved) { try { records.value = JSON.parse(saved) } catch (e) {} }
})
</script>
<style lang="scss" scoped>
.study-page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #3b82f6, #2563eb); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.today-card { background: linear-gradient(135deg, #3b82f6, #2563eb); border-radius: 24rpx; padding: 40rpx; text-align: center; margin-bottom: 24rpx; }
.today-hours { font-size: 64rpx; color: #fff; font-weight: 700; display: block; }
.today-label { font-size: 24rpx; color: rgba(255,255,255,0.7); margin-top: 8rpx; display: block; }
.section-title { font-size: 28rpx; font-weight: 600; color: #333; margin: 24rpx 0 16rpx; }
.subject-select { margin-bottom: 24rpx; }
.subject-grid { display: flex; flex-wrap: wrap; gap: 12rpx; }
.subject-item { padding: 12rpx 24rpx; background: #fff; border-radius: 30rpx; font-size: 24rpx; color: #666; }
.subject-item.active { background: linear-gradient(135deg, #3b82f6, #2563eb); color: #fff; }
.timer-card { background: #fff; border-radius: 24rpx; padding: 40rpx; text-align: center; margin-bottom: 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.timer-display { font-size: 80rpx; font-weight: 700; color: #3b82f6; display: block; font-variant-numeric: tabular-nums; }
.timer-actions { display: flex; gap: 24rpx; margin-top: 24rpx; }
.timer-btn { flex: 1; height: 72rpx; line-height: 72rpx; background: linear-gradient(135deg, #3b82f6, #2563eb); color: #fff; border-radius: 16rpx; font-size: 26rpx; }
.timer-btn.reset { background: #f5f5f5; color: #666; }
.week-chart { display: flex; align-items: flex-end; justify-content: space-between; background: #fff; border-radius: 24rpx; padding: 28rpx 16rpx; height: 200rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); margin-bottom: 24rpx; }
.w-bar { flex: 1; display: flex; flex-direction: column; align-items: center; height: 100%; justify-content: flex-end; }
.w-fill { width: 32rpx; background: linear-gradient(to top, #3b82f6, #93c5fd); border-radius: 8rpx 8rpx 0 0; min-height: 10rpx; }
.w-label { font-size: 20rpx; color: #999; margin-top: 8rpx; }
.subject-stats { background: #fff; border-radius: 24rpx; padding: 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.subj-item { display: flex; align-items: center; margin-bottom: 16rpx; }
.subj-name { width: 100rpx; font-size: 24rpx; color: #333; }
.subj-bar { flex: 1; height: 24rpx; background: #f5f5f5; border-radius: 12rpx; overflow: hidden; margin: 0 16rpx; }
.subj-fill { height: 100%; background: linear-gradient(135deg, #3b82f6, #2563eb); border-radius: 12rpx; }
.subj-min { width: 80rpx; text-align: right; font-size: 22rpx; color: #3b82f6; font-weight: 600; }
</style>
