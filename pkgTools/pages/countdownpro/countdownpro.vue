<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u5012\u8ba1\u65f6\u96c6\u5408</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="add-btn" @click="showAdd=true">+ \u6dfb\u52a0\u5012\u8ba1\u65f6</view>
      <view class="countdown-list">
        <view class="cd-card" v-for="(c, i) in countdowns" :key="i">
          <text class="cd-name">{{ c.name }}</text>
          <text class="cd-date">{{ c.date }}</text>
          <text class="cd-days">{{ getDays(c.date) }} \u5929</text>
        </view>
      </view>
      <view class="preset-card">
        <text class="preset-title">\u5feb\u901f\u6dfb\u52a0</text>
        <view class="preset-grid">
          <text class="preset-item" @click="addPreset('\u5143\u65e6','2025-01-01')">\u5143\u65e6</text>
          <text class="preset-item" @click="addPreset('\u6625\u8282','2025-01-29')">\u6625\u8282</text>
          <text class="preset-item" @click="addPreset('\u590d\u6d88','2025-02-14')">\u590d\u6d88</text>
          <text class="preset-item" @click="addPreset('\u56db\u516d','2025-04-06')">\u56db\u516d</text>
          <text class="preset-item" @click="addPreset('\u52b3\u52a8','2025-05-01')">\u52b3\u52a8</text>
          <text class="preset-item" @click="addPreset('\u56fd\u5e86','2025-10-01')">\u56fd\u5e86</text>
        </view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const countdowns = ref([
  {name:"\u5143\u65e6", date:"2025-01-01"},
  {name:"\u6625\u8282", date:"2025-01-29"},
  {name:"\u590d\u6d88", date:"2025-02-14"}
])
const showAdd = ref(false)
function getDays(date) {
  var d = new Date(date) - new Date()
  return Math.max(0, Math.ceil(d / 86400000))
}
function addPreset(name, date) {
  if (!countdowns.value.find(function(c){return c.name===name})) {
    countdowns.value.push({name:name, date:date})
  }
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #f6d365, #fda085); }
.custom-nav { background: linear-gradient(135deg, #f39c12, #e17055); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.add-btn { background: linear-gradient(135deg, #f39c12, #e17055); border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 24rpx; color: #fff; font-size: 28rpx; font-weight: 600; }
.countdown-list { display: flex; flex-direction: column; gap: 16rpx; margin-bottom: 24rpx; }
.cd-card { background: #fff; border-radius: 20rpx; padding: 24rpx; display: flex; justify-content: space-between; align-items: center; }
.cd-name { font-size: 28rpx; font-weight: 600; color: #333; }
.cd-date { font-size: 24rpx; color: #999; }
.cd-days { font-size: 32rpx; font-weight: 700; color: #f39c12; }
.preset-card { background: rgba(255,255,255,0.3); border-radius: 20rpx; padding: 20rpx; }
.preset-title { font-size: 24rpx; color: #fff; display: block; margin-bottom: 12rpx; }
.preset-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12rpx; }
.preset-item { background: rgba(255,255,255,0.3); border-radius: 12rpx; padding: 16rpx; text-align: center; color: #fff; font-size: 24rpx; }
</style>
