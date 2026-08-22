<template>
  <view class="loan-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">房贷计算</text><text class="nav-icon" @click="resetForm">🔄</text></view>
    </view>
    <view class="content">
      <view class="form-card">
        <view class="form-row"><text class="form-l">贷款金额(万)</text><input class="form-input" v-model="amount" type="digit" placeholder="100" /></view>
        <view class="form-row"><text class="form-l">贷款年限</text><input class="form-input" v-model="years" type="number" placeholder="30" /></view>
        <view class="form-row"><text class="form-l">年利率(%)</text><input class="form-input" v-model="rate" type="digit" placeholder="3.1" /></view>
        <view class="type-row"><text class="type-label">还款方式</text><view class="type-btns"><text class="type-btn" :class="{ active: type === 'equal' }" @click="type = 'equal'; calc()">等额本息</text><text class="type-btn" :class="{ active: type === 'principal' }" @click="type = 'principal'; calc()">等额本金</text></view></view>
        <view class="calc-trigger" @click="calc"><text>计算</text></view>
      </view>
      <view class="result-card" v-if="result">
        <view class="result-main"><text class="r-label">月供</text><text class="r-value">{{ result.monthly }}</text><text class="r-unit">元</text></view>
        <view class="result-grid">
          <view class="r-item"><text class="ri-label">贷款总额</text><text class="ri-val">{{ result.totalLoan }}</text></view>
          <view class="r-item"><text class="ri-label">利息总额</text><text class="ri-val">{{ result.totalInterest }}</text></view>
          <view class="r-item"><text class="ri-label">还款总额</text><text class="ri-val">{{ result.totalPayment }}</text></view>
        </view>
      </view>
      <view class="tips" v-if="result"><text class="tip-text">ℹ️ 为估算值，实际以银行为准</text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const amount = ref("")
const years = ref("30")
const rate = ref("3.1")
const type = ref("equal")
const result = ref(null)
function calc() {
  const P = parseFloat(amount.value) * 10000
  const n = parseInt(years.value) * 12
  const r = parseFloat(rate.value) / 100 / 12
  if (!P || !n || !r) { uni.showToast({ title: "请填写完整", icon: "none" }); return }
  let monthly, totalPayment
  if (type.value === "equal") {
    monthly = P * r * Math.pow(1 + r, n) / (Math.pow(1 + r, n) - 1)
    totalPayment = monthly * n
  } else {
    const monthlyPrincipal = P / n
    monthly = P * r + monthlyPrincipal
    totalPayment = (P * r + monthlyPrincipal + monthlyPrincipal * (n + 1) / 2) * n / 2 + P
  }
  result.value = {
    monthly: monthly.toFixed(0),
    totalLoan: (P / 10000).toFixed(1) + "万",
    totalInterest: ((totalPayment - P) / 10000).toFixed(1) + "万",
    totalPayment: (totalPayment / 10000).toFixed(1) + "万"
  }
}
function resetForm() { amount.value = ""; years.value = "30"; rate.value = "3.1"; result.value = null }
function goBack() { uni.navigateBack() }
onMounted(() => { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.loan-page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #4facfe, #00f2fe); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 44rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.form-card { background: #fff; border-radius: 24rpx; padding: 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); margin-bottom: 24rpx; }
.form-row { display: flex; align-items: center; padding: 20rpx 0; border-bottom: 2rpx solid #f8f8f8; }
.form-l { font-size: 28rpx; color: #333; width: 200rpx; flex-shrink: 0; font-weight: 500; }
.form-input { flex: 1; font-size: 30rpx; height: 56rpx; text-align: right; }
.type-row { padding: 20rpx 0; }
.type-label { font-size: 28rpx; color: #333; font-weight: 500; display: block; margin-bottom: 16rpx; }
.type-btns { display: flex; gap: 16rpx; }
.type-btn { flex: 1; text-align: center; padding: 16rpx; background: #f5f5f5; border-radius: 12rpx; font-size: 26rpx; color: #666; }
.type-btn.active { background: linear-gradient(135deg, #4facfe, #00f2fe); color: #fff; }
.calc-trigger { background: linear-gradient(135deg, #4facfe, #00f2fe); border-radius: 16rpx; padding: 24rpx; text-align: center; margin-top: 24rpx; }
.calc-trigger text { font-size: 30rpx; color: #fff; font-weight: 600; }
.result-card { background: linear-gradient(135deg, #4facfe, #00f2fe); border-radius: 24rpx; padding: 32rpx; margin-bottom: 16rpx; }
.result-main { text-align: center; margin-bottom: 24rpx; }
.r-label { font-size: 24rpx; color: rgba(255,255,255,0.8); display: block; }
.r-value { font-size: 64rpx; color: #fff; font-weight: 700; display: block; }
.r-unit { font-size: 24rpx; color: rgba(255,255,255,0.8); }
.result-grid { display: flex; justify-content: space-between; background: rgba(255,255,255,0.15); border-radius: 16rpx; padding: 20rpx; }
.r-item { flex: 1; text-align: center; }
.ri-label { font-size: 22rpx; color: rgba(255,255,255,0.7); display: block; }
.ri-val { font-size: 30rpx; color: #fff; font-weight: 600; display: block; margin-top: 8rpx; }
.tips { text-align: center; }
.tip-text { font-size: 22rpx; color: #999; }
</style>
