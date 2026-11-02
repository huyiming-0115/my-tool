
<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">银行卡校验</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="cv-card">
        <text class="cv-label">银行卡号</text>
        <input class="cv-input" type="number" v-model="cardNumber" placeholder="请输入银行卡号" maxlength="19" />
      </view>
      <view class="cv-btn" @click="validate"><text>验证</text></view>
      <view class="cv-result" v-if="validated">
        <view class="cv-result-icon" :class="{valid: isValid, invalid: !isValid}">{{isValid ? '✓' : '✗'}}</view>
        <text class="cv-result-text">{{resultText}}</text>
        <view class="cv-card-type" v-if="cardType"><text>卡类型: {{cardType}}</text></view>
      </view>
      <view class="cv-info">
        <text class="cv-info-title">Luhn算法说明</text>
        <text class="cv-info-text">Luhn算法（模10算法）是一种简单的校验和公式，用于验证银行卡号、信用卡号等数字标识符的有效性。</text>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const cardNumber = ref("")
const isValid = ref(false)
const validated = ref(false)
const resultText = ref("")
const cardType = ref("")
function luhnCheck(num) {
  var sum = 0
  var alternate = false
  for (var i = num.length - 1; i >= 0; i--) {
    var n = parseInt(num[i])
    if (alternate) {
      n *= 2
      if (n > 9) n -= 9
    }
    sum += n
    alternate = !alternate
  }
  return sum % 10 === 0
}
function getCardType(num) {
  if (/^4/.test(num)) return "Visa"
  if (/^5[1-5]/.test(num)) return "MasterCard"
  if (/^62/.test(num)) return "银联"
  if (/^3[47]/.test(num)) return "American Express"
  if (/^35/.test(num)) return "JCB"
  return "未知"
}
function validate() {
  var num = cardNumber.value.replace(/\s/g, "")
  if (!num || num.length < 13) {
    validated.value = true
    isValid.value = false
    resultText.value = "请输入有效的银行卡号"
    cardType.value = ""
    return
  }
  isValid.value = luhnCheck(num)
  cardType.value = getCardType(num)
  resultText.value = isValid.value ? "卡号有效（Luhn校验通过）" : "卡号无效（Luhn校验失败）"
  validated.value = true
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #11998e, #38ef7d); }
.custom-nav { background: linear-gradient(135deg, #11998e, #38ef7d); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 32rpx; }
.cv-card { background: rgba(255,255,255,0.2); border-radius: 20rpx; padding: 24rpx; margin-bottom: 24rpx; }
.cv-label { color: rgba(255,255,255,0.8); font-size: 26rpx; display: block; margin-bottom: 12rpx; }
.cv-input { background: rgba(255,255,255,0.3); border-radius: 12rpx; padding: 20rpx 24rpx; font-size: 36rpx; color: #fff; font-weight: 600; letter-spacing: 4rpx; }
.cv-btn { background: #fff; border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 24rpx; }
.cv-btn text { color: #11998e; font-size: 32rpx; font-weight: 700; }
.cv-result { background: rgba(255,255,255,0.2); border-radius: 20rpx; padding: 32rpx; text-align: center; margin-bottom: 24rpx; }
.cv-result-icon { width: 100rpx; height: 100rpx; border-radius: 50%; margin: 0 auto 16rpx; display: flex; align-items: center; justify-content: center; font-size: 48rpx; color: #fff; }
.cv-result-icon.valid { background: rgba(255,255,255,0.3); }
.cv-result-icon.invalid { background: rgba(255,0,0,0.3); }
.cv-result-text { color: #fff; font-size: 30rpx; font-weight: 600; display: block; }
.cv-card-type { margin-top: 12rpx; }
.cv-card-type text { color: rgba(255,255,255,0.7); font-size: 26rpx; }
.cv-info { background: rgba(255,255,255,0.1); border-radius: 20rpx; padding: 24rpx; }
.cv-info-title { color: rgba(255,255,255,0.8); font-size: 26rpx; font-weight: 600; display: block; margin-bottom: 12rpx; }
.cv-info-text { color: rgba(255,255,255,0.6); font-size: 24rpx; line-height: 1.6; }
</style>
