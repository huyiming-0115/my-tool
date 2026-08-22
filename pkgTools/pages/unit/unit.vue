<template>
  <view class="unit-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">←</text>
        <text class="nav-title">单位转换</text>
        <text class="nav-icon empty"> </text>
      </view>
    </view>

    <view class="content">
      <view class="category-tabs">
        <text class="tab" :class="{ active: category === 'length' }" @click="category = 'length'">长度</text>
        <text class="tab" :class="{ active: category === 'weight' }" @click="category = 'weight'">重量</text>
        <text class="tab" :class="{ active: category === 'temp' }" @click="category = 'temp'">温度</text>
        <text class="tab" :class="{ active: category === 'area' }" @click="category = 'area'">面积</text>
        <text class="tab" :class="{ active: category === 'volume' }" @click="category = 'volume'">体积</text>
        <text class="tab" :class="{ active: category === 'speed' }" @click="category = 'speed'">速度</text>
      </view>

      <view class="converter-card">
        <view class="conv-row">
          <input class="conv-input" v-model="inputValue" type="digit" placeholder="输入数值" @input="convert" />
          <picker class="conv-picker" :value="fromIdx" :range="currentUnits" range-key="name" @change="onFromChange">
            <text>{{ currentUnits[fromIdx].name }}</text>
          </picker>
        </view>
        <view class="conv-arrow">↓</view>
        <view class="conv-row">
          <text class="conv-result">{{ outputValue }}</text>
          <picker class="conv-picker" :value="toIdx" :range="currentUnits" range-key="name" @change="onToChange">
            <text>{{ currentUnits[toIdx].name }}</text>
          </picker>
        </view>
      </view>

      <view class="quick-table" v-if="quickList.length > 0">
        <text class="table-title">常用换算</text>
        <view class="table-row" v-for="(item, idx) in quickList" :key="idx">
          <text class="table-text">{{ item.from }}</text>
          <text class="table-arrow">=</text>
          <text class="table-text">{{ item.to }}</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from "vue"

const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const category = ref("length")
const inputValue = ref("")
const outputValue = ref("")
const fromIdx = ref(0)
const toIdx = ref(1)

const units = {
  length: [
    { name: "毫米 (mm)", factor: 0.001 },
    { name: "厘米 (cm)", factor: 0.01 },
    { name: "米 (m)", factor: 1 },
    { name: "千米 (km)", factor: 1000 },
    { name: "英寸 (in)", factor: 0.0254 },
    { name: "英尺 (ft)", factor: 0.3048 },
    { name: "码 (yd)", factor: 0.9144 },
    { name: "英里 (mi)", factor: 1609.344 },
    { name: "海里 (nmi)", factor: 1852 },
  ],
  weight: [
    { name: "毫克 (mg)", factor: 0.000001 },
    { name: "克 (g)", factor: 0.001 },
    { name: "千克 (kg)", factor: 1 },
    { name: "吨 (t)", factor: 1000 },
    { name: "盎司 (oz)", factor: 0.0283495 },
    { name: "磅 (lb)", factor: 0.453592 },
    { name: "斤", factor: 0.5 },
    { name: "两", factor: 0.05 },
  ],
  temp: [
    { name: "摄氏度 (°C)", factor: 1, type: "temp" },
    { name: "华氏度 (°F)", factor: 1, type: "temp" },
    { name: "开尔文 (K)", factor: 1, type: "temp" },
  ],
  area: [
    { name: "平方厘米 (cm²)", factor: 0.0001 },
    { name: "平方米 (m²)", factor: 1 },
    { name: "公顷 (ha)", factor: 10000 },
    { name: "平方公里 (km²)", factor: 1000000 },
    { name: "平方英寸 (in²)", factor: 0.00064516 },
    { name: "平方英尺 (ft²)", factor: 0.092903 },
    { name: "英亩 (acre)", factor: 4046.856422 },
    { name: "亩", factor: 666.6667 },
  ],
  volume: [
    { name: "毫升 (mL)", factor: 0.001 },
    { name: "升 (L)", factor: 1 },
    { name: "立方米 (m³)", factor: 1000 },
    { name: "立方厘米 (cm³)", factor: 0.001 },
    { name: "加仑 (US)", factor: 3.78541 },
    { name: "夸脱 (US)", factor: 0.946353 },
    { name: "品脱 (US)", factor: 0.473176 },
    { name: "杯 (US)", factor: 0.236588 },
    { name: "液盎司 (US)", factor: 0.029574 },
  ],
  speed: [
    { name: "米/秒 (m/s)", factor: 1 },
    { name: "千米/时 (km/h)", factor: 0.277778 },
    { name: "英里/时 (mph)", factor: 0.44704 },
    { name: "节 (kn)", factor: 0.514444 },
    { name: "马赫 (Ma)", factor: 340.29 },
  ],
}

