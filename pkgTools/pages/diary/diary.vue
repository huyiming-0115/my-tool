<template>
  <view class="diary-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">←</text>
        <text class="nav-title">每日日记</text>
        <text class="nav-icon" @click="openAdd">+</text>
      </view>
    </view>
    <view class="content">
      <view class="mood-stats">
        <text class="section-title">本月心情</text>
        <view class="mood-row">
          <view class="mood-item" v-for="(m, idx) in moodStats" :key="idx">
            <text class="mood-emoji">{{ m.emoji }}</text>
            <text class="mood-count">{{ m.count }}</text>
          </view>
        </view>
      </view>
      <view class="section-title">月卡历</view>
      <view class="calendar">
        <view class="cal-header">
          <text class="cal-month">{{ currentMonthLabel }}</text>
        </view>
        <view class="cal-grid">
          <text class="cal-weekday" v-for="d in ['日','一','二','三','四','五','六']" :key="d">{{ d }}</text>
          <view class="cal-cell" v-for="(cell, idx) in calendarCells" :key="idx" :class="{ hasDiary: cell.hasDiary, today: cell.isToday }">
            <text class="cell-day">{{ cell.day }}</text>
          </view>
        </view>
      </view>
      <view class="section-title">最近日记</view>
      <view class="diary-list">
        <view class="diary-item" v-for="(d, idx) in records.slice(0, 10)" :key="idx">
          <view class="d-top"><text class="d-date">{{ d.date }}</text><text class="d-mood">{{ d.mood }}</text></view>
          <text class="d-content">{{ d.content }}</text>
        </view>
      </view>
      <view class="empty-mini" v-if="records.length === 0"><text>开始记录你的日记吧</text></view>
    </view>
    <view v-if="showAdd" class="mask" @click="showAdd = false">
      <view class="create-panel" @click.stop>
        <view class="panel-head"><text class="panel-title">写日记</text><text class="panel-close" @click="showAdd = false">×</text></view>
        <view class="panel-body">
          <view class="mood-select">
            <text class="mood-opt" v-for="m in moods" :key="m" :class="{ active: newDiary.mood === m }" @click="newDiary.mood = m">{{ m }}</text>
          </view>
          <textarea class="diary-input" v-model="newDiary.content" placeholder="今天发生了什么..." maxlength="500"></textarea>
        </view>
        <view class="panel-footer"><button class="btn-cancel" @click="showAdd = false">取消</button><button class="btn-save" @click="addDiary">保存</button></view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, computed, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const records = ref([])
