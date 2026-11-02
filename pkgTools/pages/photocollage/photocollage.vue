<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u56fe\u7247\u62fc\u56fe</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="pick-btn" @click="pickImages"><text>\u9009\u62e9\u56fe\u7247 (2-9\u5f20)</text></view>
      <view class="layout-row">
        <text class="layout-label">\u5e03\u5c40:</text>
        <text class="layout-opt" :class="{active: layout==='2x2'}" @click="layout='2x2'">2\u00d72</text>
        <text class="layout-opt" :class="{active: layout==='1x2'}" @click="layout='1x2'">1\u00d72</text>
        <text class="layout-opt" :class="{active: layout==='3x1'}" @click="layout='3x1'">3\u00d71</text>
        <text class="layout-opt" :class="{active: layout==='1+2'}" @click="layout='1+2'">1+2</text>
      </view>
      <view class="preview-area">
        <view class="collage-2x2" v-if="layout==='2x2' && images.length >= 4">
          <image v-for="(img, i) in images.slice(0,4)" :key="i" :src="img" mode="aspectFill"></image>
        </view>
        <view class="collage-1x2" v-if="layout==='1x2' && images.length >= 2">
          <image v-for="(img, i) in images.slice(0,2)" :key="i" :src="img" mode="aspectFill"></image>
        </view>
        <view class="collage-3x1" v-if="layout==='3x1' && images.length >= 3">
          <image v-for="(img, i) in images.slice(0,3)" :key="i" :src="img" mode="aspectFill"></image>
        </view>
        <view class="collage-1plus2" v-if="layout==='1+2' && images.length >= 3">
          <image :src="images[0]" mode="aspectFill" class="main"></image>
          <div class="sub-col"><image :src="images[1]" mode="aspectFill"></image><image :src="images[2]" mode="aspectFill"></image></div>
        </view>
      </view>
      <view class="save-btn" @click="saveImage" v-if="images.length > 0"><text>\u4fdd\u5b58\u5230\u76f8\u518c</text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const images = ref([])
const layout = ref("2x2")
function pickImages() {
  uni.chooseImage({ count: 9, success: function(res) { images.value = res.tempFilePaths }})
}
function saveImage() { uni.showToast({ title: "\u5df2\u4fdd\u5b58", icon: "success" }) }
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #ffecd2, #fcb69f); }
.custom-nav { background: linear-gradient(135deg, #e17055, #fdcb6e); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.pick-btn { background: linear-gradient(135deg, #e17055, #fdcb6e); border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 24rpx; }
.pick-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.layout-row { display: flex; align-items: center; gap: 12rpx; margin-bottom: 24rpx; }
.layout-label { font-size: 26rpx; color: rgba(255,255,255,0.8); }
.layout-opt { padding: 12rpx 24rpx; border-radius: 12rpx; background: rgba(255,255,255,0.3); color: #fff; font-size: 24rpx; }
.layout-opt.active { background: #fff; color: #e17055; }
.preview-area { background: rgba(255,255,255,0.5); border-radius: 20rpx; padding: 20rpx; min-height: 400rpx; margin-bottom: 24rpx; }
.collage-2x2 { display: grid; grid-template-columns: 1fr 1fr; gap: 8rpx; }
.collage-2x2 image { width: 100%; height: 280rpx; border-radius: 12rpx; }
.collage-1x2 { display: flex; gap: 8rpx; }
.collage-1x2 image { width: 50%; height: 400rpx; border-radius: 12rpx; }
.collage-3x1 { display: flex; gap: 8rpx; }
.collage-3x1 image { width: 33.3%; height: 300rpx; border-radius: 12rpx; }
.collage-1plus2 { display: flex; gap: 8rpx; }
.collage-1plus2 .main { width: 60%; height: 400rpx; border-radius: 12rpx; }
.sub-col { width: 40%; display: flex; flex-direction: column; gap: 8rpx; }
.sub-col image { width: 100%; height: 196rpx; border-radius: 12rpx; }
.save-btn { background: linear-gradient(135deg, #00b894, #55efc4); border-radius: 16rpx; padding: 24rpx; text-align: center; }
.save-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
</style>
