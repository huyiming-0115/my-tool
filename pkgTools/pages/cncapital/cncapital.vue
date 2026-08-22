<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u5927\u5199\u91d1\u989d\u8f6c\u6362</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="form-card"><text class="form-label">\u8f93\u5165\u91d1\u989d</text><input class="form-input" type="digit" v-model="amount" placeholder="\u5982: 12345.67" /></view>
      <view class="calc-btn" @click="convert"><text>\u8f6c\u6362</text></view>
      <view class="result-card" v-if="result">
        <text class="result-label">\u4e2d\u6587\u5927\u5199</text>
        <text class="result-text">{{ result }}</text>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const amount = ref("")
const result = ref("")
const digits = ["\u96f6","\u58f9","\u8d30","\u53c1","\u8086","\u4f0d","\u9646","\u67d2","\u634c","\u7396"]
const units = ["", "\u62fe", "\u4f70", "\u4edf", "\u4e07", "\u62fe", "\u4f70", "\u4edf", "\u4ebf"]
function convert() {
  const val = parseFloat(amount.value)
  if (isNaN(val) || val < 0) { uni.showToast({ title: "\u8bf7\u8f93\u5165\u6709\u6548\u91d1\u989d", icon: "none" }); return }
  if (val > 999999999999.99) { uni.showToast({ title: "\u91d1\u989d\u8fc7\u5927", icon: "none" }); return }
  const parts = val.toFixed(2).split(".")
  const intPart = parts[0]
  const decPart = parts[1]
  let chinese = ""
  let zeroFlag = false
  const len = intPart.length
  for (let i = 0; i < len; i++) {
    const n = parseInt(intPart[i])
    const pos = len - i - 1
    if (n === 0) { zeroFlag = true }
    else {
      if (zeroFlag) { chinese += "\u96f6"; zeroFlag = false }
      chinese += digits[n] + units[pos % 8]
    }
    if (pos === 4 && zeroFlag) { chinese += "\u4e07"; zeroFlag = false }
    if (pos === 8) { chinese += "\u4ebf"; zeroFlag = false }
  }
  if (!chinese) chinese = "\u96f6"
  chinese += "\u5143"
  if (decPart[0] === "0" && decPart[1] === "0") chinese += "\u6574"
  else {
    if (decPart[0] !== "0") chinese += digits[parseInt(decPart[0])] + "\u89d2"
    if (decPart[1] !== "0") chinese += digits[parseInt(decPart[1])] + "\u5206"
  }
  result.value = chinese
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #ffecd2, #fcb69f); }
.custom-nav { background: linear-gradient(135deg, #e17055, #fdcb6e); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.form-card { background: #fff; border-radius: 20rpx; padding: 24rpx; margin-bottom: 20rpx; }
.form-label { font-size: 26rpx; color: #666; display: block; margin-bottom: 12rpx; }
.form-input { font-size: 36rpx; color: #333; font-weight: 600; }
.calc-btn { background: linear-gradient(135deg, #e17055, #fdcb6e); border-radius: 16rpx; padding: 24rpx; text-align: center; margin: 32rpx 0; }
.calc-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.result-card { background: #fff; border-radius: 24rpx; padding: 32rpx; text-align: center; }
.result-label { font-size: 24rpx; color: #999; display: block; margin-bottom: 12rpx; }
.result-text { font-size: 36rpx; color: #e17055; font-weight: 700; line-height: 1.6; }
</style>
