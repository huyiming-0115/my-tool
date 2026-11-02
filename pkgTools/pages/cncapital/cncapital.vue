
<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">大写金额转换</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="cc-card">
        <text class="cc-label">输入金额</text>
        <input class="cc-input" type="digit" v-model="amount" placeholder="请输入数字金额" maxlength="14" />
      </view>
      <view class="cc-btn" @click="convert"><text>转换为大写</text></view>
      <view class="cc-result" v-if="result">
        <text class="cc-result-label">中文大写金额</text>
        <view class="cc-result-box"><text class="cc-result-text">{{result}}</text></view>
        <view class="cc-copy" @click="copyResult"><text>复制结果</text></view>
      </view>
      <view class="cc-examples">
        <text class="cc-ex-title">示例</text>
        <view class="cc-ex-row" v-for="ex in examples" :key="ex.num"><text>{{ex.num}}</text><text>{{ex.cn}}</text></view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const amount = ref("")
const result = ref("")
const digits = ["零","壹","贰","叁","肆","伍","陆","柒","捌","玖"]
const units = ["","拾","佰","仟","万","拾","佰","仟","亿","拾","佰","仟"]
const examples = [
  { num: "100.00", cn: "壹佰元整" },
  { num: "2068.50", cn: "贰仟零佰陆拾捌元伍角整" },
  { num: "10000.00", cn: "壹万元整" }
]
function convert() {
  var val = parseFloat(amount.value)
  if (isNaN(val) || val < 0) { result.value = "请输入有效金额"; return }
  if (val > 999999999999.99) { result.value = "金额过大"; return }
  var parts = val.toFixed(2).split(".")
  var intPart = parseInt(parts[0])
  var decPart = parseInt(parts[1])
  var cn = ""
  if (intPart === 0) {
    cn = "零元"
  } else {
    var intStr = intPart.toString()
    var len = intStr.length
    var zeroFlag = false
    for (var i = 0; i < len; i++) {
      var d = parseInt(intStr[i])
      var u = units[len - 1 - i]
      if (d === 0) {
        zeroFlag = true
        if (u === "万" || u === "亿") { cn += u }
      } else {
        if (zeroFlag) { cn += "零"; zeroFlag = false }
        cn += digits[d] + u
      }
    }
    cn += "元"
  }
  var jiao = Math.floor(decPart / 10)
  var fen = decPart % 10
  if (jiao === 0 && fen === 0) { cn += "整" }
  else {
    if (jiao > 0) cn += digits[jiao] + "角"
    if (fen > 0) cn += digits[fen] + "分"
  }
  result.value = cn
}
function copyResult() {
  uni.setClipboardData({ data: result.value })
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #43e97b, #38f9d7); }
.custom-nav { background: linear-gradient(135deg, #43e97b, #38f9d7); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 32rpx; }
.cc-card { background: rgba(255,255,255,0.2); border-radius: 20rpx; padding: 24rpx; margin-bottom: 20rpx; }
.cc-label { color: rgba(255,255,255,0.8); font-size: 26rpx; display: block; margin-bottom: 12rpx; }
.cc-input { background: rgba(255,255,255,0.3); border-radius: 12rpx; padding: 20rpx 24rpx; font-size: 36rpx; color: #fff; font-weight: 600; }
.cc-btn { background: #fff; border-radius: 16rpx; padding: 24rpx; text-align: center; margin: 24rpx 0; }
.cc-btn text { color: #38f9d7; font-size: 32rpx; font-weight: 700; }
.cc-result { background: rgba(255,255,255,0.2); border-radius: 20rpx; padding: 28rpx; margin-bottom: 24rpx; }
.cc-result-label { color: rgba(255,255,255,0.7); font-size: 24rpx; display: block; margin-bottom: 12rpx; }
.cc-result-box { background: rgba(255,255,255,0.15); border-radius: 16rpx; padding: 24rpx; }
.cc-result-text { color: #fff; font-size: 36rpx; font-weight: 700; line-height: 1.6; }
.cc-copy { margin-top: 16rpx; text-align: center; padding: 12rpx; background: rgba(255,255,255,0.2); border-radius: 12rpx; }
.cc-copy text { color: #fff; font-size: 26rpx; }
.cc-examples { background: rgba(255,255,255,0.1); border-radius: 20rpx; padding: 24rpx; }
.cc-ex-title { color: rgba(255,255,255,0.6); font-size: 24rpx; display: block; margin-bottom: 16rpx; }
.cc-ex-row { display: flex; justify-content: space-between; padding: 10rpx 0; border-bottom: 1rpx solid rgba(255,255,255,0.1); }
.cc-ex-row text { color: rgba(255,255,255,0.8); font-size: 26rpx; }
</style>
