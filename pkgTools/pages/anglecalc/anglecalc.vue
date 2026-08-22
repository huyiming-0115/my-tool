<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">←</text>
        <text class="nav-title">角度计算</text>
        <text class="nav-icon"> </text>
      </view>
    </view>
    <view class="content">
      <view class="input-card">
        <text class="section-label">输入角度</text>
        <view class="input-row">
          <input class="num-input" type="digit" v-model="inputVal" @input="calcAll" placeholder="请输入数值" />
          <picker class="unit-picker" :range="units" @change="onUnitChange">
            <text class="picker-text">{{ units[unitIndex] }}</text>
          </picker>
        </view>
      </view>

      <view class="visual-card">
        <text class="section-label">角度示意</text>
        <view class="angle-display">
          <view class="angle-arc" :style="{ transform: 'rotate(' + (-displayAngle) + 'deg)' }"></view>
          <view class="angle-line"></view>
          <text class="angle-text">{{ displayAngle.toFixed(0) }}°</text>
        </view>
      </view>

      <view class="result-card">
        <text class="section-label">转换结果</text>
        <view class="result-item">
          <text class="result-name">度度 (°)</text>
          <text class="result-value">{{ degStr }}</text>
        </view>
        <view class="result-item">
          <text class="result-name">弧度 (rad)</text>
          <text class="result-value">{{ radStr }}</text>
        </view>
        <view class="result-item">
          <text class="result-name">盘度 (gon)</text>
          <text class="result-value">{{ gonStr }}</text>
        </view>
      </view>

      <view class="dms-card">
        <text class="section-label">度分秒 (DMS)</text>
        <view class="dms-row">
          <view class="dms-cell">
            <text class="dms-val">{{ dmsDeg }}</text>
            <text class="dms-unit">°</text>
          </view>
          <view class="dms-cell">
            <text class="dms-val">{{ dmsMin }}</text>
            <text class="dms-unit">''</text>
          </view>
          <view class="dms-cell">
            <text class="dms-val">{{ dmsSec }}</text>
            <text class="dms-unit">"</text>
          </view>
        </view>
      </view>

      <view class="formula-card">
        <text class="section-label">转换公式</text>
        <text class="formula-text">rad = deg × π / 180</text>
        <text class="formula-text">deg = rad × 180 / π</text>
        <text class="formula-text">gon = deg × 10 / 9</text>
      </view>

      <view class="ref-card">
        <text class="section-label">常用角度</text>
        <view class="quick-grid">
          <view class="quick-btn" @click="setAngle(30)"><text class="quick-text">30°</text></view>
          <view class="quick-btn" @click="setAngle(45)"><text class="quick-text">45°</text></view>
          <view class="quick-btn" @click="setAngle(60)"><text class="quick-text">60°</text></view>
          <view class="quick-btn" @click="setAngle(90)"><text class="quick-text">90°</text></view>
          <view class="quick-btn" @click="setAngle(180)"><text class="quick-text">180°</text></view>
          <view class="quick-btn" @click="setAngle(360)"><text class="quick-text">360°</text></view>
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
const units = ["度度 (°)", "弧度 (rad)", "盘度 (gon)"]
const unitIndex = ref(0)
const degStr = ref("0.00")
const radStr = ref("0.00")
const gonStr = ref("0.00")
const dmsDeg = ref("0")
const dmsMin = ref("0")
const dmsSec = ref("0.00")
const displayAngle = ref(0)

function onUnitChange(e) { unitIndex.value = e.detail.value; calcAll() }

function calcAll() {
  let v = parseFloat(inputVal.value)
  if (isNaN(v)) {
    degStr.value = "0.00"; radStr.value = "0.00"; gonStr.value = "0.00"
    dmsDeg.value = "0"; dmsMin.value = "0"; dmsSec.value = "0.00"
    displayAngle.value = 0
    return
  }
  let deg, rad, gon
  if (unitIndex.value === 0) { deg = v; rad = v * Math.PI / 180; gon = v * 10 / 9 }
  else if (unitIndex.value === 1) { deg = v * 180 / Math.PI; rad = v; gon = deg * 10 / 9 }
  else { deg = v * 9 / 10; rad = deg * Math.PI / 180; gon = v }
  degStr.value = deg.toFixed(2)
  radStr.value = rad.toFixed(4)
  gonStr.value = gon.toFixed(2)
  displayAngle.value = Math.min(Math.abs(deg), 360)
  updateDMS(deg)
}

