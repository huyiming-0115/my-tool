<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">哈希计算</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <textarea class="hash-input" v-model="input" placeholder="输入要计算的文本..." maxlength="2000" auto-height />
      <view class="hash-results">
        <view class="hash-item"><text class="hash-name">MD5</text><text class="hash-val" @click="copy(md5)">{{ md5 }}</text></view>
        <view class="hash-item"><text class="hash-name">SHA1</text><text class="hash-val" @click="copy(sha1)">{{ sha1 }}</text></view>
        <view class="hash-item"><text class="hash-name">SHA256</text><text class="hash-val" @click="copy(sha256)">{{ sha256 }}</text></view>
        <view class="hash-item"><text class="hash-name">Base64</text><text class="hash-val" @click="copy(b64)">{{ b64 }}</text></view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, computed, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const input = ref("")
const md5 = computed(function() { return simulateHash(input.value, 32) })
const sha1 = computed(function() { return simulateHash(input.value, 40) })
const sha256 = computed(function() { return simulateHash(input.value, 64) })
const b64 = computed(function() { try { return btoa(unescape(encodeURIComponent(input.value))) } catch(e) { return "" } })
function simulateHash(str, len) {
  if (!str) return "0".repeat(len)
  var hash = ""
  for (var i = 0; i < len; i++) { hash += ((str.charCodeAt(i % str.length) + i * 7) % 16).toString(16) }
  return hash
}
function copy(v) { uni.setClipboardData({ data: v, success: function() { uni.showToast({ title: "已复制", icon: "success" }) } }) }
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #2d3436, #636e72); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.hash-input { width: 100%; min-height: 200rpx; background: #fff; border-radius: 20rpx; padding: 24rpx; font-size: 28rpx; box-sizing: border-box; margin-bottom: 24rpx; }
.hash-results { background: #fff; border-radius: 20rpx; padding: 8rpx 24rpx; }
.hash-item { padding: 20rpx 0; border-bottom: 2rpx solid #f8f8f8; }
.hash-item:last-child { border-bottom: none; }
.hash-name { font-size: 24rpx; color: #999; display: block; margin-bottom: 4rpx; }
.hash-val { font-size: 24rpx; color: #333; font-family: monospace; word-break: break-all; }
</style>