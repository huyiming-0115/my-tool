<template>
<view class="page">
  <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
    <view class="nav-row">
      <text class="nav-icon" @click="goBack">←</text>
      <text class="nav-title">图片裁剪</text>
      <text class="nav-icon"> </text>
    </view>
  </view>
  <view class="content">
    <view class="pick-btn" @click="pickImage" v-if="!tempFilePath">
      <text class="pick-btn-text">+ 选择图片</text>
    </view>
    <view v-if="tempFilePath">
      <view class="canvas-wrap">
        <canvas canvas-id="cropCanvas" :style="{ width: canvasW + 'px', height: canvasH + 'px' }" class="crop-canvas" @touchstart="onTouchStart" @touchmove="onTouchMove" @touchend="onTouchEnd"></canvas>
        <view class="crop-overlay" v-if="showOverlay">
          <view class="crop-box" :style="{ left: cropX + 'px', top: cropY + 'px', width: cropW + 'px', height: cropH + 'px' }">
            <view class="crop-handle tl" @touchstart.stop="startResize('tl',$event)"></view>
            <view class="crop-handle tr" @touchstart.stop="startResize('tr',$event)"></view>
            <view class="crop-handle bl" @touchstart.stop="startResize('bl',$event)"></view>
            <view class="crop-handle br" @touchstart.stop="startResize('br',$event)"></view>
            <view class="crop-grid">
              <view class="grid-line v1"></view><view class="grid-line v2"></view>
              <view class="grid-line h1"></view><view class="grid-line h2"></view>
            </view>
          </view>
        </view>
      </view>
      <view class="info-row">
        <text class="info-label">图片尺寸：</text>
        <text class="info-value">{{ imageWidth }} x {{ imageHeight }}</text>
      </view>
      <view class="section-title">裁剪比例</view>
      <view class="ratio-btns">
        <view class="ratio-btn" :class="{ active: ratio === 'free' }" @click="setRatio('free')">自由</view>
        <view class="ratio-btn" :class="{ active: ratio === '1:1' }" @click="setRatio('1:1')">1:1</view>
        <view class="ratio-btn" :class="{ active: ratio === '4:3' }" @click="setRatio('4:3')">4:3</view>
        <view class="ratio-btn" :class="{ active: ratio === '16:9' }" @click="setRatio('16:9')">16:9</view>
      </view>
      <view class="section-title">旋转</view>
      <view class="rotate-btns">
        <view class="rotate-btn" @click="rotate(-90)">↺ 左转90°</view>
        <view class="rotate-btn" @click="rotate(90)">↻ 右转90°</view>
      </view>
      <view v-if="croppedPath" class="result-section">
        <view class="section-title">裁剪结果</view>
        <view class="preview-box">
          <image :src="croppedPath" mode="aspectFit" class="preview-img"></image>
        </view>
        <view class="info-row">
          <text class="info-label">结果尺寸：</text>
          <text class="info-value highlight">{{ cropResultW }} x {{ cropResultH }}</text>
        </view>
      </view>
      <view class="action-row">
        <view class="action-btn crop-btn" @click="cropImage">确认裁剪</view>
        <view class="action-btn save-btn" @click="saveImage" v-if="croppedPath">保存到相册</view>
      </view>
    </view>
  </view>
</view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const sysInfo = uni.getSystemInfoSync()
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })

const tempFilePath = ref("")
const imageWidth = ref(0)
const imageHeight = ref(0)
const canvasW = ref(300)
const canvasH = ref(300)
const cropX = ref(20)
const cropY = ref(20)
const cropW = ref(100)
const cropH = ref(100)
const ratio = ref("free")
const rotation = ref(0)
const showOverlay = ref(false)
const croppedPath = ref("")
const cropResultW = ref(0)
const cropResultH = ref(0)
const dragging = ref(false)
const resizing = ref(false)
const resizeDir = ref("")
const touchStartX = ref(0)
const touchStartY = ref(0)
const startCropX = ref(0)
const startCropY = ref(0)
const startCropW = ref(0)
const startCropH = ref(0)

