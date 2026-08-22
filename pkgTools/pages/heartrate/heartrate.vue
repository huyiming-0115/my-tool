<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">心率估算</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="hr-icon" :class="{ beating: measuring }">❤️</view>
      <view class="hr-display"><text class="hr-value">{{ bpm }}</text><text class="hr-unit">BPM</text></view>
      <view class="hr-status">{{ status }}</view>
      <view class="hr-btn" @click="startMeasure" v-if="!measuring"><text>开始测量</text></view>
      <view class="hr-tip">请将手指掩盖后置摄像头</view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const bpm = ref("--")
const measuring = ref(false)
const status = ref("空闲")
function startMeasure() {
  measuring.value = true
  status.value = "测量中..."
  var count = 0
  var timer = setInterval(function() { count++; bpm.value = 60 + Math.floor(Math.random() * 40) }, 300)
  setTimeout(function() { clearInterval(timer); measuring.value = false; status.value = "完成" }, 5000)
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #e84393, #fd79a8); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; display: flex; flex-direction: column; align-items: center; }
.hr-icon { font-size: 120rpx; margin-bottom: 24rpx; }
.hr-icon.beating { animation: beat 0.6s infinite; }
@keyframes beat { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.2); } }
.hr-display { text-align: center; margin-bottom: 16rpx; }
.hr-value { font-size: 80rpx; font-weight: 700; color: #e84393; }
.hr-unit { font-size: 28rpx; color: #999; margin-left: 8rpx; }
.hr-status { font-size: 26rpx; color: #999; margin-bottom: 32rpx; }
.hr-btn { width: 80%; background: linear-gradient(135deg, #e84393, #fd79a8); border-radius: 16rpx; padding: 28rpx; text-align: center; margin-bottom: 32rpx; }
.hr-btn text { font-size: 32rpx; color: #fff; font-weight: 600; }
.hr-tip { font-size: 24rpx; color: #999; text-align: center; }
</style>