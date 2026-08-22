<template>
  <view class="weather-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">\u2190</text>
        <text class="nav-title">实时天气</text>
        <text class="nav-icon empty"> </text>
      </view>
    </view>

    <view v-if="!showMap" class="content">
      <view class="now-card">
        <view class="now-top">
          <text class="now-temp">{{ temperature }}°</text>
          <text class="now-icon">{{ weatherIcon }}</text>
        </view>
        <text class="now-desc">{{ weatherDesc }}</text>
        <text class="now-loc">{{ location }}</text>
      </view>

      <view class="detail-grid">
        <view class="d-card">
          <text class="d-icon">💧</text>
          <text class="d-label">湿度</text>
          <text class="d-value">{{ humidity }}%</text>
        </view>
        <view class="d-card">
          <text class="d-icon">💨</text>
          <text class="d-label">风速</text>
          <text class="d-value">{{ windSpeed }}km/h</text>
        </view>
        <view class="d-card">
          <text class="d-icon">🌡️</text>
          <text class="d-label">体感</text>
          <text class="d-value">{{ apparentTemp }}°</text>
        </view>
        <view class="d-card">
          <text class="d-icon">🔽</text>
          <text class="d-label">气压</text>
          <text class="d-value">{{ pressure }}hPa</text>
        </view>
        <view class="d-card">
          <text class="d-icon">👁️</text>
          <text class="d-label">能见度</text>
          <text class="d-value">{{ visibility }}km</text>
        </view>
        <view class="d-card">
          <text class="d-icon">☀️</text>
          <text class="d-label">紫外线</text>
          <text class="d-value">{{ uvIndex }}</text>
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

      <view class="cloud-card">
        <text class="cloud-title">🛰️ 卫星云图</text>
        <button class="cloud-btn" @click="showMap = true">查看实时云图</button>
        <text class="cloud-time">点击打开全球天气雷达地图</text>
      </view>

      <view class="hourly-card">
        <text class="hourly-title">⏰ 24小时预报</text>
        <scroll-view class="hourly-scroll" scroll-x>
          <view class="hourly-list">
            <view class="hour-item" v-for="(h, idx) in hourlyData" :key="idx">
              <text class="h-time">{{ h.time }}</text>
              <text class="h-icon">{{ h.icon }}</text>
              <text class="h-temp">{{ h.temp }}°</text>
            </view>
          </view>
        </scroll-view>
      </view>

      <button class="refresh-btn" @click="refreshWeather">刷新数据</button>
    </view>

    <view v-if="showMap" class="map-fullscreen">
      <view class="map-nav">
        <text class="map-back" @click="showMap = false">‹ 返回</text>
        <text class="map-title">🛰️ 全球天气雷达</text>
        <text class="map-space"> </text>
      </view>
      <web-view :src="mapUrl"></web-view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from "vue"

const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const temperature = ref("--")
const weatherIcon = ref("🌤️")
const weatherDesc = ref("加载中...")
const location = ref("")
const humidity = ref("--")
const windSpeed = ref("--")
const apparentTemp = ref("--")
const pressure = ref("--")
const visibility = ref("--")
const uvIndex = ref("--")
const hourlyData = ref([])
const manualLat = ref("")
const manualLng = ref("")
const showMap = ref(false)
const mapUrl = ref("")

function goBack() {
  if (showMap.value) { showMap.value = false; return }
  uni.navigateBack()
}

function getWeatherIcon(code) {
  if (code === 0) return "☀️"
  if (code <= 3) return "⛅"
  if (code <= 48) return "🌫️"
  if (code <= 57) return "🌦️"
  if (code <= 67) return "🌧️"
  if (code <= 77) return "🌨️"
  if (code <= 82) return "🌧️"
  if (code <= 86) return "❄️"
  if (code <= 99) return "⛈️"
  return "🌤️"
}

