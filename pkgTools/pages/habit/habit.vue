<template>
  <view class="habit-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">←</text>
        <text class="nav-title">习惯打卡</text>
        <text class="nav-icon" @click="openAdd">+</text>
      </view>
    </view>
    <view class="content">
      <view class="streak-card">
        <text class="streak-num">{{ totalStreak }}</text>
        <text class="streak-label">总连续天数</text>
      </view>
      <view class="section-title">今日习惯</view>
      <view class="habit-list">
        <view class="habit-item" v-for="(h, idx) in habits" :key="h.id">
          <view class="h-left" @click="toggleHabit(h.id)">
            <text class="h-check" :class="{ done: isChecked(h.id) }">{{ isChecked(h.id) ? "✓" : "" }}</text>
            <text class="h-name">{{ h.name }}</text>
          </view>
          <view class="h-right">
            <text class="h-streak">{{ getStreak(h.id) }}天</text>
            <text class="h-del" @click="deleteHabit(h.id)">×</text>
          </view>
        </view>
      </view>
      <view class="empty-mini" v-if="habits.length === 0"><text>添加第一个习惯吧</text></view>
      <view class="section-title">本周打卡</view>
      <view class="week-calendar">
        <view class="cal-day" v-for="(d, idx) in weekCalendar" :key="idx">
          <text class="cal-label">{{ d.label }}</text>
          <text class="cal-dot" :class="{ active: d.checked }"></text>
          <text class="cal-count">{{ d.count }}/{{ habits.length }}</text>
        </view>
      </view>
    </view>
    <view v-if="showAdd" class="mask" @click="showAdd = false">
      <view class="create-panel" @click.stop>
        <view class="panel-head"><text class="panel-title">新建习惯</text><text class="panel-close" @click="showAdd = false">×</text></view>
        <view class="panel-body">
          <view class="form-row"><text class="form-l">习惯名称</text><input class="form-input" v-model="newHabit" placeholder="如：每天读书30分钟" /></view>
        </view>
        <view class="panel-footer"><button class="btn-cancel" @click="showAdd = false">取消</button><button class="btn-save" @click="addHabit">创建</button></view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, computed, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const habits = ref([])
const checkins = ref([])
const showAdd = ref(false)
const newHabit = ref("")
const totalStreak = computed(() => habits.value.reduce((s, h) => s + getStreak(h.id), 0))
const weekCalendar = computed(() => {
  const days = ["日", "一", "二", "三", "四", "五", "六"]
  const result = []
  const today = new Date()
  for (let i = 6; i >= 0; i--) {
    const d = new Date(today); d.setDate(d.getDate() - i)
    const dateStr = d.toISOString().slice(0, 10)
    const count = checkins.value.filter(c => c.date === dateStr).length
    result.push({ label: days[d.getDay()], count, checked: count === habits.value.length && habits.value.length > 0 })
  }
  return result
})
function goBack() { uni.navigateBack() }
function openAdd() { newHabit.value = ""; showAdd.value = true }
function addHabit() {
  if (!newHabit.value.trim()) { uni.showToast({ title: "请输入名称", icon: "none" }); return }
  habits.value.push({ id: Date.now(), name: newHabit.value }); saveData(); showAdd.value = false
}
function deleteHabit(id) {
  uni.showModal({ title: "删除", content: "确定删除？", success: (r) => { if (r.confirm) { habits.value = habits.value.filter(h => h.id !== id); checkins.value = checkins.value.filter(c => c.habitId !== id); saveData() } } })
}
function isChecked(habitId) {
  const today = new Date().toISOString().slice(0, 10)
  return checkins.value.some(c => c.habitId === habitId && c.date === today)
}
function toggleHabit(habitId) {
  const today = new Date().toISOString().slice(0, 10)
  const idx = checkins.value.findIndex(c => c.habitId === habitId && c.date === today)
  if (idx >= 0) checkins.value.splice(idx, 1)
  else checkins.value.push({ habitId, date: today })
  saveData()
}
function getStreak(habitId) {
  let streak = 0
  const d = new Date()
  while (true) {
    const dateStr = d.toISOString().slice(0, 10)
    if (checkins.value.some(c => c.habitId === habitId && c.date === dateStr)) { streak++; d.setDate(d.getDate() - 1) }
    else break
  }
  return streak
}
function saveData() { uni.setStorageSync("habit_habits", JSON.stringify(habits.value)); uni.setStorageSync("habit_checkins", JSON.stringify(checkins.value)) }
onMounted(() => {
  if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }
  const h = uni.getStorageSync("habit_habits"); if (h) { try { habits.value = JSON.parse(h) } catch (e) {} }
  const c = uni.getStorageSync("habit_checkins"); if (c) { try { checkins.value = JSON.parse(c) } catch (e) {} }
})
</script>
<style lang="scss" scoped>
.habit-page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #8b5cf6, #7c3aed); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.streak-card { background: linear-gradient(135deg, #8b5cf6, #7c3aed); border-radius: 24rpx; padding: 32rpx; text-align: center; margin-bottom: 24rpx; }
.streak-num { font-size: 64rpx; color: #fff; font-weight: 700; display: block; }
.streak-label { font-size: 24rpx; color: rgba(255,255,255,0.7); margin-top: 8rpx; display: block; }
.section-title { font-size: 28rpx; font-weight: 600; color: #333; margin: 24rpx 0 16rpx; }
.habit-list { background: #fff; border-radius: 24rpx; padding: 8rpx 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.habit-item { display: flex; justify-content: space-between; align-items: center; padding: 20rpx 0; border-bottom: 2rpx solid #f9f9f9; }
.h-left { display: flex; align-items: center; gap: 16rpx; flex: 1; }
.h-check { width: 40rpx; height: 40rpx; border-radius: 50%; border: 2rpx solid #ddd; display: flex; align-items: center; justify-content: center; font-size: 22rpx; color: #fff; }
.h-check.done { background: #8b5cf6; border-color: #8b5cf6; }
.h-name { font-size: 26rpx; color: #333; }
.h-right { display: flex; align-items: center; gap: 16rpx; }
.h-streak { font-size: 22rpx; color: #8b5cf6; font-weight: 600; }
.h-del { font-size: 32rpx; color: #ccc; }
.empty-mini { text-align: center; padding: 32rpx; font-size: 24rpx; color: #999; }
.week-calendar { display: flex; justify-content: space-between; background: #fff; border-radius: 24rpx; padding: 24rpx 16rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.cal-day { text-align: center; flex: 1; }
.cal-label { font-size: 22rpx; color: #999; display: block; }
.cal-dot { width: 16rpx; height: 16rpx; border-radius: 50%; background: #e5e7eb; margin: 8rpx auto; display: block; }
.cal-dot.active { background: #8b5cf6; }
.cal-count { font-size: 18rpx; color: #666; display: block; margin-top: 4rpx; }
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
.btn-save { flex: 1; height: 80rpx; line-height: 80rpx; border-radius: 40rpx; background: linear-gradient(135deg, #8b5cf6, #7c3aed); color: #fff; font-size: 28rpx; font-weight: 600; border: none; }
.btn-save::after { border: none; }
</style>
