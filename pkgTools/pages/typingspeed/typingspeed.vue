<template><view class="page"><view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }"><view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">打字测速</text><text class="nav-icon" @click="reset">🔄</text></view></view><view class="content"><view class="ts-display"><text class="ts-wpm">{{ wpm }}</text><text class="ts-label">WPM</text></view><view class="ts-target">{{ targetText }}</view><input class="ts-input" v-model="typed" @input="checkInput" placeholder="输入..." /><view class="ts-stats"><text>正确率: {{ accuracy }}%</text><text>用时: {{ elapsed }}s</text></view></view></view></template><script setup>import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const targetText = "The quick brown fox jumps over the lazy dog"
const typed = ref(""); const wpm = ref(0); const accuracy = ref(100); const elapsed = ref(0)
var startTime = null; var timer = null
function checkInput() {
  if (!startTime) { startTime = Date.now(); timer = setInterval(function() { elapsed.value = Math.floor((Date.now() - startTime) / 1000) }, 1000) }
  var correct = 0
  for (var i = 0; i < typed.value.length; i++) { if (typed.value[i] === targetText[i]) correct++ }
  accuracy.value = typed.value.length > 0 ? Math.round(correct / typed.value.length * 100) : 100
  var mins = (Date.now() - startTime) / 60000
  wpm.value = mins > 0 ? Math.round(typed.value.length / 5 / mins) : 0
  if (typed.value === targetText) { clearInterval(timer); uni.showToast({ title: "完成!", icon: "success" }) }
}
function reset() { typed.value = ""; wpm.value = 0; accuracy.value = 100; elapsed.value = 0; startTime = null; clearInterval(timer) }
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script><style scoped>.page{min-height:100vh;background:#f5f7fb}.custom-nav{background:linear-gradient(135deg,#6c5ce7,#a29bfe);width:100%}.nav-row{height:88rpx;display:flex;align-items:center;padding:0 24rpx}.nav-icon{width:72rpx;text-align:center;font-size:44rpx;color:#fff;font-weight:700;flex-shrink:0}.nav-title{flex:1;text-align:center;font-size:32rpx;color:#fff;font-weight:600}.content{padding:32rpx}.ts-display{text-align:center;margin-bottom:24rpx}.ts-wpm{font-size:80rpx;font-weight:700;color:#6c5ce7;display:block}.ts-label{font-size:24rpx;color:#999}.ts-target{background:#fff;border-radius:16rpx;padding:24rpx;font-size:28rpx;color:#666;margin-bottom:24rpx;line-height:1.6}.ts-input{width:100%;height:80rpx;background:#fff;border-radius:16rpx;padding:0 24rpx;font-size:28rpx;box-sizing:border-box;margin-bottom:24rpx}.ts-stats{display:flex;justify-content:space-between;font-size:26rpx;color:#666}</style>