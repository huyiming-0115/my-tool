<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u62c9\u4f38\u52a8\u4f5c\u5e93</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="category-tabs"><text class="cat-tab" :class="{active: category==='\u529e\u516c\u5ba4'}" @click="category='\u529e\u516c\u5ba4'">\u529e\u516c\u5ba4</text><text class="cat-tab" :class="{active: category==='\u8fd0\u52a8\u524d'}" @click="category='\u8fd0\u52a8\u524d'">\u8fd0\u52a8\u524d</text><text class="cat-tab" :class="{active: category==='\u7761\u524d'}" @click="category='\u7761\u524d'">\u7761\u524d</text></view>
      <view class="stretch-list">
        <view class="stretch-card" v-for="(s, i) in stretches[category]" :key="i">
          <text class="stretch-name">{{ s.name }}</text>
          <text class="stretch-desc">{{ s.desc }}</text>
          <text class="stretch-time">{{ s.time }}</text>
        </view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const category = ref("\u529e\u516c\u5ba4")
const stretches = {
  "\u529e\u516c\u5ba4": [
    {name:"\u9888\u90e8\u62c9\u4f38", desc:"\u53f3\u624b\u5f80\u53f3\u4fa7\u538b\u5934\uff0c\u4fdd\u630115\u79d2", time:"30\u79d2"},
    {name:"\u80a9\u90e8\u65cb\u8f6c", desc:"\u80a9\u8180\u524d\u540e\u65cb\u8f6c\u540410\u6b21", time:"1\u5206\u949f"},
    {name:"\u8170\u90e8\u4f38\u5c55", desc:"\u53cc\u624b\u5347\u9ad8\uff0c\u8eab\u4f53\u5f80\u4fa7\u4f38\u5c55", time:"30\u79d2"},
    {name:"\u624b\u81c2\u62c9\u4f38", desc:"\u4e00\u53ea\u624b\u82cd\u8fc7\u5934\u9876\uff0c\u53e6\u4e00\u53ea\u624b\u5f80\u4e0b\u638c", time:"30\u79d2"},
    {name:"\u819d\u76f8\u62e5", desc:"\u5750\u7740\u628a\u819d\u76f8\u62e5\u62c9\u81f3\u80f8\u524d", time:"30\u79d2"}
  ],
  "\u8fd0\u52a8\u524d": [
    {name:"\u5927\u817f\u524d\u4fa7", desc:"\u7ad9\u7acb\u62c9\u4f38\u5927\u817f\u524d\u4fa7\u808c\u7fa4", time:"30\u79d2"},
    {name:"\u5927\u817f\u540e\u4fa7", desc:"\u7ad9\u7acb\u62c9\u4f38\u5927\u817f\u540e\u4fa7\u808c\u7fa4", time:"30\u79d2"},
    {name:"\u952f\u9f3b\u62c9\u4f38", desc:"\u53cc\u819d\u8e32\u4e0b\uff0c\u8eab\u4f53\u5f80\u540e\u5fae\u5fae\u503e\u659c", time:"30\u79d2"},
    {name:"\u952f\u9f3b\u62c9\u4f38", desc:"\u53cc\u819d\u8e32\u4e0b\uff0c\u8eab\u4f53\u5f80\u540e\u5fae\u5fae\u503e\u659c", time:"30\u79d2"},
    {name:"\u8f6c\u9abf\u62c9\u4f38", desc:"\u53cc\u819d\u8e32\u4e0b\uff0c\u8eab\u4f53\u5f80\u540e\u5fae\u5fae\u503e\u659c", time:"30\u79d2"}
  ],
  "\u7761\u524d": [
    {name:"\u59ff\u52bf\u62c9\u4f38", desc:"\u8e32\u4e0b\uff0c\u8eab\u4f53\u524d\u503e\u62c9\u4f38\u80cc\u90e8", time:"1\u5206\u949f"},
    {name:"\u87ba\u65cb\u62c9\u4f38", desc:"\u8eba\u7740\u53cc\u817f\u5f2f\u66f2\u65cb\u8f6c", time:"1\u5206\u949f"},
    {name:"\u62e5\u62b1\u819d\u76f8", desc:"\u8eba\u7740\u628a\u819d\u76f8\u62e5\u62c9\u81f3\u80f8\u524d", time:"1\u5206\u949f"},
    {name:"\u4f38\u5c55\u5f0f", desc:"\u8eba\u7740\u53cc\u624b\u5347\u9ad8\uff0c\u8eab\u4f53\u5c3d\u91cf\u62c9\u957f", time:"1\u5206\u949f"}
  ]
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #84fab0, #8fd3f4); }
.custom-nav { background: linear-gradient(135deg, #00b894, #55efc4); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.category-tabs { display: flex; gap: 12rpx; margin-bottom: 24rpx; }
.cat-tab { flex: 1; text-align: center; padding: 16rpx; border-radius: 12rpx; background: rgba(255,255,255,0.3); color: #fff; font-size: 24rpx; }
.cat-tab.active { background: #fff; color: #00b894; }
.stretch-list { display: flex; flex-direction: column; gap: 16rpx; }
.stretch-card { background: #fff; border-radius: 20rpx; padding: 24rpx; }
.stretch-name { font-size: 30rpx; font-weight: 600; color: #333; display: block; }
.stretch-desc { font-size: 24rpx; color: #666; display: block; margin: 8rpx 0; }
.stretch-time { font-size: 22rpx; color: #00b894; font-weight: 600; }
</style>