const showAdd = ref(false)
const moods = ["😊", "😐", "😢", "😠", "😴"]
const newDiary = ref({ content: "", mood: "😊" })
const currentMonthLabel = computed(() => { const d = new Date(); return d.getFullYear() + "年" + (d.getMonth() + 1) + "月" })
const calendarCells = computed(() => {
  const now = new Date(); const year = now.getFullYear(); const month = now.getMonth()
  const firstDay = new Date(year, month, 1).getDay(); const daysInMonth = new Date(year, month + 1, 0).getDate()
  const cells = []
  for (let i = 0; i < firstDay; i++) cells.push({ day: "", hasDiary: false, isToday: false })
  for (let d = 1; d <= daysInMonth; d++) {
    const dateStr = year + "-" + String(month + 1).padStart(2, "0") + "-" + String(d).padStart(2, "0")
    cells.push({ day: d, hasDiary: records.value.some(r => r.date === dateStr), isToday: d === now.getDate() })
  }
  return cells
})
const moodStats = computed(() => {
  const month = new Date().toISOString().slice(0, 7)
  const monthRecords = records.value.filter(r => r.date.slice(0, 7) === month)
  return moods.map(m => ({ emoji: m, count: monthRecords.filter(r => r.mood === m).length }))
})
function goBack() { uni.navigateBack() }
function openAdd() { newDiary.value = { content: "", mood: "😊" }; showAdd.value = true }
function addDiary() {
  if (!newDiary.value.content.trim()) { uni.showToast({ title: "请输入内容", icon: "none" }); return }
  records.value.unshift({ date: new Date().toISOString().slice(0, 10), content: newDiary.value.content, mood: newDiary.value.mood })
  saveData(); showAdd.value = false
}
function saveData() { uni.setStorageSync("diary_records", JSON.stringify(records.value)) }
onMounted(() => {
  if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }
  const saved = uni.getStorageSync("diary_records"); if (saved) { try { records.value = JSON.parse(saved) } catch (e) {} }
})
</script>
<style lang="scss" scoped>
.diary-page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #ec4899, #db2777); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.section-title { font-size: 28rpx; font-weight: 600; color: #333; margin: 24rpx 0 16rpx; }
.mood-stats { background: #fff; border-radius: 24rpx; padding: 24rpx; margin-bottom: 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.mood-row { display: flex; justify-content: space-around; }
.mood-item { text-align: center; }
.mood-emoji { font-size: 40rpx; display: block; }
.mood-count { font-size: 22rpx; color: #666; margin-top: 4rpx; display: block; }
.calendar { background: #fff; border-radius: 24rpx; padding: 24rpx; margin-bottom: 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.cal-header { text-align: center; margin-bottom: 16rpx; }
.cal-month { font-size: 28rpx; font-weight: 600; color: #333; }
.cal-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 8rpx; }
.cal-weekday { text-align: center; font-size: 22rpx; color: #999; padding: 8rpx 0; }
.cal-cell { text-align: center; padding: 12rpx 0; border-radius: 50%; }
.cell-day { font-size: 24rpx; color: #333; }
.cal-cell.hasDiary { background: #fce7f3; }
.cal-cell.today { background: #ec4899; }
.cal-cell.today .cell-day { color: #fff; }
.diary-list { background: #fff; border-radius: 24rpx; padding: 8rpx 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.diary-item { padding: 20rpx 0; border-bottom: 2rpx solid #f9f9f9; }
.diary-item:last-child { border-bottom: none; }
.d-top { display: flex; justify-content: space-between; margin-bottom: 8rpx; }
.d-date { font-size: 22rpx; color: #999; }
.d-mood { font-size: 28rpx; }
.d-content { font-size: 26rpx; color: #333; line-height: 1.6; }
.empty-mini { text-align: center; padding: 32rpx; font-size: 24rpx; color: #999; }
.mask { position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 999; display: flex; align-items: flex-end; }
.create-panel { width: 100%; background: #fff; border-radius: 32rpx 32rpx 0 0; max-height: 70vh; display: flex; flex-direction: column; }
.panel-head { display: flex; justify-content: space-between; align-items: center; padding: 28rpx 32rpx; border-bottom: 2rpx solid #f0f0f0; }
.panel-title { font-size: 30rpx; font-weight: 600; color: #1a1a1a; }
.panel-close { font-size: 40rpx; color: #999; padding: 4rpx 8rpx; }
.panel-body { flex: 1; padding: 12rpx 32rpx; overflow-y: auto; }
.mood-select { display: flex; gap: 16rpx; margin: 20rpx 0; }
.mood-opt { font-size: 40rpx; padding: 8rpx 16rpx; border-radius: 16rpx; background: #f5f5f5; }
.mood-opt.active { background: #fce7f3; }
.diary-input { width: 100%; height: 200rpx; border: 2rpx solid #e5e7eb; border-radius: 16rpx; padding: 16rpx; font-size: 26rpx; box-sizing: border-box; }
.panel-footer { display: flex; gap: 24rpx; padding: 24rpx 32rpx; border-top: 2rpx solid #f0f0f0; }
.btn-cancel { flex: 1; height: 80rpx; line-height: 80rpx; border-radius: 40rpx; background: #f5f5f5; color: #666; font-size: 28rpx; border: none; }
.btn-cancel::after { border: none; }
.btn-save { flex: 1; height: 80rpx; line-height: 80rpx; border-radius: 40rpx; background: linear-gradient(135deg, #ec4899, #db2777); color: #fff; font-size: 28rpx; font-weight: 600; border: none; }
.btn-save::after { border: none; }
</style>
