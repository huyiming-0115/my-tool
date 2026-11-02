
<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">历史今日</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="th-date"><text>{{todayStr}}</text></view>
      <view class="th-list">
        <view class="th-item" v-for="(item, i) in events" :key="i">
          <view class="th-year"><text>{{item.year}}</text></view>
          <view class="th-dot"></view>
          <view class="th-content"><text>{{item.event}}</text></view>
        </view>
      </view>
      <view class="th-refresh" @click="refresh"><text>换一批</text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const todayStr = ref("")
const events = ref([])
const allEvents = [
  {year:"1949年",event:"中华人民共和国成立，开国大典在天安门广场隆重举行。"},
  {year:"1969年",event:"阿波罗11号登月成功，人类首次踏上月球表面。"},
  {year:"1997年",event:"香港回归祖国，结束英国殖民统治。"},
  {year:"2008年",event:"北京奥运会开幕，第29届夏季奥林匹克运动会在鸟巢举行。"},
  {year:"1879年",event:"爱迪生发明实用白炽灯泡，改变人类生活方式。"},
  {year:"1776年",event:"美国独立宣言签署，宣告美利坚合众国成立。"},
  {year:"1964年",event:"中国第一颗原子弹爆炸成功。"},
  {year:"1990年",event:"万维网（WWW）由蒂姆·伯纳斯-李发明。"},
  {year:"2010年",event:"上海世博会开幕，主题为城市让生活更美好。"},
  {year:"1452年",event:"达·芬奇诞生，文艺复兴时期杰出艺术家。"},
  {year:"1848年",event：《共产党宣言》发表，标志着马克思主义诞生。"},
  {year:"2003年",event:"中国首次载人航天飞行，杨利伟乘坐神舟五号进入太空。"},
  {year:"1886年",event:"卡尔·本茨发明世界上第一辆汽车。"},
  {year:"1953年",event:"DNA双螺旋结构被发现，开启分子生物学新纪元。"},
  {year:"2015年",event:"屠呦呦获诺贝尔生理学或医学奖，表彰青蒿素发现。"}
]
function refresh() {
  var shuffled = allEvents.slice().sort(function() { return Math.random() - 0.5 })
  events.value = shuffled.slice(0, 6)
}
function goBack() { uni.navigateBack() }
onMounted(function() {
  if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }
  var d = new Date()
  todayStr.value = (d.getMonth()+1) + "月" + d.getDate() + "日"
  refresh()
})
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #ff9a9e, #fad0c4); }
.custom-nav { background: linear-gradient(135deg, #ff9a9e, #fad0c4); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 32rpx; }
.th-date { text-align: center; margin-bottom: 32rpx; }
.th-date text { color: #fff; font-size: 36rpx; font-weight: 700; }
.th-list { padding-left: 20rpx; }
.th-item { display: flex; margin-bottom: 24rpx; align-items: flex-start; }
.th-year { width: 140rpx; flex-shrink: 0; }
.th-year text { color: #fff; font-size: 26rpx; font-weight: 600; }
.th-dot { width: 16rpx; height: 16rpx; border-radius: 50%; background: #fff; margin-top: 8rpx; flex-shrink: 0; position: relative; }
.th-dot::after { content: ""; position: absolute; top: 16rpx; left: 7rpx; width: 2rpx; height: 60rpx; background: rgba(255,255,255,0.3); }
.th-content { flex: 1; padding-left: 20rpx; }
.th-content text { color: rgba(255,255,255,0.9); font-size: 28rpx; line-height: 1.6; }
.th-refresh { text-align: center; margin-top: 32rpx; }
.th-refresh text { color: #fff; font-size: 28rpx; background: rgba(255,255,255,0.2); padding: 16rpx 40rpx; border-radius: 30rpx; }
</style>
