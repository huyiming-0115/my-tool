<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u6587\u672c\u52a0\u5bc6\u89e3\u5bc6</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="mode-tabs"><text class="mode-tab" :class="{active: mode==='encrypt'}" @click="mode='encrypt'">\u52a0\u5bc6</text><text class="mode-tab" :class="{active: mode==='decrypt'}" @click="mode='decrypt'">\u89e3\u5bc6</text></view>
      <view class="form-card"><text class="form-label">\u7b97\u6cd5</text><picker class="algo-picker" :range="algorithms" @change="algo=$event.detail.value"><text>{{ algorithms[algo] }} \u25bc</text></picker></view>
      <view class="form-card" v-if="algo===3"><text class="form-label">\u5bc6\u94a5</text><input class="form-input" v-model="key" placeholder="\u8f93\u5165\u5bc6\u94a5" /></view>
      <view class="form-card"><text class="form-label">{{ mode==='encrypt'?'\u660e\u6587':'\u5bc6\u6587' }}</text><textarea class="te-input" v-model="inputText" placeholder="\u8f93\u5165\u6587\u672c" auto-height></textarea></view>
      <view class="calc-btn" @click="process"><text>{{ mode==='encrypt'?'\u52a0\u5bc6':'\u89e3\u5bc6' }}</text></view>
      <view class="result-card" v-if="outputText"><text class="result-label">{{ mode==='encrypt'?'\u5bc6\u6587':'\u660e\u6587' }}</text><textarea class="result-area" :value="outputText" disabled></textarea><text class="copy-btn" @click="copyText">\u590d\u5236</text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const mode = ref("encrypt")
const algo = ref(0)
const key = ref("3")
const inputText = ref("")
const outputText = ref("")
const algorithms = ["Base64","URL\u7f16\u7801","\u641c\u9f3b\u9f3b\u7801","\u51ef\u6492\u5bc6\u7801","\u6469\u65af\u7535\u7801"]
function caesar(text, shift, decrypt) {
  if (decrypt) shift = -shift
  return text.split("").map(function(c) {
    if (c.match(/[a-z]/)) return String.fromCharCode((c.charCodeAt(0)-97+shift+26)%26+97)
    if (c.match(/[A-Z]/)) return String.fromCharCode((c.charCodeAt(0)-65+shift+26)%26+65)
    return c
  }).join("")
}
function morse(text, decrypt) {
  var map = {a:".-",b:"-...",c:"-.-.",d:"-..",e:".",f:"..-.",g:"--.",h:"....",i:"..",j:".---",k:"-.-",l:".-..",m:"--",n:"-.",o:"---",p:".--.",q:"--.-",r:".-.",s:"...",t:"-",u:"..-",v:"...-",w:".--",x:"-..-",y:"-.--",z:"--..","0":"-----","1":".----","2":"..---","3":"...--","4":"....-","5":"....-","6":"-...","7":"--...","8":"---..","9":"----."," ":"/"}
  var rev = {}; Object.keys(map).forEach(function(k){ rev[map[k]]=k })
  if (decrypt) return text.split(" ").map(function(c){ return rev[c]||c }).join("")
  return text.toLowerCase().split("").map(function(c){ return map[c]||c }).join(" ")
}
function process() {
  if (!inputText.value) { uni.showToast({ title: "\u8bf7\u8f93\u5165\u6587\u672c", icon: "none" }); return }
  var t = inputText.value
  if (algo.value === 0) outputText.value = mode.value === "encrypt" ? btoa(unescape(encodeURIComponent(t))) : decodeURIComponent(escape(atob(t)))
  else if (algo.value === 1) outputText.value = mode.value === "encrypt" ? encodeURIComponent(t) : decodeURIComponent(t)
  else if (algo.value === 2) outputText.value = mode.value === "encrypt" ? btoa(unescape(encodeURIComponent(t))) : decodeURIComponent(escape(atob(t)))
  else if (algo.value === 3) outputText.value = caesar(t, parseInt(key.value)||3, mode.value === "decrypt")
  else outputText.value = morse(t, mode.value === "decrypt")
}
function copyText() { uni.setClipboardData({ data: outputText.value, success: function() { uni.showToast({ title: "\u5df2\u590d\u5236", icon: "success" }) } }) }
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #1a1a2e, #16213e); }
.custom-nav { background: linear-gradient(135deg, #1a1a2e, #16213e); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.mode-tabs { display: flex; gap: 16rpx; margin-bottom: 24rpx; }
.mode-tab { flex: 1; text-align: center; padding: 20rpx; border-radius: 16rpx; background: rgba(255,255,255,0.2); color: #fff; font-size: 26rpx; }
.mode-tab.active { background: #fff; color: #1a1a2e; }
.form-card { background: rgba(255,255,255,0.1); border-radius: 20rpx; padding: 24rpx; margin-bottom: 20rpx; }
.form-label { font-size: 26rpx; color: rgba(255,255,255,0.7); display: block; margin-bottom: 12rpx; }
.form-input { font-size: 28rpx; color: #fff; background: rgba(255,255,255,0.1); border-radius: 12rpx; padding: 16rpx; }
.algo-picker { background: rgba(255,255,255,0.1); border-radius: 12rpx; padding: 16rpx; color: #fff; font-size: 26rpx; }
.te-input { background: rgba(255,255,255,0.1); border-radius: 12rpx; padding: 16rpx; font-size: 26rpx; color: #fff; min-height: 120rpx; }
.calc-btn { background: linear-gradient(135deg, #00b894, #00cec9); border-radius: 16rpx; padding: 24rpx; text-align: center; margin: 32rpx 0; }
.calc-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.result-card { background: rgba(255,255,255,0.1); border-radius: 20rpx; padding: 24rpx; }
.result-label { font-size: 24rpx; color: rgba(255,255,255,0.6); display: block; margin-bottom: 8rpx; }
.result-area { width: 100%; min-height: 100rpx; background: rgba(0,0,0,0.3); border-radius: 12rpx; padding: 16rpx; font-size: 24rpx; color: #fff; }
.copy-btn { display: block; background: #00b894; color: #fff; text-align: center; border-radius: 12rpx; padding: 16rpx; margin-top: 16rpx; font-size: 26rpx; }
</style>
