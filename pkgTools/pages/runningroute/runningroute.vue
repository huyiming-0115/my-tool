<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u8dd1\u6b65\u8def\u7ebf</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="stats-row">
        <view class="stat-card"><text class="stat-val">{{ totalDistance }}</text><text class="stat-label">\u603b\u8ddd\u79bb km</text></view>
        <view class="stat-card"><text class="stat-val">{{ totalRuns }}</text><text class="stat-label">\u6b21\u6570</text></view>
        <view class="stat-card"><text class="stat-val">{{ avgPace }}</text><text class="stat-label">\u5e73\u5747\u914d\u901f</text></view>
      </view>
      <view class="start-btn" @click="startRun"><text>{{ tracking ? '\u7ed3\u675f\u8dd1\u6b65' : '\u5f00\u59cb\u8dd1\u6b65' }}</text></view>
      <view class="run-info" v-if="tracking">
        <text class="run-time">{{ runTime }}</text>
        <text class="run-dist">{{ currentDist }} km</text>
      </view>
      <view class="history-card">
        <text class="hist-title">\u6700\u8fd1\u8bb0\u5f55</text>
        <view class="hist-item" v-for="(r, i) in history" :key="i">
          <text>{{ r.date }}</text>
          <text>{{ r.dist }} km</text>
          <text>{{ r.pace }}</text>
        </view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const totalDistance = ref("12.5")
const totalRuns = ref(8)
const avgPace = ref("5'30\"")
const tracking = ref(false)
const runTime = ref("00:00:00")
const currentDist = ref("0.00")
const history = ref([
  {date:"\u4eca\u5929", dist:"3.2", pace:"5'20\""},
  {date:"\u6628\u5929", dist:"5.0", pace:"5'40\""},
  {date:"\u524d\u5929", dist:"4.3", pace:"5'15\""}
])
let timer = null
let sec = 0
function startRun() {
  if (tracking.value) {
    clearInterval(timer); tracking.value = false
    totalRuns.value++
    totalDistance.value = (parseFloat(totalDistance.value) + parseFloat(currentDist.value)).toFixed(1)
    history.value.unshift({date:"\u4eca\u5929", dist: currentDist.value, pace: "5'30\""})
    return
  }
  tracking.value = true; sec = 0; currentDist.value = "0.00"
  timer = setInterval(function() {
    sec++
    var h = Math.floor(sec/3600), m = Math.floor((sec%3600)/60), s = sec%60
    runTime.value = (h<10?"0":"")+h+":"+(m<10?"0":"")+m+":"+(s<10?"0":"")+s
    currentDist.value = (sec * 0.0025).toFixed(2)
  }, 1000)
}
function goBack() { clearInterval(timer); uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #f6d365, #fda085); }
.custom-nav { background: linear-gradient(135deg, #f39c12, #e17055); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.stats-row { display: flex; gap: 16rpx; margin-bottom: 32rpx; }
.stat-card { flex: 1; background: #fff; border-radius: 20rpx; padding: 24rpx; text-align: center; }
.stat-val { font-size: 36rpx; font-weight: 700; color: #f39c12; display: block; }
.stat-label { font-size: 22rpx; color: #999; }
.start-btn { background: linear-gradient(135deg, #f39c12, #e17055); border-radius: 16rpx; padding: 28rpx; text-align: center; margin-bottom: 24rpx; }
.start-btn text { color: #fff; font-size: 32rpx; font-weight: 600; }
.run-info { background: #fff; border-radius: 20rpx; padding: 32rpx; text-align: center; margin-bottom: 24rpx; }
.run-time { font-size: 60rpx; font-weight: 200; color: #333; display: block; font-family: monospace; }
.run-dist { font-size: 28rpx; color: #999; }
.history-card { background: #fff; border-radius: 20rpx; padding: 24rpx; }
.hist-title { font-size: 26rpx; font-weight: 600; color: #333; display: block; margin-bottom: 16rpx; }
.hist-item { display: flex; justify-content: space-between; padding: 12rpx 0; border-bottom: 2rpx solid #f0f0f0; font-size: 24rpx; color: #666; }
</style>
