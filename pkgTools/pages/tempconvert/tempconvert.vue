<template>
<view class="page">
  <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
    <view class="nav-row">
      <text class="nav-icon" @click="goBack">←</text>
      <text class="nav-title">温度转换</text>
      <text class="nav-icon"> </text>
    </view>
  </view>
  <view class="content">
    <view class="input-card">
      <text class="section-label">输入温度值</text>
      <view class="input-row">
        <input class="num-input" type="digit" v-model="inputVal" @input="calcAll" placeholder="请输入数值" />
        <picker class="unit-picker" :range="units" @change="onUnitChange">
          <text class="picker-text">{{ units[unitIndex] }}</text>
        </picker>
      </view>
    </view>
    <view class="result-card">
      <text class="section-label">转换结果</text>
      <view class="result-item" :style="{ background: tempColor(celsius) }">
        <text class="result-name">摄氏度 (°C)</text>
        <text class="result-value">{{ celsiusStr }}</text>
      </view>
      <view class="result-item" :style="{ background: tempColor(fahrenheit, 'f') }">
        <text class="result-name">华氏度 (°F)</text>
        <text class="result-value">{{ fahrenheitStr }}</text>
      </view>
      <view class="result-item" :style="{ background: tempColor(kelvin, 'k') }">
        <text class="result-name">开尔文 (K)</text>
        <text class="result-value">{{ kelvinStr }}</text>
      </view>
    </view>
    <view class="formula-card">
      <text class="section-label">转换公式</text>
      <text class="formula-text">°C = (°F - 32) × 5/9</text>
      <text class="formula-text">°F = °C × 9/5 + 32</text>
      <text class="formula-text">K = °C + 273.15</text>
      <text class="formula-text">°C = K - 273.15</text>
    </view>
    <view class="ref-card">
      <text class="section-label">常用参考</text>
      <view class="ref-item">
        <text class="ref-label">水的冰点</text>
        <text class="ref-val">0°C / 32°F / 273.15K</text>
      </view>
      <view class="ref-item">
        <text class="ref-label">室温</text>
        <text class="ref-val">20°C / 68°F / 293.15K</text>
      </view>
      <view class="ref-item">
        <text class="ref-label">冰箱冷藏</text>
        <text class="ref-val">4°C / 39.2°F / 277.15K</text>
      </view>
      <view class="ref-item">
        <text class="ref-label">人体体温</text>
        <text class="ref-val">37°C / 98.6°F / 310.15K</text>
      </view>
      <view class="ref-item">
        <text class="ref-label">水的沸点</text>
        <text class="ref-val">100°C / 212°F / 373.15K</text>
      </view>
    </view>
  </view>
</view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
function goBack() { uni.navigateBack() }
onMounted(function () {
  if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }
})
const inputVal = ref("")
const units = ["摄氏度 °C", "华氏度 °F", "开尔文 K"]
const unitIndex = ref(0)
const celsius = ref(0)
const fahrenheit = ref(32)
const kelvin = ref(273.15)
const celsiusStr = ref("0.00")
const fahrenheitStr = ref("32.00")
const kelvinStr = ref("273.15")
function onUnitChange(e) { unitIndex.value = e.detail.value; calcAll() }
function calcAll() {
  let v = parseFloat(inputVal.value)
  if (isNaN(v)) { celsiusStr.value = "—"; fahrenheitStr.value = "—"; kelvinStr.value = "—"; return }
  let c, f, k
  if (unitIndex.value === 0) { c = v; f = v * 9 / 5 + 32; k = v + 273.15 }
  else if (unitIndex.value === 1) { c = (v - 32) * 5 / 9; f = v; k = c + 273.15 }
  else { c = v - 273.15; f = c * 9 / 5 + 32; k = v }
  celsius.value = c; fahrenheit.value = f; kelvin.value = k
  celsiusStr.value = c.toFixed(2)
  fahrenheitStr.value = f.toFixed(2)
  kelvinStr.value = k.toFixed(2)
}
function tempColor(val, type) {
  let c = type === 'f' ? (val - 32) * 5 / 9 : type === 'k' ? val - 273.15 : val
  if (c <= 0) return "linear-gradient(135deg,#38bdf8,#0ea5e9)"
  if (c <= 15) return "linear-gradient(135deg,#67e8f9,#22d3ee)"
  if (c <= 25) return "linear-gradient(135deg,#a7f3d0,#34d399)"
  if (c <= 35) return "linear-gradient(135deg,#fde68a,#fbbf24)"
  return "linear-gradient(135deg,#fca5a5,#ef4444)"
}
</script>
<style scoped>
.page { min-height: 100vh; background: #f5f7fb }
.custom-nav { background: linear-gradient(135deg, #06b6d4, #0ea5e9); width: 100% }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx }
.nav-icon { width: 72rpx; text-align: center; font-size: 44rpx; color: #fff; font-weight: 700; flex-shrink: 0 }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600 }
.content { padding: 24rpx }
.section-label { font-size: 26rpx; color: #64748b; font-weight: 600; margin-bottom: 16rpx; display: block }
.input-card, .result-card, .formula-card, .ref-card { background: #fff; border-radius: 16rpx; padding: 24rpx; margin-bottom: 24rpx; box-shadow: 0 2rpx 12rpx rgba(0,0,0,0.06) }
.input-row { display: flex; align-items: center; gap: 16rpx }
.num-input { flex: 1; height: 80rpx; background: #f1f5f9; border-radius: 12rpx; padding: 0 24rpx; font-size: 32rpx; color: #1e293b }
.unit-picker { width: 220rpx; height: 80rpx; background: #e0f2fe; border-radius: 12rpx; display: flex; align-items: center; justify-content: center }
.picker-text { font-size: 26rpx; color: #0369a1; font-weight: 600 }
.result-item { border-radius: 12rpx; padding: 24rpx; margin-bottom: 16rpx; display: flex; justify-content: space-between; align-items: center }
.result-item:last-child { margin-bottom: 0 }
.result-name { font-size: 28rpx; color: #fff; font-weight: 600 }
.result-value { font-size: 36rpx; color: #fff; font-weight: 700 }
.formula-text { font-size: 26rpx; color: #475569; line-height: 2 }
.ref-item { display: flex; justify-content: space-between; align-items: center; padding: 16rpx 0; border-bottom: 1rpx solid #f1f5f9 }
.ref-item:last-child { border-bottom: none }
.ref-label { font-size: 26rpx; color: #334155 }
.ref-val { font-size: 24rpx; color: #64748b }
</style>