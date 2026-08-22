<template>
  <view class="sleep-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">←</text>
        <text class="nav-title">睡眠记录</text>
        <text class="nav-icon" @click="openAdd">+</text>
      </view>
    </view>
    <view class="content">
      <view class="sleep-card">
        <text class="sleep-hours">{{ lastSleepHours }}</text>
        <text class="sleep-label">昨晚睡眠时长</text>
        <view class="quality-stars">
          <text class="star" v-for="i in 5" :key="i" :class="{ active: i <= lastQuality }">★</text>
        </view>
      </view>
      <view class="section-title">本周睡眠</view>
      <view class="week-chart">
        <view class="w-bar" v-for="(d, idx) in weekData" :key="idx">
          <view class="w-fill" :style="{ height: (d.hours / 10) * 100 + '%' }"></view>
          <text class="w-label">{{ d.label }}</text>
          <text class="w-hours">{{ d.hours }}h</text>
        </view>
      </view>
      <view class="section-title">记录历史</view>
      <view class="record-list">
        <view class="record-item" v-for="(r, idx) in records" :key="idx">
          <text class="r-date">{{ r.date }}</text>
          <text class="r-time">{{ r.bedtime }} - {{ r.wakeup }}</text>
          <text class="r-hours">{{ r.hours }}h</text>
        </view>
      </view>
      <view class="empty-mini" v-if="records.length === 0"><text>暂无记录</text></view>
    </view>
    <view v-if="showAdd" class="mask" @click="showAdd = false">
      <view class="create-panel" @click.stop>
        <view class="panel-head"><text class="panel-title">记录睡眠</text><text class="panel-close" @click="showAdd = false">×</text></view>
        <view class="panel-body">
          <view class="form-row"><text class="form-l">入睡时间</text><picker class="form-picker" mode="time" v-model="newRecord.bedtime" @change="onBedChange"><text>{{ newRecord.bedtime }}</text></picker></view>
          <view class="form-row"><text class="form-l">起床时间</text><picker class="form-picker" mode="time" v-model="newRecord.wakeup" @change="onWakeChange"><text>{{ newRecord.wakeup }}</text></picker></view>
          <view class="form-row"><text class="form-l">质量评分</text><view class="quality-pick"><text class="q-star" v-for="i in 5" :key="i" @click="newRecord.quality = i" :class="{ active: i <= newRecord.quality }">★</text></view></view>
        </view>
        <view class="panel-footer"><button class="btn-cancel" @click="showAdd = false">取消</button><button class="btn-save" @click="addRecord">保存</button></view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, computed, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const records = ref([])
