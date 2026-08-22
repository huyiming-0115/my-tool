<template>
  <view class="period-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">←</text>
        <text class="nav-title">生理期记录</text>
        <text class="nav-icon" @click="openSettings">⚙</text>
      </view>
    </view>
    <view class="content">
      <view class="cycle-card">
        <view class="cycle-info">
          <text class="cycle-day">{{ currentCycleDay }}</text>
          <text class="cycle-label">当前周期天数</text>
        </view>
        <view class="next-predict">
          <text class="predict-label">预测下次</text>
          <text class="predict-date">{{ nextPeriodDate }}</text>
        </view>
      </view>
      <view class="section-title">疲力日</view>
      <view class="symptom-grid">
        <view class="sym-btn" v-for="s in symptoms" :key="s" :class="{ active: selectedSymptoms.includes(s) }" @click="toggleSymptom(s)">{{ s }}</view>
      </view>
      <view class="action-btn" @click="togglePeriod">
        <text v-if="!isPerioding" class="action-text">▶ 开始生理期</text>
        <text v-else class="action-text stop">■ 结束生理期</text>
      </view>
      <view class="section-title">历史记录</view>
      <view class="record-list">
        <view class="record-item" v-for="(r, idx) in records" :key="idx">
          <text class="r-date">{{ r.startDate }} ~ {{ r.endDate || "至今" }}</text>
          <text class="r-days">{{ r.days }}天</text>
        </view>
      </view>
      <view class="empty-mini" v-if="records.length === 0"><text>暂无记录</text></view>
    </view>
    <view v-if="showSettings" class="mask" @click="showSettings = false">
      <view class="create-panel" @click.stop>
        <view class="panel-head"><text class="panel-title">设置</text><text class="panel-close" @click="showSettings = false">×</text></view>
        <view class="panel-body">
          <view class="form-row"><text class="form-l">周期天数</text><input class="form-input" v-model="cycleLength" type="number" placeholder="28" /></view>
        </view>
        <view class="panel-footer"><button class="btn-cancel" @click="showSettings = false">取消</button><button class="btn-save" @click="saveSettings">保存</button></view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, computed, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const records = ref([])
