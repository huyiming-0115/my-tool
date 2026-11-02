
<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">跑步配速计算</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="rp-card">
        <text class="rp-label">距离</text>
        <view class="rp-row"><input class="rp-input" type="digit" v-model="distance" placeholder="0" /><picker class="rp-unit" :value="distUnitIdx" :range="distUnits" @change="distUnitIdx=$event.detail.value"><text>{{distUnits[distUnitIdx]}}</text></picker></view>
      </view>
      <view class="rp-card">
        <text class="rp-label">用时</text>
        <view class="rp-time-row">
          <view class="rp-time-col"><input class="rp-input" type="number" v-model="hours" placeholder="0" /><text class="rp-time-label">时</text></view>
          <view class="rp-time-col"><input class="rp-input" type="number" v-model="minutes" placeholder="0" /><text class="rp-time-label">分</text></view>
          <view class="rp-time-col"><input class="rp-input" type="number" v-model="seconds" placeholder="0" /><text class="rp-time-label">秒</text></view>
        </view>
      </view>
      <view class="rp-btn" @click="calculate"><text>计算配速</text></view>
      <view class="rp-result" v-if="showResult">
        <view class="rp-result-card">
          <text class="rp-result-label">配速</text>
          <text class="rp-result-value">{{pace}}</text>
          <text class="rp-result-unit">/公里</text>
        </view>
        <view class="rp-result-card">
          <text class="rp-result-label">速度</text>
          <text class="rp-result-value">{{speed}}</text>
          <text class="rp-result-unit">km/h</text>
        </view>
        <view class="rp-result-card">
          <text class="rp-result-label">总用时</text>
          <text class="rp-result-value">{{totalTimeStr}}</text>
        </view>
      </view>
      <view class="rp-presets">
        <text class="rp-presets-title">常用距离</text>
        <view class="rp-presets-row">
          <view class="rp-preset" v-for="d in presets" :key="d" @click="distance=d; distUnitIdx=0"><text>{{d}}km</text></view>
        </view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const distance = ref("")
const distUnits = ["公里", "英里"]
const distUnitIdx = ref(0)
const hours = ref("")
const minutes = ref("")
const seconds = ref("")
const showResult = ref(false)
const pace = ref("")
const speed = ref("")
const totalTimeStr = ref("")
const presets = [3, 5, 10, 21.0975, 42.195]
function calculate() {
  var d = parseFloat(distance.value) || 0
  if (d <= 0) return
  if (distUnitIdx.value === 1) d = d * 1.60934
  var h = parseInt(hours.value) || 0
  var m = parseInt(minutes.value) || 0
  var s = parseInt(seconds.value) || 0
  var totalSec = h * 3600 + m * 60 + s
  if (totalSec <= 0) return
  var paceSec = totalSec / d
  var paceMin = Math.floor(paceSec / 60)
  var paceSecRem = Math.round(paceSec % 60)
  pace.value = paceMin + "'" + (paceSecRem < 10 ? "0" : "") + paceSecRem + """
  speed.value = (3600 / paceSec).toFixed(1)
  totalTimeStr.value = h + "时" + m + "分" + s + "秒"
  showResult.value = true
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #11998e, #38ef7d); }
.custom-nav { background: linear-gradient(135deg, #11998e, #38ef7d); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 32rpx; }
.rp-card { background: rgba(255,255,255,0.2); border-radius: 20rpx; padding: 24rpx; margin-bottom: 20rpx; }
.rp-label { color: rgba(255,255,255,0.8); font-size: 26rpx; display: block; margin-bottom: 12rpx; }
.rp-row { display: flex; gap: 12rpx; }
.rp-input { flex: 1; background: rgba(255,255,255,0.3); border-radius: 12rpx; padding: 16rpx 20rpx; font-size: 32rpx; color: #fff; font-weight: 600; }
.rp-unit { background: rgba(255,255,255,0.3); border-radius: 12rpx; padding: 16rpx 20rpx; display: flex; align-items: center; }
.rp-unit text { color: #fff; font-size: 28rpx; }
.rp-time-row { display: flex; gap: 12rpx; }
.rp-time-col { flex: 1; text-align: center; }
.rp-time-label { color: rgba(255,255,255,0.6); font-size: 24rpx; display: block; margin-top: 4rpx; }
.rp-btn { background: #fff; border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 24rpx; }
.rp-btn text { color: #11998e; font-size: 32rpx; font-weight: 700; }
.rp-result { display: flex; gap: 12rpx; margin-bottom: 24rpx; }
.rp-result-card { flex: 1; background: rgba(255,255,255,0.2); border-radius: 20rpx; padding: 20rpx; text-align: center; }
.rp-result-label { color: rgba(255,255,255,0.7); font-size: 22rpx; display: block; margin-bottom: 8rpx; }
.rp-result-value { color: #fff; font-size: 32rpx; font-weight: 700; display: block; }
.rp-result-unit { color: rgba(255,255,255,0.6); font-size: 20rpx; }
.rp-presets { background: rgba(255,255,255,0.1); border-radius: 20rpx; padding: 24rpx; }
.rp-presets-title { color: rgba(255,255,255,0.7); font-size: 24rpx; display: block; margin-bottom: 12rpx; }
.rp-presets-row { display: flex; gap: 12rpx; flex-wrap: wrap; }
.rp-preset { background: rgba(255,255,255,0.2); border-radius: 12rpx; padding: 12rpx 20rpx; }
.rp-preset text { color: #fff; font-size: 26rpx; }
</style>
