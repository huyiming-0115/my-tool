<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">←</text>
        <text class="nav-title">图片风格转换</text>
        <text class="nav-icon"> </text>
      </view>
    </view>
    <view class="content">
      <view class="pick-area" @click="pickImage" v-if="!imageSrc">
        <text class="pick-icon">+</text>
        <text class="pick-text">点击选择图片</text>
      </view>
      <view v-if="imageSrc">
        <view class="preview-section">
          <text class="section-label">原图</text>
          <image class="preview-img" :src="imageSrc" mode="aspectFit"></image>
        </view>
        <view class="filter-list">
          <text class="section-label">选择滤镜</text>
          <scroll-view scroll-x class="filter-scroll">
            <view v-for="(f, i) in filters" :key="i" class="filter-item" :class="{ active: activeFilter === f.name }" @click="applyFilter(f.name)">
              <view class="filter-thumb" :style="{ filter: f.css }"></view>
              <text class="filter-name">{{ f.label }}</text>
            </view>
          </scroll-view>
        </view>
        <view class="preview-section">
          <text class="section-label">效果预览</text>
          <image class="preview-img" :src="imageSrc" mode="aspectFit" :style="{ filter: currentFilterCss }"></image>
        </view>
        <view class="slider-section" v-if="showSlider">
          <text class="slider-label">{{ activeFilterLabel }}: {{ filterIntensity }}%</text>
          <slider :value="filterIntensity" :min="0" :max="200" block-size="20" block-color="#a855f7" @change="onSliderChange" />
        </view>
        <view class="action-row">
          <view class="action-btn primary" @click="saveImage">
            <text class="action-text">保存图片</text>
          </view>
          <view class="action-btn secondary" @click="resetImage">
            <text class="action-text">重新选择</text>
          </view>
        </view>
      </view>
    </view>
    <canvas canvas-id="filterCanvas" :style="{ width: canvasWidth + 'px', height: canvasHeight + 'px', position: 'fixed', top: '-9999px', left: '-9999px' }"></canvas>
  </view>
