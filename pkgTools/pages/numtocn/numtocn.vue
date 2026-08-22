<template><view class="page"><view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }"><view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">数字大写</text><text class="nav-icon empty"> </text></view></view><view class="content"><input class="nc-input" v-model="number" type="digit" placeholder="输入金额..." maxlength="12" /><view class="nc-result" v-if="cnResult"><text>{{ cnResult }}</text></view><view class="nc-presets"><text class="preset-btn" v-for="p in [100,1000,10000,99999]" :key="p" @click="number = p + ''">{{ p }}元</text></view></view></view></template><script setup>import { ref, computed, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const number = ref("")
const digits = ["零","壹","贰","叁","肆","伍","陆","柒","捌","玖"]
const units = ["","拾","佰","仟","万","拾","佰","仟","亿"]
const cnResult = computed(function() {
  if (!number.value) return ""
  var num = parseFloat(number.value); if (isNaN(num) || num > 999999999999) return "超出范围"
  var intPart = Math.floor(num); var decPart = Math.round((num - intPart) * 100)
  var result = ""; var str = intPart + ""; var len = str.length
  for (var i = 0; i < len; i++) {
    var d = parseInt(str[i]); var u = units[len - 1 - i]
    if (d === 0) { if (result && !result.endsWith("零") && u !== "万" && u !== "亿") result += "零" }
    else { result += digits[d] + u }
  }
  result = result.replace(/零+$/, "").replace(/零万/g, "万").replace(/零亿/g, "亿")
  result = result || "零"; result += "元"
  if (decPart > 0) { var j = Math.floor(decPart / 10); var f = decPart % 10; if (j > 0) result += digits[j] + "角"; if (f > 0) result += digits[f] + "分" }
  else result += "整"
  return result
})
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script><style scoped>.page{min-height:100vh;background:#f5f7fb}.custom-nav{background:linear-gradient(135deg,#fdcb6e,#e17055);width:100%}.nav-row{height:88rpx;display:flex;align-items:center;padding:0 24rpx}.nav-icon{width:72rpx;text-align:center;font-size:48rpx;color:#fff;font-weight:700;flex-shrink:0}.nav-title{flex:1;text-align:center;font-size:32rpx;color:#fff;font-weight:600}.content{padding:24rpx}.nc-input{width:100%;height:100rpx;background:#fff;border-radius:20rpx;padding:0 24rpx;font-size:36rpx;box-sizing:border-box;margin-bottom:24rpx}.nc-result{background:#fff;border-radius:20rpx;padding:32rpx;font-size:32rpx;color:#e17055;font-weight:600;margin-bottom:24rpx}.nc-presets{display:flex;gap:16rpx}.preset-btn{flex:1;text-align:center;padding:20rpx;background:#fff;border-radius:16rpx;font-size:26rpx;color:#666}</style>