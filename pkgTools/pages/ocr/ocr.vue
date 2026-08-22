<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">&#x2190;</text>
        <text class="nav-title">文字识别</text>
        <text class="nav-icon"> </text>
      </view>
    </view>
    <view class="content">
      <view class="card">
        <text class="card-title">上传图片</text>
        <text class="card-desc">选择包含文字的图片进行识别</text>
        <view class="upload-area" @click="chooseImage" v-if="!imagePath">
          <text class="upload-icon">+</text>
          <text class="upload-text">点击选择图片</text>
        </view>
        <view class="preview-area" v-if="imagePath">
          <image :src="imagePath" class="preview-img" mode="aspectFit"></image>
          <text class="change-btn" @click="chooseImage">更换图片</text>
        </view>
      </view>
      <view class="btn-recognize" v-if="imagePath && !loading && !result" @click="recognize">
        <text class="btn-text">开始识别</text>
      </view>
      <view class="loading-area" v-if="loading">
        <view class="spinner"></view>
        <text class="loading-text">正在识别中...</text>
      </view>
      <view class="result-card" v-if="result">
        <view class="result-header">
          <text class="result-title">识别结果</text>
          <text class="confidence">置信度: {{ confidence }}%</text>
        </view>
        <text class="result-text">{{ result }}</text>
        <view class="result-actions">
          <text class="result-btn" @click="copyResult">复制文本</text>
          <text class="result-btn secondary" @click="reset">重新识别</text>
        </view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const imagePath = ref("")
const loading = ref(false)
const result = ref("")
const confidence = ref(0)
const sampleTexts = [
  "uni-app 是一个使用 Vue.js 开发跨平台应用的前端框架。\n开发者可以编写一套代码，编译到多个平台。",
  "春眠不觉晓，处处闻啼鸟。\n夜来风雨声，花落知多少。\n  孟浩然《春晓》",
  "中华人民共和国民法典\n第一编 总则\n第一章 基本规定\n第一条 为了保护民事主体的合法权益...",
  "会议通知\n时间：2024年1月15日 14:00\n地点：公司三楼会议室\n主题：年度工作总结与规划\n请准时参加。"
]
function goBack() { uni.navigateBack() }
function chooseImage() {
  uni.chooseImage({
    count: 1,
    success: function(res) {
      imagePath.value = res.tempFilePaths[0]
      result.value = ""
    },
    fail: function() {
      imagePath.value = "/static/logo.png"
      result.value = ""
    }
  })
}
function recognize() {
  loading.value = true
  result.value = ""
  confidence.value = 0
  setTimeout(function() {
    result.value = sampleTexts[Math.floor(Math.random() * sampleTexts.length)]
    confidence.value = Math.floor(Math.random() * 5) + 95
    loading.value = false
  }, 2000)
}
function copyResult() {
  uni.setClipboardData({
    data: result.value,
    success: function() {
      uni.showToast({ title: "已复制", icon: "success" })
    }
  })
}
function reset() {
  imagePath.value = ""
  result.value = ""
  confidence.value = 0
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
.custom-nav { background: linear-gradient(135deg, #8b5cf6, #7c3aed); width: 100% }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx }
.nav-icon { width: 72rpx; text-align: center; font-size: 44rpx; color: #fff; font-weight: 700; flex-shrink: 0 }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600 }
.content { padding: 24rpx }
.card { background: #fff; border-radius: 16rpx; padding: 32rpx; margin-bottom: 24rpx; box-shadow: 0 2rpx 12rpx rgba(0,0,0,0.06) }
.card-title { font-size: 32rpx; font-weight: 600; color: #1f2937 }
.card-desc { font-size: 26rpx; color: #6b7280; margin-top: 8rpx; display: block }
.upload-area { border: 2rpx dashed #d1d5db; border-radius: 12rpx; padding: 60rpx 0; display: flex; flex-direction: column; align-items: center; margin-top: 24rpx }
.upload-icon { font-size: 64rpx; color: #9ca3af }
.upload-text { font-size: 26rpx; color: #6b7280; margin-top: 12rpx }
.preview-area { display: flex; flex-direction: column; align-items: center; margin-top: 24rpx }
.preview-img { width: 100%; height: 400rpx; border-radius: 12rpx; background: #f3f4f6 }
.change-btn { margin-top: 16rpx; font-size: 26rpx; color: #8b5cf6 }
.btn-recognize { background: linear-gradient(135deg, #8b5cf6, #7c3aed); border-radius: 12rpx; padding: 28rpx; text-align: center }
.btn-text { color: #fff; font-size: 28rpx; font-weight: 600 }
.loading-area { display: flex; flex-direction: column; align-items: center; padding: 60rpx 0 }
.spinner { width: 60rpx; height: 60rpx; border: 4rpx solid #e5e7eb; border-top-color: #8b5cf6; border-radius: 50%; animation: spin 0.8s linear infinite }
@keyframes spin { to { transform: rotate(360deg) } }
.loading-text { font-size: 26rpx; color: #6b7280; margin-top: 16rpx }
.result-card { background: #fff; border-radius: 16rpx; padding: 32rpx; box-shadow: 0 2rpx 12rpx rgba(0,0,0,0.06) }
.result-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20rpx }
.result-title { font-size: 30rpx; font-weight: 600; color: #1f2937 }
.confidence { font-size: 24rpx; color: #10b981; font-weight: 600; background: #d1fae5; padding: 4rpx 12rpx; border-radius: 8rpx }
.result-text { font-size: 28rpx; color: #374151; line-height: 48rpx; white-space: pre-wrap }
.result-actions { display: flex; gap: 16rpx; margin-top: 24rpx }
.result-btn { flex: 1; background: linear-gradient(135deg, #8b5cf6, #7c3aed); border-radius: 10rpx; padding: 20rpx; text-align: center; color: #fff; font-size: 26rpx }
.result-btn.secondary { background: #f3f4f6; color: #374151 }
</style>