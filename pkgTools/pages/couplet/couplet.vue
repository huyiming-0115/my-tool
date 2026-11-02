<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u5bf9\u8054\u751f\u6210\u5668</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="form-card"><text class="form-label">\u4e0a\u8054</text><input class="form-input" v-model="upperLine" placeholder="\u8f93\u5165\u4e0a\u8054" /></view>
      <view class="gen-btn" @click="generate"><text>\u751f\u6210\u4e0b\u8054</text></view>
      <view class="result-card" v-if="lowerLine">
        <view class="couplet-display">
          <text class="couplet-upper">{{ upperLine }}</text>
          <text class="couplet-lower">{{ lowerLine }}</text>
          <text class="couplet-horizontal">{{ horizontal }}</text>
        </view>
        <text class="copy-btn" @click="copyText">\u590d\u5236</text>
      </view>
      <view class="preset-card"><text class="preset-title">\u7ecf\u5178\u4e0a\u8054</text><view class="preset-list"><text class="preset-item" v-for="(p, i) in presetUppers" :key="i" @click="upperLine=p.line; lowerLine=p.lower; horizontal=p.h">{{ p.line }}</text></view></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const upperLine = ref("\u5929\u589e\u5c81\u6708\u589e\u5bff")
const lowerLine = ref("")
const horizontal = ref("")
const presetUppers = [
  {line:"\u5929\u589e\u5c81\u6708\u589e\u5bff", lower:"\u6625\u6ee1\u798f\u95e8\u5bcc\u6c49\u5b85", h:"\u559c\u6c14\u6c47\u95e8"},
  {line:"\u5409\u7965\u5982\u610f\u4e8b\u4e8b\u6210", lower:"\u5e78\u798f\u9999\u5bb6\u6709\u6709\u6709", h:"\u5409\u7965\u5982\u610f"},
  {line:"\u4e00\u6574\u5e74\u597d\u6625\u5168\u5728", lower:"\u5343\u91cc\u8305\u5c65\u6709\u4f59\u6708", h:"\u5409\u661f\u9ad8\u7167"},
  {line:"\u6c34\u6e05\u6708\u5148\u89c1", lower:"\u96e8\u8fc7\u5929\u6de1\u5fc3", h:"\u597d\u6625\u597d\u6708"},
  {line:"\u4e00\u4e16\u5409\u7965\u5409\u7965\u5409", lower:"\u5343\u95e8\u559c\u6c14\u559c\u6c14\u559c", h:"\u5409\u7965\u5982\u610f"}
]
function generate() {
  if (!upperLine.value) { uni.showToast({ title: "\u8bf7\u8f93\u5165\u4e0a\u8054", icon: "none" }); return }
  var found = presetUppers.find(function(p){return p.line === upperLine.value})
  if (found) { lowerLine.value = found.lower; horizontal.value = found.h }
  else { lowerLine.value = "\u559c\u6c14\u6c47\u95e8\u5bcc\u6c47\u5b85"; horizontal.value = "\u559c\u6c14\u6c47\u95e8" }
}
function copyText() {
  var text = "\u4e0a\u8054: " + upperLine.value + "\n\u4e0b\u8054: " + lowerLine.value + "\n\u6a2a\u627f: " + horizontal.value
  uni.setClipboardData({ data: text, success: function() { uni.showToast({ title: "\u5df2\u590d\u5236", icon: "success" }) } })
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #c0392b, #e74c3c); }
.custom-nav { background: linear-gradient(135deg, #c0392b, #e74c3c); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.form-card { background: #fff; border-radius: 20rpx; padding: 24rpx; margin-bottom: 20rpx; }
.form-label { font-size: 26rpx; color: #666; display: block; margin-bottom: 12rpx; }
.form-input { font-size: 32rpx; color: #333; font-weight: 600; }
.gen-btn { background: linear-gradient(135deg, #f39c12, #e17055); border-radius: 16rpx; padding: 24rpx; text-align: center; margin: 32rpx 0; }
.gen-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.result-card { background: #fff; border-radius: 24rpx; padding: 32rpx; text-align: center; margin-bottom: 24rpx; }
.couplet-display { margin-bottom: 20rpx; }
.couplet-upper, .couplet-lower { display: block; font-size: 32rpx; font-weight: 700; color: #c0392b; padding: 12rpx 0; }
.couplet-horizontal { display: block; font-size: 28rpx; font-weight: 600; color: #f39c12; margin-top: 12rpx; }
.copy-btn { display: inline-block; padding: 16rpx 32rpx; background: #c0392b; color: #fff; border-radius: 12rpx; font-size: 26rpx; }
.preset-card { background: rgba(255,255,255,0.2); border-radius: 16rpx; padding: 20rpx; }
.preset-title { font-size: 24rpx; color: #fff; display: block; margin-bottom: 12rpx; }
.preset-list { display: flex; flex-direction: column; gap: 8rpx; }
.preset-item { padding: 12rpx 16rpx; background: rgba(255,255,255,0.3); border-radius: 8rpx; color: #fff; font-size: 24rpx; }
</style>