const currentUnits = computed(() => units[category.value] || [])

const quickList = computed(() => {
  const list = []
  const u = currentUnits.value
  const val = parseFloat(inputValue.value) || 1
  for (let i = 0; i < Math.min(3, u.length); i++) {
    if (i === fromIdx.value) continue
    const result = doConvert(val, fromIdx.value, i)
    list.push({ from: val + " " + u[fromIdx.value].name, to: result + " " + u[i].name })
  }
  return list
})

function doConvert(val, from, to) {
  const u = currentUnits.value
  if (!u.length) return 0
  // Temperature special handling
  if (category.value === "temp") {
    let celsius
    if (from === 0) celsius = val
    else if (from === 1) celsius = (val - 32) * 5 / 9
    else celsius = val - 273.15
    if (to === 0) return celsius.toFixed(2)
    if (to === 1) return (celsius * 9 / 5 + 32).toFixed(2)
    return (celsius + 273.15).toFixed(2)
  }
  const base = val * u[from].factor
  const result = base / u[to].factor
  return result < 0.001 ? result.toExponential(3) : parseFloat(result.toFixed(6))
}

function convert() {
  const val = parseFloat(inputValue.value)
  if (isNaN(val)) { outputValue.value = ""; return }
  outputValue.value = doConvert(val, fromIdx.value, toIdx.value)
}

function onFromChange(e) {
  fromIdx.value = e.detail.value
  convert()
}

function onToChange(e) {
  toIdx.value = e.detail.value
  convert()
}

function goBack() { uni.navigateBack() }

onMounted(() => {
  if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }
})
</script>

<style lang="scss" scoped>
.unit-page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #6366f1, #8b5cf6); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.category-tabs { display: flex; flex-wrap: wrap; gap: 12rpx; margin-bottom: 24rpx; }
.tab { padding: 12rpx 24rpx; background: #fff; border-radius: 30rpx; font-size: 24rpx; color: #666; }
.tab.active { background: linear-gradient(135deg, #6366f1, #8b5cf6); color: #fff; }
.converter-card { background: #fff; border-radius: 24rpx; padding: 32rpx; margin-bottom: 24rpx; }
.conv-row { display: flex; align-items: center; gap: 16rpx; }
.conv-input { flex: 1; height: 80rpx; border: 2rpx solid #e5e7eb; border-radius: 12rpx; padding: 0 20rpx; font-size: 32rpx; font-weight: 600; }
.conv-result { flex: 1; height: 80rpx; line-height: 80rpx; font-size: 32rpx; font-weight: 600; color: #6366f1; }
.conv-picker { padding: 12rpx 20rpx; background: #f5f5f5; border-radius: 12rpx; font-size: 26rpx; min-width: 200rpx; }
.conv-arrow { text-align: center; font-size: 32rpx; color: #999; margin: 16rpx 0; }
.quick-table { background: #fff; border-radius: 24rpx; padding: 24rpx; }
.table-title { font-size: 26rpx; font-weight: 600; color: #333; margin-bottom: 16rpx; display: block; }
.table-row { display: flex; align-items: center; padding: 12rpx 0; border-bottom: 2rpx solid #f9f9f9; }
.table-text { flex: 1; font-size: 24rpx; color: #666; }
.table-arrow { font-size: 24rpx; color: #999; margin: 0 16rpx; }
</style>
