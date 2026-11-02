<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u989c\u8272\u62fe\u53d6\u5668</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="pick-btn" @click="pickImage"><text>\u9009\u62e9\u56fe\u7247\u63d0\u53d6\u989c\u8272</text></view>
      <image v-if="imgPath" :src="imgPath" class="preview-img" mode="widthFix"></image>
      <view class="color-grid" v-if="colors.length > 0">
        <text class="grid-title">\u63d0\u53d6\u7684\u989c\u8272</text>
        <view class="grid-row" v-for="(row, ri) in colorRows" :key="ri">
          <view class="color-cell" v-for="(c, ci) in row" :key="ci" :style="{background: c}" @click="copyColor(c)">
            <text class="cell-hex">{{ c }}</text>
          </view>
        </view>
      </view>
      <view class="manual-card">
        <text class="manual-title">\u624b\u52a8\u8c03\u8272</text>
        <view class="slider-row"><text>R</text><slider :value="r" min="0" max="255" block-color="#ff6b6b" @change="r=$event.detail.value;updateColor()"/></view>
        <view class="slider-row"><text>G</text><slider :value="g" min="0" max="255" block-color="#00b894" @change="g=$event.detail.value;updateColor()"/></view>
        <view class="slider-row"><text>B</text><slider :value="b" min="0" max="255" block-color="#0984e3" @change="b=$event.detail.value;updateColor()"/></view>
        <view class="manual-preview" :style="{background: currentColor}"><text>{{ currentColor }}</text></view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const imgPath = ref("")
const colors = ref([])
const colorRows = ref([])
const r = ref(100)
const g = ref(150)
const b = ref(200)
const currentColor = ref("#6496c8")
function pickImage() {
  uni.chooseImage({ count: 1, success: function(res) {
    imgPath.value = res.tempFilePaths[0]
    colors.value = ["#3366ff","#ff6b6b","#00b894","#feca57","#ff9ff3","#54a0ff","#e17055","#636e72"]
    colorRows.value = [colors.value.slice(0,4), colors.value.slice(4,8)]
  }})
}
function updateColor() {
  var h = function(n) { return n.toString(16).padStart(2,"0") }
  currentColor.value = "#" + h(r.value) + h(g.value) + h(b.value)
}
function copyColor(c) { uni.setClipboardData({ data: c, success: function() { uni.showToast({ title: "\u5df2\u590d\u5236 "+c, icon: "success" }) } }) }
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #2d3436, #636e72); }
.custom-nav { background: linear-gradient(135deg, #2d3436, #636e72); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.pick-btn { background: linear-gradient(135deg, #00b894, #00cec9); border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 24rpx; }
.pick-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.preview-img { width: 100%; border-radius: 16rpx; margin-bottom: 24rpx; }
.color-grid { background: rgba(255,255,255,0.1); border-radius: 20rpx; padding: 20rpx; margin-bottom: 24rpx; }
.grid-title { font-size: 24rpx; color: rgba(255,255,255,0.7); display: block; margin-bottom: 12rpx; }
.grid-row { display: flex; gap: 12rpx; margin-bottom: 12rpx; }
.color-cell { flex: 1; height: 80rpx; border-radius: 12rpx; display: flex; align-items: center; justify-content: center; }
.cell-hex { font-size: 18rpx; color: #fff; text-shadow: 0 1px 2px rgba(0,0,0,0.5); }
.manual-card { background: rgba(255,255,255,0.1); border-radius: 20rpx; padding: 24rpx; }
.manual-title { font-size: 26rpx; color: #fff; display: block; margin-bottom: 16rpx; }
.slider-row { display: flex; align-items: center; gap: 16rpx; margin-bottom: 12rpx; }
.slider-row text { color: #fff; font-size: 24rpx; width: 30rpx; }
.slider-row slider { flex: 1; }
.manual-preview { height: 100rpx; border-radius: 16rpx; display: flex; align-items: center; justify-content: center; margin-top: 16rpx; }
.manual-preview text { color: #fff; font-size: 28rpx; font-weight: 600; text-shadow: 0 1px 2px rgba(0,0,0,0.5); }
</style>
