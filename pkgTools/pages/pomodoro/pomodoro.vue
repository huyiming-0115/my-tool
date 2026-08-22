<template>
  <view class="pomo-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">←</text>
        <text class="nav-title">番茄钟</text>
        <text class="nav-icon" @click="showStats = !showStats">{{ showStats ? "📊" : "📊" }}</text>
      </view>
    </view>

    <view class="content">
      <view class="phase-badge" :class="phase">
        <text>{{ phaseLabel }}</text>
      </view>

      <view class="timer-circle">
        <view class="circle-ring">
          <text class="timer-text">{{ displayTime }}</text>
          <text class="timer-phase">{{ phaseLabel }}</text>
        </view>
      </view>

      <view class="session-info">
        <text class="session-label">第 {{ completedSessions + 1 }} 个番茄</text>
        <text class="session-dots">
          <text v-for="i in 4" :key="i" class="dot" :class="{ done: i <= completedSessions % 4 }"></text>
        </text>
      </view>

      <view class="controls">
        <button class="ctrl-btn reset" @click="resetTimer">重置</button>
        <button class="ctrl-btn start" :class="{ running }" @click="toggleTimer">{{ running ? "暂停" : "开始" }}</button>
        <button class="ctrl-btn skip" @click="skipPhase">跳过</button>
      </view>

      <view class="settings-card" v-if="showSettings">
        <view class="set-row"><text class="set-l">专注(分)</text><input class="set-input" v-model="workMin" type="number" /></view>
        <view class="set-row"><text class="set-l">短休(分)</text><input class="set-input" v-model="shortBreakMin" type="number" /></view>
        <view class="set-row"><text class="set-l">长休(分)</text><input class="set-input" v-model="longBreakMin" type="number" /></view>
        <view class="set-row"><text class="set-l">长休间隔</text><input class="set-input" v-model="sessionsForLong" type="number" /></view>
        <button class="set-save" @click="saveSettings">保存</button>
      </view>

      <text class="toggle-settings" @click="showSettings = !showSettings">{{ showSettings ? "收起设置 ▲" : "展开设置 ▼" }}</text>
    </view>

    <view v-if="showStats" class="stats-overlay" @click="showStats = false">
      <view class="stats-panel" @click.stop>
        <view class="stats-head"><text class="stats-title">今日统计</text><text class="stats-close" @click="showStats = false">×</text></view>
        <view class="stats-body">
          <view class="stat-item"><text class="stat-num">{{ todaySessions }}</text><text class="stat-label">完成番茄</text></view>
          <view class="stat-item"><text class="stat-num">{{ todayMinutes }}</text><text class="stat-label">专注分钟</text></view>
          <view class="stat-item"><text class="stat-num">{{ totalSessions }}</text><text class="stat-label">累计番茄</text></view>
        </view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20

const workMin = ref(25)
const shortBreakMin = ref(5)
const longBreakMin = ref(15)
const sessionsForLong = ref(4)

const phase = ref("work")
const remainingSeconds = ref(25 * 60)
const running = ref(false)
const completedSessions = ref(0)
const showSettings = ref(false)
const showStats = ref(false)
const sessionHistory = ref([])

let timer = null

const phaseLabel = computed(() => {
  if (phase.value === "work") return "专注中"
  if (phase.value === "short") return "短休息"
  return "长休息"
})

const displayTime = computed(() => {
  const m = Math.floor(remainingSeconds.value / 60)
  const s = remainingSeconds.value % 60
  return String(m).padStart(2, "0") + ":" + String(s).padStart(2, "0")
})

const totalSessions = computed(() => sessionHistory.value.length)
const todaySessions = computed(() => {
  const today = new Date().toISOString().slice(0, 10)
  return sessionHistory.value.filter(s => s.date === today).length
})
const todayMinutes = computed(() => todaySessions.value * workMin.value)

function toggleTimer() {
  if (running.value) {
    clearInterval(timer)
    running.value = false
  } else {
    running.value = true
    timer = setInterval(() => {
      remainingSeconds.value--
      if (remainingSeconds.value <= 0) {
        clearInterval(timer)
        running.value = false
        uni.vibrateLong({})
        if (phase.value === "work") {
          completedSessions.value++
          sessionHistory.value.push({ date: new Date().toISOString().slice(0, 10), timestamp: Date.now() })
          saveHistory()
          const cycle = completedSessions.value % sessionsForLong.value
          phase.value = cycle === 0 ? "long" : "short"
          remainingSeconds.value = (cycle === 0 ? longBreakMin.value : shortBreakMin.value) * 60
        } else {
          phase.value = "work"
          remainingSeconds.value = workMin.value * 60
        }
      }
    }, 1000)
  }
}

function resetTimer() {
  clearInterval(timer)
  running.value = false
  phase.value = "work"
  remainingSeconds.value = workMin.value * 60
}

function skipPhase() {
  clearInterval(timer)
  running.value = false
  if (phase.value === "work") {
    completedSessions.value++
    sessionHistory.value.push({ date: new Date().toISOString().slice(0, 10), timestamp: Date.now() })
    saveHistory()
  }
  phase.value = phase.value === "work" ? "short" : "work"
  remainingSeconds.value = (phase.value === "work" ? workMin.value : shortBreakMin.value) * 60
}

