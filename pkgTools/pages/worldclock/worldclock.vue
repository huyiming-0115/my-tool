<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">世界时钟</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="clock-list">
        <view class="clock-item" v-for="(c, idx) in cities" :key="idx">
          <text class="clock-city">{{ c.name }}</text>
          <text class="clock-time">{{ c.time }}</text>
          <text class="clock-date">{{ c.date }}</text>
        </view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const cities = ref([])
function update() {
  const offsets = [0, 1, -5, 9, -8, 5.5, -3, 8]
  const names = ["北京", "东京", "纽约", "伦敦", "梵蒂冈", "孟买", "巴黎", "惠灵顿"]
  const now = new Date()
  cities.value = names.map((n, i) => {
    const d = new Date(now.getTime() + (offsets[i] - 8 + now.getTimezoneOffset() / 60) * 3600000)
    return { name: n, time: d.toTimeString().slice(0, 8), date: d.toISOString().slice(0, 10) }
  })
}
update()
setInterval(update, 1000)
function goBack() { uni.navigateBack() }
onMounted(() => { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #6c5ce7, #a29bfe); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.clock-list { display: flex; flex-direction: column; gap: 16rpx; }
.clock-item { background: #fff; border-radius: 20rpx; padding: 24rpx; display: flex; align-items: center; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.clock-city { font-size: 28rpx; font-weight: 600; color: #333; width: 160rpx; }
.clock-time { flex: 1; font-size: 40rpx; font-weight: 700; color: #6c5ce7; text-align: center; font-family: monospace; }
.clock-date { font-size: 22rpx; color: #999; text-align: right; }
</style>
