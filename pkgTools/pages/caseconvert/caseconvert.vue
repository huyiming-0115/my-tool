<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">大小写转换</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <textarea class="cc-input" v-model="input" placeholder="输入英文文本..." auto-height maxlength="2000" />
      <view class="cc-btns">
        <text class="cc-btn" @click="output = input.toUpperCase()">全大写</text>
        <text class="cc-btn" @click="output = input.toLowerCase()">全小写</text>
        <text class="cc-btn" @click="output = input.replace(/\w/g, function(c){return c.toUpperCase()})}">首字母大写</text>
        <text class="cc-btn" @click="output = input.split(". ").map(function(s){return s.charAt(0).toUpperCase()+s.slice(1).toLowerCase()}).join(". ")}">句字首大写</text>
      </view>
      <view class="cc-output" v-if="output"><view class="io-head"><text class="io-label">结果</text><text class="copy-btn" @click="copyResult">复制</text></view><textarea class="cc-result" :value="output" auto-height readonly /></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const input = ref("")
const output = ref("")
function copyResult() { if (output.value) { uni.setClipboardData({ data: output.value, success: function() { uni.showToast({ title: "已复制", icon: "success" }) } }) } }
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #a29bfe, #6c5ce7); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.cc-input { width: 100%; min-height: 200rpx; background: #fff; border-radius: 20rpx; padding: 24rpx; font-size: 28rpx; box-sizing: border-box; margin-bottom: 24rpx; }
.cc-btns { display: flex; flex-wrap: wrap; gap: 16rpx; margin-bottom: 24rpx; }
.cc-btn { flex: 1; min-width: 45%; text-align: center; padding: 20rpx; background: #fff; border-radius: 16rpx; font-size: 26rpx; color: #666; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.cc-btn:active { background: #6c5ce7; color: #fff; }
.cc-output { background: #fff; border-radius: 20rpx; padding: 24rpx; }
.io-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12rpx; }
.io-label { font-size: 26rpx; color: #999; }
.copy-btn { font-size: 24rpx; color: #6c5ce7; }
.cc-result { width: 100%; min-height: 150rpx; font-size: 28rpx; background: #f8f9fa; border-radius: 12rpx; padding: 16rpx; box-sizing: border-box; }
</style>