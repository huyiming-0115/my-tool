<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">分贝计</text><text class="nav-icon" @click="toggle">{{ monitoring ? "⏸" : "⏵" }}</text></view>
    </view>
    <view class="content">
      <view class="db-display"><text class="db-value">{{ db }}</text><text class="db-unit">dB</text></view>
      <view class="db-bar"><view class="db-fill" :style="{ width: Math.min(100, db) + '%', background: dbColor }"></view></view>
      <view class="db-level">{{ dbLevel }}</view>
      <view class="db-btn" @click="toggle"><text>{{ monitoring ? "停止" : "开始测量" }}</text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, computed, onUnmounted, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const db = ref(30)
const monitoring = ref(false)
var timer = null
var Context = null
const dbColor = computed(function() { return db.value < 60 ? "#00b894" : db.value < 80 ? "#fdcb6e" : "#e17055" })
const dbLevel = computed(function() { return db.value < 40 ? "安静" : db.value < 60 ? "正常" : db.value < 80 ? "噪音" : "很哙" })
function toggle() {
  if (monitoring.value) { clearInterval(timer); monitoring.value = false; db.value = 30 }
  else {
    monitoring.value = true
    timer = setInterval(function() { db.value = Math.floor(30 + Math.random() * 70) }, 500)
  }
}
onUnmounted(function() { clearInterval(timer) })
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #6c5ce7, #a29bfe); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 44rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; display: flex; flex-direction: column; align-items: center; }
.db-display { text-align: center; margin-bottom: 32rpx; }
.db-value { font-size: 96rpx; font-weight: 700; color: #6c5ce7; }
.db-unit { font-size: 32rpx; color: #999; margin-left: 8rpx; }
.db-bar { width: 100%; height: 40rpx; background: #eee; border-radius: 20rpx; overflow: hidden; margin-bottom: 24rpx; }
.db-fill { height: 100%; border-radius: 20rpx; transition: width 0.3s, background 0.3s; }
.db-level { font-size: 32rpx; color: #333; font-weight: 600; margin-bottom: 32rpx; }
.db-btn { width: 80%; background: linear-gradient(135deg, #6c5ce7, #a29bfe); border-radius: 16rpx; padding: 28rpx; text-align: center; }
.db-btn text { font-size: 32rpx; color: #fff; font-weight: 600; }
</style>