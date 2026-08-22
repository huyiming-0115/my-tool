<template>
  <view class="dt-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">日期计算</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="mode-tabs"><text class="mode-tab" :class="{ active: mode === 'diff' }" @click="mode = 'diff'">日期间隔</text><text class="mode-tab" :class="{ active: mode === 'add' }" @click="mode = 'add'">日期加减</text></view>
      <view class="form-card" v-if="mode === 'diff'">
        <view class="form-row"><text class="form-l">开始日期</text><picker mode="date" :value="startDate" @change="startDate = $event.detail.value"><text class="picker-val">{{ startDate }}</text></picker></view>
        <view class="form-row"><text class="form-l">结束日期</text><picker mode="date" :value="endDate" @change="endDate = $event.detail.value"><text class="picker-val">{{ endDate }}</text></picker></view>
        <view class="calc-trigger" @click="calcDiff"><text>计算间隔</text></view>
        <view class="dt-result" v-if="diffResult"><text class="dt-num">{{ diffResult.days }}</text><text class="dt-unit">天</text><text class="dt-extra">{{ diffResult.weeks }}周 {{ diffResult.years }}</text></view>
      </view>
      <view class="form-card" v-else>
        <view class="form-row"><text class="form-l">基础日期</text><picker mode="date" :value="baseDate" @change="baseDate = $event.detail.value"><text class="picker-val">{{ baseDate }}</text></picker></view>
        <view class="form-row"><text class="form-l">增减天数</text><input class="form-input" v-model="addDays" type="number" placeholder="30" /></view>
        <view class="calc-trigger" @click="calcAdd"><text>计算结果</text></view>
        <view class="dt-result" v-if="addResult"><text class="dt-num">{{ addResult.date }}</text><text class="dt-extra">{{ addResult.weekday }} 已{{ addResult.dir }}{{ Math.abs(addDays) }}天</text></view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const today = new Date().toISOString().slice(0, 10)
const mode = ref("diff")
const startDate = ref(today)
const endDate = ref(today)
const baseDate = ref(today)
const addDays = ref("30")
const diffResult = ref(null)
const addResult = ref(null)
function calcDiff() {
  const d1 = new Date(startDate.value); const d2 = new Date(endDate.value)
  const diff = Math.abs((d2 - d1) / 86400000)
  diffResult.value = { days: diff, weeks: (diff / 7).toFixed(1), years: (diff / 365).toFixed(2) }
}
function calcAdd() {
  const d = new Date(baseDate.value)
  d.setDate(d.getDate() + (parseInt(addDays.value) || 0))
  const w = ["日", "一", "二", "三", "四", "五", "六"][d.getDay()]
  addResult.value = { date: d.toISOString().slice(0, 10), weekday: "星期" + w, dir: parseInt(addDays.value) >= 0 ? "过" : "前" }
}
function goBack() { uni.navigateBack() }
onMounted(() => { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.dt-page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #43e97b, #38f9d7); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.mode-tabs { display: flex; gap: 16rpx; margin-bottom: 24rpx; }
.mode-tab { flex: 1; text-align: center; padding: 20rpx; background: #fff; border-radius: 16rpx; font-size: 28rpx; color: #666; }
.mode-tab.active { background: linear-gradient(135deg, #43e97b, #38f9d7); color: #fff; }
.form-card { background: #fff; border-radius: 24rpx; padding: 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.form-row { display: flex; align-items: center; padding: 24rpx 0; border-bottom: 2rpx solid #f8f8f8; }
.form-l { font-size: 28rpx; color: #333; width: 200rpx; flex-shrink: 0; font-weight: 500; }
.form-input { flex: 1; font-size: 30rpx; height: 56rpx; text-align: right; }
.picker-val { flex: 1; font-size: 30rpx; color: #333; text-align: right; }
.calc-trigger { background: linear-gradient(135deg, #43e97b, #38f9d7); border-radius: 16rpx; padding: 24rpx; text-align: center; margin-top: 24rpx; }
.calc-trigger text { font-size: 30rpx; color: #fff; font-weight: 600; }
.dt-result { text-align: center; padding: 40rpx 0 16rpx; }
.dt-num { font-size: 60rpx; color: #43e97b; font-weight: 700; }
.dt-unit { font-size: 28rpx; color: #666; margin-left: 8rpx; }
.dt-extra { display: block; font-size: 24rpx; color: #999; margin-top: 12rpx; }
</style>
