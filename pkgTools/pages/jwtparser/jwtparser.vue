<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">JWT\u89e3\u6790\u5668</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <textarea class="jwt-input" v-model="jwtText" placeholder="\u7c98\u8d34JWT Token" auto-height></textarea>
      <view class="calc-btn" @click="parse"><text>\u89e3\u6790</text></view>
      <view class="result-card" v-if="header">
        <text class="section-title">\u2728 Header</text>
        <textarea class="json-output" :value="header" disabled></textarea>
        <text class="section-title">\u2728 Payload</text>
        <textarea class="json-output" :value="payload" disabled></textarea>
        <text class="section-title">\u2728 Signature</text>
        <text class="sig-text">{{ signature }}</text>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const jwtText = ref("")
const header = ref("")
const payload = ref("")
const signature = ref("")
function base64UrlDecode(str) {
  try {
    str = str.replace(/-/g, "+").replace(/_/g, "/")
    while (str.length % 4) str += "="
    return decodeURIComponent(escape(atob(str)))
  } catch(e) { return "\u89e3\u7801\u5931\u8d25" }
}
function parse() {
  const parts = jwtText.value.trim().split(".")
  if (parts.length !== 3) { uni.showToast({ title: "\u65e0\u6548\u7684JWT\u683c\u5f0f", icon: "none" }); return }
  header.value = JSON.stringify(JSON.parse(base64UrlDecode(parts[0])), null, 2)
  payload.value = JSON.stringify(JSON.parse(base64UrlDecode(parts[1])), null, 2)
  signature.value = parts[2]
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #fad0c4, #ffd1ff); }
.custom-nav { background: linear-gradient(135deg, #e17055, #fd79a8); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.jwt-input { background: #fff; border-radius: 20rpx; padding: 24rpx; font-size: 24rpx; min-height: 160rpx; margin-bottom: 20rpx; }
.calc-btn { background: linear-gradient(135deg, #e17055, #fd79a8); border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 24rpx; }
.calc-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.result-card { background: #fff; border-radius: 24rpx; padding: 32rpx; }
.section-title { font-size: 28rpx; font-weight: 600; color: #333; display: block; margin: 16rpx 0 8rpx; }
.json-output { width: 100%; background: #f8f8f8; border-radius: 12rpx; padding: 16rpx; font-size: 22rpx; color: #333; min-height: 120rpx; }
.sig-text { font-size: 20rpx; color: #999; word-break: break-all; }
</style>