function getWeatherDesc(code) {
  if (code === 0) return "晴朗"
  if (code <= 3) return "多云"
  if (code <= 48) return "雾"
  if (code <= 57) return "毛毛雨"
  if (code <= 67) return "雨"
  if (code <= 77) return "雪"
  if (code <= 82) return "阵雨"
  if (code <= 86) return "阵雪"
  if (code <= 99) return "雷暴"
  return "未知"
}

function fetchWeather(lat, lng) {
  const params = "latitude=" + lat + "&longitude=" + lng + "&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,surface_pressure,visibility,uv_index&hourly=temperature_2m,weather_code&timezone=auto&forecast_days=1"
  uni.request({
    url: "https://api.open-meteo.com/v1/forecast?" + params,
    success: (res) => {
      const data = res.data
      if (data && data.current) {
        const c = data.current
        temperature.value = Math.round(c.temperature_2m)
        weatherIcon.value = getWeatherIcon(c.weather_code)
        weatherDesc.value = getWeatherDesc(c.weather_code)
        humidity.value = c.relative_humidity_2m
        windSpeed.value = c.wind_speed_10m
        apparentTemp.value = Math.round(c.apparent_temperature)
        pressure.value = Math.round(c.surface_pressure)
        visibility.value = (c.visibility / 1000).toFixed(1)
        uvIndex.value = c.uv_index != null ? c.uv_index : "--"
      }
      if (data && data.hourly) {
        const times = data.hourly.time
        const temps = data.hourly.temperature_2m
        const codes = data.hourly.weather_code
        const now = new Date()
        const list = []
        for (let i = 0; i < times.length; i++) {
          const t = new Date(times[i])
          if (t >= now && list.length < 24) {
            list.push({ time: t.getHours() + ":00", icon: getWeatherIcon(codes[i]), temp: Math.round(temps[i]) })
          }
        }
        hourlyData.value = list
      }
    },
    fail: () => { weatherDesc.value = "获取失败，请检查网络" }
  })
}

function fetchCityName(lat, lng) {
  uni.request({
    url: "https://nominatim.openstreetmap.org/reverse?format=json&lat=" + lat + "&lon=" + lng + "&zoom=10&addressdetails=1",
    header: { "User-Agent": "uni-app-tool/1.0" },
    success: (res) => {
      const addr = res.data && res.data.address
      if (addr) {
        const city = addr.city || addr.town || addr.village || addr.county || addr.state || ""
        const country = addr.country || ""
        location.value = city + (country ? ", " + country : "") + " (" + lat.toFixed(2) + ", " + lng.toFixed(2) + ")"
      } else {
        location.value = lat.toFixed(2) + ", " + lng.toFixed(2)
      }
    },
    fail: () => { location.value = lat.toFixed(2) + ", " + lng.toFixed(2) }
  })
}

function refreshWeather() { getLocation() }

function getLocation() {
  uni.showLoading({ title: "定位中..." })
  uni.getLocation({
    type: "wgs84",
    success: (res) => {
      uni.hideLoading()
      fetchWeatherAndCity(res.latitude, res.longitude)
    },
    fail: () => {
      uni.getLocation({
        type: "gcj02",
        success: (res) => {
          uni.hideLoading()
          fetchWeatherAndCity(res.latitude, res.longitude)
        },
        fail: () => {
          uni.hideLoading()
          uni.showToast({ title: "定位失败，请手动输入坐标", icon: "none" })
        }
      })
    }
  })
}

function fetchWeatherAndCity(lat, lng) {
  fetchWeather(lat, lng)
  fetchCityName(lat, lng)
  mapUrl.value = "https://www.windy.com/?" + lat.toFixed(2) + "," + lng.toFixed(2) + ",8"
}

function queryByManual() {
  if (!manualLat.value || !manualLng.value) { uni.showToast({ title: "请输入经纬度", icon: "none" }); return }
  const lat = parseFloat(manualLat.value)
  const lng = parseFloat(manualLng.value)
  if (lat < -90 || lat > 90 || lng < -180 || lng > 180) { uni.showToast({ title: "坐标范围无效", icon: "none" }); return }
  fetchWeatherAndCity(lat, lng)
}

