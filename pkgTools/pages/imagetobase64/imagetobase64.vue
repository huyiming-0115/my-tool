<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u56fe\u7247\u8f6cBase64</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="pick-btn" @click="pickImage"><text>\u9009\u62e9\u56fe\u7247</text></view>
      <image v-if="imgPath" :src="imgPath" class="preview-img" mode="widthFix"></image>
      <view class="result-card" v-if="base64Result">
        <text class="result-label">Base64 \u7f16\u7801</text>
        <textarea class="b64-output" :value="base64Result" disabled auto-height></textarea>
        <text class="copy-btn" @click="copyText">\u590d\u5236</text>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const imgPath = ref("")
const base64Result = ref("")
function pickImage() {
  uni.chooseImage({
    count: 1,
    success: function(res) {
      imgPath.value = res.tempFilePaths[0]
      uni.getFileSystemManager().readFile({
        filePath: res.tempFilePaths[0],
        encoding: "base64",
        success: function(r) {
          base64Result.value = "data:image/jpeg;base64," + r.data
        }
      })
    }
  })
}
function copyText() {
  uni.setClipboardData({ data: base64Result.value, success: function() { uni.showToast({ title: "\u5df2\u590d\u5236", icon: "success" }) } })
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #43e97b, #38f9d7); }
.custom-nav { background: linear-gradient(135deg, #00b894, #55efc4); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.pick-btn { background: linear-gradient(135deg, #00b894, #55efc4); border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 32rpx; }
.pick-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.preview-img { width: 100%; border-radius: 16rpx; margin-bottom: 24rpx; }
.result-card { background: #fff; border-radius: 24rpx; padding: 32rpx; }
.result-label { font-size: 26rpx; color: #666; display: block; margin-bottom: 12rpx; }
.b64-output { width: 100%; background: #f8f8f8; border-radius: 12rpx; padding: 16rpx; font-size: 20rpx; color: #666; min-height: 120rpx; }
.copy-btn { display: block; background: #00b894; color: #fff; text-align: center; border-radius: 12rpx; padding: 16rpx; margin-top: 16rpx; font-size: 26rpx; }
</style>
