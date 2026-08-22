<template>
<view class="page">
  <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
    <view class="nav-row">
      <text class="nav-icon" @click="goBack">←</text>
      <text class="nav-title">图片水印</text>
      <text class="nav-icon"> </text>
    </view>
  </view>
  <view class="content">
    <view class="pick-btn" @click="pickImage" v-if="!tempFilePath">
      <text class="pick-btn-text">+ 选择图片</text>
    </view>
    <view v-if="tempFilePath">
      <view class="canvas-wrap">
        <canvas canvas-id="wmCanvas" :style="{ width: canvasW + 'px', height: canvasH + 'px' }" class="wm-canvas"></canvas>
      </view>
      <view class="info-row">
        <text class="info-label">图片尺寸：</text>
        <text class="info-value">{{ imageWidth }} x {{ imageHeight }}</text>
      </view>
      <view class="section-title">水印文字</view>
      <input class="text-input" v-model="watermarkText" placeholder="请输入水印文字" @input="redrawCanvas" maxlength="50"/>
      <view class="section-title">位置</view>
      <view class="position-grid">
        <view class="pos-cell" :class="{ active: position === 'tl' }" @click="setPosition('tl')"></view>
        <view class="pos-cell" :class="{ active: position === 'tc' }" @click="setPosition('tc')"></view>
        <view class="pos-cell" :class="{ active: position === 'tr' }" @click="setPosition('tr')"></view>
        <view class="pos-cell" :class="{ active: position === 'ml' }" @click="setPosition('ml')"></view>
        <view class="pos-cell" :class="{ active: position === 'mc' }" @click="setPosition('mc')"></view>
        <view class="pos-cell" :class="{ active: position === 'mr' }" @click="setPosition('mr')"></view>
        <view class="pos-cell" :class="{ active: position === 'bl' }" @click="setPosition('bl')"></view>
        <view class="pos-cell" :class="{ active: position === 'bc' }" @click="setPosition('bc')"></view>
        <view class="pos-cell" :class="{ active: position === 'br' }" @click="setPosition('br')"></view>
      </view>
      <view class="section-title">颜色</view>
      <view class="color-row">
        <view class="color-btn" v-for="c in colorPresets" :key="c" :style="{ background: c }" :class="{ active: color === c }" @click="setColor(c)"></view>
        <view class="color-input-wrap">
          <input class="color-input" v-model="color" @input="redrawCanvas" maxlength="7"/>
        </view>
      </view>
      <view class="section-row">
        <text class="info-label">大小：{{ fontSize }}px</text>
        <slider class="param-slider" :value="fontSize" min="12" max="80" @change="onFontSizeChange" block-size="20" block-color="#f59e0b" activeColor="#f59e0b" backgroundColor="#ddd"/>
      </view>
      <view class="section-row">
        <text class="info-label">透明度：{{ Math.round(opacity * 100) }}%</text>
        <slider class="param-slider" :value="Math.round(opacity * 100)" min="10" max="100" @change="onOpacityChange" block-size="20" block-color="#f59e0b" activeColor="#f59e0b" backgroundColor="#ddd"/>
      </view>
      <view class="section-row">
        <text class="info-label">旋转角度：{{ rotateAngle }}°</text>
        <slider class="param-slider" :value="rotateAngle" min="-90" max="90" @change="onRotateChange" block-size="20" block-color="#f59e0b" activeColor="#f59e0b" backgroundColor="#ddd"/>
      </view>
      <view class="action-row">
        <view class="action-btn preview-btn" @click="redrawCanvas">刷新预览</view>
        <view class="action-btn save-btn" @click="saveImage">保存到相册</view>
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
const watermarkText = ref("水印文字")
const position = ref("br")
const color = ref("#ffffff")
const colorPresets = ref(["#ffffff", "#000000", "#ff0000", "#00ff00", "#0000ff", "#f59e0b", "#ef4444", "#8b5cf6"])
const fontSize = ref(24)
const opacity = ref(0.6)
const rotateAngle = ref(-30)

function pickImage() {
  uni.chooseImage({
    count: 1,
    sizeType: ["original", "compressed"],
    sourceType: ["album", "camera"],
    success: function(res) {
      tempFilePath.value = res.tempFilePaths[0]
      uni.getImageInfo({
        src: res.tempFilePaths[0],
        success: function(info) {
          imageWidth.value = info.width
          imageHeight.value = info.height
          var maxW = sysInfo.windowWidth - 48
          var scale = Math.min(maxW / info.width, 400 / info.height, 1)
          canvasW.value = Math.round(info.width * scale)
          canvasH.value = Math.round(info.height * scale)
          redrawCanvas()
        }
      })
    }
  })
}

function setPosition(p) {
  position.value = p
  redrawCanvas()
}

function setColor(c) {
  color.value = c
  redrawCanvas()
}

function onFontSizeChange(e) {
  fontSize.value = e.detail.value
  redrawCanvas()
}

function onOpacityChange(e) {
  opacity.value = e.detail.value / 100
  redrawCanvas()
}

function onRotateChange(e) {
  rotateAngle.value = e.detail.value
  redrawCanvas()
}