onMounted(() => {
  if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }
  getLocation()
})
</script>

<style lang="scss" scoped>
.weather-page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #f59e0b, #f97316); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 32rpx; }
.now-card { background: linear-gradient(135deg, #f59e0b, #f97316); border-radius: 32rpx; padding: 48rpx 40rpx; margin-bottom: 24rpx; }
.now-top { display: flex; align-items: center; justify-content: space-between; }
.now-temp { font-size: 96rpx; color: #fff; font-weight: 700; }
.now-icon { font-size: 80rpx; }
.now-desc { font-size: 32rpx; color: #fff; margin-top: 16rpx; display: block; }
.now-loc { font-size: 24rpx; color: rgba(255,255,255,0.8); margin-top: 8rpx; display: block; }
.detail-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16rpx; margin-bottom: 24rpx; }
.d-card { background: #fff; border-radius: 20rpx; padding: 24rpx 16rpx; display: flex; flex-direction: column; align-items: center; }
.d-icon { font-size: 36rpx; margin-bottom: 8rpx; }
.d-label { font-size: 22rpx; color: #999; margin-bottom: 4rpx; }
.d-value { font-size: 28rpx; color: #333; font-weight: 600; }
.input-card { background: #fff; border-radius: 20rpx; padding: 24rpx; margin-bottom: 24rpx; }
.input-title { font-size: 26rpx; color: #333; font-weight: 600; margin-bottom: 16rpx; display: block; }
.input-row { display: flex; gap: 16rpx; margin-bottom: 16rpx; }
.coord-input { flex: 1; height: 72rpx; border: 2rpx solid #e5e7eb; border-radius: 12rpx; padding: 0 20rpx; font-size: 26rpx; }
.input-btn { background: linear-gradient(135deg, #f59e0b, #f97316); color: #fff; border-radius: 12rpx; font-size: 26rpx; }
.cloud-card { background: #fff; border-radius: 24rpx; padding: 24rpx; margin-bottom: 24rpx; text-align: center; }
.cloud-title { font-size: 28rpx; font-weight: 600; color: #333; margin-bottom: 16rpx; display: block; }
.cloud-btn { background: linear-gradient(135deg, #06b6d4, #0ea5e9); color: #fff; border-radius: 50rpx; font-size: 28rpx; margin-bottom: 12rpx; }
.cloud-time { font-size: 22rpx; color: #999; display: block; }
.hourly-card { background: #fff; border-radius: 24rpx; padding: 24rpx; margin-bottom: 24rpx; }
.hourly-title { font-size: 28rpx; font-weight: 600; color: #333; margin-bottom: 16rpx; display: block; }
.hourly-scroll { white-space: nowrap; }
.hourly-list { display: inline-flex; gap: 24rpx; }
.hour-item { display: flex; flex-direction: column; align-items: center; padding: 8rpx 12rpx; }
.h-time { font-size: 22rpx; color: #999; }
.h-icon { font-size: 36rpx; margin: 8rpx 0; }
.h-temp { font-size: 26rpx; color: #333; font-weight: 600; }
.refresh-btn { background: linear-gradient(135deg, #f59e0b, #f97316); color: #fff; border-radius: 50rpx; font-size: 28rpx; }
.map-fullscreen { position: fixed; top: 0; left: 0; right: 0; bottom: 0; z-index: 999; background: #fff; display: flex; flex-direction: column; }
.map-nav { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; background: linear-gradient(135deg, #06b6d4, #0ea5e9); }
.map-back { width: 120rpx; font-size: 32rpx; color: #fff; font-weight: 600; }
.map-title { flex: 1; text-align: center; font-size: 30rpx; color: #fff; font-weight: 600; }
.map-space { width: 120rpx; }
.web-view { flex: 1; }
</style>