const showAdd = ref(false)
const newRecord = ref({ bedtime: "23:00", wakeup: "07:00", quality: 4 })
const lastSleepHours = computed(() => { if (!records.value.length) return "--"; return records.value[0].hours + "h" })
const lastQuality = computed(() => { if (!records.value.length) return 0; return records.value[0].quality })
const weekData = computed(() => {
  const days = ["日", "一", "二", "三", "四", "五", "六"]
  const result = []; const today = new Date()
  for (let i = 6; i >= 0; i--) {
    const d = new Date(today); d.setDate(d.getDate() - i)
    const dateStr = d.toISOString().slice(0, 10)
    const r = records.value.find(r => r.date === dateStr)
    result.push({ label: days[d.getDay()], hours: r ? r.hours : 0 })
  }
  return result
})
function goBack() { uni.navigateBack() }
function openAdd() { newRecord.value = { bedtime: "23:00", wakeup: "07:00", quality: 4 }; showAdd.value = true }
function onBedChange(e) { newRecord.value.bedtime = e.detail.value }
function onWakeChange(e) { newRecord.value.wakeup = e.detail.value }
function addRecord() {
  const [bh, bm] = newRecord.value.bedtime.split(":").map(Number)
  const [wh, wm] = newRecord.value.wakeup.split(":").map(Number)
  let hours = (wh * 60 + wm - bh * 60 - bm) / 60
  if (hours < 0) hours += 24
  records.value.unshift({ date: new Date().toISOString().slice(0, 10), bedtime: newRecord.value.bedtime, wakeup: newRecord.value.wakeup, hours: hours.toFixed(1), quality: newRecord.value.quality })
  saveData(); showAdd.value = false
}
function saveData() { uni.setStorageSync("sleep_records", JSON.stringify(records.value)) }
onMounted(() => {
  if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }
  const saved = uni.getStorageSync("sleep_records"); if (saved) { try { records.value = JSON.parse(saved) } catch (e) {} }
})
</script>
<style lang="scss" scoped>
.sleep-page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #6366f1, #4f46e5); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.sleep-card { background: linear-gradient(135deg, #6366f1, #4f46e5); border-radius: 24rpx; padding: 40rpx; text-align: center; margin-bottom: 24rpx; }
.sleep-hours { font-size: 64rpx; color: #fff; font-weight: 700; display: block; }
.sleep-label { font-size: 24rpx; color: rgba(255,255,255,0.7); margin-top: 8rpx; display: block; }
.quality-stars { margin-top: 16rpx; }
.star { font-size: 36rpx; color: rgba(255,255,255,0.3); margin: 0 4rpx; }
.star.active { color: #fbbf24; }
.section-title { font-size: 28rpx; font-weight: 600; color: #333; margin: 24rpx 0 16rpx; }
.week-chart { display: flex; align-items: flex-end; justify-content: space-between; background: #fff; border-radius: 24rpx; padding: 28rpx 16rpx; height: 240rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); margin-bottom: 24rpx; }
.w-bar { flex: 1; display: flex; flex-direction: column; align-items: center; height: 100%; justify-content: flex-end; }
.w-fill { width: 32rpx; background: linear-gradient(to top, #6366f1, #a5b4fc); border-radius: 8rpx 8rpx 0 0; min-height: 10rpx; }
.w-label { font-size: 20rpx; color: #999; margin-top: 8rpx; }
.w-hours { font-size: 18rpx; color: #666; margin-top: 2rpx; }
.record-list { background: #fff; border-radius: 24rpx; padding: 8rpx 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.record-item { display: flex; align-items: center; padding: 20rpx 0; border-bottom: 2rpx solid #f9f9f9; }
.r-date { font-size: 24rpx; color: #333; font-weight: 600; width: 140rpx; }
.r-time { flex: 1; font-size: 22rpx; color: #666; }
.r-hours { font-size: 24rpx; color: #6366f1; font-weight: 600; }
.empty-mini { text-align: center; padding: 32rpx; font-size: 24rpx; color: #999; }
.mask { position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 999; display: flex; align-items: flex-end; }
.create-panel { width: 100%; background: #fff; border-radius: 32rpx 32rpx 0 0; max-height: 60vh; display: flex; flex-direction: column; }
.panel-head { display: flex; justify-content: space-between; align-items: center; padding: 28rpx 32rpx; border-bottom: 2rpx solid #f0f0f0; }
.panel-title { font-size: 30rpx; font-weight: 600; color: #1a1a1a; }
.panel-close { font-size: 40rpx; color: #999; padding: 4rpx 8rpx; }
.panel-body { flex: 1; padding: 12rpx 32rpx; overflow-y: auto; }
.form-row { display: flex; align-items: center; padding: 20rpx 0; border-bottom: 2rpx solid #f8f8f8; }
.form-l { font-size: 26rpx; color: #333; width: 160rpx; flex-shrink: 0; font-weight: 500; }
.form-picker { flex: 1; height: 56rpx; line-height: 56rpx; font-size: 26rpx; }
.quality-pick { flex: 1; }
.q-star { font-size: 40rpx; color: #ddd; margin-right: 8rpx; }
.q-star.active { color: #fbbf24; }
.panel-footer { display: flex; gap: 24rpx; padding: 24rpx 32rpx; border-top: 2rpx solid #f0f0f0; }
.btn-cancel { flex: 1; height: 80rpx; line-height: 80rpx; border-radius: 40rpx; background: #f5f5f5; color: #666; font-size: 28rpx; border: none; }
.btn-cancel::after { border: none; }
.btn-save { flex: 1; height: 80rpx; line-height: 80rpx; border-radius: 40rpx; background: linear-gradient(135deg, #6366f1, #4f46e5); color: #fff; font-size: 28rpx; font-weight: 600; border: none; }
.btn-save::after { border: none; }
</style>
