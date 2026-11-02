<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u6587\u5b57\u4e91\u751f\u6210</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="form-card"><text class="form-label">\u8f93\u5165\u6587\u5b57 (\u7528\u7a7a\u683c\u6216\u9017\u53f7\u5206\u9694)</text><textarea class="wc-input" v-model="words" placeholder="\u5feb\u4e50 \u5e78\u798f \u5065\u5eb7 \u6210\u529f \u52aa\u529b \u68a6\u60f3" auto-height></textarea></view>
      <view class="gen-btn" @click="generate"><text>\u751f\u6210\u6587\u5b57\u4e91</text></view>
      <view class="cloud-display" v-if="cloudWords.length > 0">
        <view class="cloud-word" v-for="(w, i) in cloudWords" :key="i" :style="{fontSize: w.size+'rpx', color: w.color}">{{ w.text }}</view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const words = ref("\u5feb\u4e50 \u5e78\u798f \u5065\u5eb7 \u6210\u529f \u52aa\u529b \u68a6\u60f3 \u81ea\u4fe1 \u575a\u6301 \u5e0c\u671b")
const cloudWords = ref([])
const colors = ["#ff6b6b","#feca57","#48dbfb","#ff9ff3","#54a0ff","#5f27cd","#00d2d3","#ff9f43","#ee5a24","#0abde3"]
function generate() {
  var arr = words.value.split(/[\s,]+/).filter(function(w){return w})
  if (arr.length === 0) { uni.showToast({ title: "\u8bf7\u8f93\u5165\u6587\u5b57", icon: "none" }); return }
  cloudWords.value = arr.map(function(w, i) {
    return { text: w, size: Math.floor(Math.random()*40)+30, color: colors[i%colors.length] }
  })
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }; generate() })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #a18cd1, #fbc2eb); }
.custom-nav { background: linear-gradient(135deg, #6c5ce7, #a29bfe); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.form-card { background: #fff; border-radius: 20rpx; padding: 24rpx; margin-bottom: 24rpx; }
.form-label { font-size: 26rpx; color: #666; display: block; margin-bottom: 12rpx; }
.wc-input { width: 100%; min-height: 120rpx; font-size: 28rpx; color: #333; }
.gen-btn { background: linear-gradient(135deg, #6c5ce7, #a29bfe); border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 32rpx; }
.gen-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.cloud-display { background: #fff; border-radius: 24rpx; padding: 40rpx; display: flex; flex-wrap: wrap; gap: 20rpx; justify-content: center; align-items: center; min-height: 300rpx; }
.cloud-word { font-weight: 700; padding: 8rpx 16rpx; }
</style>