function pickImage() {
  uni.chooseImage({
    count: 1,
    sizeType: ["original", "compressed"],
    sourceType: ["album", "camera"],
    success: function(res) {
      tempFilePath.value = res.tempFilePaths[0]
      croppedPath.value = ""
      uni.getImageInfo({
        src: res.tempFilePaths[0],
        success: function(info) {
          imageWidth.value = info.width
          imageHeight.value = info.height
          rotation.value = 0
          var maxW = sysInfo.windowWidth - 48
          var scale = Math.min(maxW / info.width, 400 / info.height, 1)
          canvasW.value = Math.round(info.width * scale)
          canvasH.value = Math.round(info.height * scale)
          cropX.value = 10
          cropY.value = 10
          cropW.value = Math.min(canvasW.value - 20, canvasH.value - 20)
          cropH.value = cropW.value
          ratio.value = "1:1"
          showOverlay.value = true
          drawCanvas()
        }
      })
    }
  })
}

function drawCanvas() {
  var ctx = uni.createCanvasContext("cropCanvas", this)
  ctx.clearRect(0, 0, canvasW.value, canvasH.value)
  ctx.save()
  ctx.translate(canvasW.value / 2, canvasH.value / 2)
  ctx.rotate((rotation.value * Math.PI) / 180)
  ctx.drawImage(tempFilePath.value, -canvasW.value / 2, -canvasH.value / 2, canvasW.value, canvasH.value)
  ctx.restore()
  ctx.draw()
}

function setRatio(r) {
  ratio.value = r
  if (r === "free") return
  var parts = r.split(":")
  var rw = parseInt(parts[0])
  var rh = parseInt(parts[1])
  var newH = (cropW.value * rh) / rw
  var newW = (cropH.value * rw) / rh
  if (cropY.value + newH > canvasH.value - 5) {
    newH = canvasH.value - cropY.value - 5
    newW = (newH * rw) / rh
  }
  if (cropX.value + newW > canvasW.value - 5) {
    newW = canvasW.value - cropX.value - 5
    newH = (newW * rh) / rw
  }
  cropW.value = Math.round(Math.max(40, newW))
  cropH.value = Math.round(Math.max(40, newH))
}

function rotate(deg) {
  rotation.value = (rotation.value + deg) % 360
  drawCanvas()
}

function onTouchStart(e) {
  var touch = e.touches[0]
  touchStartX.value = touch.x
  touchStartY.value = touch.y
  startCropX.value = cropX.value
  startCropY.value = cropY.value
  dragging.value = true
}

function onTouchMove(e) {
  if (!dragging.value) return
  var touch = e.touches[0]
  var dx = touch.x - touchStartX.value
  var dy = touch.y - touchStartY.value
  var newX = Math.max(0, Math.min(canvasW.value - cropW.value, startCropX.value + dx))
  var newY = Math.max(0, Math.min(canvasH.value - cropH.value, startCropY.value + dy))
  cropX.value = newX
  cropY.value = newY
}

function onTouchEnd() {
  dragging.value = false
}

function startResize(dir, e) {
  resizing.value = true
  resizeDir.value = dir
  var touch = e.touches[0]
  touchStartX.value = touch.x
  touchStartY.value = touch.y
  startCropX.value = cropX.value
  startCropY.value = cropY.value
  startCropW.value = cropW.value
  startCropH.value = cropH.value
}

function cropImage() {
  if (!tempFilePath.value) return
  uni.showLoading({ title: "裁剪中..." })
  var scaleX = imageWidth.value / canvasW.value
  var scaleY = imageHeight.value / canvasH.value
  var sx = Math.round(cropX.value * scaleX)
  var sy = Math.round(cropY.value * scaleY)
  var sw = Math.round(cropW.value * scaleX)
  var sh = Math.round(cropH.value * scaleY)
  var tw = sw
  var th = sh
  var ctx2 = uni.createCanvasContext("cropResultCanvas", this)
  ctx2.drawImage(tempFilePath.value, sx, sy, sw, sh, 0, 0, tw, th)
  ctx2.draw(false, function() {
    setTimeout(function() {
      uni.canvasToTempFilePath({
        canvasId: "cropResultCanvas",
        success: function(res) {
          croppedPath.value = res.tempFilePath
          cropResultW.value = sw
          cropResultH.value = sh
          uni.hideLoading()
          uni.showToast({ title: "裁剪成功", icon: "success" })
        },
        fail: function() {
          uni.hideLoading()
          uni.showToast({ title: "裁剪失败", icon: "none" })
        }
      }, this)
    }, 300)
  })
}