</template>
<script setup>
import { ref, onMounted, computed } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
function goBack() { uni.navigateBack() }
onMounted(function () {
  if (!uni.getStorageSync("isLoggedIn")) {
    uni.reLaunch({ url: "/pages/login/login" })
    return
  }
})
const imageSrc = ref("")
const activeFilter = ref("none")
const filterIntensity = ref(100)
const canvasWidth = ref(300)
const canvasHeight = ref(300)
const filters = [
  { name: "none", label: "原图", css: "none" },
  { name: "grayscale", label: "灰度", css: "grayscale(1)" },
  { name: "sepia", label: "复古", css: "sepia(1)" },
  { name: "invert", label: "反相", css: "invert(1)" },
  { name: "blur", label: "模糊", css: "blur(5px)" },
  { name: "brightness", label: "亮度", css: "brightness(1.5)" },
  { name: "contrast", label: "对比", css: "contrast(1.5)" },
  { name: "saturate", label: "饱和", css: "saturate(2)" },
  { name: "hue-rotate", label: "色相", css: "hue-rotate(90deg)" },
  { name: "vintage", label: "老照片", css: "sepia(0.5) contrast(1.2) brightness(0.9) saturate(0.8)" },
  { name: "pixelate", label: "像素", css: "contrast(1.5)" },
]
const filterMap = {
  none: function() { return "none" },
  grayscale: function(v) { return "grayscale(" + (v / 100) + ")" },
  sepia: function(v) { return "sepia(" + (v / 100) + ")" },
  invert: function(v) { return "invert(" + (v / 100) + ")" },
  blur: function(v) { return "blur(" + ((v / 100) * 10) + "px)" },
  brightness: function(v) { return "brightness(" + (0.5 + (v / 100)) + ")" },
  contrast: function(v) { return "contrast(" + (0.5 + (v / 100)) + ")" },
  saturate: function(v) { return "saturate(" + (v / 50) + ")" },
  "hue-rotate": function(v) { return "hue-rotate(" + ((v / 100) * 360) + "deg)" },
  vintage: function(v) { return "sepia(" + (0.5 * (v / 100)) + ") contrast(" + (1 + 0.2 * (v / 100)) + ") brightness(" + (0.9 + 0.1 * (v / 100)) + ") saturate(" + (0.8 + 0.2 * (v / 100)) + ")" },
  pixelate: function(v) { return "contrast(" + (1 + 0.5 * (v / 100)) + ")" },
}
const showSlider = computed(function() { return activeFilter.value !== "none" })
const activeFilterLabel = computed(function() {
  var f = filters.find(function(x) { return x.name === activeFilter.value })
  return f ? f.label : ""
})
const currentFilterCss = computed(function() {
  var fn = filterMap[activeFilter.value]
  return fn ? fn(filterIntensity.value) : "none"
})
function applyFilter(name) {
  activeFilter.value = name
  filterIntensity.value = 100
}
function onSliderChange(e) {
  filterIntensity.value = e.detail.value
}
function pickImage() {
  uni.chooseImage({
    count: 1,
    sizeType: ["compressed"],
    success: function(res) {
      imageSrc.value = res.tempFilePaths[0]
      activeFilter.value = "none"
      filterIntensity.value = 100
    },
  })
}
function resetImage() {
  imageSrc.value = ""
  activeFilter.value = "none"
  filterIntensity.value = 100
}
function saveImage() {
  if (!imageSrc.value) return
  uni.getImageInfo({
    src: imageSrc.value,
    success: function(res) {
      var w = res.width
      var h = res.height
      canvasWidth.value = w
      canvasHeight.value = h
      var ctx = uni.createCanvasContext("filterCanvas")
      ctx.filter = currentFilterCss.value
      ctx.drawImage(imageSrc.value, 0, 0, w, h)
      ctx.draw(false, function() {
        setTimeout(function() {
          uni.canvasToTempFilePath({
            canvasId: "filterCanvas",
            success: function(result) {
              uni.saveImageToPhotosAlbum({
                filePath: result.tempFilePath,
                success: function() {
                  uni.showToast({ title: "已保存到相册", icon: "success" })
                },
                fail: function() {
                  uni.showToast({ title: "保存失败", icon: "none" })
                },
              })
            },
            fail: function() {
              uni.showToast({ title: "导出失败", icon: "none" })
            },
          })
        }, 300)
      })
    },
    fail: function() {
      uni.showToast({ title: "图片信息获取失败", icon: "none" })
    },
  })
}
</script>
<style scoped>
.page{min-height:100vh;background:#f5f7fb}.custom-nav{background:linear-gradient(135deg,#a855f7,#ec4899);width:100%}.nav-row{height:88rpx;display:flex;align-items:center;padding:0 24rpx}.nav-icon{width:72rpx;text-align:center;font-size:44rpx;color:#fff;font-weight:700;flex-shrink:0}.nav-title{flex:1;text-align:center;font-size:32rpx;color:#fff;font-weight:600}.content{padding:24rpx}.pick-area{height:400rpx;border:2rpx dashed #ccc;border-radius:16rpx;display:flex;flex-direction:column;align-items:center;justify-content:center;background:#fff}.pick-icon{font-size:80rpx;color:#a855f7;line-height:1}.pick-text{font-size:28rpx;color:#999;margin-top:16rpx}.section-label{font-size:28rpx;color:#333;font-weight:600;margin:24rpx 0 12rpx;display:block}.preview-section{background:#fff;border-radius:16rpx;padding:16rpx;margin-bottom:16rpx}.preview-img{width:100%;height:400rpx;border-radius:12rpx;background:#f0f0f0}.filter-scroll{white-space:nowrap;width:100%}.filter-item{display:inline-flex;flex-direction:column;align-items:center;margin-right:20rpx;padding:12rpx;border-radius:12rpx;background:#fff}.filter-item.active{background:#f3e8ff;border:2rpx solid #a855f7}.filter-thumb{width:100rpx;height:100rpx;border-radius:8rpx;background:linear-gradient(135deg,#a855f7,#ec4899)}.filter-name{font-size:22rpx;color:#666;margin-top:8rpx}.slider-section{background:#fff;border-radius:16rpx;padding:24rpx;margin-bottom:16rpx}.slider-label{font-size:26rpx;color:#333;margin-bottom:8rpx}.action-row{display:flex;gap:16rpx;margin-top:24rpx}.action-btn{flex:1;height:88rpx;border-radius:44rpx;display:flex;align-items:center;justify-content:center}.action-btn.primary{background:linear-gradient(135deg,#a855f7,#ec4899)}.action-btn.secondary{background:#fff;border:2rpx solid #ddd}.action-text{font-size:30rpx;font-weight:600;color:#fff}.action-btn.secondary .action-text{color:#666}
</style>