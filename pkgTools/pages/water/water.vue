<template>
  <view class="water-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">←</text>
        <text class="nav-title">喝水记录</text>
        <text class="nav-icon" @click="openSettings">⚙</text>
      </view>
    </view>
    <view class="content">
      <view class="progress-card">
        <view class="progress-ring">
          <view class="ring-bg"></view>
          <view class="ring-fill" :style="{ transform: 'rotate(' + (progress * 3.6 - 90) + 'deg)' }"></view>
          <view class="ring-center">
            <text class="ring-pct">{{ Math.round(progress) }}%</text>
            <text class="ring-ml">{{ todayAmount }}ml</text>
          </view>
        </view>
        <text class="target-text">目标: {{ target }}ml</text>
      </view>
      <view class="add-section">
        <view class="add-grid">
          <view class="add-btn" @click="addWater(250)">
            <text class="add-ml">+250ml</text>
            <text class="add-icon">🚰</text>
          </view>
          <view class="add-btn" @click="addWater(500)">
            <text class="add-ml">+500ml</text>
            <text class="add-icon">🥤</text>
          </view>
        </view>
      </view>
      <view class="section-title">本周趋势</view>
      <view class="trend-card">
        <view class="trend-chart">
          <view class="chart-bar" v-for="(day, idx) in weekData" :key="idx">
            <view class="bar-fill" :style="{ height: getBarHeight(day.amount) + '%' }"></view>
            <text class="bar-label">{{ day.label }}</text>
          </view>
        </view>
      </view>
      <view class="section-title">今日记录</view>
      <view class="record-list">
        <view class="record-item" v-for="(r, idx) in todayRecords" :key="idx">
          <text class="record-time">{{ r.time }}</text>
          <text class="record-amount">{{ r.amount }}ml</text>
        </view>
      </view>
      <view class="empty-mini" v-if="todayRecords.length === 0">
        <text>还没有记录，快来喝水吧</text>
      </view>
    </view>
    <view v-if="showSettings" class="mask" @click="showSettings = false">
      <view class="create-panel" @click.stop>
        <view class="panel-head">
          <text class="panel-title">目标设置</text>
          <text class="panel-close" @click="showSettings = false">×</text>
        </view>
        <view class="panel-body">
          <view class="form-row">
            <text class="form-l">每日目标 (ml)</text>
            <input class="form-input" v-model="targetInput" type="number" placeholder="2000" />
          </view>
        </view>
        <view class="panel-footer">
          <button class="btn-cancel" @click="showSettings = false">取消</button>
          <button class="btn-save" @click="saveTarget">保存</button>
        </view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, computed, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const records = ref([])
