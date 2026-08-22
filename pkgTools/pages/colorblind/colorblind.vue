<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u8272\u76f2\u6d4b\u8bd5</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <text class="test-title">\u7b2c{{ current+1 }}\u9898 / {{ tests.length }}</text>
      <view class="cb-plate" :style="{ background: tests[current].bg }" @click="showAnswer=!showAnswer">
        <text class="cb-number" :style="{ color: tests[current].fg }">{{ showAnswer ? tests[current].num : '?' }}</text>
      </view>
      <text class="cb-hint">{{ showAnswer ? '\u70b9\u51fb\u7eed\u7eed\u4e0b\u4e00\u9898' : '\u70b9\u51fb\u67e5\u770b\u7b54\u6848' }}</text>
      <view class="cb-actions">
        <text class="cb-btn" @click="prevTest" v-if="current > 0">\u4e0a\u4e00\u9898</text>
        <text class="cb-btn next" @click="nextTest" v-if="current < tests.length-1">\u4e0b\u4e00\u9898</text>
        <text class="cb-btn next" v-else @click="reset">\u91cd\u65b0\u5f00\u59cb</text>
      </view>
      <view class="cb-result" v-if="current === tests.length-1 && showAnswer">
        <text>\u6d4b\u8bd5\u5b8c\u6210\uff01\u5982\u679c\u4f60\u80fd\u770b\u6e05\u6240\u6709\u6570\u5b57\uff0c\u8bf4\u660e\u4f60\u7684\u89c6\u529b\u5f88\u597d\u3002</text>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const current = ref(0)
const showAnswer = ref(false)
const tests = [
  { num: "74", bg: "#4a90d9", fg: "#f5a623" },
  { num: "6", bg: "#7ed321", fg: "#d0021b" },
  { num: "29", bg: "#f5a623", fg: "#4a90d9" },
  { num: "8", bg: "#d0021b", fg: "#7ed321" },
  { num: "42", fg: "#4a90d9", bg: "#f5a623" }
]
function nextTest() { if (current.value < tests.length-1) { current.value++; showAnswer.value = false } }
function prevTest() { if (current.value > 0) { current.value--; showAnswer.value = false } }
function reset() { current.value = 0; showAnswer.value = false }
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #ff9a9e, #fecfef); }
.custom-nav { background: linear-gradient(135deg, #e84393, #fd79a8); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; text-align: center; }
.test-title { font-size: 30rpx; color: #fff; font-weight: 600; display: block; margin-bottom: 32rpx; }
.cb-plate { width: 400rpx; height: 400rpx; border-radius: 50%; margin: 0 auto 32rpx; display: flex; align-items: center; justify-content: center; box-shadow: 0 8rpx 32rpx rgba(0,0,0,0.15); }
.cb-number { font-size: 120rpx; font-weight: 900; }
.cb-hint { font-size: 26rpx; color: rgba(255,255,255,0.8); display: block; margin-bottom: 24rpx; }
.cb-actions { display: flex; gap: 16rpx; justify-content: center; }
.cb-btn { padding: 20rpx 40rpx; border-radius: 16rpx; background: rgba(255,255,255,0.3); color: #fff; font-size: 26rpx; }
.cb-btn.next { background: #fff; color: #e84393; }
.cb-result { margin-top: 32rpx; background: #fff; border-radius: 20rpx; padding: 24rpx; font-size: 26rpx; color: #333; }
</style>
