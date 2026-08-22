<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u5386\u53f2\u4eca\u65e5</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <text class="today-date">{{ todayStr }}</text>
      <view class="event-list">
        <view class="event-card" v-for="(e, i) in events" :key="i">
          <text class="event-year">{{ e.year }}\u5e74</text>
          <text class="event-text">{{ e.text }}</text>
        </view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const todayStr = ref("")
const events = ref([])
const allEvents = {
  "1/1":[{year:1912,text:"\u4e2d\u534e\u6c11\u56fd\u6210\u7acb"},{year:1979,text:"\u4e2d\u7f8e\u5efa\u4ea4"}],
  "5/4":[{year:1919,text:"\u4e94\u56db\u8fd0\u52a8\u7206\u53d1"}],
  "7/1":[{year:1921,text:"\u4e2d\u56fd\u5171\u4ea7\u515a\u6210\u7acb"},{year:1997,text:"\u9999\u6e2f\u56de\u5f52"}],
  "8/1":[{year:1927,text:"\u5357\u660c\u8d77\u4e49"}],
  "10/1":[{year:1949,text:"\u4e2d\u534e\u4eba\u6c11\u5171\u548c\u56fd\u6210\u7acb"}],
  "12/26":[{year:1893,text:"\u6bdb\u6cfd\u4e1c\u8bde\u8fb0"}]
}
onMounted(function() {
  if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }
  const d = new Date()
  const key = (d.getMonth()+1) + "/" + d.getDate()
  todayStr.value = d.getFullYear() + "\u5e74" + (d.getMonth()+1) + "\u6708" + d.getDate() + "\u65e5"
  events.value = allEvents[key] || [{year:d.getFullYear()-100,text:"\u8fd9\u4e00\u5929\u4e5f\u6709\u5f88\u591a\u6545\u4e8b\u53d1\u751f"}]
})
function goBack() { uni.navigateBack() }
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #a18cd1, #fbc2eb); }
.custom-nav { background: linear-gradient(135deg, #6c5ce7, #a29bfe); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.today-date { font-size: 36rpx; font-weight: 700; color: #fff; text-align: center; display: block; margin-bottom: 32rpx; }
.event-list { display: flex; flex-direction: column; gap: 20rpx; }
.event-card { background: #fff; border-radius: 20rpx; padding: 28rpx; display: flex; align-items: center; gap: 24rpx; }
.event-year { font-size: 32rpx; font-weight: 700; color: #6c5ce7; min-width: 120rpx; }
.event-text { font-size: 28rpx; color: #333; flex: 1; }
</style>
