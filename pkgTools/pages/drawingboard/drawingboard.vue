<template><view class="page"><view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }"><view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">简笔画</text><text class="nav-icon" @click="clear">🗑</text></view></view><view class="content"><view class="canvas-area"><canvas canvas-id="drawCanvas" class="draw-canvas" @touchstart="startDraw" @touchmove="doDraw" @touchend="endDraw"></canvas></view><view class="toolbar"><view class="color-pick"><text class="cp-label">颜色</text><view class="cp-colors"><text class="cp-c" v-for="c in colors" :key="c" :style="{background:c}" :class="{active:penColor===c}" @click="penColor=c"></text></view></view><view class="size-pick"><text class="cp-label">粗细</text><slider class="size-slider" :value="penSize" min="1" max="20" @change="penSize=$event.detail.value" block-size="16"/></view></view></view></view></template><script setup>import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const colors = ["#2d3436","#e17055","#00b894","#0984e3","#6c5ce7","#fdcb6e","#e84393","#636e72"]
const penColor = ref("#2d3436"); const penSize = ref(4)
var isDrawing = false, lastX = 0, lastY = 0
function startDraw(e) { isDrawing = true; var t = e.touches[0]; lastX = t.x; lastY = t.y }
function doDraw(e) {
  if (!isDrawing) return
  var t = e.touches[0]; var ctx = uni.createCanvasContext("drawCanvas")
  ctx.beginPath(); ctx.moveTo(lastX, lastY); ctx.lineTo(t.x, t.y)
  ctx.setStrokeStyle(penColor.value); ctx.setLineWidth(penSize.value); ctx.setLineCap("round"); ctx.stroke(); ctx.draw(true)
  lastX = t.x; lastY = t.y
}
function endDraw() { isDrawing = false }
function clear() { var ctx = uni.createCanvasContext("drawCanvas"); ctx.clearRect(0,0,600,800); ctx.draw() }
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script><style scoped>.page{min-height:100vh;background:#f5f7fb}.custom-nav{background:linear-gradient(135deg,#e84393,#fd79a8);width:100%}.nav-row{height:88rpx;display:flex;align-items:center;padding:0 24rpx}.nav-icon{width:72rpx;text-align:center;font-size:44rpx;color:#fff;font-weight:700;flex-shrink:0}.nav-title{flex:1;text-align:center;font-size:32rpx;color:#fff;font-weight:600}.content{padding:24rpx}.canvas-area{background:#fff;border-radius:20rpx;overflow:hidden;margin-bottom:24rpx}.draw-canvas{width:100%;height:600rpx}.toolbar{background:#fff;border-radius:20rpx;padding:24rpx}.color-pick{margin-bottom:24rpx}.cp-label{font-size:26rpx;color:#999;display:block;margin-bottom:12rpx}.cp-colors{display:flex;gap:16rpx}.cp-c{width:56rpx;height:56rpx;border-radius:50%}.cp-c.active{box-shadow:0 0 0 4rpx #333}.size-pick{display:flex;align-items:center;gap:16rpx}.size-slider{flex:1}</style>