<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">←</text>
        <text class="nav-title">图片拼接</text>
        <text class="nav-icon"> </text>
      </view>
    </view>
    <view class="content">
      <view class="pick-area" @click="pickImages" v-if="images.length === 0">
        <text class="pick-icon">+</text>
        <text class="pick-text">点击选择图片（最多9张）</text>
      </view>
      <view v-if="images.length > 0">
        <view class="img-grid">
          <view v-for="(img, i) in images" :key="i" class="grid-item">
            <image :src="img" mode="aspectFill" class="grid-img"></image>
            <text class="remove-btn" @click="removeImage(i)">×</text>
          </view>
          <view class="grid-item add-more" @click="pickImages" v-if="images.length < 9">
            <text class="add-icon">+</text>
          </view>
        </view>
        <view class="option-section">
          <text class="section-label">布局方式</text>
          <view class="layout-options">
            <view v-for="opt in layouts" :key="opt.value" class="layout-btn" :class="{ active: layout === opt.value }" @click="layout = opt.value">
              <text class="layout-text">{{ opt.label }}</text>
            </view>
          </view>
        </view>
        <view class="option-section">
          <text class="section-label">间距: {{ spacing }}px</text>
          <slider :value="spacing" :min="0" :max="30" block-size="20" block-color="#10b981" @change="onSpacingChange" />
        </view>
        <view class="option-section">
          <text class="section-label">背景颜色</text>
          <view class="color-row">
            <view v-for="c in bgColors" :key="c" class="color-dot" :class="{ active: bgColor === c }" :style="{ background: c }" @click="bgColor = c"></view>
            <view class="color-dot custom" @click="showCustomColor = !showCustomColor">
              <text class="plus-mini">+</text>
            </view>
          </view>
          <input v-if="showCustomColor" class="color-input" placeholder="输入颜色如 #ffffff" v-model="bgColor" />
        </view>
        <view class="preview-section">
          <text class="section-label">预览</text>
          <view class="merge-preview" :style="{ background: bgColor, padding: spacing + 'px' }">
            <view v-if="layout === vertical" class="layout-vertical">
              <image v-for="(img, i) in images" :key="i" :src="img" mode="widthFix" class="merged-img" :style="{ marginBottom: i < images.length - 1 ? spacing + 'px' : '0' }"></image>
            </view>
            <view v-if="layout === horizontal" class="layout-horizontal">
              <image v-for="(img, i) in images" :key="i" :src="img" mode="heightFix" class="merged-img-h" :style="{ marginRight: i < images.length - 1 ? spacing + 'px' : '0' }"></image>
            </view>
            <view v-if="layout === grid2" class="layout-grid2">
              <image v-for="(img, i) in images.slice(0,4)" :key="i" :src="img" mode="aspectFill" class="grid2-img"></image>
            </view>
            <view v-if="layout === grid3" class="layout-grid3">
              <image v-for="(img, i) in images.slice(0,9)" :key="i" :src="img" mode="aspectFill" class="grid3-img"></image>
            </view>
          </view>
        </view>
        <view class="action-row">
          <view class="action-btn primary" @click="saveMerged">
            <text class="action-text">保存拼接图</text>
          </view>
          <view class="action-btn secondary" @click="resetAll">
            <text class="action-text">重新选择</text>
          </view>
        </view>
      </view>
    </view>
    <canvas canvas-id="mergeCanvas" :style="{ width: canvasW + 'px', height: canvasH + 'px', position: 'fixed', top: '-9999px', left: '-9999px' }"></canvas>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