function saveImage() {
  if (!croppedPath.value) return
  uni.saveImageToPhotosAlbum({
    filePath: croppedPath.value,
    success: function() { uni.showToast({ title: "已保存到相册", icon: "success" }) },
    fail: function() { uni.showToast({ title: "保存失败", icon: "none" }) }
  })
}
</script>
<style scoped>
.page{min-height:100vh;background:#f5f7fb}
.custom-nav{background:linear-gradient(135deg,#8b5cf6,#a855f7);width:100%}
.nav-row{height:88rpx;display:flex;align-items:center;padding:0 24rpx}
.nav-icon{width:72rpx;text-align:center;font-size:44rpx;color:#fff;font-weight:700;flex-shrink:0}
.nav-title{flex:1;text-align:center;font-size:32rpx;color:#fff;font-weight:600}
.content{padding:24rpx}
.pick-btn{background:#fff;border:2rpx dashed #8b5cf6;border-radius:16rpx;padding:80rpx 0;text-align:center;margin-bottom:24rpx}
.pick-btn-text{font-size:32rpx;color:#8b5cf6}
.canvas-wrap{position:relative;background:#000;border-radius:12rpx;overflow:hidden;margin-bottom:24rpx;min-height:300px}
.crop-canvas{display:block;width:100%}
.crop-overlay{position:absolute;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.4)}
.crop-box{position:absolute;border:2rpx solid #fff;box-shadow:0 0 0 10000rpx rgba(0,0,0,0.5)}
.crop-handle{position:absolute;width:40rpx;height:40rpx;background:#fff;border-radius:50%}
.crop-handle.tl{top:-20rpx;left:-20rpx}.crop-handle.tr{top:-20rpx;right:-20rpx}
.crop-handle.bl{bottom:-20rpx;left:-20rpx}.crop-handle.br{bottom:-20rpx;right:-20rpx}
.crop-grid{position:absolute;top:0;left:0;right:0;bottom:0;pointer-events:none}
.grid-line{position:absolute;background:rgba(255,255,255,0.5)}
.v1{left:33.3%;top:0;bottom:0;width:1px}.v2{left:66.6%;top:0;bottom:0;width:1px}
.h1{top:33.3%;left:0;right:0;height:1px}.h2{top:66.6%;left:0;right:0;height:1px}
.info-row{display:flex;align-items:center;padding:12rpx 0;border-bottom:1rpx solid #eee}
.info-label{font-size:28rpx;color:#666;width:200rpx}
.info-value{font-size:28rpx;color:#333}
.highlight{color:#8b5cf6;font-weight:600}
.section-title{font-size:30rpx;color:#333;font-weight:600;margin:24rpx 0 16rpx;display:block}
.ratio-btns{display:flex;gap:16rpx;margin-bottom:24rpx}
.ratio-btn{flex:1;text-align:center;padding:20rpx 0;border-radius:12rpx;background:#fff;font-size:28rpx;color:#666;border:2rpx solid #ddd}
.ratio-btn.active{background:#8b5cf6;color:#fff;border-color:#8b5cf6}
.rotate-btns{display:flex;gap:16rpx;margin-bottom:24rpx}
.rotate-btn{flex:1;text-align:center;padding:20rpx 0;border-radius:12rpx;background:#fff;font-size:28rpx;color:#8b5cf6;border:2rpx solid #8b5cf6}
.result-section{margin-top:24rpx}
.preview-box{background:#fff;border-radius:16rpx;padding:16rpx;margin-bottom:16rpx;text-align:center}
.preview-img{width:100%;max-height:400rpx;border-radius:8rpx}
.action-row{display:flex;gap:16rpx;margin-top:24rpx}
.action-btn{flex:1;text-align:center;padding:24rpx 0;border-radius:12rpx;font-size:30rpx;font-weight:600}
.crop-btn{background:#8b5cf6;color:#fff}
.save-btn{background:#10b981;color:#fff}
</style>
<canvas canvas-id="cropResultCanvas" style="position:fixed;left:-9999px;width:1px;height:1px"></canvas>
