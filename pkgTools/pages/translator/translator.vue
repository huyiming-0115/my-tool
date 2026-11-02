
<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">翻译工具</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="tr-lang-bar">
        <picker class="tr-lang-picker" :value="fromIdx" :range="langs" range-key="name" @change="fromIdx=$event.detail.value">
          <text>{{langs[fromIdx].name}}</text>
        </picker>
        <view class="tr-swap" @click="swapLang">↔</view>
        <picker class="tr-lang-picker" :value="toIdx" :range="langs" range-key="name" @change="toIdx=$event.detail.value">
          <text>{{langs[toIdx].name}}</text>
        </picker>
      </view>
      <view class="tr-input-area">
        <textarea class="tr-textarea" v-model="inputText" placeholder="请输入要翻译的文本" maxlength="500" />
        <text class="tr-count">{{inputText.length}}/500</text>
      </view>
      <view class="tr-btn" @click="translate"><text>翻译</text></view>
      <view class="tr-result" v-if="outputText">
        <text class="tr-result-label">译文</text>
        <view class="tr-result-box"><text>{{outputText}}</text></view>
        <view class="tr-copy" @click="copyResult"><text>复制</text></view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const langs = [
  {name:"中文", code:"zh"}, {name:"英语", code:"en"}, {name:"日语", code:"ja"},
  {name:"韩语", code:"ko"}, {name:"法语", code:"fr"}, {name:"德语", code:"de"},
  {name:"西班牙语", code:"es"}, {name:"俄语", code:"ru"}
]
const fromIdx = ref(0)
const toIdx = ref(1)
const inputText = ref("")
const outputText = ref("")
const dict = {
  "你好": {en:"Hello", ja:"こんにちは", ko:"안녕하세요", fr:"Bonjour", de:"Hallo", es:"Hola", ru:"Здравствуйте"},
  "谢谢": {en:"Thank you", ja:"ありがとう", ko:"감사합니다", fr:"Merci", de:"Danke", es:"Gracias", ru:"Спасибо"},
  "再见": {en:"Goodbye", ja:"さようなら", ko:"안녕히 가세요", fr:"Au revoir", de:"Auf Wiedersehen", es:"Adiós", ru:"До свидания"},
  "我爱你": {en:"I love you", ja:"大好きだ", ko:"사랑해", fr:"Je t'aime", de:"Ich liebe dich", es:"Te amo", ru:"Я люблю тебя"},
  "早上好": {en:"Good morning", ja:"おはよう", ko:"좋을 아침", fr:"Bonjour", de:"Guten Morgen", es:"Buenos días", ru:"Доброе утро"}
}
function translate() {
  var text = inputText.value.trim()
  if (!text) return
  var fromCode = langs[fromIdx.value].code
  var toCode = langs[toIdx.value].code
  if (fromCode === toCode) { outputText.value = text; return }
  if (fromCode === "zh" && dict[text] && dict[text][toCode]) {
    outputText.value = dict[text][toCode]
  } else if (toCode === "zh") {
    for (var key in dict) {
      if (dict[key] && dict[key][fromCode] === text) { outputText.value = key; return }
    }
    outputText.value = "（离线词库未收录，请尝试常见词汇）"
  } else {
    outputText.value = "（离线词库仅支持中文互译）"
  }
}
function swapLang() {
  var tmp = fromIdx.value
  fromIdx.value = toIdx.value
  toIdx.value = tmp
}
function copyResult() {
  uni.setClipboardData({ data: outputText.value })
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #89f7fe, #66a6ff); }
.custom-nav { background: linear-gradient(135deg, #89f7fe, #66a6ff); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 32rpx; }
.tr-lang-bar { display: flex; align-items: center; justify-content: space-between; margin-bottom: 24rpx; }
.tr-lang-picker { flex: 1; background: rgba(255,255,255,0.3); border-radius: 16rpx; padding: 16rpx; text-align: center; }
.tr-lang-picker text { color: #fff; font-size: 28rpx; font-weight: 600; }
.tr-swap { width: 72rpx; text-align: center; color: #fff; font-size: 40rpx; }
.tr-input-area { position: relative; margin-bottom: 24rpx; }
.tr-textarea { background: rgba(255,255,255,0.3); border-radius: 20rpx; padding: 24rpx; font-size: 30rpx; color: #fff; width: 100%; box-sizing: border-box; min-height: 200rpx; }
.tr-count { position: absolute; bottom: 16rpx; right: 24rpx; color: rgba(255,255,255,0.6); font-size: 22rpx; }
.tr-btn { background: #fff; border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 24rpx; }
.tr-btn text { color: #66a6ff; font-size: 32rpx; font-weight: 700; }
.tr-result { background: rgba(255,255,255,0.2); border-radius: 20rpx; padding: 24rpx; }
.tr-result-label { color: rgba(255,255,255,0.7); font-size: 24rpx; display: block; margin-bottom: 12rpx; }
.tr-result-box { background: rgba(255,255,255,0.15); border-radius: 16rpx; padding: 20rpx; }
.tr-result-box text { color: #fff; font-size: 30rpx; line-height: 1.6; }
.tr-copy { margin-top: 12rpx; text-align: center; }
.tr-copy text { color: #fff; font-size: 26rpx; background: rgba(255,255,255,0.2); padding: 8rpx 24rpx; border-radius: 8rpx; }
</style>
