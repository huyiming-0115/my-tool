
<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">JWT解析器</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="jp-card">
        <text class="jp-label">JWT Token</text>
        <textarea class="jp-textarea" v-model="token" placeholder="粘贴JWT token..." />
      </view>
      <view class="jp-btn" @click="parse"><text>解析</text></view>
      <view class="jp-result" v-if="parsed">
        <view class="jp-section">
          <text class="jp-section-title">Header（头部）</text>
          <view class="jp-section-box"><text>{{header}}</text></view>
        </view>
        <view class="jp-section">
          <text class="jp-section-title">Payload（载荷）</text>
          <view class="jp-section-box"><text>{{payload}}</text></view>
        </view>
        <view class="jp-section" v-if="expireInfo">
          <text class="jp-section-title">过期信息</text>
          <text class="jp-expire" :class="{expired: isExpired}">{{expireInfo}}</text>
        </view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const token = ref("")
const header = ref("")
const payload = ref("")
const parsed = ref(false)
const expireInfo = ref("")
const isExpired = ref(false)
function base64UrlDecode(str) {
  str = str.replace(/-/g, "+").replace(/_/g, "/")
  while (str.length % 4) str += "="
  try {
    return decodeURIComponent(escape(atob(str)))
  } catch(e) {
    return atob(str)
  }
}
function parse() {
  if (!token.value.trim()) return
  var parts = token.value.trim().split(".")
  if (parts.length !== 3) {
    header.value = "无效的JWT格式"
    payload.value = "JWT应由三部分组成，用点号分隔"
    parsed.value = true
    return
  }
  try {
    header.value = JSON.stringify(JSON.parse(base64UrlDecode(parts[0])), null, 2)
    var payloadObj = JSON.parse(base64UrlDecode(parts[1]))
    payload.value = JSON.stringify(payloadObj, null, 2)
    if (payloadObj.exp) {
      var expDate = new Date(payloadObj.exp * 1000)
      isExpired.value = expDate < new Date()
      expireInfo.value = "过期时间: " + expDate.toLocaleString() + (isExpired.value ? " (已过期)" : " (有效)")
    }
    parsed.value = true
  } catch(e) {
    header.value = "解析失败"
    payload.value = e.message
    parsed.value = true
  }
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #6a11cb, #2575fc); }
.custom-nav { background: linear-gradient(135deg, #6a11cb, #2575fc); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 32rpx; }
.jp-card { background: rgba(255,255,255,0.15); border-radius: 20rpx; padding: 24rpx; margin-bottom: 20rpx; }
.jp-label { color: rgba(255,255,255,0.8); font-size: 26rpx; display: block; margin-bottom: 12rpx; }
.jp-textarea { background: rgba(255,255,255,0.15); border-radius: 12rpx; padding: 16rpx 20rpx; font-size: 24rpx; color: #fff; width: 100%; box-sizing: border-box; min-height: 200rpx; }
.jp-btn { background: #fff; border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 24rpx; }
.jp-btn text { color: #6a11cb; font-size: 32rpx; font-weight: 700; }
.jp-result { display: flex; flex-direction: column; gap: 20rpx; }
.jp-section { background: rgba(255,255,255,0.15); border-radius: 20rpx; padding: 24rpx; }
.jp-section-title { color: rgba(255,255,255,0.7); font-size: 26rpx; font-weight: 600; display: block; margin-bottom: 12rpx; }
.jp-section-box { background: rgba(0,0,0,0.2); border-radius: 12rpx; padding: 16rpx; }
.jp-section-box text { color: #fff; font-size: 24rpx; font-family: monospace; line-height: 1.6; white-space: pre-wrap; word-break: break-all; }
.jp-expire { color: #fff; font-size: 28rpx; font-weight: 600; }
.jp-expire.expired { color: #ff6b6b; }
</style>