function updateDMS(deg) {
  let sign = deg < 0 ? -1 : 1
  let abs = Math.abs(deg)
  let d = Math.floor(abs)
  let mFloat = (abs - d) * 60
  let m = Math.floor(mFloat)
  let s = (mFloat - m) * 60
  dmsDeg.value = (sign * d).toString()
  dmsMin.value = m.toString()
  dmsSec.value = s.toFixed(2)
}

function setAngle(val) {
  if (unitIndex.value === 0) { inputVal.value = val.toString() }
  else if (unitIndex.value === 1) { inputVal.value = (val * Math.PI / 180).toFixed(4) }
  else { inputVal.value = (val * 10 / 9).toFixed(2) }
  calcAll()
}
</script>
<style scoped>
.page { min-height: 100vh; background: #f5f7fb }
.custom-nav { background: linear-gradient(135deg, #14b8a6, #06b6d4); width: 100% }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx }
.nav-icon { width: 72rpx; text-align: center; font-size: 44rpx; color: #fff; font-weight: 700; flex-shrink: 0 }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600 }
.content { padding: 24rpx }
.section-label { font-size: 26rpx; color: #64748b; font-weight: 600; margin-bottom: 16rpx; display: block }
.input-card, .visual-card, .result-card, .dms-card, .formula-card, .ref-card { background: #fff; border-radius: 16rpx; padding: 24rpx; margin-bottom: 24rpx; box-shadow: 0 2rpx 12rpx rgba(0,0,0,0.06) }
.input-row { display: flex; align-items: center; gap: 16rpx }
.num-input { flex: 1; height: 80rpx; background: #f1f5f9; border-radius: 12rpx; padding: 0 24rpx; font-size: 32rpx; color: #1e293b }
.unit-picker { width: 220rpx; height: 80rpx; background: #ccfbf1; border-radius: 12rpx; display: flex; align-items: center; justify-content: center }
.picker-text { font-size: 26rpx; color: #0f766e; font-weight: 600 }
.angle-display { position: relative; width: 240rpx; height: 240rpx; margin: 20rpx auto }
.angle-arc { position: absolute; width: 200rpx; height: 200rpx; border: 6rpx solid #14b8a6; border-bottom: none; border-radius: 200rpx 200rpx 0 0; top: 20rpx; left: 20rpx; transform-origin: bottom center; transition: transform 0.3s }
.angle-line { position: absolute; width: 6rpx; height: 100rpx; background: #0d9488; left: 50%; top: 40rpx; transform-origin: bottom center; border-radius: 3rpx }
.angle-text { position: absolute; bottom: 0; left: 50%; transform: translateX(-50%); font-size: 28rpx; color: #0f766e; font-weight: 600 }
.result-item { background: linear-gradient(135deg, #ccfbf1, #cffafe); border-radius: 12rpx; padding: 24rpx; margin-bottom: 16rpx; display: flex; justify-content: space-between; align-items: center }
.result-item:last-child { margin-bottom: 0 }
.result-name { font-size: 28rpx; color: #115e59; font-weight: 600 }
.result-value { font-size: 36rpx; color: #1e293b; font-weight: 700 }
.dms-row { display: flex; gap: 16rpx }
.dms-cell { flex: 1; background: #f0fdfa; border-radius: 12rpx; padding: 24rpx; text-align: center; border: 1rpx solid #99f6e4 }
.dms-val { font-size: 40rpx; color: #0f766e; font-weight: 700 }
.dms-unit { font-size: 24rpx; color: #14b8a6; margin-left: 4rpx }
.formula-text { font-size: 26rpx; color: #475569; line-height: 2 }
.quick-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16rpx }
.quick-btn { background: #f0fdfa; border-radius: 12rpx; padding: 24rpx; text-align: center; border: 1rpx solid #99f6e4 }
.quick-text { font-size: 30rpx; color: #0f766e; font-weight: 600 }
</style>