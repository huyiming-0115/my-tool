<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">←</text>
        <text class="nav-title">坡度计算</text>
        <text class="nav-icon"> </text>
      </view>
    </view>
    <view class="content">
      <view class="input-card">
        <text class="section-label">输入参数</text>
        <view class="input-group">
          <text class="inp-label">垂直高度 (rise)</text>
          <input class="num-input" type="digit" v-model="rise" @input="calcAll" placeholder="请输入垂直高度" />
        </view>
        <view class="input-group">
          <text class="inp-label">水平距离 (run)</text>
          <input class="num-input" type="digit" v-model="run" @input="calcAll" placeholder="请输入水平距离" />
        </view>
      </view>

      <view class="visual-card">
        <text class="section-label">三角形示意</text>
        <view class="triangle-container">
          <view class="triangle">
            <view class="tri-rise" :style="{ height: triRiseH + 'px' }">
              <text class="tri-label" v-show="rise">{{ rise }}</text>
            </view>
            <view class="tri-run" :style="{ width: triRunW + 'px' }">
              <text class="tri-label-run" v-show="run">{{ run }}</text>
            </view>
            <view class="tri-hyp"></view>
          </view>
        </view>
      </view>

      <view class="result-card">
        <text class="section-label">计算结果</text>
        <view class="result-grid">
          <view class="result-cell">
            <text class="cell-name">坡度百分比</text>
            <text class="cell-value">{{ slopePct }}%</text>
          </view>
          <view class="result-cell">
            <text class="cell-name">坡度比 (1:X)</text>
            <text class="cell-value">1:{{ slopeRatio }}</text>
          </view>
          <view class="result-cell">
            <text class="cell-name">角度 (°)</text>
            <text class="cell-value">{{ angleDeg }}°</text>
          </view>
          <view class="result-cell">
            <text class="cell-name">角度 (rad)</text>
            <text class="cell-value">{{ angleRad }}</text>
          </view>
        </view>
      </view>

      <view class="formula-card">
        <text class="section-label">计算公式</text>
        <text class="formula-text">坡度% = (rise / run) × 100</text>
        <text class="formula-text">角度 = arctan(rise / run)</text>
        <text class="formula-text">坡度比 = 1 : (run / rise)</text>
      </view>

      <view class="ref-card">
        <text class="section-label">常用参考</text>
        <view class="ref-item">
          <text class="ref-label">楼梯 (ADA标准)</text>
          <text class="ref-val">4.76° / 8.3% / 1:12</text>
        </view>
        <view class="ref-item">
          <text class="ref-label">楼梯 (一般)</text>
          <text class="ref-val">30°-35° / 58%-70%</text>
        </view>
        <view class="ref-item">
          <text class="ref-label">屋顶坡度 (低)</text>
          <text class="ref-val">18.4° / 33.3% / 1:3</text>
        </view>
        <view class="ref-item">
          <text class="ref-label">屋顶坡度 (中)</text>
          <text class="ref-val">26.6° / 50% / 1:2</text>
        </view>
        <view class="ref-item">
          <text class="ref-label">公路最大坡度</text>
          <text class="ref-val">6°-8° / 10%-14%</text>
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

const rise = ref("")
const run = ref("")
const slopePct = ref("0.00")
const slopeRatio = ref("0.00")
const angleDeg = ref("0.00")
const angleRad = ref("0.00")
const triRiseH = ref(20)
const triRunW = ref(80)

function calcAll() {
  let r = parseFloat(rise.value)
  let h = parseFloat(run.value)
  if (isNaN(r) || isNaN(h) || h === 0) {
    slopePct.value = "0.00"
    slopeRatio.value = "0.00"
    angleDeg.value = "0.00"
    angleRad.value = "0.00"
    triRiseH.value = 20
    triRunW.value = 80
    return
  }
  let pct = (r / h) * 100
  let ratio = r !== 0 ? (h / r).toFixed(2) : "0.00"
  let rad = Math.atan(r / h)
  let deg = rad * 180 / Math.PI
  slopePct.value = pct.toFixed(2)
  slopeRatio.value = ratio
  angleDeg.value = deg.toFixed(2)
  angleRad.value = rad.toFixed(4)
  let maxDim = 120
  let scale = Math.min(maxDim / Math.abs(h), maxDim / Math.abs(r))
  triRiseH.value = Math.max(20, Math.abs(r) * scale)
  triRunW.value = Math.max(40, Math.abs(h) * scale)
}
</script>
<style scoped>
.page { min-height: 100vh; background: #f5f7fb }
.custom-nav { background: linear-gradient(135deg, #8b5cf6, #7c3aed); width: 100% }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx }
.nav-icon { width: 72rpx; text-align: center; font-size: 44rpx; color: #fff; font-weight: 700; flex-shrink: 0 }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600 }
.content { padding: 24rpx }
.section-label { font-size: 26rpx; color: #64748b; font-weight: 600; margin-bottom: 16rpx; display: block }
.input-card, .visual-card, .result-card, .formula-card, .ref-card { background: #fff; border-radius: 16rpx; padding: 24rpx; margin-bottom: 24rpx; box-shadow: 0 2rpx 12rpx rgba(0,0,0,0.06) }
.input-group { margin-bottom: 20rpx }
.input-group:last-child { margin-bottom: 0 }
.inp-label { font-size: 26rpx; color: #475569; margin-bottom: 8rpx; display: block }
.num-input { height: 80rpx; background: #f1f5f9; border-radius: 12rpx; padding: 0 24rpx; font-size: 32rpx; color: #1e293b }
.triangle-container { display: flex; justify-content: center; padding: 20rpx 0 }
.triangle { position: relative; width: 200rpx; height: 200rpx; border-left: 3rpx solid #7c3aed; border-bottom: 3rpx solid #7c3aed; margin: 40rpx }
.tri-rise { position: absolute; left: -6rpx; bottom: 3rpx; width: 12rpx; background: rgba(139,92,246,0.3); border-radius: 6rpx 6rpx 0 0 }
.tri-label { position: absolute; top: -40rpx; left: 50%; transform: translateX(-50%); font-size: 22rpx; color: #7c3aed; white-space: nowrap }
.tri-run { position: absolute; left: 3rpx; bottom: -6rpx; height: 12rpx; background: rgba(124,58,237,0.3); border-radius: 0 6rpx 6rpx 0 }
.tri-label-run { position: absolute; bottom: -40rpx; left: 50%; transform: translateX(-50%); font-size: 22rpx; color: #7c3aed; white-space: nowrap }
.result-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16rpx }
.result-cell { background: #f8f5ff; border-radius: 12rpx; padding: 20rpx; border: 1rpx solid #ede9fe }
.cell-name { font-size: 24rpx; color: #6d28d9; display: block; margin-bottom: 8rpx }
.cell-value { font-size: 32rpx; color: #1e293b; font-weight: 700 }
.formula-text { font-size: 26rpx; color: #475569; line-height: 2 }
.ref-item { display: flex; justify-content: space-between; align-items: center; padding: 16rpx 0; border-bottom: 1rpx solid #f1f5f9 }
.ref-item:last-child { border-bottom: none }
.ref-label { font-size: 26rpx; color: #334155 }
.ref-val { font-size: 24rpx; color: #64748b }
</style>