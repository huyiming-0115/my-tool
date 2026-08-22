<template>
  <view class="filter-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">←</text>
        <text class="nav-title">图片滤镜</text>
        <text class="nav-icon" @click="saveImage" v-if="hasImage">💾</text>
        <text class="nav-icon empty" v-else> </text>
      </view>
    </view>
    <view class="content">
      <view class="upload-area" v-if="!hasImage" @click="chooseImage">
        <text class="upload-icon">🖼️</text>
        <text class="upload-text">点击选择图片</text>
        <text class="upload-hint">支持 JPG / PNG 格式</text>
      </view>
      <view class="preview-area" v-else>
        <image class="preview-img" :src="imagePath" mode="aspectFit" :style="showOriginal ? {} : { filter: getFilterStyle() }" @load="onImgLoad"></image>
        <view class="compare-btn" @click="toggleCompare">
          <text>{{ showOriginal ? "查看效果" : "查看原图" }}</text>
        </view>
      </view>
      <view class="filter-section" v-if="hasImage">
        <view class="section-title">风格滤镜</view>
        <scroll-view class="filter-scroll" scroll-x>
          <view class="filter-list">
            <view class="filter-item" v-for="f in filters" :key="f.name" :class="{ active: activeFilter === f.name }" @click="applyFilter(f.name)">
              <view class="filter-thumb" :style="{ background: f.color }">
                <text>{{ f.icon }}</text>
              </view>
              <text class="filter-name">{{ f.name }}</text>
            </view>
          </view>
        </scroll-view>
      </view>
      <view class="adjust-section" v-if="hasImage && showAdjust">
        <view class="slider-row">
          <text class="slider-label">亮度 {{ adjust.brightness }}</text>
          <slider class="slider" :value="adjust.brightness" min="-100" max="100" @change="onBrightness" block-size="20" />
        </view>
        <view class="slider-row">
          <text class="slider-label">对比度 {{ adjust.contrast }}</text>
          <slider class="slider" :value="adjust.contrast" min="-100" max="100" @change="onContrast" block-size="20" />
        </view>
        <view class="slider-row">
          <text class="slider-label">饱和度 {{ adjust.saturation }}</text>
          <slider class="slider" :value="adjust.saturation" min="-100" max="100" @change="onSaturation" block-size="20" />
        </view>
      </view>
      <view class="toggle-adjust" v-if="hasImage" @click="showAdjust = !showAdjust">
        <text>{{ showAdjust ? "收起调节 ▲" : "参数调节 ▼" }}</text>
      </view>
      <view class="action-bar" v-if="hasImage">
        <button class="act-btn reselect" @click="chooseImage">重新选择</button>
        <button class="act-btn save" @click="saveImage">保存图片</button>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, reactive, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const imagePath = ref("")