function goBack() { uni.navigateBack() }
onMounted(function () {
  if (!uni.getStorageSync("isLoggedIn")) {
    uni.reLaunch({ url: "/pages/login/login" })
    return
  }
})
const images = ref([])
const layout = ref("vertical")
const spacing = ref(4)
const bgColor = ref("#ffffff")
const showCustomColor = ref(false)
const canvasW = ref(600)
const canvasH = ref(800)
const layouts = [
  { value: "vertical", label: "垂直" },
  { value: "horizontal", label: "水平" },
  { value: "grid2", label: "2×2" },
  { value: "grid3", label: "3×3" },
]
const bgColors = ["#ffffff", "#000000", "#f5f7fb", "#10b981", "#06b6d4", "#f43f5e", "#f97316", "#a855f7"]
function onSpacingChange(e) { spacing.value = e.detail.value }
function pickImages() {
  var remain = 9 - images.value.length
  uni.chooseImage({
    count: remain,
    sizeType: ["compressed"],
    success: function(res) {
      images.value = images.value.concat(res.tempFilePaths)
    },
  })
}
function removeImage(i) { images.value.splice(i, 1) }
function resetAll() {
  images.value = []
  layout.value = "vertical"
  spacing.value = 4
  bgColor.value = "#ffffff"
}
function saveMerged() {
  if (images.value.length === 0) return
  uni.showLoading({ title: "生成中..." })
  var loaded = 0
  var infos = []
  var total = images.value.length
  for (var i = 0; i < total; i++) {
    uni.getImageInfo({
      src: images.value[i],
      success: function(res) {
        infos.push(res)
        loaded++
        if (loaded === total) {
          drawMerged(infos)
        }
      },
      fail: function() {
        loaded++
        infos.push(null)
        if (loaded === total) {
          drawMerged(infos.filter(function(x) { return x !== null }))
        }
      },
    })
  }
}
function drawMerged(infos) {
  if (infos.length === 0) {
    uni.hideLoading()
    uni.showToast({ title: "图片加载失败", icon: "none" })
    return
  }
  var sp = spacing.value
  var w = 600
  var h = 800
  var ctx = uni.createCanvasContext("mergeCanvas")
  ctx.setFillStyle(bgColor.value)
  ctx.fillRect(0, 0, w, h)
  if (layout.value === "vertical") {
    var totalH = 0
    for (var i = 0; i < infos.length; i++) {
      var ratio = infos[i].height / infos[i].width
      totalH += w * ratio + (i < infos.length - 1 ? sp : 0)
    }
    canvasW.value = w
    canvasH.value = totalH
    var yOffset = 0
    for (var i = 0; i < infos.length; i++) {
      var h_i = w * (infos[i].height / infos[i].width)
      ctx.drawImage(infos[i].path, 0, yOffset, w, h_i)
      yOffset += h_i + sp
    }
  } else if (layout.value === "horizontal") {
    var totalW = 0
    for (var i = 0; i < infos.length; i++) {
      var ratio2 = infos[i].width / infos[i].height
      totalW += h * ratio2 + (i < infos.length - 1 ? sp : 0)
    }
    canvasW.value = totalW
    canvasH.value = h
    var xOffset = 0
    for (var i = 0; i < infos.length; i++) {
      var w_i = h * (infos[i].width / infos[i].height)
      ctx.drawImage(infos[i].path, xOffset, 0, w_i, h)
      xOffset += w_i + sp
    }
  } else if (layout.value === "grid2") {
    var cellW = (w - sp) / 2
    var cellH = (h - sp) / 2
    canvasW.value = w
    canvasH.value = h
    for (var i = 0; i < Math.min(infos.length, 4); i++) {
      var col = i % 2
      var row = Math.floor(i / 2)
      ctx.drawImage(infos[i].path, col * (cellW + sp), row * (cellH + sp), cellW, cellH)
    }
  } else if (layout.value === "grid3") {
    var cellW3 = (w - 2 * sp) / 3
    var cellH3 = (h - 2 * sp) / 3
    canvasW.value = w
    canvasH.value = h
    for (var i = 0; i < Math.min(infos.length, 9); i++) {
      var col3 = i % 3
      var row3 = Math.floor(i / 3)
      ctx.drawImage(infos[i].path, col3 * (cellW3 + sp), row3 * (cellH3 + sp), cellW3, cellH3)
    }
  }
  ctx.draw(false, function() {
    setTimeout(function() {
      uni.canvasToTempFilePath({
        canvasId: "mergeCanvas",
        success: function(result) {
          uni.saveImageToPhotosAlbum({
            filePath: result.tempFilePath,
            success: function() {
              uni.hideLoading()
              uni.showToast({ title: "已保存到相册", icon: "success" })
            },
            fail: function() {
              uni.hideLoading()
              uni.showToast({ title: "保存失败", icon: "none" })
            },
          })
        },
        fail: function() {
          uni.hideLoading()
          uni.showToast({ title: "导出失败", icon: "none" })
        },
      })
    }, 300)
  })
}
</script>
<style scoped>
.page{min-height:100vh;background:#f5f7fb}.custom-nav{background:linear-gradient(135deg,#10b981,#06b6d4);width:100%}.nav-row{height:88rpx;display:flex;align-items:center;padding:0 24rpx}.nav-icon{width:72rpx;text-align:center;font-size:44rpx;color:#fff;font-weight:700;flex-shrink:0}.nav-title{flex:1;text-align:center;font-size:32rpx;color:#fff;font-weight:600}.content{padding:24rpx}.pick-area{height:400rpx;border:2rpx dashed #ccc;border-radius:16rpx;display:flex;flex-direction:column;align-items:center;justify-content:center;background:#fff}.pick-icon{font-size:80rpx;color:#10b981;line-height:1}.pick-text{font-size:28rpx;color:#999;margin-top:16rpx}.img-grid{display:flex;flex-wrap:wrap;gap:12rpx;margin-bottom:24rpx}.grid-item{width:210rpx;height:210rpx;position:relative;border-radius:12rpx;overflow:hidden}.grid-img{width:100%;height:100%}.remove-btn{position:absolute;top:4rpx;right:4rpx;width:40rpx;height:40rpx;background:rgba(0,0,0,0.5);border-radius:50%;text-align:center;line-height:40rpx;color:#fff;font-size:32rpx}.add-more{display:flex;align-items:center;justify-content:center;background:#f0f0f0;border:2rpx dashed #ccc}.add-icon{font-size:60rpx;color:#10b981}.option-section{background:#fff;border-radius:16rpx;padding:24rpx;margin-bottom:16rpx}.section-label{font-size:28rpx;color:#333;font-weight:600;margin-bottom:16rpx;display:block}.layout-options{display:flex;gap:12rpx}.layout-btn{flex:1;height:72rpx;border-radius:36rpx;background:#f5f7fb;display:flex;align-items:center;justify-content:center;border:2rpx solid transparent}.layout-btn.active{background:#d1fae5;border-color:#10b981}.layout-text{font-size:26rpx;color:#333}.layout-btn.active .layout-text{color:#10b981;font-weight:600}.color-row{display:flex;gap:16rpx;flex-wrap:wrap}.color-dot{width:60rpx;height:60rpx;border-radius:50%;border:3rpx solid transparent}.color-dot.active{border-color:#333}.color-dot.custom{background:#f0f0f0;border:2rpx dashed #ccc;display:flex;align-items:center;justify-content:center}.plus-mini{font-size:32rpx;color:#999}.color-input{margin-top:12rpx;height:72rpx;border:2rpx solid #ddd;border-radius:12rpx;padding:0 20rpx;font-size:26rpx}.preview-section{background:#fff;border-radius:16rpx;padding:16rpx;margin-bottom:16rpx}.merge-preview{border-radius:12rpx;min-height:300rpx;overflow:hidden}.layout-vertical,.layout-horizontal{display:flex;flex-direction:column}.layout-horizontal{flex-direction:row}.merged-img{width:100%}.merged-img-h{height:300rpx}.layout-grid2,.layout-grid3{display:flex;flex-wrap:wrap;gap:4px}.grid2-img{width:calc(50% - 2px);height:200rpx}.grid3-img{width:calc(33.33% - 3px);height:160rpx}.action-row{display:flex;gap:16rpx;margin-top:24rpx}.action-btn{flex:1;height:88rpx;border-radius:44rpx;display:flex;align-items:center;justify-content:center}.action-btn.primary{background:linear-gradient(135deg,#10b981,#06b6d4)}.action-btn.secondary{background:#fff;border:2rpx solid #ddd}.action-text{font-size:30rpx;font-weight:600;color:#fff}.action-btn.secondary .action-text{color:#666}
</style>