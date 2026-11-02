<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u751f\u7406\u671f\u8bb0\u5f55</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="status-card">
        <text {{ daysUntil }} \u5929</text>
        <text class="status-label">{{ statusText }}</text>
      </view>
      <view class="form-card"><text class="form-label">\u5468\u671f\u5929\u6570</text><input class="form-input" type="number" v-model="cycleLen" /></view>
      <view class="form-card"><text class="form-label">\u6700\u540e\u4e00\u6b21\u6765\u65e5</text><input class="form-input" type="date" v-model="lastDate" /></view>
      <view class="form-card"><text class="form-label">\u6301\u7eed\u5929\u6570</text><input class="form-input" type="number" v-model="duration" /></view>
      <view class="calc-btn" @click="save"><text>\u4fdd\u5b58\u8bb0\u5f55</text></view>
      <view class="history-card" v-if="history.length > 0">
        <text class="hist-title">\u5386\u53f2\u8bb0\u5f55</text>
        <view class="hist-item" v-for="(h, i) in history.slice(0,6)" :key="i">
          <text>{{ h.date }}</text>
          <text>{{ h.duration }}\u5929</text>
          <text>{{ h.cycle }}\u5929\u5468\u671f</text>
        </view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const cycleLen = ref(28)
const lastDate = ref("")
const duration = ref(5)
const daysUntil = ref("?")
const statusText = ref("\u8bbe\u7f6e\u540e\u67e5\u770b")
const history = ref([])
function save() {
  if (!lastDate.value) { uni.showToast({ title: "\u8bf7\u586b\u5199\u65e5\u671f", icon: "none" }); return }
  const last = new Date(lastDate.value)
  const next = new Date(last.getTime() + cycleLen.value * 86400000)
  const now = new Date()
  const diff = Math.ceil((next - now) / 86400000)
  daysUntil.value = diff
  if (diff > 5) statusText.value = "\u5b89\u5168\u671f"
  else if (diff > 0) statusText.value = "\u63a5\u8fd1\u671f"
  else if (diff >= -duration.value) statusText.value = "\u751f\u7406\u671f"
  else statusText.value = "\u5ef6\u8fdf"
  history.value.unshift({ date: lastDate.value, duration: duration.value, cycle: cycleLen.value })
  if (history.value.length > 12) history.value.pop()
}
function goBack() { uni.navigateBack() }
onMounted(function() {
  if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }
  const saved = uni.getStorageSync("period_history")
  if (saved) history.value = saved
})
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #ffecd2, #fcb69f); }
.custom-nav { background: linear-gradient(135deg, #e84393, #fd79a8); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.status-card { background: #fff; border-radius: 24rpx; padding: 40rpx; text-align: center; margin-bottom: 24rpx; }
.status-days { font-size: 80rpx; font-weight: 700; color: #e84393; display: block; }
.status-label { font-size: 26rpx; color: #999; display: block; margin-top: 8rpx; }
.form-card { background: #fff; border-radius: 20rpx; padding: 24rpx; margin-bottom: 20rpx; }
.form-label { font-size: 26rpx; color: #666; display: block; margin-bottom: 12rpx; }
.form-input { font-size: 32rpx; color: #333; font-weight: 600; }
.calc-btn { background: linear-gradient(135deg, #e84393, #fd79a8); border-radius: 16rpx; padding: 24rpx; text-align: center; margin: 32rpx 0; }
.calc-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.history-card { background: #fff; border-radius: 24rpx; padding: 24rpx; }
.hist-title { font-size: 28rpx; font-weight: 600; color: #333; display: block; margin-bottom: 16rpx; }
.hist-item { display: flex; justify-content: space-between; padding: 12rpx 0; border-bottom: 2rpx solid #f0f0f0; font-size: 24rpx; color: #666; }
</style>
