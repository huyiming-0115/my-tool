<template>
  <view class="altitude-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">\u2190</text>
        <text class="nav-title">海拔高度</text>
        <text class="nav-icon empty"> </text>
      </view>
    </view>

    <view class="content">
      <view class="main-card">
        <view class="alt-circle">
          <text class="alt-value">{{ altitude }}</text>
          <text class="alt-unit">米</text>
        </view>
        <text class="alt-label">当前海拔</text>
      </view>

      <view class="info-grid">
        <view class="info-card">
          <text class="info-icon">📍</text>
          <text class="info-label">纬度</text>
          <text class="info-value">{{ latitude }}</text>
        </view>
        <view class="info-card">
          <text class="info-icon">📍</text>
          <text class="info-label">经度</text>
          <text class="info-value">{{ longitude }}</text>
        </view>
        <view class="info-card">
          <text class="info-icon">🎯</text>
          <text class="info-label">精度</text>
          <text class="info-value">{{ accuracy }}m</text>
        </view>
        <view class="info-card">
          <text class="info-icon">📡</text>
          <text class="info-label">来源</text>
          <text class="info-value">{{ source }}</text>
        </view>
      </view>

      <view class="input-card">
        <text class="input-title">手动输入坐标</text>
        <view class="input-row">
          <input class="coord-input" v-model="manualLat" placeholder="纬度 (如 39.9)" type="digit" />
          <input class="coord-input" v-model="manualLng" placeholder="经度 (如 116.4)" type="digit" />
        </view>
        <button class="input-btn" @click="queryByManual">查询</button>
      </view>

      <button class="refresh-btn" @click="getLocation">重新定位</button>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from "vue"

const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const altitude = ref("--")
const latitude = ref("--")
const longitude = ref("--")
const accuracy = ref("--")
const source = ref("--")
const manualLat = ref("")
const manualLng = ref("")

function goBack() {
  uni.navigateBack()
}

function getLocation() {
  uni.showLoading({ title: "定位中..." })
  uni.getLocation({
    type: "wgs84",
    success: (res) => {
      latitude.value = res.latitude.toFixed(6)
      longitude.value = res.longitude.toFixed(6)
      accuracy.value = Math.round(res.accuracy)
      source.value = "GPS"
      if (res.altitude) {
        altitude.value = res.altitude.toFixed(1)
      } else {
        fetchAltitude(res.latitude, res.longitude)
      }
      uni.hideLoading()
    },
    fail: () => {
      uni.getLocation({
        type: "gcj02",
        success: (res) => {
          latitude.value = res.latitude.toFixed(6)
          longitude.value = res.longitude.toFixed(6)
          accuracy.value = Math.round(res.accuracy)
          source.value = "网络"
          if (res.altitude) {
            altitude.value = res.altitude.toFixed(1)
          } else {
            fetchAltitude(res.latitude, res.longitude)
          }
          uni.hideLoading()
        },
        fail: () => {
          uni.hideLoading()
          uni.showToast({ title: "定位失败，请手动输入", icon: "none" })
        }
      })
    }
  })
}

function fetchAltitude(lat, lng) {
  uni.request({
    url: "https://api.open-elevation.com/api/v1/lookup?locations=" + lat + "," + lng,
    success: (res) => {
      if (res.data && res.data.results && res.data.results[0]) {
        altitude.value = res.data.results[0].elevation.toFixed(1)
        source.value = "API"
      } else {
        altitude.value = "无数据"
      }
    },
    fail: () => {
      altitude.value = "获取失败"
    }
  })
}

function queryByManual() {
  if (!manualLat.value || !manualLng.value) {
    uni.showToast({ title: "请输入经纬度", icon: "none" })
    return
  }
  const lat = parseFloat(manualLat.value)
  const lng = parseFloat(manualLng.value)
  if (lat < -90 || lat > 90 || lng < -180 || lng > 180) {
    uni.showToast({ title: "坐标范围无效", icon: "none" })
    return
  }
  latitude.value = lat.toFixed(6)
  longitude.value = lng.toFixed(6)
  accuracy.value = "--"
  source.value = "手动"
  fetchAltitude(lat, lng)
}

onMounted(() => {
  if (!uni.getStorageSync("isLoggedIn")) {
    uni.reLaunch({ url: "/pages/login/login" })
    return
  }
  getLocation()
})
</script>

<style lang="scss" scoped>
.altitude-page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #06b6d4, #0ea5e9); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 32rpx; }
.main-card { background: #fff; border-radius: 32rpx; padding: 60rpx 40rpx; display: flex; flex-direction: column; align-items: center; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); margin-bottom: 24rpx; }
.alt-circle { width: 240rpx; height: 240rpx; border-radius: 50%; background: linear-gradient(135deg, #06b6d4, #0ea5e9); display: flex; flex-direction: column; align-items: center; justify-content: center; margin-bottom: 24rpx; }
.alt-value { font-size: 64rpx; color: #fff; font-weight: 700; }
.alt-unit { font-size: 24rpx; color: rgba(255,255,255,0.8); }
.alt-label { font-size: 28rpx; color: #666; }
.info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16rpx; margin-bottom: 24rpx; }
.info-card { background: #fff; border-radius: 20rpx; padding: 24rpx; display: flex; flex-direction: column; align-items: center; }
.info-icon { font-size: 36rpx; margin-bottom: 8rpx; }
.info-label { font-size: 22rpx; color: #999; margin-bottom: 4rpx; }
.info-value { font-size: 28rpx; color: #333; font-weight: 600; }
.input-card { background: #fff; border-radius: 20rpx; padding: 24rpx; margin-bottom: 24rpx; }
.input-title { font-size: 26rpx; color: #333; font-weight: 600; margin-bottom: 16rpx; display: block; }
.input-row { display: flex; gap: 16rpx; margin-bottom: 16rpx; }
.coord-input { flex: 1; height: 72rpx; border: 2rpx solid #e5e7eb; border-radius: 12rpx; padding: 0 20rpx; font-size: 26rpx; }
.input-btn { background: linear-gradient(135deg, #06b6d4, #0ea5e9); color: #fff; border-radius: 12rpx; font-size: 26rpx; }
.refresh-btn { background: linear-gradient(135deg, #06b6d4, #0ea5e9); color: #fff; border-radius: 50rpx; font-size: 28rpx; }
</style>