const symptoms = ["腹痛", "头痛", "疲制", "情绪波动", "晕厥", "喉咽痛"]
const selectedSymptoms = ref([])
const cycleLength = ref(28)
const isPerioding = ref(false)
const showSettings = ref(false)
const currentPeriod = ref(null)
const currentCycleDay = computed(() => {
  if (!currentPeriod.value) return 0
  const start = new Date(currentPeriod.value.startDate)
  return Math.floor((new Date() - start) / (1000 * 60 * 60 * 24)) + 1
})
const nextPeriodDate = computed(() => {
  if (!records.value.length) return "暂无数据"
  const last = records.value[0]
  const d = new Date(last.startDate)
  d.setDate(d.getDate() + parseInt(cycleLength.value) || 28)
  return d.toISOString().slice(0, 10)
})
function goBack() { uni.navigateBack() }
function openSettings() { cycleLength.value = parseInt(cycleLength.value) || 28; showSettings.value = true }
function saveSettings() { saveData(); showSettings.value = false }
function toggleSymptom(s) {
  const idx = selectedSymptoms.value.indexOf(s)
  if (idx >= 0) selectedSymptoms.value.splice(idx, 1)
  else selectedSymptoms.value.push(s)
}
function togglePeriod() {
  if (isPerioding.value) {
    if (currentPeriod.value) {
      currentPeriod.value.endDate = new Date().toISOString().slice(0, 10)
      currentPeriod.value.days = currentCycleDay.value
      records.value.unshift({ ...currentPeriod.value })
    }
    isPerioding.value = false; currentPeriod.value = null
  } else {
    isPerioding.value = true
    currentPeriod.value = { startDate: new Date().toISOString().slice(0, 10), endDate: null, days: 0, symptoms: [...selectedSymptoms.value] }
  }
  saveData()
}
function saveData() { uni.setStorageSync("period_records", JSON.stringify(records.value)); uni.setStorageSync("period_cycle", cycleLength.value) }
onMounted(() => {
  if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }
  const saved = uni.getStorageSync("period_records"); if (saved) { try { records.value = JSON.parse(saved) } catch (e) {} }
  const c = uni.getStorageSync("period_cycle"); if (c) cycleLength.value = c
  if (records.value.length && !records.value[0].endDate) { isPerioding.value = true; currentPeriod.value = records.value[0] }
})
</script>
<style lang="scss" scoped>
.period-page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #f43f5e, #e11d48); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 40rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.cycle-card { background: linear-gradient(135deg, #f43f5e, #e11d48); border-radius: 24rpx; padding: 32rpx; display: flex; justify-content: space-between; align-items: center; margin-bottom: 24rpx; }
.cycle-day { font-size: 56rpx; color: #fff; font-weight: 700; display: block; }
.cycle-label { font-size: 22rpx; color: rgba(255,255,255,0.7); }
.next-predict { text-align: right; }
.predict-label { font-size: 22rpx; color: rgba(255,255,255,0.7); display: block; }
.predict-date { font-size: 28rpx; color: #fff; font-weight: 600; margin-top: 4rpx; display: block; }
.section-title { font-size: 28rpx; font-weight: 600; color: #333; margin: 24rpx 0 16rpx; }
.symptom-grid { display: flex; flex-wrap: wrap; gap: 12rpx; margin-bottom: 24rpx; }
.sym-btn { padding: 12rpx 24rpx; background: #fff; border-radius: 30rpx; font-size: 24rpx; color: #666; }
.sym-btn.active { background: #f43f5e; color: #fff; }
.action-btn { background: #fff; border-radius: 24rpx; padding: 28rpx; text-align: center; margin-bottom: 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.action-text { font-size: 28rpx; font-weight: 600; color: #f43f5e; }
.action-text.stop { color: #999; }
.record-list { background: #fff; border-radius: 24rpx; padding: 8rpx 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.record-item { display: flex; justify-content: space-between; padding: 20rpx 0; border-bottom: 2rpx solid #f9f9f9; }
.r-date { font-size: 24rpx; color: #333; }
.r-days { font-size: 24rpx; color: #f43f5e; font-weight: 600; }
.empty-mini { text-align: center; padding: 32rpx; font-size: 24rpx; color: #999; }
.mask { position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 999; display: flex; align-items: flex-end; }
.create-panel { width: 100%; background: #fff; border-radius: 32rpx 32rpx 0 0; max-height: 50vh; display: flex; flex-direction: column; }
.panel-head { display: flex; justify-content: space-between; align-items: center; padding: 28rpx 32rpx; border-bottom: 2rpx solid #f0f0f0; }
.panel-title { font-size: 30rpx; font-weight: 600; color: #1a1a1a; }
.panel-close { font-size: 40rpx; color: #999; padding: 4rpx 8rpx; }
.panel-body { flex: 1; padding: 12rpx 32rpx; overflow-y: auto; }
.form-row { display: flex; align-items: center; padding: 20rpx 0; border-bottom: 2rpx solid #f8f8f8; }
.form-l { font-size: 26rpx; color: #333; width: 160rpx; flex-shrink: 0; font-weight: 500; }
.form-input { flex: 1; font-size: 28rpx; color: #333; height: 56rpx; }
.panel-footer { display: flex; gap: 24rpx; padding: 24rpx 32rpx; border-top: 2rpx solid #f0f0f0; }
.btn-cancel { flex: 1; height: 80rpx; line-height: 80rpx; border-radius: 40rpx; background: #f5f5f5; color: #666; font-size: 28rpx; border: none; }
.btn-cancel::after { border: none; }
.btn-save { flex: 1; height: 80rpx; line-height: 80rpx; border-radius: 40rpx; background: linear-gradient(135deg, #f43f5e, #e11d48); color: #fff; font-size: 28rpx; font-weight: 600; border: none; }
.btn-save::after { border: none; }
</style>
