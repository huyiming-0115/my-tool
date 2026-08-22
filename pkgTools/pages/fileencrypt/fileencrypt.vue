<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">&#x2190;</text>
        <text class="nav-title">文件加密</text>
        <text class="nav-icon"> </text>
      </view>
    </view>
    <view class="content">
      <view class="card">
        <text class="card-title">输入文本</text>
        <textarea class="text-input" v-model="inputText" placeholder="输入要加密或解密的文本..." />
      </view>
      <view class="card">
        <text class="card-title">密码</text>
        <view class="password-row">
          <input class="password-input" :password="!showPassword" v-model="password" placeholder="输入密码" />
          <text class="toggle-pw" @click="showPassword = !showPassword">{{ showPassword ? '隐藏' : '显示' }}</text>
        </view>
      </view>
      <view class="action-row">
        <view class="action-btn encrypt" @click="encrypt">
          <text class="action-text">加密</text>
        </view>
        <view class="action-btn decrypt" @click="decrypt">
          <text class="action-text">解密</text>
        </view>
      </view>
      <view class="card" v-if="outputText">
        <view class="output-header">
          <text class="card-title">输出结果</text>
          <text class="copy-btn" @click="copyOutput">复制</text>
        </view>
        <text class="output-text">{{ outputText }}</text>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const inputText = ref("")
const password = ref("")
const outputText = ref("")
const showPassword = ref(false)
function goBack() { uni.navigateBack() }
function xorCipher(text, key) {
  if (!key) return text
  let result = ""
  for (let i = 0; i < text.length; i++) {
    result += String.fromCharCode(text.charCodeAt(i) ^ key.charCodeAt(i % key.length))
  }
  return result
}
function toBase64(str) {
  try {
    return uni.arrayBufferToBase64(new TextEncoder().encode(str).buffer)
  } catch (e) {
    let binary = ""
    for (let i = 0; i < str.length; i++) {
      binary += String.fromCharCode(str.charCodeAt(i) & 0xFF)
    }
    return btoa(binary)
  }
}
function fromBase64(str) {
  try {
    const buf = uni.base64ToArrayBuffer(str)
    return new TextDecoder().decode(buf)
  } catch (e) {
    return atob(str)
  }
}
function encrypt() {
  if (!inputText.value) {
    uni.showToast({ title: "请输入文本", icon: "none" })
    return
  }
  if (!password.value) {
    uni.showToast({ title: "请输入密码", icon: "none" })
    return
  }
  const encrypted = xorCipher(inputText.value, password.value)
  outputText.value = toBase64(encrypted)
  uni.showToast({ title: "加密完成", icon: "success" })
}
function decrypt() {
  if (!inputText.value) {
    uni.showToast({ title: "请输入文本", icon: "none" })
    return
  }
  if (!password.value) {
    uni.showToast({ title: "请输入密码", icon: "none" })
    return
  }
  try {
    const decoded = fromBase64(inputText.value)
    outputText.value = xorCipher(decoded, password.value)
    uni.showToast({ title: "解密完成", icon: "success" })
  } catch (e) {
    uni.showToast({ title: "解密失败，请检查输入", icon: "none" })
  }
}
function copyOutput() {
  uni.setClipboardData({
    data: outputText.value,
    success: function() {
      uni.showToast({ title: "已复制", icon: "success" })
    }
  })
}
onMounted(function() {
  if (!uni.getStorageSync("isLoggedIn")) {
    uni.reLaunch({ url: "/pages/login/login" })
    return
  }
})
</script>
<style scoped>
.page { min-height: 100vh; background: #f5f7fb }
.custom-nav { background: linear-gradient(135deg, #10b981, #059669); width: 100% }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx }
.nav-icon { width: 72rpx; text-align: center; font-size: 44rpx; color: #fff; font-weight: 700; flex-shrink: 0 }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600 }
.content { padding: 24rpx }
.card { background: #fff; border-radius: 16rpx; padding: 32rpx; margin-bottom: 24rpx; box-shadow: 0 2rpx 12rpx rgba(0,0,0,0.06) }
.card-title { font-size: 30rpx; font-weight: 600; color: #1f2937; margin-bottom: 16rpx; display: block }
.text-input { width: 100%; height: 200rpx; background: #f9fafb; border-radius: 12rpx; padding: 20rpx; font-size: 28rpx; color: #374151; box-sizing: border-box }
.password-row { display: flex; align-items: center; background: #f9fafb; border-radius: 12rpx; padding: 0 20rpx }
.password-input { flex: 1; height: 80rpx; font-size: 28rpx; color: #374151 }
.toggle-pw { font-size: 26rpx; color: #10b981; padding: 8rpx 12rpx }
.action-row { display: flex; gap: 16rpx; margin-bottom: 24rpx }
.action-btn { flex: 1; border-radius: 12rpx; padding: 24rpx; text-align: center }
.action-btn.encrypt { background: linear-gradient(135deg, #10b981, #059669) }
.action-btn.decrypt { background: linear-gradient(135deg, #06b6d4, #0891b2) }
.action-text { color: #fff; font-size: 28rpx; font-weight: 600 }
.output-header { display: flex; justify-content: space-between; align-items: center }
.copy-btn { font-size: 26rpx; color: #10b981; padding: 8rpx 16rpx; background: #d1fae5; border-radius: 8rpx }
.output-text { font-size: 26rpx; color: #374151; line-height: 44rpx; word-break: break-all; white-space: pre-wrap; margin-top: 16rpx; display: block }
</style>