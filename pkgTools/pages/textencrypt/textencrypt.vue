<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">&#x2190;</text>
        <text class="nav-title">文本加密</text>
        <text class="nav-icon"> </text>
      </view>
    </view>
    <view class="content">
      <view class="card">
        <text class="card-title">输入文本</text>
        <textarea class="text-input" v-model="inputText" placeholder="输入要编码或解码的文本..." />
      </view>
      <view class="card">
        <text class="card-title">选择加密方式</text>
        <view class="cipher-grid">
          <view class="cipher-item" v-for="c in ciphers" :key="c.id" :class="{ active: selectedCipher === c.id }" @click="selectedCipher = c.id">
            <text class="cipher-name">{{ c.name }}</text>
          </view>
        </view>
      </view>
      <view class="mode-row">
        <view class="mode-btn" :class="{ active: mode === 'encode' }" @click="mode = 'encode'">
          <text class="mode-text">编码</text>
        </view>
        <view class="mode-btn" :class="{ active: mode === 'decode' }" @click="mode = 'decode'">
          <text class="mode-text">解码</text>
        </view>
      </view>
      <view class="process-btn" @click="process">
        <text class="btn-text">{{ mode === 'encode' ? '编码' : '解码' }}</text>
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
const outputText = ref("")
const selectedCipher = ref("caesar")
const mode = ref("encode")
const ciphers = [
  { id: "caesar", name: "凯撒密码" },
  { id: "reverse", name: "反转" },
  { id: "base64", name: "Base64" },
  { id: "binary", name: "二进制" }
]
function goBack() { uni.navigateBack() }
function caesarEncode(text) {
  return text.split("").map(function(c) {
    if (c >= "a" && c <= "z") return String.fromCharCode((c.charCodeAt(0) - 97 + 3) % 26 + 97)
    if (c >= "A" && c <= "Z") return String.fromCharCode((c.charCodeAt(0) - 65 + 3) % 26 + 65)
    return c
  }).join("")
}
function caesarDecode(text) {
  return text.split("").map(function(c) {
    if (c >= "a" && c <= "z") return String.fromCharCode((c.charCodeAt(0) - 97 + 23) % 26 + 97)
    if (c >= "A" && c <= "Z") return String.fromCharCode((c.charCodeAt(0) - 65 + 23) % 26 + 65)
    return c
  }).join("")
}
function reverseText(text) {
  return text.split("").reverse().join("")
}
function base64Encode(text) {
  try { return uni.arrayBufferToBase64(new TextEncoder().encode(text).buffer) } catch (e) { return btoa(unescape(encodeURIComponent(text))) }
}
function base64Decode(text) {
  try { return new TextDecoder().decode(uni.base64ToArrayBuffer(text)) } catch (e) { return decodeURIComponent(escape(atob(text))) }
}
function textToBinary(text) {
  return text.split("").map(function(c) {
    return c.charCodeAt(0).toString(2).padStart(8, "0")
  }).join(" ")
}
function binaryToText(binary) {
  return binary.split(" ").map(function(b) {
    return String.fromCharCode(parseInt(b, 2))
  }).join("")
}
function process() {
  if (!inputText.value) {
    uni.showToast({ title: "请输入文本", icon: "none" })
    return
  }
  let result = ""
  const m = mode.value
  switch (selectedCipher.value) {
    case "caesar":
      result = m === "encode" ? caesarEncode(inputText.value) : caesarDecode(inputText.value)
      break
    case "reverse":
      result = reverseText(inputText.value)
      break
    case "base64":
      try {
        result = m === "encode" ? base64Encode(inputText.value) : base64Decode(inputText.value)
      } catch (e) {
        uni.showToast({ title: "解码失败", icon: "none" })
        return
      }
      break
    case "binary":
      try {
        result = m === "encode" ? textToBinary(inputText.value) : binaryToText(inputText.value)
      } catch (e) {
        uni.showToast({ title: "转换失败", icon: "none" })
        return
      }
      break
  }
  outputText.value = result
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
.custom-nav { background: linear-gradient(135deg, #f59e0b, #d97706); width: 100% }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx }
.nav-icon { width: 72rpx; text-align: center; font-size: 44rpx; color: #fff; font-weight: 700; flex-shrink: 0 }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600 }
.content { padding: 24rpx }
.card { background: #fff; border-radius: 16rpx; padding: 32rpx; margin-bottom: 24rpx; box-shadow: 0 2rpx 12rpx rgba(0,0,0,0.06) }
.card-title { font-size: 30rpx; font-weight: 600; color: #1f2937; margin-bottom: 16rpx; display: block }
.text-input { width: 100%; height: 180rpx; background: #f9fafb; border-radius: 12rpx; padding: 20rpx; font-size: 28rpx; color: #374151; box-sizing: border-box }
.cipher-grid { display: flex; flex-wrap: wrap; gap: 16rpx }
.cipher-item { padding: 16rpx 28rpx; border-radius: 10rpx; background: #f3f4f6; border: 2rpx solid transparent }
.cipher-item.active { background: #fef3c7; border-color: #f59e0b }
.cipher-name { font-size: 26rpx; color: #374151 }
.cipher-item.active .cipher-name { color: #d97706; font-weight: 600 }
.mode-row { display: flex; background: #fff; border-radius: 16rpx; padding: 8rpx; margin-bottom: 24rpx; box-shadow: 0 2rpx 12rpx rgba(0,0,0,0.06) }
.mode-btn { flex: 1; padding: 20rpx; text-align: center; border-radius: 12rpx }
.mode-btn.active { background: linear-gradient(135deg, #f59e0b, #d97706) }
.mode-text { font-size: 28rpx; color: #6b7280 }
.mode-btn.active .mode-text { color: #fff; font-weight: 600 }
.process-btn { background: linear-gradient(135deg, #f59e0b, #d97706); border-radius: 12rpx; padding: 28rpx; text-align: center; margin-bottom: 24rpx }
.btn-text { color: #fff; font-size: 28rpx; font-weight: 600 }
.output-header { display: flex; justify-content: space-between; align-items: center }
.copy-btn { font-size: 26rpx; color: #d97706; padding: 8rpx 16rpx; background: #fef3c7; border-radius: 8rpx }
.output-text { font-size: 26rpx; color: #374151; line-height: 44rpx; word-break: break-all; white-space: pre-wrap; margin-top: 16rpx; display: block }
</style>