const hasImage = ref(false)
const activeFilter = ref("原图")
const showOriginal = ref(false)
const showAdjust = ref(false)
const imgWidth = ref(0)
const imgHeight = ref(0)
const adjust = reactive({ brightness: 0, contrast: 0, saturation: 0 })
const filters = [
  { name: "原图", value: "", color: "linear-gradient(135deg, #667eea, #764ba2)", icon: "🖼" },
  { name: "黑白", value: "grayscale(100%)", color: "linear-gradient(135deg, #333, #999)", icon: "⬛" },
  { name: "怀旧", value: "sepia(80%) contrast(90%) brightness(95%)", color: "linear-gradient(135deg, #d4a574, #8b6914)", icon: "📜" },
  { name: "反相", value: "invert(100%)", color: "linear-gradient(135deg, #fff, #000)", icon: "🔄" },
  { name: "模糊", value: "blur(3px)", color: "linear-gradient(135deg, #a8c0ff, #3f2b96)", icon: "💨" },
  { name: "锐化", value: "contrast(150%) saturate(120%)", color: "linear-gradient(135deg, #f093fb, #f5576c)", icon: "✨" },
  { name: "浮雕", value: "grayscale(50%) contrast(120%) brightness(110%)", color: "linear-gradient(135deg, #c9b896, #8b7355)", icon: "🗿" },
  { name: "复古", value: "sepia(40%) saturate(140%) hue-rotate(-15deg)", color: "linear-gradient(135deg, #e8cbc0, #636fa4)", icon: "🎞" },
  { name: "冷调", value: "hue-rotate(180deg) saturate(80%)", color: "linear-gradient(135deg, #89f7fe, #66a6ff)", icon: "❄️" },
  { name: "暖调", value: "sepia(30%) saturate(130%) brightness(105%)", color: "linear-gradient(135deg, #f6d365, #fda085)", icon: "🔥" },
  { name: "高对比", value: "contrast(180%) brightness(90%)", color: "linear-gradient(135deg, #000, #fff)", icon: "◐" },
  { name: "鲜艳", value: "saturate(200%) contrast(110%)", color: "linear-gradient(135deg, #f5af19, #f12711)", icon: "🌈" }
]
function chooseImage() {
  uni.chooseImage({ count: 1, sizeType: ["compressed"], sourceType: ["album", "camera"], success: (res) => {
    imagePath.value = res.tempFilePaths[0]; hasImage.value = true; activeFilter.value = "原图"; resetAdjust()
  } })
}
function resetAdjust() { adjust.brightness = 0; adjust.contrast = 0; adjust.saturation = 0 }
function applyFilter(name) { activeFilter.value = name; resetAdjust() }
function onBrightness(e) { adjust.brightness = e.detail.value }
function onContrast(e) { adjust.contrast = e.detail.value }
function onSaturation(e) { adjust.saturation = e.detail.value }
function getFilterStyle() {
  const f = filters.find(x => x.name === activeFilter.value)
  const base = f ? f.value : ""
  const extra = []
  if (adjust.brightness !== 0) extra.push("brightness(" + (100 + adjust.brightness) + "%)")
  if (adjust.contrast !== 0) extra.push("contrast(" + (100 + adjust.contrast) + "%)")
  if (adjust.saturation !== 0) extra.push("saturate(" + (100 + adjust.saturation) + "%)")
  const all = base ? [base, ...extra] : extra
  return all.length > 0 ? all.join(" ") : "none"
}
function toggleCompare() { showOriginal.value = !showOriginal.value }
function onImgLoad(e) { imgWidth.value = e.detail.width; imgHeight.value = e.detail.height }
function saveImage() {
  if (!hasImage.value) return
  uni.showLoading({ title: "保存中..." })
  uni.saveImageToPhotosAlbum({ filePath: imagePath.value, success: () => {
    uni.hideLoading(); uni.showToast({ title: "已保存到相册", icon: "success" })
  }, fail: () => { uni.hideLoading(); uni.showToast({ title: "保存失败", icon: "none" }) } })
}
function goBack() { uni.navigateBack() }
onMounted(() => { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style lang="scss" scoped>
.filter-page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #667eea, #764ba2); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.upload-area { height: 400rpx; border: 4rpx dashed #d1d5db; border-radius: 24rpx; display: flex; flex-direction: column; align-items: center; justify-content: center; background: #fff; }
.upload-icon { font-size: 80rpx; }
.upload-text { font-size: 32rpx; color: #333; font-weight: 600; margin-top: 16rpx; }
.upload-hint { font-size: 24rpx; color: #999; margin-top: 8rpx; }
.preview-area { position: relative; background: #fff; border-radius: 24rpx; padding: 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); margin-bottom: 24rpx; }
.preview-img { width: 100%; height: 600rpx; border-radius: 16rpx; transition: filter 0.3s; }
.compare-btn { position: absolute; bottom: 40rpx; right: 40rpx; background: rgba(0,0,0,0.6); padding: 12rpx 24rpx; border-radius: 30rpx; }
.compare-btn text { font-size: 22rpx; color: #fff; }
.filter-section { margin-bottom: 24rpx; }
.section-title { font-size: 28rpx; font-weight: 600; color: #333; margin-bottom: 16rpx; }
.filter-scroll { white-space: nowrap; }
.filter-list { display: inline-flex; gap: 16rpx; padding: 8rpx 0; }
.filter-item { display: flex; flex-direction: column; align-items: center; width: 120rpx; opacity: 0.6; transition: opacity 0.2s; }
.filter-item.active { opacity: 1; }
.filter-item.active .filter-thumb { box-shadow: 0 0 0 4rpx #667eea; }
.filter-thumb { width: 96rpx; height: 96rpx; border-radius: 16rpx; display: flex; align-items: center; justify-content: center; }
.filter-thumb text { font-size: 40rpx; }
.filter-name { font-size: 22rpx; color: #666; margin-top: 8rpx; text-align: center; }
.adjust-section { background: #fff; border-radius: 24rpx; padding: 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); margin-bottom: 16rpx; }
.slider-row { display: flex; align-items: center; padding: 12rpx 0; }
.slider-label { font-size: 26rpx; color: #333; width: 180rpx; flex-shrink: 0; }
.slider { flex: 1; }
.toggle-adjust { text-align: center; padding: 16rpx; font-size: 24rpx; color: #999; }
.action-bar { display: flex; gap: 24rpx; margin-top: 24rpx; }
.act-btn { flex: 1; height: 88rpx; line-height: 88rpx; text-align: center; border-radius: 16rpx; font-size: 28rpx; font-weight: 600; border: none; }
.act-btn::after { border: none; }
.act-btn.reselect { background: #fff; color: #666; border: 2rpx solid #e5e7eb; }
.act-btn.reselect::after { border: 2rpx solid #e5e7eb; }
.act-btn.save { background: linear-gradient(135deg, #667eea, #764ba2); color: #fff; }
</style>
