<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u94f6\u884c\u5361\u6821\u9a8c</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="form-card"><text class="form-label">\u94f6\u884c\u5361\u53f7</text><input class="form-input" type="number" v-model="cardNo" placeholder="\u8f93\u5165\u5361\u53f7" maxlength="19" /></view>
      <view class="calc-btn" @click="validate"><text>\u6821\u9a8c</text></view>
      <view class="result-card" v-if="result">
        <text class="result-label">\u6821\u9a8c\u7ed3\u679c</text>
        <text class="result-valid" v-if="result.valid" style="color:#00b894;">\u2714 \u6709\u6548\u7684\u5361\u53f7</text>
        <text class="result-valid" v-else style="color:#e17055;">\u2718 \u65e0\u6548\u7684\u5361\u53f7</text>
        <text class="result-text">\u5361\u7c7b\u578b: {{ result.type }}</text>
        <text class="result-text">\u4f4d\u6570: {{ cardNo.length }}</text>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const cardNo = ref("")
const result = ref(null)
function luhnCheck(num) {
  let sum = 0, alt = false
  for (let i = num.length - 1; i >= 0; i--) {
    let n = parseInt(num[i])
    if (alt) { n *= 2; if (n > 9) n -= 9 }
    sum += n; alt = !alt
  }
  return sum % 10 === 0
}
function getCardType(num) {
  if (/^4/.test(num)) return "Visa"
  if (/^5[1-5]/.test(num)) return "MasterCard"
  if (/^62/.test(num)) return "\u94f6\u8054"
  if (/^9558/.test(num)) return "\u5de5\u5546\u94f6\u884c"
  if (/^6222|^6223/.test(num)) return "\u4e2d\u65b9\u94f6\u884c"
  return "\u672a\u77e5"
}
function validate() {
  const num = cardNo.value.replace(/\s/g, "")
  if (!num || num.length < 13) { uni.showToast({ title: "\u8bf7\u8f93\u5165\u6709\u6548\u5361\u53f7", icon: "none" }); return }
  result.value = { valid: luhnCheck(num), type: getCardType(num) }
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #f093fb, #f5576c); }
.custom-nav { background: linear-gradient(135deg, #e84393, #fd79a8); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.form-card { background: #fff; border-radius: 20rpx; padding: 24rpx; margin-bottom: 20rpx; }
.form-label { font-size: 26rpx; color: #666; display: block; margin-bottom: 12rpx; }
.form-input { font-size: 32rpx; color: #333; font-weight: 600; letter-spacing: 4rpx; }
.calc-btn { background: linear-gradient(135deg, #e84393, #fd79a8); border-radius: 16rpx; padding: 24rpx; text-align: center; margin: 32rpx 0; }
.calc-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.result-card { background: #fff; border-radius: 24rpx; padding: 32rpx; text-align: center; }
.result-label { font-size: 24rpx; color: #999; display: block; margin-bottom: 12rpx; }
.result-valid { font-size: 32rpx; font-weight: 700; display: block; margin-bottom: 16rpx; }
.result-text { font-size: 26rpx; color: #666; display: block; padding: 4rpx 0; }
</style>
