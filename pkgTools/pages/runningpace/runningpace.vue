<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u8dd1\u6b65\u914d\u901f\u8ba1\u7b97</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="form-card"><text class="form-label">\u8ddd\u79bb (km)</text><input class="form-input" type="digit" v-model="distance" placeholder="\u5982: 5, 10, 21.0975" /></view>
      <view class="form-card"><text class="form-label">\u65f6\u95f4</text><view class="time-row"><input class="time-input" type="number" v-model="hours" placeholder="\u65f6" /><text class="time-sep">:</text><input class="time-input" type="number" v-model="minutes" placeholder="\u5206" /><text class="time-sep">:</text><input class="time-input" type="number" v-model="seconds" placeholder="\u79d2" /></view></view>
      <view class="calc-btn" @click="calc"><text>\u8ba1\u7b97\u914d\u901f</text></view>
      <view class="result-card" v-if="pace">
        <view class="result-row"><text>\u914d\u901f:</text><text class="result-val">{{ pace }} /km</text></view>
        <view class="result-row"><text>\u5e73\u5747\u901f\u5ea6:</text><text class="result-val">{{ speed }} km/h</text></view>
        <view class="result-row"><text>\u603b\u65f6\u95f4:</text><text class="result-val">{{ totalTime }}</text></view>
      </view>
      <view class="preset-row"><text class="preset-title">\u5feb\u901f\u8bbe\u7f6e:</text><text class="preset-btn" v-for="p in presets" :key="p.d" @click="distance=p.d">{{ p.label }}</text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const distance = ref("")
const hours = ref("")
const minutes = ref("")
const seconds = ref("")
const pace = ref("")
const speed = ref("")
const totalTime = ref("")
const presets = [{label:"5K",d:"5"},{label:"10K",d:"10"},{label:"\u534a\u9a6c",d:"21.0975"},{label:"\u5168\u9a6c",d:"42.195"}]
function calc() {
  const d = parseFloat(distance.value) || 0
  const h = parseInt(hours.value) || 0
  const m = parseInt(minutes.value) || 0
  const s = parseInt(seconds.value) || 0
  if (d <= 0) { uni.showToast({ title: "\u8bf7\u8f93\u5165\u8ddd\u79bb", icon: "none" }); return }
  if (h === 0 && m === 0 && s === 0) { uni.showToast({ title: "\u8bf7\u8f93\u5165\u65f6\u95f4", icon: "none" }); return }
  const totalSec = h * 3600 + m * 60 + s
  const paceSec = totalSec / d
  const pm = Math.floor(paceSec / 60)
  const ps = Math.round(paceSec % 60)
  pace.value = pm + "'" + (ps < 10 ? "0" : "") + ps + """
  speed.value = (d / (totalSec / 3600)).toFixed(2)
  totalTime.value = (h ? h + "\u65f6" : "") + (m ? m + "\u5206" : "") + (s ? s + "\u79d2" : "")
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #84fab0, #8fd3f4); }
.custom-nav { background: linear-gradient(135deg, #00b894, #55efc4); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.form-card { background: #fff; border-radius: 20rpx; padding: 24rpx; margin-bottom: 20rpx; }
.form-label { font-size: 26rpx; color: #666; display: block; margin-bottom: 12rpx; }
.form-input { font-size: 32rpx; color: #333; font-weight: 600; }
.time-row { display: flex; align-items: center; gap: 8rpx; }
.time-input { flex: 1; background: #f8f8f8; border-radius: 12rpx; padding: 16rpx; font-size: 32rpx; text-align: center; }
.time-sep { font-size: 36rpx; color: #999; font-weight: 700; }
.calc-btn { background: linear-gradient(135deg, #00b894, #55efc4); border-radius: 16rpx; padding: 24rpx; text-align: center; margin: 32rpx 0; }
.calc-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.result-card { background: #fff; border-radius: 24rpx; padding: 32rpx; }
.result-row { display: flex; justify-content: space-between; padding: 12rpx 0; font-size: 28rpx; }
.result-val { color: #00b894; font-weight: 700; }
.preset-row { margin-top: 24rpx; display: flex; align-items: center; gap: 12rpx; flex-wrap: wrap; }
.preset-title { color: rgba(255,255,255,0.8); font-size: 24rpx; }
.preset-btn { padding: 12rpx 24rpx; background: rgba(255,255,255,0.3); border-radius: 12rpx; color: #fff; font-size: 24rpx; }
</style>
