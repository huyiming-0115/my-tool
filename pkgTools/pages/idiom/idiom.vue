<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u6210\u8bed\u8bcd\u5178</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="search-bar"><input class="search-input" v-model="keyword" placeholder="\u641c\u7d22\u6210\u8bed" @input="search" /><text class="search-btn" @click="search">\u641c\u7d22</text></view>
      <view class="idiom-list">
        <view class="idiom-card" v-for="(item, i) in results" :key="i">
          <text class="ic-word">{{ item.word }}</text>
          <text class="ic-pinyin">{{ item.pinyin }}</text>
          <text class="ic-meaning">{{ item.meaning }}</text>
        </view>
      </view>
      <view class="empty" v-if="results.length === 0"><text>\u6ca1\u6709\u627e\u5230\u76f8\u5173\u6210\u8bed</text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const keyword = ref("")
const results = ref([])
const idioms = [
  {word:"\u4e00\u5c71\u4e0d\u5bb9\u4e8c\u864e",pinyin:"y\u012b sh\u0101n b\u00f9 r\u00f3ng \u00e8r h\u01d4",meaning:"\u4e24\u864e\u4e0d\u80fd\u5171\u5b58\uff0c\u6bd4\u55bb\u4e24\u4e2a\u5f3a\u654c\u4e0d\u80fd\u5171\u5b58"},
  {word:"\u4e94\u82b1\u516b\u95e8",pinyin:"w\u01d4 hu\u0101 b\u0101 m\u00e9n",meaning:"\u5f62\u5bb9\u5408\u79cd\u591a\u6837\uff0c\u53d1\u5c55\u4e0d\u660e\u786e"},
  {word:"\u4eba\u5c71\u4eba\u6d77",pinyin:"r\u00e9n sh\u0101n r\u00e9n h\u01d0i",meaning:"\u5f62\u5bb9\u4eba\u6c14\u96c6\u4e2d\uff0c\u4eba\u6570\u6781\u591a"},
  {word:"\u5929\u5730\u957f\u4e45",pinyin:"ti\u0101n d\u00ec ch\u00e1ng ji\u01d4",meaning:"\u5f62\u5bb9\u65f6\u95f4\u6781\u5176\u4e45\u8fdc"},
  {word:"\u4e07\u53d8\u4e0d\u79bb\u5176\u5b97",pinyin:"w\u00e0n bi\u00e0n b\u00f9 l\u00ed q\u00ed z\u014dng",meaning:"\u5f62\u5bb9\u867d\u7136\u53d8\u5316\u5f88\u5927\uff0c\u4f46\u672c\u8d28\u6ca1\u6709\u53d8"},
  {word:"\u4e00\u5fc3\u4e00\u610f",pinyin:"y\u012b x\u012bn y\u012b y\u00ec",meaning:"\u5fc3\u5ff5\u4e00\uff0c\u4e0d\u5206\u5fc3"},
  {word:"\u5343\u519b\u4e07\u9a6c",pinyin:"qi\u0101n j\u016bn w\u00e0n m\u01d0",meaning:"\u5f62\u5bb9\u884c\u519b\u7eb5\u6a2a\uff0c\u58ee\u89c2\u6c14\u52bf"},
  {word:"\u4e09\u987e\u8305\u5e90",pinyin:"s\u0101n g\u00f9 m\u00e1o l\u00fa",meaning:"\u6bd4\u55bb\u7740\u7740\u5b9d\u8d1d\u5730\u89d2\u65b9\u5207"},
  {word:"\u6795\u4e2d\u5e15\u9999",pinyin:"zh\u011bn zh\u014dng p\u00e0 xi\u0101ng",meaning:"\u6bd4\u55bb\u5e38\u5e38\u60f3\u5230\u67d0\u4e8b\u800c\u4e0d\u5982\u610f"},
  {word:"\u9f99\u98de\u51e4\u821e",pinyin:"l\u00f3ng f\u0113i f\u00e8ng w\u01d4",meaning:"\u5f62\u5bb9\u4e66\u6cd5\u7cbe\u5de7\uff0c\u8c61\u5f81\u5409\u7965"}
]
function search() {
  const k = keyword.value.trim()
  if (!k) { results.value = []; return }
  results.value = idioms.filter(function(i){return i.word.includes(k) || i.pinyin.includes(k.toLowerCase())})
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #f6d365, #fda085); }
.custom-nav { background: linear-gradient(135deg, #e17055, #f39c12); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.search-bar { display: flex; gap: 16rpx; margin-bottom: 32rpx; }
.search-input { flex: 1; background: #fff; border-radius: 16rpx; padding: 20rpx 24rpx; font-size: 28rpx; }
.search-btn { background: #e17055; color: #fff; border-radius: 16rpx; padding: 20rpx 32rpx; font-size: 28rpx; display: flex; align-items: center; }
.idiom-list { display: flex; flex-direction: column; gap: 16rpx; }
.idiom-card { background: #fff; border-radius: 20rpx; padding: 24rpx; }
.ic-word { font-size: 36rpx; font-weight: 700; color: #333; display: block; }
.ic-pinyin { font-size: 24rpx; color: #999; display: block; margin: 4rpx 0; }
.ic-meaning { font-size: 26rpx; color: #666; display: block; }
.empty { text-align: center; padding: 60rpx; color: rgba(255,255,255,0.7); }
</style>