function saveSettings() {
  workMin.value = Math.max(1, parseInt(workMin.value) || 25)
  shortBreakMin.value = Math.max(1, parseInt(shortBreakMin.value) || 5)
  longBreakMin.value = Math.max(1, parseInt(longBreakMin.value) || 15)
  sessionsForLong.value = Math.max(2, parseInt(sessionsForLong.value) || 4)
  uni.setStorageSync("pomo_settings", JSON.stringify({
    workMin: workMin.value, shortBreakMin: shortBreakMin.value, longBreakMin: longBreakMin.value, sessionsForLong: sessionsForLong.value
  }))
  resetTimer()
  showSettings.value = false
  uni.showToast({ title: "已保存", icon: "success" })
}

function saveHistory() { uni.setStorageSync("pomo_history", JSON.stringify(sessionHistory.value)) }

function goBack() { uni.navigateBack() }

onUnmounted(() => { clearInterval(timer) })

onMounted(() => {
  if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }
  const s = uni.getStorageSync("pomo_settings")
  if (s) {
    try {
      const obj = JSON.parse(s)
      workMin.value = obj.workMin || 25
      shortBreakMin.value = obj.shortBreakMin || 5
      longBreakMin.value = obj.longBreakMin || 15
      sessionsForLong.value = obj.sessionsForLong || 4
      remainingSeconds.value = workMin.value * 60
    } catch (e) {}
  }
  const h = uni.getStorageSync("pomo_history")
  if (h) { try { sessionHistory.value = JSON.parse(h) } catch (e) {} }
})
</script>
<style lang="scss" scoped>
.pomo-page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #ef4444, #dc2626); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 32rpx; display: flex; flex-direction: column; align-items: center; }
.phase-badge { padding: 8rpx 32rpx; border-radius: 40rpx; font-size: 26rpx; font-weight: 600; margin-bottom: 32rpx; }
.phase-badge.work { background: #fef2f2; color: #ef4444; }
.phase-badge.short { background: #ecfdf5; color: #10b981; }
.phase-badge.long { background: #eff6ff; color: #3b82f6; }
.timer-circle { width: 480rpx; height: 480rpx; border-radius: 50%; background: #fff; box-shadow: 0 8rpx 40rpx rgba(0,0,0,0.06); display: flex; align-items: center; justify-content: center; margin-bottom: 32rpx; }
.circle-ring { display: flex; flex-direction: column; align-items: center; }
.timer-text { font-size: 96rpx; font-weight: 700; color: #1a1a1a; font-variant-numeric: tabular-nums; }
.timer-phase { font-size: 26rpx; color: #999; margin-top: 16rpx; }
.session-info { text-align: center; margin-bottom: 40rpx; }
.session-label { font-size: 26rpx; color: #666; display: block; }
.session-dots { display: flex; gap: 12rpx; justify-content: center; margin-top: 16rpx; }
.dot { width: 16rpx; height: 16rpx; border-radius: 50%; background: #e5e7eb; }
.dot.done { background: #ef4444; }
.controls { display: flex; gap: 24rpx; width: 100%; margin-bottom: 32rpx; }
.ctrl-btn { flex: 1; height: 88rpx; line-height: 88rpx; text-align: center; border-radius: 16rpx; font-size: 30rpx; font-weight: 600; border: none; }
.ctrl-btn::after { border: none; }
.ctrl-btn.start { background: linear-gradient(135deg, #ef4444, #dc2626); color: #fff; }
.ctrl-btn.start.running { background: linear-gradient(135deg, #f59e0b, #d97706); }
.ctrl-btn.reset { background: #fff; color: #666; border: 2rpx solid #e5e7eb; }
.ctrl-btn.reset::after { border: 2rpx solid #e5e7eb; }
.ctrl-btn.skip { background: #fff; color: #666; border: 2rpx solid #e5e7eb; }
.ctrl-btn.skip::after { border: 2rpx solid #e5e7eb; }
.settings-card { width: 100%; background: #fff; border-radius: 24rpx; padding: 24rpx; margin-bottom: 16rpx; }
.set-row { display: flex; align-items: center; padding: 16rpx 0; border-bottom: 2rpx solid #f8f8f8; }
.set-l { font-size: 26rpx; color: #333; width: 160rpx; font-weight: 500; }
.set-input { flex: 1; height: 56rpx; font-size: 28rpx; border: 2rpx solid #e5e7eb; border-radius: 8rpx; padding: 0 16rpx; }
.set-save { margin-top: 16rpx; height: 72rpx; line-height: 72rpx; background: linear-gradient(135deg, #ef4444, #dc2626); color: #fff; border-radius: 12rpx; font-size: 28rpx; font-weight: 600; border: none; }
.set-save::after { border: none; }
.toggle-settings { font-size: 24rpx; color: #999; padding: 16rpx; }
.stats-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 999; display: flex; align-items: center; justify-content: center; }
.stats-panel { width: 80%; background: #fff; border-radius: 32rpx; padding: 32rpx; }
.stats-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 32rpx; }
.stats-title { font-size: 32rpx; font-weight: 600; color: #1a1a1a; }
.stats-close { font-size: 40rpx; color: #999; padding: 4rpx 8rpx; }
.stats-body { display: flex; justify-content: space-between; }
.stat-item { text-align: center; flex: 1; }
.stat-num { font-size: 48rpx; font-weight: 700; color: #ef4444; display: block; }
.stat-label { font-size: 22rpx; color: #999; margin-top: 8rpx; display: block; }
</style>
