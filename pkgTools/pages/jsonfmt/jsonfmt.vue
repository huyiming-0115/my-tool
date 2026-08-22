<template>
  <view class="jf-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">JSON 格式化</text><text class="nav-icon" @click="copyResult">📋</text></view>
    </view>
    <view class="content">
      <view class="action-row"><text class="action-btn" @click="format">美化</text><text class="action-btn" @click="compress">压缩</text><text class="action-btn" @click="clear">清空</text></view>
      <textarea class="jf-input" v-model="input" placeholder="粘贴 JSON 数据..." maxlength="10000" auto-height />
      <view class="jf-output" v-if="output"><textarea class="jf-result" :value="output" auto-height readonly /></view>
      <view class="jf-error" v-if="error"><text>{{ error }}</text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const input = ref("")
const output = ref("")
const error = ref("")
function format() { try { output.value = JSON.stringify(JSON.parse(input.value), null, 2); error.value = "" } catch (e) { error.value = e.message } }
function compress() { try { output.value = JSON.stringify(JSON.parse(input.value)); error.value = "" } catch (e) { error.value = e.message } }
function clear() { input.value = ""; output.value = ""; error.value = "" }
function copyResult() { if (output.value) { uni.setClipboardData({ data: output.value, success: () => uni.showToast({ title: "已复制", icon: "success" }) }) } }
function goBack() { uni.navigateBack() }
onMounted(() => { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.jf-page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #2d3436, #636e72); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 44rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.action-row { display: flex; gap: 16rpx; margin-bottom: 24rpx; }
.action-btn { flex: 1; text-align: center; padding: 16rpx; background: #fff; border-radius: 12rpx; font-size: 26rpx; color: #666; }
.jf-input { width: 100%; min-height: 300rpx; background: #fff; border-radius: 20rpx; padding: 24rpx; font-size: 26rpx; font-family: monospace; box-sizing: border-box; margin-bottom: 24rpx; }
.jf-output { background: #2d3436; border-radius: 20rpx; padding: 24rpx; }
.jf-result { width: 100%; min-height: 200rpx; color: #00b894; font-size: 26rpx; font-family: monospace; }
.jf-error { background: #ffeaa7; border-radius: 12rpx; padding: 16rpx; margin-top: 16rpx; font-size: 24rpx; color: #d63031; }
</style>
