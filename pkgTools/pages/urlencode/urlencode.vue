<template>
  <view class="ue-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">URL 编解码</text><text class="nav-icon" @click="swap">⇄</text></view>
    </view>
    <view class="content">
      <view class="mode-tabs"><text class="mode-tab" :class="{ active: mode === 'encode' }" @click="mode = 'encode'; convert()">编码</text><text class="mode-tab" :class="{ active: mode === 'decode' }" @click="mode = 'decode'; convert()">解码</text></view>
      <view class="io-card"><text class="io-label">{{ mode === 'encode' ? '原文' : 'URL编码' }}</text><textarea class="io-input" v-model="input" :placeholder="mode === 'encode' ? '输入要编码的内容' : '输入要解码的URL'" auto-height maxlength="5000" /></view>
      <view class="io-card"><view class="io-head"><text class="io-label">{{ mode === 'encode' ? 'URL编码' : '原文' }}</text><text class="copy-btn" @click="copyResult">复制</text></view><textarea class="io-input result" :value="output" placeholder="结果..." auto-height readonly /></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const mode = ref("encode")
const input = ref("")
const output = ref("")
function convert() { try { output.value = mode.value === "encode" ? encodeURIComponent(input.value) : decodeURIComponent(input.value) } catch (e) { output.value = "错误: " + e.message } }
function swap() { mode.value = mode.value === "encode" ? "decode" : "encode"; const t = input.value; input.value = output.value; output.value = t }
function copyResult() { if (output.value) { uni.setClipboardData({ data: output.value, success: () => uni.showToast({ title: "已复制", icon: "success" }) }) } }
function goBack() { uni.navigateBack() }
onMounted(() => { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.ue-page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #00b894, #00cec9); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.mode-tabs { display: flex; gap: 16rpx; margin-bottom: 24rpx; }
.mode-tab { flex: 1; text-align: center; padding: 20rpx; background: #fff; border-radius: 16rpx; font-size: 28rpx; color: #666; }
.mode-tab.active { background: linear-gradient(135deg, #00b894, #00cec9); color: #fff; }
.io-card { background: #fff; border-radius: 24rpx; padding: 24rpx; margin-bottom: 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.io-head { display: flex; justify-content: space-between; align-items: center; }
.io-label { font-size: 26rpx; color: #999; display: block; margin-bottom: 12rpx; }
.copy-btn { font-size: 24rpx; color: #00b894; padding: 4rpx 12rpx; }
.io-input { width: 100%; min-height: 200rpx; font-size: 28rpx; line-height: 1.6; }
.io-input.result { background: #f8f9fa; border-radius: 12rpx; padding: 16rpx; }
</style>
