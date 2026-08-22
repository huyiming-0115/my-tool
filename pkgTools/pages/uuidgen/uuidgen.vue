<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">UUID 生成</text><text class="nav-icon" @click="generate">✅</text></view>
    </view>
    <view class="content">
      <view class="uuid-display"><text class="uuid-text">{{ uuid }}</text></view>
      <view class="uuid-btn" @click="generate"><text>生成 UUID</text></view>
      <view class="uuid-list">
        <view class="uuid-item" v-for="(u, idx) in history" :key="idx" @click="copy(u)">
          <text class="uuid-str">{{ u }}</text>
        </view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const uuid = ref("")
const history = ref([])
function generate() {
  var u = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    var r = Math.random() * 16 | 0, v = c === 'x' ? r : (r & 0x3 | 0x8)
    return v.toString(16)
  })
  uuid.value = u
  history.value.unshift(u)
  if (history.value.length > 10) history.value.pop()
}
function copy(v) { uni.setClipboardData({ data: v, success: function() { uni.showToast({ title: "已复制", icon: "success" }) } }) }
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #636e72, #b2bec3); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 44rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.uuid-display { background: #fff; border-radius: 20rpx; padding: 32rpx; margin-bottom: 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.uuid-text { font-size: 28rpx; color: #2d3436; font-family: monospace; word-break: break-all; }
.uuid-btn { background: linear-gradient(135deg, #636e72, #b2bec3); border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 24rpx; }
.uuid-btn text { font-size: 30rpx; color: #fff; font-weight: 600; }
.uuid-list { background: #fff; border-radius: 20rpx; padding: 16rpx; }
.uuid-item { padding: 16rpx; border-bottom: 2rpx solid #f8f8f8; }
.uuid-str { font-size: 24rpx; color: #666; font-family: monospace; }
</style>