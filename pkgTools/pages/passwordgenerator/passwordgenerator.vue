<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u5bc6\u7801\u751f\u6210\u5668</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="opt-card"><text class="opt-label">\u957f\u5ea6: {{ length }}</text><slider :value="length" min="6" max="32" show-value @change="length=Number($event.detail.value)"/></view>
      <view class="opt-card">
        <view class="check-row"><checkbox :checked="useLower" @click="useLower=!useLower"/><text>\u5c0f\u5199\u5b57\u6bcd (a-z)</text></view>
        <view class="check-row"><checkbox :checked="useUpper" @click="useUpper=!useUpper"/><text>\u5927\u5199\u5b57\u6bcd (A-Z)</text></view>
        <view class="check-row"><checkbox :checked="useNum" @click="useNum=!useNum"/><text>\u6570\u5b57 (0-9)</text></view>
        <view class="check-row"><checkbox :checked="useSymbol" @click="useSymbol=!useSymbol"/><text>\u7279\u6b8a\u5b57\u7b26 (!@#$)</text></view>
      </view>
      <view class="gen-btn" @click="generate"><text>\u751f\u6210\u5bc6\u7801</text></view>
      <view class="result-card" v-if="password">
        <text class="pwd-text">{{ password }}</text>
        <view class="pwd-actions"><text class="pwd-btn" @click="copyPwd">\u590d\u5236</text><text class="pwd-btn regen" @click="generate">\u91cd\u65b0\u751f\u6210</text></view>
        <text class="strength-text" :style="{color: strengthColor}">{{ strengthText }}</text>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const length = ref(12)
const useLower = ref(true)
const useUpper = ref(true)
const useNum = ref(true)
const useSymbol = ref(false)
const password = ref("")
const strengthText = ref("")
const strengthColor = ref("#999")
function generate() {
  let chars = ""
  if (useLower.value) chars += "abcdefghijklmnopqrstuvwxyz"
  if (useUpper.value) chars += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  if (useNum.value) chars += "0123456789"
  if (useSymbol.value) chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
  if (!chars) { uni.showToast({ title: "\u81f3\u5c11\u9009\u4e00\u79cd", icon: "none" }); return }
  let pwd = ""
  for (let i = 0; i < length.value; i++) pwd += chars[Math.floor(Math.random() * chars.length)]
  password.value = pwd
  const s = (useLower.value?1:0)+(useUpper.value?1:0)+(useNum.value?1:0)+(useSymbol.value?1:0)
  if (s >= 3 && length.value >= 12) { strengthText.value = "\u5f3a"; strengthColor.value = "#00b894" }
  else if (s >= 2 && length.value >= 8) { strengthText.value = "\u4e2d"; strengthColor.value = "#fdcb6e" }
  else { strengthText.value = "\u5f31"; strengthColor.value = "#e17055" }
}
function copyPwd() {
  uni.setClipboardData({ data: password.value, success: function() { uni.showToast({ title: "\u5df2\u590d\u5236", icon: "success" }) } })
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }; generate() })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #1e3c72, #2a5298); }
.custom-nav { background: linear-gradient(135deg, #1e3c72, #2a5298); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.opt-card { background: rgba(255,255,255,0.1); border-radius: 20rpx; padding: 24rpx; margin-bottom: 20rpx; }
.opt-label { font-size: 28rpx; color: #fff; display: block; margin-bottom: 12rpx; }
.check-row { display: flex; align-items: center; gap: 16rpx; padding: 12rpx 0; color: #fff; font-size: 26rpx; }
.gen-btn { background: linear-gradient(135deg, #00b894, #00cec9); border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 32rpx; }
.gen-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.result-card { background: #fff; border-radius: 24rpx; padding: 32rpx; text-align: center; }
.pwd-text { font-size: 28rpx; color: #333; font-family: monospace; word-break: break-all; display: block; margin-bottom: 20rpx; }
.pwd-actions { display: flex; gap: 16rpx; justify-content: center; margin-bottom: 16rpx; }
.pwd-btn { padding: 12rpx 24rpx; border-radius: 12rpx; background: #1e3c72; color: #fff; font-size: 24rpx; }
.pwd-btn.regen { background: #00b894; }
.strength-text { font-size: 24rpx; font-weight: 600; }
</style>
