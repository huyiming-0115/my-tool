<template>
<view class="page">
  <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
    <view class="nav-row">
      <text class="nav-icon" @click="goBack">←</text>
      <text class="nav-title">图片格式转换</text>
      <text class="nav-icon"> </text>
    </view>
  </view>
  <view class="content">
    <view class="pick-btn" @click="pickImage" v-if="!tempFilePath">
      <text class="pick-btn-text">+ 选择图片</text>
    </view>
    <view v-if="tempFilePath">
      <view class="preview-box">
        <image :src="tempFilePath" mode="aspectFit" class="preview-img"></image>
      </view>
      <view class="info-row">
        <text class="info-label">原始大小：</text>
        <text class="info-value">{{ originalSize }}</text>
      </view>
      <view class="info-row">
        <text class="info-label">尺寸：</text>
        <text class="info-value">{{ imageWidth }} x {{ imageHeight }}</text>
      </view>
      <view class="section-title">选择目标格式</view>
      <view class="format-btns">
        <view class="fmt-btn" :class="{ active: targetFormat === 'jpeg' }" @click="targetFormat = 'jpeg'">JPEG</view>
        <view class="fmt-btn" :class="{ active: targetFormat === 'png' }" @click="targetFormat = 'png'">PNG</view>
        <view class="fmt-btn" :class="{ active: targetFormat === 'webp' }" @click="targetFormat = 'webp'">WEBP</view>
      </view>
      <view v-if="targetFormat === 'jpeg'" class="quality-row">
        <text class="info-label">质量：{{ quality }}%</text>
        <slider class="quality-slider" :value="quality" min="10" max="100" @change="onQualityChange" block-size="20" block-color="#06b6d4" activeColor="#06b6d4" backgroundColor="#ddd"/>
      </view>
      <view v-if="convertedSize" class="info-row">
        <text class="info-label">转换后大小：</text>
        <text class="info-value highlight">{{ convertedSize }}</text>
      </view>
      <view class="action-row">
        <view class="action-btn convert-btn" @click="convertFormat">转换</view>
        <view class="action-btn save-btn" @click="saveImage" v-if="convertedPath">保存到相册</view>
      </view>
    </view>
  </view>
  <canvas canvas-id="convertCanvas" :style="{ width: imageWidth + 'px', height: imageHeight + 'px', position: 'fixed', left: '-9999px' }"></canvas>
</view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })

const tempFilePath = ref("")
const originalSize = ref("")
const convertedSize = ref("")
const convertedPath = ref("")
const imageWidth = ref(0)
const imageHeight = ref(0)
const targetFormat = ref("jpeg")
const quality = ref(80)

function pickImage() {
  uni.chooseImage({
    count: 1,
    sizeType: ["original", "compressed"],
    sourceType: ["album", "camera"],
    success: function(res) {
      tempFilePath.value = res.tempFilePaths[0]
      convertedPath.value = ""
      convertedSize.value = ""
      uni.getImageInfo({
        src: res.tempFilePaths[0],
        success: function(info) {
          imageWidth.value = info.width
          imageHeight.value = info.height
          if (res.tempFiles && res.tempFiles[0]) {
            originalSize.value = formatSize(res.tempFiles[0].size)
          }
        }
      })
    }
  })
}

function formatSize(bytes) {
  if (bytes < 1024) return bytes + " B"
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB"
  return (bytes / (1024 * 1024)).toFixed(2) + " MB"
}

function onQualityChange(e) {
  quality.value = e.detail.value
}

function convertFormat() {
  if (!tempFilePath.value) return
  uni.showLoading({ title: "转换中..." })
  var ctx = uni.createCanvasContext("convertCanvas", this)
  ctx.drawImage(tempFilePath.value, 0, 0, imageWidth.value, imageHeight.value)
  ctx.draw(false, function() {
    setTimeout(function() {
      uni.canvasToTempFilePath({
        canvasId: "convertCanvas",
        format: targetFormat.value === "jpeg" ? "jpg" : targetFormat.value,
        quality: quality.value / 100,
        success: function(res) {
          convertedPath.value = res.tempFilePath
          uni.getFileSystemManager().readFile({
            filePath: res.tempFilePath,
            success: function(r) {
              convertedSize.value = formatSize(r.data.byteLength)
              uni.hideLoading()
              uni.showToast({ title: "转换成功", icon: "success" })
            },
            fail: function() {
              uni.hideLoading()
              uni.showToast({ title: "转换成功", icon: "success" })
            }
          })
        },
        fail: function() {
          uni.hideLoading()
          uni.showToast({ title: "转换失败", icon: "none" })
        }
      }, this)
    }, 300)
  })
}

function saveImage() {
  if (!convertedPath.value) return
  uni.saveImageToPhotosAlbum({
    filePath: convertedPath.value,
    success: function() {
      uni.showToast({ title: "已保存到相册", icon: "success" })
    },
    fail: function() {
      uni.showToast({ title: "保存失败", icon: "none" })
    }
  })
}
</script>
<style scoped>
.page{min-height:100vh;background:#f5f7fb}
.custom-nav{background:linear-gradient(135deg,#06b6d4,#0ea5e9);width:100%}
.nav-row{height:88rpx;display:flex;align-items:center;padding:0 24rpx}
.nav-icon{width:72rpx;text-align:center;font-size:44rpx;color:#fff;font-weight:700;flex-shrink:0}
.nav-title{flex:1;text-align:center;font-size:32rpx;color:#fff;font-weight:600}
.content{padding:24rpx}
.pick-btn{background:#fff;border:2rpx dashed #06b6d4;border-radius:16rpx;padding:80rpx 0;text-align:center;margin-bottom:24rpx}
.pick-btn-text{font-size:32rpx;color:#06b6d4}
.preview-box{background:#fff;border-radius:16rpx;padding:16rpx;margin-bottom:24rpx;text-align:center}
.preview-img{width:100%;max-height:400rpx;border-radius:8rpx}
.info-row{display:flex;align-items:center;padding:12rpx 0;border-bottom:1rpx solid #eee}
.info-label{font-size:28rpx;color:#666;width:200rpx}
.info-value{font-size:28rpx;color:#333}
.highlight{color:#06b6d4;font-weight:600}
.section-title{font-size:30rpx;color:#333;font-weight:600;margin:24rpx 0 16rpx;display:block}
.format-btns{display:flex;gap:16rpx;margin-bottom:24rpx}
.fmt-btn{flex:1;text-align:center;padding:20rpx 0;border-radius:12rpx;background:#fff;font-size:28rpx;color:#666;border:2rpx solid #ddd}
.fmt-btn.active{background:#06b6d4;color:#fff;border-color:#06b6d4}
.quality-row{background:#fff;border-radius:12rpx;padding:16rpx 24rpx;margin-bottom:24rpx}
.quality-slider{width:100%;margin-top:8rpx}
.action-row{display:flex;gap:16rpx;margin-top:24rpx}
.action-btn{flex:1;text-align:center;padding:24rpx 0;border-radius:12rpx;font-size:30rpx;font-weight:600}
.convert-btn{background:#06b6d4;color:#fff}
.save-btn{background:#10b981;color:#fff}
</style>