const target = ref(2000)
const targetInput = ref(2000)
const showSettings = ref(false)
const todayAmount = computed(() => {
  const today = new Date().toISOString().slice(0, 10)
  return records.value.filter(r => r.date === today).reduce((s, r) => s + r.amount, 0)
})
const progress = computed(() => Math.min(100, (todayAmount.value / target.value) * 100))
const todayRecords = computed(() => {
  const today = new Date().toISOString().slice(0, 10)
  return records.value.filter(r => r.date === today).reverse()
})
const weekData = computed(() => {
  const days = ["日", "一", "二", "三", "四", "五", "六"]
  const result = []
  const today = new Date()
  for (let i = 6; i >= 0; i--) {
    const d = new Date(today)
    d.setDate(d.getDate() - i)
    const dateStr = d.toISOString().slice(0, 10)
    const amount = records.value.filter(r => r.date === dateStr).reduce((s, r) => s + r.amount, 0)
    result.push({ label: days[d.getDay()], amount })
  }
  return result
})
function getBarHeight(amount) {
  const max = Math.max(...weekData.value.map(d => d.amount), target.value)
  return max > 0 ? (amount / max) * 100 : 5
}
function goBack() { uni.navigateBack() }
function openSettings() { targetInput.value = target.value; showSettings.value = true }
function saveTarget() {
  target.value = parseInt(targetInput.value) || 2000
  saveData()
  showSettings.value = false
}
function addWater(ml) {
  const now = new Date()
  records.value.push({
    date: now.toISOString().slice(0, 10),
    time: now.getHours() + ":" + String(now.getMinutes()).padStart(2, "0"),
    amount: ml
  })
  saveData()
}
function saveData() { uni.setStorageSync("water_records", JSON.stringify(records.value)); uni.setStorageSync("water_target", target.value) }
onMounted(() => {
  if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }
  const saved = uni.getStorageSync("water_records")
  if (saved) { try { records.value = JSON.parse(saved) } catch (e) {} }
  const t = uni.getStorageSync("water_target")
  if (t) target.value = t
})
</script>
<style lang="scss" scoped>
.water-page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #06b6d4, #0891b2); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 40rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.progress-card { background: #fff; border-radius: 24rpx; padding: 40rpx; text-align: center; margin-bottom: 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.progress-ring { width: 240rpx; height: 240rpx; margin: 0 auto; position: relative; }
.ring-bg { position: absolute; inset: 0; border-radius: 50%; border: 16rpx solid #e0f2fe; }
.ring-fill { position: absolute; inset: 0; border-radius: 50%; border: 16rpx solid transparent; border-top-color: #06b6d4; border-right-color: #06b6d4; transition: transform 0.5s; }
.ring-center { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; }
.ring-pct { font-size: 48rpx; font-weight: 700; color: #06b6d4; }
.ring-ml { font-size: 22rpx; color: #999; }
.target-text { font-size: 24rpx; color: #666; margin-top: 20rpx; display: block; }
.add-section { margin-bottom: 24rpx; }
.add-grid { display: flex; gap: 16rpx; }
.add-btn { flex: 1; background: #fff; border-radius: 20rpx; padding: 28rpx; text-align: center; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.add-ml { font-size: 28rpx; font-weight: 600; color: #06b6d4; display: block; }
.add-icon { font-size: 40rpx; margin-top: 8rpx; display: block; }
.section-title { font-size: 28rpx; font-weight: 600; color: #333; margin: 24rpx 0 16rpx; }
.trend-card { background: #fff; border-radius: 24rpx; padding: 28rpx; margin-bottom: 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.trend-chart { display: flex; align-items: flex-end; justify-content: space-between; height: 200rpx; }
.chart-bar { flex: 1; display: flex; flex-direction: column; align-items: center; height: 100%; justify-content: flex-end; }
.bar-fill { width: 32rpx; background: linear-gradient(to top, #06b6d4, #67e8f9); border-radius: 8rpx 8rpx 0 0; min-height: 10rpx; }
.bar-label { font-size: 20rpx; color: #999; margin-top: 8rpx; }
.record-list { background: #fff; border-radius: 24rpx; padding: 8rpx 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.record-item { display: flex; justify-content: space-between; padding: 20rpx 0; border-bottom: 2rpx solid #f9f9f9; }
.record-time { font-size: 24rpx; color: #666; }
.record-amount { font-size: 24rpx; color: #06b6d4; font-weight: 600; }
.empty-mini { text-align: center; padding: 32rpx; font-size: 24rpx; color: #999; }
.mask { position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 999; display: flex; align-items: flex-end; }
.create-panel { width: 100%; background: #fff; border-radius: 32rpx 32rpx 0 0; max-height: 60vh; display: flex; flex-direction: column; }
.panel-head { display: flex; justify-content: space-between; align-items: center; padding: 28rpx 32rpx; border-bottom: 2rpx solid #f0f0f0; }
.panel-title { font-size: 30rpx; font-weight: 600; color: #1a1a1a; }
.panel-close { font-size: 40rpx; color: #999; padding: 4rpx 8rpx; }
.panel-body { flex: 1; padding: 12rpx 32rpx; overflow-y: auto; }
.form-row { display: flex; align-items: center; padding: 20rpx 0; border-bottom: 2rpx solid #f8f8f8; }
.form-l { font-size: 26rpx; color: #333; width: 200rpx; flex-shrink: 0; font-weight: 500; }
.form-input { flex: 1; font-size: 28rpx; color: #333; height: 56rpx; }
.panel-footer { display: flex; gap: 24rpx; padding: 24rpx 32rpx; border-top: 2rpx solid #f0f0f0; }
.btn-cancel { flex: 1; height: 80rpx; line-height: 80rpx; border-radius: 40rpx; background: #f5f5f5; color: #666; font-size: 28rpx; border: none; }
.btn-cancel::after { border: none; }
.btn-save { flex: 1; height: 80rpx; line-height: 80rpx; border-radius: 40rpx; background: linear-gradient(135deg, #06b6d4, #0891b2); color: #fff; font-size: 28rpx; font-weight: 600; border: none; }
.btn-save::after { border: none; }
</style>