function redrawCanvas() {
  if (!tempFilePath.value) return
  var ctx = uni.createCanvasContext("wmCanvas", this)
  ctx.clearRect(0, 0, canvasW.value, canvasH.value)
  ctx.drawImage(tempFilePath.value, 0, 0, canvasW.value, canvasH.value)
  if (watermarkText.value) {
    var scale = canvasW.value / imageWidth.value
    var fs = Math.round(fontSize.value * scale)
    var pad = Math.round(fs * 0.8)
    var tw = ctx.measureText ? 0 : 0
    var textW = watermarkText.value.length * fs * 0.6
    var textH = fs
    var x = pad, y = pad + textH
    var pos = position.value
    if (pos.indexOf("c") === 0) { x = (canvasW.value - textW) / 2 }
    else if (pos.indexOf("r") === 0) { x = canvasW.value - textW - pad }
    if (pos.indexOf("m") === 1) { y = (canvasH.value + textH) / 2 }
    else if (pos.indexOf("b") === 1) { y = canvasH.value - pad }
    ctx.save()
    ctx.globalAlpha = opacity.value
    ctx.setFillStyle(color.value)
    ctx.setFontSize(fs)
    ctx.translate(x, y)
    ctx.rotate((rotateAngle.value * Math.PI) / 180)
    ctx.fillText(watermarkText.value, 0, 0)
    ctx.restore()
  }
  ctx.draw()
}

function saveImage() {
  if (!tempFilePath.value) return
  uni.showLoading({ title: "生成中..." })
  var ctx2 = uni.createCanvasContext("wmSaveCanvas", this)
  ctx2.clearRect(0, 0, imageWidth.value, imageHeight.value)
  ctx2.drawImage(tempFilePath.value, 0, 0, imageWidth.value, imageHeight.value)
  if (watermarkText.value) {
    var fs = fontSize.value
    var pad = Math.round(fs * 0.8)
    var textW = watermarkText.value.length * fs * 0.6
    var textH = fs
    var x = pad, y = pad + textH
    var pos = position.value
    if (pos.indexOf("c") === 0) { x = (imageWidth.value - textW) / 2 }
    else if (pos.indexOf("r") === 0) { x = imageWidth.value - textW - pad }
    if (pos.indexOf("m") === 1) { y = (imageHeight.value + textH) / 2 }
    else if (pos.indexOf("b") === 1) { y = imageHeight.value - pad }
    ctx2.save()
    ctx2.globalAlpha = opacity.value
    ctx2.setFillStyle(color.value)
    ctx2.setFontSize(fs)
    ctx2.translate(x, y)
    ctx2.rotate((rotateAngle.value * Math.PI) / 180)
    ctx2.fillText(watermarkText.value, 0, 0)
    ctx2.restore()
  }
  ctx2.draw(false, function() {
    setTimeout(function() {
      uni.canvasToTempFilePath({
        canvasId: "wmSaveCanvas",
        success: function(res) {
          uni.saveImageToPhotosAlbum({
            filePath: res.tempFilePath,
            success: function() {
              uni.hideLoading()
              uni.showToast({ title: "已保存到相册", icon: "success" })
            },
            fail: function() {
              uni.hideLoading()
              uni.showToast({ title: "保存失败", icon: "none" })
            }
          })
        },
        fail: function() {
          uni.hideLoading()
          uni.showToast({ title: "生成失败", icon: "none" })
        }
      }, this)
    }, 300)
  })
}
</script>
<style scoped>
.page{min-height:100vh;background:#f5f7fb}
.custom-nav{background:linear-gradient(135deg,#f59e0b,#ef4444);width:100%}
.nav-row{height:88rpx;display:flex;align-items:center;padding:0 24rpx}
.nav-icon{width:72rpx;text-align:center;font-size:44rpx;color:#fff;font-weight:700;flex-shrink:0}
.nav-title{flex:1;text-align:center;font-size:32rpx;color:#fff;font-weight:600}
.content{padding:24rpx}
.pick-btn{background:#fff;border:2rpx dashed #f59e0b;border-radius:16rpx;padding:80rpx 0;text-align:center;margin-bottom:24rpx}
.pick-btn-text{font-size:32rpx;color:#f59e0b}
.canvas-wrap{background:#fff;border-radius:12rpx;padding:16rpx;margin-bottom:24rpx;text-align:center}
.wm-canvas{border:1rpx solid #eee;max-width:100%}
.info-row{display:flex;align-items:center;padding:12rpx 0;border-bottom:1rpx solid #eee}
.info-label{font-size:28rpx;color:#666;width:200rpx}
.info-value{font-size:28rpx;color:#333}
.highlight{color:#f59e0b;font-weight:600}
.section-title{font-size:30rpx;color:#333;font-weight:600;margin:24rpx 0 16rpx;display:block}
.text-input{background:#fff;border-radius:12rpx;padding:20rpx 24rpx;font-size:30rpx;margin-bottom:24rpx;border:2rpx solid #ddd}
.position-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12rpx;width:240rpx;margin:0 auto 24rpx}
.pos-cell{width:60rpx;height:60rpx;border:2rpx solid #ddd;border-radius:8rpx;background:#f9f9f9}
.pos-cell.active{background:#f59e0b;border-color:#f59e0b}
.color-row{display:flex;flex-wrap:wrap;gap:16rpx;align-items:center;margin-bottom:24rpx}
.color-btn{width:60rpx;height:60rpx;border-radius:50%;border:3rpx solid #ddd}
.color-btn.active{border-color:#333;transform:scale(1.15)}
.color-input-wrap{background:#fff;border-radius:12rpx;padding:12rpx 20rpx;border:2rpx solid #ddd}
.color-input{font-size:28rpx;width:140rpx}
.section-row{background:#fff;border-radius:12rpx;padding:16rpx 24rpx;margin-bottom:16rpx}
.param-slider{width:100%;margin-top:8rpx}
.action-row{display:flex;gap:16rpx;margin-top:24rpx}
.action-btn{flex:1;text-align:center;padding:24rpx 0;border-radius:12rpx;font-size:30rpx;font-weight:600}
.preview-btn{background:#f59e0b;color:#fff}
.save-btn{background:#10b981;color:#fff}
</style>
<canvas canvas-id="wmSaveCanvas" style="position:fixed;left:-9999px;width:1px;height:1px"></canvas>
