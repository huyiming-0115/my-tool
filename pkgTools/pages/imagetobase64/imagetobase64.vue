
<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">图片转Base64</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="ib-btn" @click="chooseImage"><text>选择图片</text></view>
      <view class="ib-preview" v-if="imagePath">
        <image class="ib-image" :src="imagePath" mode="aspectFit"></image>
      </view>
      <view class="ib-result" v-if="base64Result">
        <view class="ib-result-header">
          <text class="ib-result-label">Base64编码</text>
          <view class="ib-copy" @click="copyResult"><text>复制</text></view>
        </view>
        <scroll-view class="ib-result-box" scroll-y><text>{{base64Result}}</text></scroll-view>
        <text class="ib-length">长度: {{base64Result.length}} 字符</text>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const imagePath = ref("")
const base64Result = ref("")
function chooseImage() {
  uni.chooseImage({
    count: 1,
    success: function(res) {
      imagePath.value = res.tempFilePaths[0]
      var fs = uni.getFileSystemManager()
      try {
        var data = fs.readFileSync(res.tempFilePaths[0], "base64")
        var ext = res.tempFilePaths[0].split(".").pop().toLowerCase()
        var mime = ext === "png" ? "png" : ext === "gif" ? "gif" : "jpeg"
        base64Result.value = "data:image/" + mime + ";base64," + data
      } catch(e) {
        base64Result.value = "转换失败: " + e.message
      }
    }
  })
}
function copyResult() {
  uni.setClipboardData({ data: base64Result.value })
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #ee9ca7, #ffdde1); }
.custom-nav { background: linear-gradient(135deg, #ee9ca7, #ffdde1); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 32rpx; }
.ib-btn { background: #fff; border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 24rpx; }
.ib-btn text { color: #ee9ca7; font-size: 32rpx; font-weight: 700; }
.ib-preview { background: rgba(255,255,255,0.3); border-radius: 20rpx; padding: 20rpx; margin-bottom: 24rpx; text-align: center; }
.ib-image { max-width: 100%; max-height: 400rpx; border-radius: 12rpx; }
.ib-result { background: rgba(255,255,255,0.3); border-radius: 20rpx; padding: 24rpx; }
.ib-result-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12rpx; }
.ib-result-label { color: #fff; font-size: 28rpx; font-weight: 600; }
.ib-copy { background: rgba(255,255,255,0.3); padding: 8rpx 20rpx; border-radius: 8rpx; }
.ib-copy text { color: #fff; font-size: 24rpx; }
.ib-result-box { background: rgba(0,0,0,0.2); border-radius: 12rpx; padding: 16rpx; max-height: 300rpx; }
.ib-result-box text { color: rgba(255,255,255,0.8); font-size: 20rpx; word-break: break-all; line-height: 1.5; }
.ib-length { color: rgba(255,255,255,0.7); font-size: 24rpx; display: block; margin-top: 12rpx; }
</style>
