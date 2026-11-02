<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u756a\u8304\u949fPro</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="stats-overview">
        <view class="stat-card"><text class="stat-num">{{ todayCount }}</text><text class="stat-label">\u4eca\u65e5</text></view>
        <view class="stat-card"><text class="stat-num">{{ weekCount }}</text><text class="stat-label">\u672c\u5468</text></view>
        <view class="stat-card"><text class="stat-num">{{ totalCount }}</text><text class="stat-label">\u603b\u8ba1</text></view>
      </view>
      <view class="timer-section">
        <text class="timer-display">{{ displayTime }}</text>
        <text class="timer-status">{{ isBreak ? '\u4f11\u606f\u4e2d' : '\u4e13\u6ce8\u4e2d' }}</text>
        <view class="timer-btns">
          <text class="t-btn start" @click="toggleTimer">{{ running ? '\u6682\u505c' : '\u5f00\u59cb' }}</text>
          <text class="t-btn reset" @click="resetTimer">\u91cd\u7f6e</text>
        </view>
      </view>
      <view class="history-section">
        <text class="hist-title">\u6700\u8fd1\u8bb0\u5f55</text>
        <view class="hist-item" v-for="(h, i) in history" :key="i">
          <text>{{ h.time }}</text>
          <text>{{ h.duration }}min</text>
          <text>{{ h.type }}</text>
        </view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, computed, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const todayCount = ref(5)
const weekCount = ref(23)
const totalCount = ref(156)
const totalSec = ref(25 * 60)
const running = ref(false)
const isBreak = ref(false)
let timer = null
const displayTime = computed(function() {
  var m = Math.floor(totalSec.value / 60), s = totalSec.value % 60
  return (m<10?"0":"")+m+":"+(s<10?"0":"")+s
})
const history = ref([
  {time:"10:30", duration:25, type:"\u5b66\u4e60"},
  {time:"11:00", duration:25, type:"\u5de5\u4f5c"},
  {time:"14:00", duration:25, type:"\u9605\u8bfb"},
  {time:"15:30", duration:25, type:"\u5199\u4f5c"}
])
function toggleTimer() {
  if (running.value) { clearInterval(timer); running.value = false; return }
  running.value = true
  timer = setInterval(function() {
    if (totalSec.value <= 0) {
      clearInterval(timer); running.value = false; uni.vibrateShort({})
      todayCount.value++; weekCount.value++; totalCount.value++
      isBreak.value = !isBreak.value
      totalSec.value = isBreak.value ? 5*60 : 25*60
    } else totalSec.value--
  }, 1000)
}
function resetTimer() { clearInterval(timer); running.value = false; isBreak.value = false; totalSec.value = 25*60 }
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
.content { padding: 40rpx; }
.stats-overview { display: flex; gap: 16rpx; margin-bottom: 32rpx; }
.stat-card { flex: 1; background: rgba(255,255,255,0.2); border-radius: 20rpx; padding: 24rpx; text-align: center; }
.stat-num { font-size: 40rpx; font-weight: 700; color: #fff; display: block; }
.stat-label { font-size: 22rpx; color: rgba(255,255,255,0.8); }
.timer-section { background: #fff; border-radius: 24rpx; padding: 40rpx; text-align: center; margin-bottom: 24rpx; }
.timer-display { font-size: 80rpx; font-weight: 200; color: #e17055; display: block; font-family: monospace; }
.timer-status { font-size: 26rpx; color: #999; display: block; margin-bottom: 24rpx; }
.timer-btns { display: flex; gap: 16rpx; justify-content: center; }
.t-btn { padding: 20rpx 40rpx; border-radius: 12rpx; font-size: 26rpx; font-weight: 600; }
.t-btn.start { background: #e17055; color: #fff; }
.t-btn.reset { background: #f0f0f0; color: #666; }
.history-section { background: #fff; border-radius: 20rpx; padding: 24rpx; }
.hist-title { font-size: 26rpx; font-weight: 600; color: #333; display: block; margin-bottom: 16rpx; }
.hist-item { display: flex; justify-content: space-between; padding: 12rpx 0; border-bottom: 2rpx solid #f0f0f0; font-size: 24rpx; color: #666; }
</style>
