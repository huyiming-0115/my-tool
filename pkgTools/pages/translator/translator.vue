<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u7ffb\u8bd1\u5de5\u5177</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="lang-row">
        <picker class="lang-picker" :range="langs" range-key="name" @change="fromLang=Number($event.detail.value)"><text>{{ langs[fromLang].name }} \u25bc</text></picker>
        <text class="swap-btn" @click="swapLang">\u2194</text>
        <picker class="lang-picker" :range="langs" range-key="name" @change="toLang=Number($event.detail.value)"><text>{{ langs[toLang].name }} \u25bc</text></picker>
      </view>
      <textarea class="tr-input" v-model="inputText" placeholder="\u8f93\u5165\u8981\u7ffb\u8bd1\u7684\u6587\u672c" auto-height></textarea>
      <view class="tr-btn" @click="translate"><text>\u7ffb\u8bd1</text></view>
      <view class="tr-result" v-if="outputText"><text>{{ outputText }}</text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const inputText = ref("")
const outputText = ref("")
const fromLang = ref(0)
const toLang = ref(1)
const langs = [{name:"\u4e2d\u6587",code:"zh"},{name:"\u82f1\u6587",code:"en"},{name:"\u65e5\u6587",code:"ja"},{name:"\u97e9\u6587",code:"ko"},{name:"\u6cd5\u6587",code:"fr"},{name:"\u5fb7\u6587",code:"de"},{name:"\u897f\u73ed\u7259\u6587",code:"es"}]
const dict = {
  "hello":"\u4f60\u597d","world":"\u4e16\u754c","thank":"\u8c22\u8c22","love":"\u7231","friend":"\u670b\u53cb",
  "\u4f60\u597d":"hello","\u4e16\u754c":"world","\u8c22\u8c22":"thank you","\u7231":"love","\u670b\u53cb":"friend"
}
function translate() {
  if (!inputText.value.trim()) { uni.showToast({ title: "\u8bf7\u8f93\u5165\u6587\u672c", icon: "none" }); return }
  const key = inputText.value.trim().toLowerCase()
  outputText.value = dict[key] || "\u7ffb\u8bd1\u7ed3\u679c: " + inputText.value + " (" + langs[fromLang.value].name + "\u2192" + langs[toLang.value].name + ")"
}
function swapLang() { const t = fromLang.value; fromLang.value = toLang.value; toLang.value = t }
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #a1c4fd, #c2e9fb); }
.custom-nav { background: linear-gradient(135deg, #0984e3, #74b9ff); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.lang-row { display: flex; align-items: center; gap: 16rpx; margin-bottom: 24rpx; }
.lang-picker { flex: 1; background: #fff; border-radius: 16rpx; padding: 20rpx; text-align: center; font-size: 28rpx; }
.swap-btn { font-size: 36rpx; color: #fff; }
.tr-input { background: #fff; border-radius: 20rpx; padding: 24rpx; font-size: 28rpx; min-height: 160rpx; margin-bottom: 24rpx; }
.tr-btn { background: linear-gradient(135deg, #0984e3, #74b9ff); border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 24rpx; }
.tr-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.tr-result { background: #fff; border-radius: 20rpx; padding: 24rpx; font-size: 28rpx; color: #333; }
</style>
