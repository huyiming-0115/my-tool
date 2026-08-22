<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">万年历</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="cal-header"><text class="cal-nav" @click="prevMonth">◀</text><text class="cal-title">{{ year }}年{{ month + 1 }}月</text><text class="cal-nav" @click="nextMonth">▶</text></view>
      <view class="cal-week"><text class="cal-day-name" v-for="d in weekDays" :key="d">{{ d }}</text></view>
      <view class="cal-grid"><text class="cal-day" v-for="(d, idx) in days" :key="idx" :class="{ today: d.today, other: !d.current }">{{ d.num }}</text></view>
      <view class="cal-info"><text>今天：{{ todayStr }}</text><text>星期{{ weekday }}</text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const year = ref(new Date().getFullYear())
const month = ref(new Date().getMonth())
const days = ref([])
const weekDays = ["日", "一", "二", "三", "四", "五", "六"]
const todayStr = ref(new Date().toLocaleDateString())
const weekday = ref(["日", "一", "二", "三", "四", "五", "六"][new Date().getDay()])
function render() {
  const first = new Date(year.value, month.value, 1)
  const last = new Date(year.value, month.value + 1, 0)
  const today = new Date()
  const arr = []
  for (let i = 0; i < first.getDay(); i++) arr.push({ num: "", current: false })
  for (let i = 1; i <= last.getDate(); i++) {
    arr.push({ num: i, current: true, today: today.getDate() === i && today.getMonth() === month.value && today.getFullYear() === year.value })
  }
  days.value = arr
}
function prevMonth() { month.value--; if (month.value < 0) { month.value = 11; year.value-- } render() }
function nextMonth() { month.value++; if (month.value > 11) { month.value = 0; year.value++ } render() }
render()
function goBack() { uni.navigateBack() }
onMounted(() => { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #e17055, #fab1a0); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.cal-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 24rpx; }
.cal-title { font-size: 32rpx; font-weight: 700; color: #333; }
.cal-nav { font-size: 36rpx; color: #e17055; padding: 8rpx 16rpx; }
.cal-week { display: flex; }
.cal-day-name { flex: 1; text-align: center; font-size: 24rpx; color: #999; padding: 12rpx 0; }
.cal-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 4rpx; }
.cal-day { text-align: center; padding: 16rpx 0; font-size: 28rpx; border-radius: 12rpx; }
.cal-day.today { background: #e17055; color: #fff; font-weight: 700; }
.cal-day.other { color: #ccc; }
.cal-info { background: #fff; border-radius: 20rpx; padding: 24rpx; margin-top: 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.cal-info text { font-size: 26rpx; color: #666; display: block; }
</style>
