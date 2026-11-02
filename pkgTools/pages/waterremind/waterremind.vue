<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u559d\u6c34\u63d0\u9192</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="water-display">
        <view class="water-cup">
          <view class="water-fill" :style="{height: (today/target*100)+'%'}"></view>
          <text class="water-count">{{ today }}/{{ target }}</text>
        </view>
        <text class="water-label">\u676f</text>
      </view>
      <view class="form-card"><text class="form-label">\u6bcf\u65e5\u76ee\u6807 (\u676f)</text><input class="form-input" type="number" v-model="target" /></view>
      <view class="action-btns">
        <text class="act-btn add" @click="addWater">+ 1\u676f</text>
        <text class="act-btn reset" @click="reset">\u91cd\u7f6e</text>
      </view>
      <view class="remind-card">
        <text class="remind-title">\u5b9a\u65f6\u63d0\u9192</text>
        <view class="remind-row"><text>\u95f4\u9694:</text><picker class="remind-picker" :range="intervals" @change="interval=$event.detail.value"><text>{{ intervals[interval] }} \u25bc</text></picker></view>
        <text class="remind-toggle" :class="{on: reminding}" @click="toggleRemind">{{ reminding ? '\u5df2\u5f00\u542f' : '\u5df2\u5173\u95ed' }}</text>
      </view>
      <view class="history-card"><text class="hist-title">\u672c\u5468\u8bb0\u5f55</text><view class="hist-row"><text v-for="(d, i) in weekDays" :key="i">{{ d }}: {{ weekData[i]||0 }}</text></view></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const today = ref(3)
const target = ref(8)
const interval = ref(1)
const reminding = ref(false)
const intervals = ["30\u5206\u949f","1\u5c0f\u65f6","2\u5c0f\u65f6"]
const weekDays = ["\u4e00","\u4e8c","\u4e09","\u56db","\u4e94","\u516d","\u65e5"]
const weekData = ref([5,6,4,7,3,0,0])
function addWater() { today.value++ }
function reset() { today.value = 0 }
function toggleRemind() { reminding.value = !reminding.value; uni.showToast({ title: reminding.value?"\u5df2\u5f00\u542f":"\u5df2\u5173\u95ed", icon: "success" }) }
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #4facfe, #00f2fe); }
.custom-nav { background: linear-gradient(135deg, #0984e3, #00cec9); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.water-display { text-align: center; margin-bottom: 32rpx; }
.water-cup { width: 200rpx; height: 300rpx; border: 4rpx solid #fff; border-radius: 0 0 30rpx 30rpx; margin: 0 auto; position: relative; overflow: hidden; }
.water-fill { position: absolute; bottom: 0; width: 100%; background: linear-gradient(180deg, #74b9ff, #0984e3); transition: 0.5s; }
.water-count { position: absolute; top: 50%; left: 50%; transform: translate(-50%,-50%); font-size: 36rpx; font-weight: 700; color: #fff; z-index: 1; }
.water-label { font-size: 24rpx; color: rgba(255,255,255,0.8); }
.form-card { background: #fff; border-radius: 20rpx; padding: 24rpx; margin-bottom: 20rpx; }
.form-label { font-size: 26rpx; color: #666; display: block; margin-bottom: 12rpx; }
.form-input { font-size: 32rpx; color: #333; font-weight: 600; }
.action-btns { display: flex; gap: 16rpx; margin-bottom: 24rpx; }
.act-btn { flex: 1; text-align: center; padding: 20rpx; border-radius: 16rpx; font-size: 28rpx; font-weight: 600; }
.act-btn.add { background: #0984e3; color: #fff; }
.act-btn.reset { background: rgba(255,255,255,0.3); color: #fff; }
.remind-card { background: #fff; border-radius: 20rpx; padding: 24rpx; margin-bottom: 24rpx; }
.remind-title { font-size: 28rpx; font-weight: 600; color: #333; display: block; margin-bottom: 16rpx; }
.remind-row { display: flex; align-items: center; gap: 16rpx; margin-bottom: 16rpx; }
.remind-row text { font-size: 26rpx; color: #666; }
.remind-picker { flex: 1; background: #f8f8f8; border-radius: 12rpx; padding: 12rpx 16rpx; font-size: 26rpx; }
.remind-toggle { display: block; text-align: center; padding: 16rpx; border-radius: 12rpx; background: #f0f0f0; font-size: 26rpx; color: #999; }
.remind-toggle.on { background: #00b894; color: #fff; }
.history-card { background: #fff; border-radius: 20rpx; padding: 24rpx; }
.hist-title { font-size: 26rpx; font-weight: 600; color: #333; display: block; margin-bottom: 12rpx; }
.hist-row { display: flex; justify-content: space-between; font-size: 22rpx; color: #666; }
</style>
