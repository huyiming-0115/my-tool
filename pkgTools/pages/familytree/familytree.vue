<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u4eb2\u621a\u79f0\u547c\u8ba1\u7b97\u5668</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="input-bar"><input class="ft-input" v-model="inputText" placeholder="\u8f93\u5165\u5173\u7cfb\u6761\uff0c\u5982:\u7238\u7238\u7684\u59d0\u59d0" /><text class="ft-btn" @click="calc">\u8ba1\u7b97</text></view>
      <view class="result-card" v-if="result"><text class="result-label">\u79f0\u547c\u7ed3\u679c</text><text class="result-text">{{ result }}</text></view>
      <view class="result-card" v-if="reverseResult"><text class="result-label">\u5bf9\u65b9\u53eb\u4f60</text><text class="result-text">{{ reverseResult }}</text></view>
      <view class="quick-btns"><text class="quick-title">\u5feb\u901f\u9009\u62e9</text><view class="quick-grid"><text class="quick-item" v-for="(q, i) in quickOptions" :key="i" @click="inputText = q; calc()">{{ q }}</text></view></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const inputText = ref("")
const result = ref("")
const reverseResult = ref("")
const quickOptions = ["\u7238\u7238\u7684\u59d0\u59d0","\u5988\u5988\u7684\u54e5\u54e5","\u7238\u7238\u7684\u53d4\u53d4","\u5988\u5988\u7684\u59e8\u59e8","\u7238\u7238\u7684\u7237\u7237","\u5988\u5988\u7684\u5976\u5976","\u54e5\u54e5\u7684\u513f\u5b50","\u59b9\u59b9\u7684\u5973\u513f"]
const relationMap = {
  "\u7238\u7238\u7684\u59d0\u59d0":["\u59d0\u59d0","\u5973\u513f"],
  "\u5988\u5988\u7684\u54e5\u54e5":["\u80de\u53d4","\u513f\u5b50"],
  "\u7238\u7238\u7684\u53d4\u53d4":["\u53d4\u7236","\u4f84\u5b50"],
  "\u5988\u5988\u7684\u59e8\u59e8":["\u59e8\u6bcd","\u59e8\u5973"],
  "\u7238\u7238\u7684\u7237\u7237":["\u7956\u7236","\u5b59\u5b50"],
  "\u5988\u5988\u7684\u5976\u5976":["\u7956\u6bcd","\u5b59\u5b50"],
  "\u54e5\u54e5\u7684\u513f\u5b50":["\u4f84\u5b50","\u53d4\u7236"],
  "\u59b9\u59b9\u7684\u5973\u513f":["\u4f84\u5973","\u59e8\u6bcd"],
  "\u7238\u7238\u7684\u7236\u4eb2":["\u7236\u4eb2","\u513f\u5b50"],
  "\u5988\u5988\u7684\u6bcd\u4eb2":["\u6bcd\u4eb2","\u5973\u513f"],
  "\u54e5\u54e5\u7684\u5973\u513f":["\u4f84\u5973","\u53d4\u7236"],
  "\u59b9\u59b9\u7684\u513f\u5b50":["\u4f84\u5b50","\u59e8\u6bcd"]
}
function calc() {
  const text = inputText.value.trim()
  if (!text) { uni.showToast({ title: "\u8bf7\u8f93\u5165\u5173\u7cfb", icon: "none" }); return }
  if (relationMap[text]) {
    result.value = relationMap[text][0]
    reverseResult.value = relationMap[text][1]
  } else {
    result.value = "\u5f88\u62b1\u6b49\uff0c\u8fd9\u4e2a\u5173\u7cfb\u6211\u7b97\u4e0d\u6765"
    reverseResult.value = "\u8bf7\u5c1d\u8bd5\u5176\u4ed6\u5173\u7cfb"
  }
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #e0c3fc, #8ec5fc); }
.custom-nav { background: linear-gradient(135deg, #6c5ce7, #a29bfe); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.input-bar { display: flex; gap: 16rpx; margin-bottom: 32rpx; }
.ft-input { flex: 1; background: #fff; border-radius: 16rpx; padding: 20rpx 24rpx; font-size: 28rpx; }
.ft-btn { background: #6c5ce7; color: #fff; border-radius: 16rpx; padding: 20rpx 32rpx; font-size: 28rpx; font-weight: 600; display: flex; align-items: center; }
.result-card { background: #fff; border-radius: 24rpx; padding: 32rpx; margin-bottom: 24rpx; text-align: center; }
.result-label { font-size: 24rpx; color: #999; display: block; margin-bottom: 8rpx; }
.result-text { font-size: 40rpx; color: #333; font-weight: 700; }
.quick-btns { background: #fff; border-radius: 24rpx; padding: 24rpx; }
.quick-title { font-size: 26rpx; color: #666; margin-bottom: 16rpx; display: block; }
.quick-grid { display: flex; flex-wrap: wrap; gap: 12rpx; }
.quick-item { background: #f0f0f0; border-radius: 12rpx; padding: 12rpx 20rpx; font-size: 24rpx; color: #555; }
</style>
