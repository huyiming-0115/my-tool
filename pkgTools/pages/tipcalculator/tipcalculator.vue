<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u5c0f\u8d39\u8ba1\u7b97\u5668</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="form-card"><text class="form-label">\u8d26\u5355\u91d1\u989d</text><input class="form-input" type="digit" v-model="amount" placeholder="\u8f93\u5165\u91d1\u989d" /></view>
      <view class="form-card">
        <text class="form-label">\u670d\u52a1\u8d28\u91cf</text>
        <view class="tip-options">
          <text class="tip-opt" :class="{active: tipRate===0.1}" @click="tipRate=0.1">10% \u4e0d\u6ee1\u610f</text>
          <text class="tip-opt" :class="{active: tipRate===0.15}" @click="tipRate=0.15">15% \u4e00\u822c</text>
          <text class="tip-opt" :class="{active: tipRate===0.18}" @click="tipRate=0.18">18% \u4e0d\u9519</text>
          <text class="tip-opt" :class="{active: tipRate===0.2}" @click="tipRate=0.2">20% \u5f88\u597d</text>
          <text class="tip-opt" :class="{active: tipRate===0.25}" @click="tipRate=0.25">25% \u6781\u4f73</text>
        </view>
      </view>
      <view class="form-card"><text class="form-label">\u4eba\u6570</text><input class="form-input" type="number" v-model="people" /></view>
      <view class="calc-btn" @click="calc"><text>\u8ba1\u7b97</text></view>
      <view class="result-card" v-if="tipAmount > 0">
        <view class="res-row"><text>\u5c06\u8d39:</text><text class="res-val">{{ tipAmount }} \u5143</text></view>
        <view class="res-row"><text>\u603b\u8ba1:</text><text class="res-val">{{ totalAmount }} \u5143</text></view>
        <view class="res-row" v-if="people > 1"><text>\u6bcf\u4eba:</text><text class="res-val">{{ perPerson }} \u5143</text></view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const amount = ref("")
const tipRate = ref(0.18)
const people = ref(1)
const tipAmount = ref(0)
const totalAmount = ref(0)
const perPerson = ref(0)
function calc() {
  const a = parseFloat(amount.value) || 0
  if (a <= 0) { uni.showToast({ title: "\u8bf7\u8f93\u5165\u91d1\u989d", icon: "none" }); return }
  tipAmount.value = (a * tipRate.value).toFixed(2)
  totalAmount.value = (a * (1 + tipRate.value)).toFixed(2)
  perPerson.value = (parseFloat(totalAmount.value) / people.value).toFixed(2)
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #667eea, #764ba2); }
.custom-nav { background: linear-gradient(135deg, #5a67d8, #6b46c1); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.form-card { background: #fff; border-radius: 20rpx; padding: 24rpx; margin-bottom: 20rpx; }
.form-label { font-size: 26rpx; color: #666; display: block; margin-bottom: 12rpx; }
.form-input { font-size: 36rpx; color: #333; font-weight: 600; }
.tip-options { display: flex; flex-direction: column; gap: 8rpx; }
.tip-opt { padding: 16rpx; border-radius: 12rpx; background: #f8f8f8; font-size: 26rpx; color: #666; }
.tip-opt.active { background: #5a67d8; color: #fff; }
.calc-btn { background: linear-gradient(135deg, #5a67d8, #6b46c1); border-radius: 16rpx; padding: 24rpx; text-align: center; margin: 32rpx 0; }
.calc-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.result-card { background: #fff; border-radius: 24rpx; padding: 32rpx; }
.res-row { display: flex; justify-content: space-between; padding: 12rpx 0; font-size: 28rpx; }
.res-val { color: #5a67d8; font-weight: 700; }
</style>
