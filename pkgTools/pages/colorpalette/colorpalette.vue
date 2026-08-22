<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">←</text>
        <text class="nav-title">配色方案</text>
        <text class="nav-icon"> </text>
      </view>
    </view>
    <view class="content">
      <view class="type-section">
        <text class="section-label">配色类型</text>
        <view class="type-grid">
          <view v-for="t in types" :key="t.value" class="type-btn" :class="{ active: paletteType === t.value }" @click="generate(t.value)">
            <text class="type-label">{{ t.label }}</text>
          </view>
        </view>
      </view>
      <view class="palette-section">
        <view class="swatch-row">
          <view v-for="(c, i) in colors" :key="i" class="swatch" :style="{ background: c.hex }" @click="copyHex(c.hex)">
            <view class="lock-btn" @click.stop="toggleLock(i)">
              <text class="lock-icon">{{ locked[i] ? "🔒" : "🔓" }}</text>
            </view>
            <text class="hex-text" :style="{ color: getContrast(c.hex) }">{{ c.hex }}</text>
            <text class="copy-hint" :style="{ color: getContrast(c.hex) }">点击复制</text>
          </view>
        </view>
      </view>
      <view class="action-section">
        <view class="action-btn primary" @click="generate(paletteType)">
          <text class="action-text">重新生成</text>
        </view>
        <view class="action-btn secondary" @click="exportCss">
          <text class="action-text">导出CSS</text>
        </view>
      </view>
      <view class="info-section">
        <text class="section-label">色彩和谐规则</text>
        <view class="info-card">
          <text class="info-title">{{ currentTypeLabel }}</text>
          <text class="info-desc">{{ currentTypeDesc }}</text>
        </view>
      </view>
      <view class="css-section" v-if="cssOutput">
        <text class="section-label">CSS变量</text>
        <view class="css-box">
          <text class="css-text" @click="copyCss">{{ cssOutput }}</text>
        </view>
      </view>
    </view>
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
  generate("random")
})
const colors = ref([])
const locked = ref([false, false, false, false, false])
const paletteType = ref("random")
const cssOutput = ref("")
const types = [
  { value: "random", label: "随机" },
  { value: "complementary", label: "互补色" },
  { value: "triadic", label: "三色组" },
  { value: "analogous", label: "类似色" },
  { value: "monochromatic", label: "单色" },
]
var typeDescs = {
  random: "随机生成五种协调的颜色，每次点击都会产生新的组合。",
  complementary: "基于色轮上相对位置的两种颜色，产生强烈对比效果。",
  triadic: "色轮上等距分布的三种颜色，形成鲜明而平衡的配色。",
  analogous: "色轮上相邻的颜色组合，营造和谐统一的视觉感受。",
  monochromatic: "同一色相的不同明度和饱和度变化，简洁而优雅。",
}
const currentTypeLabel = computed(function() {
  var t = types.find(function(x) { return x.value === paletteType.value })
  return t ? t.label : ""
})
const currentTypeDesc = computed(function() { return typeDescs[paletteType.value] || "" })
function hslToHex(h, s, l) {
  h = ((h % 360) + 360) % 360
  s = s / 100
  l = l / 100
  var c = (1 - Math.abs(2 * l - 1)) * s
  var x = c * (1 - Math.abs((h / 60) % 2 - 1))
  var m = l - c / 2
  var r = 0, g = 0, b = 0
  if (h < 60) { r = c; g = x; b = 0 }
  else if (h < 120) { r = x; g = c; b = 0 }
  else if (h < 180) { r = 0; g = c; b = x }
  else if (h < 240) { r = 0; g = x; b = c }
  else if (h < 300) { r = x; g = 0; b = c }
  else { r = c; g = 0; b = x }
  var ri = Math.round((r + m) * 255)
  var gi = Math.round((g + m) * 255)
  var bi = Math.round((b + m) * 255)
  return "#" + ((1 << 24) + (ri << 16) + (gi << 8) + bi).toString(16).slice(1)
}
function hexToHsl(hex) {
  var r = parseInt(hex.slice(1, 3), 16) / 255
  var g = parseInt(hex.slice(3, 5), 16) / 255
  var b = parseInt(hex.slice(5, 7), 16) / 255
  var max = Math.max(r, g, b), min = Math.min(r, g, b)
  var h, s, l = (max + min) / 2
  if (max === min) { h = s = 0 }
  else {
    var d = max - min
    s = l > 0.5 ? d / (2 - max - min) : d / (max + min)
    switch (max) {
      case r: h = (g - b) / d + (g < b ? 6 : 0); break
      case g: h = (b - r) / d + 2; break
      case b: h = (r - g) / d + 4; break
    }
    h *= 60
  }
  return { h: h, s: s * 100, l: l * 100 }
}
function getContrast(hex) {
  var r = parseInt(hex.slice(1, 3), 16)
  var g = parseInt(hex.slice(3, 5), 16)
  var b = parseInt(hex.slice(5, 7), 16)
  var luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
  return luminance > 0.5 ? "#000000" : "#ffffff"
}
function generate(type) {
  paletteType.value = type
  var result = []
  var baseHue = Math.random() * 360
  if (type === "random") {
    for (var i = 0; i < 5; i++) {
      if (locked.value[i]) {
        result.push(colors.value[i].hex)
      } else {
        result.push(hslToHex(Math.random() * 360, 50 + Math.random() * 40, 40 + Math.random() * 30))
      }
    }
  } else if (type === "complementary") {
    for (var i = 0; i < 5; i++) {
      if (locked.value[i]) { result.push(colors.value[i].hex); continue }
      var hue = i < 3 ? baseHue : baseHue + 180
      result.push(hslToHex(hue, 60 + Math.random() * 30, 45 + Math.random() * 25))
    }
  } else if (type === "triadic") {
    var triHues = [baseHue, baseHue + 120, baseHue + 240]
    for (var i = 0; i < 5; i++) {
      if (locked.value[i]) { result.push(colors.value[i].hex); continue }
      var hue = triHues[i % 3]
      result.push(hslToHex(hue, 55 + Math.random() * 35, 40 + Math.random() * 30))
    }
  } else if (type === "analogous") {
    for (var i = 0; i < 5; i++) {
      if (locked.value[i]) { result.push(colors.value[i].hex); continue }
      var hue = baseHue + (i - 2) * 30
      result.push(hslToHex(hue, 50 + Math.random() * 35, 35 + Math.random() * 35))
    }
  } else if (type === "monochromatic") {
    for (var i = 0; i < 5; i++) {
      if (locked.value[i]) { result.push(colors.value[i].hex); continue }
      var lightness = 20 + i * 15 + Math.random() * 10
      result.push(hslToHex(baseHue, 60 + Math.random() * 30, lightness))
    }
  }
  colors.value = result.map(function(hex) { return { hex: hex } })
  updateCss()
}
function toggleLock(i) {
  locked.value[i] = !locked.value[i]
}
function copyHex(hex) {
  uni.setClipboardData({
    data: hex,
    success: function() {
      uni.showToast({ title: "已复制 " + hex, icon: "success" })
    },
  })
}
function updateCss() {
  var lines = [":root {"]
  for (var i = 0; i < colors.value.length; i++) {
    lines.push("  --color-" + (i + 1) + ": " + colors.value[i].hex + ";")
  }
  lines.push("}")
  cssOutput.value = lines.join("\n")
}
function copyCss() {
  uni.setClipboardData({
    data: cssOutput.value,
    success: function() {
      uni.showToast({ title: "CSS已复制", icon: "success" })
    },
  })
}
function exportCss() {
  uni.setClipboardData({
    data: cssOutput.value,
    success: function() {
      uni.showToast({ title: "CSS变量已复制到剪贴板", icon: "success" })
    },
  })
}
</script>
<style scoped>
.page{min-height:100vh;background:#f5f7fb}.custom-nav{background:linear-gradient(135deg,#f43f5e,#f97316);width:100%}.nav-row{height:88rpx;display:flex;align-items:center;padding:0 24rpx}.nav-icon{width:72rpx;text-align:center;font-size:44rpx;color:#fff;font-weight:700;flex-shrink:0}.nav-title{flex:1;text-align:center;font-size:32rpx;color:#fff;font-weight:600}.content{padding:24rpx}.type-section{background:#fff;border-radius:16rpx;padding:24rpx;margin-bottom:16rpx}.section-label{font-size:28rpx;color:#333;font-weight:600;margin-bottom:16rpx;display:block}.type-grid{display:flex;gap:12rpx;flex-wrap:wrap}.type-btn{padding:16rpx 24rpx;border-radius:36rpx;background:#f5f7fb;border:2rpx solid transparent}.type-btn.active{background:#ffe4e6;border-color:#f43f5e}.type-label{font-size:26rpx;color:#333}.type-btn.active .type-label{color:#f43f5e;font-weight:600}.palette-section{margin-bottom:16rpx}.swatch-row{display:flex;flex-direction:column;border-radius:16rpx;overflow:hidden}.swatch{flex:1;min-height:120rpx;display:flex;flex-direction:column;align-items:center;justify-content:center;position:relative;cursor:pointer}.lock-btn{position:absolute;top:12rpx;right:12rpx}.lock-icon{font-size:28rpx}.hex-text{font-size:32rpx;font-weight:700;letter-spacing:1rpx}.copy-hint{font-size:20rpx;opacity:0.7;margin-top:4rpx}.action-section{display:flex;gap:16rpx;margin-top:24rpx}.action-btn{flex:1;height:88rpx;border-radius:44rpx;display:flex;align-items:center;justify-content:center}.action-btn.primary{background:linear-gradient(135deg,#f43f5e,#f97316)}.action-btn.secondary{background:#fff;border:2rpx solid #ddd}.action-text{font-size:30rpx;font-weight:600;color:#fff}.action-btn.secondary .action-text{color:#666}.info-section{margin-top:24rpx}.info-card{background:#fff;border-radius:16rpx;padding:24rpx}.info-title{font-size:30rpx;font-weight:600;color:#333;margin-bottom:8rpx;display:block}.info-desc{font-size:26rpx;color:#666;line-height:40rpx}.css-section{margin-top:24rpx}.css-box{background:#1e293b;border-radius:16rpx;padding:24rpx}.css-text{font-size:24rpx;color:#e2e8f0;font-family:monospace;line-height:36rpx;white-space:pre-wrap}
</style>