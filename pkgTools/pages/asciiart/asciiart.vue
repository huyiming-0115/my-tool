<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">ASCII\u827a\u672f\u751f\u6210</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="form-card"><text class="form-label">\u8f93\u5165\u6587\u5b57</text><input class="form-input" v-model="text" placeholder="HELLO" maxlength="10" /></view>
      <view class="gen-btn" @click="generate"><text>\u751f\u6210</text></view>
      <view class="result-card" v-if="asciiResult">
        <scroll-view class="ascii-scroll" scroll-x><text class="ascii-text">{{ asciiResult }}</text></-scroll-view>
        <text class="copy-btn" @click="copyText">\u590d\u5236</text>
      </view>
      <view class="preset-card"><text class="preset-title">\u5feb\u6377\u9009\u62e9</text><view class="preset-grid"><text class="preset-item" v-for="(p, i) in presets" :key="i" @click="text=p; generate()">{{ p }}</text></view></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const text = ref("HI")
const asciiResult = ref("")
const presets = ["HI","LOVE","COOL","YES","NO","OK","CAT","DOG","STAR","HEART"]
const font = {
  "A":"  ##  #  ######  #    #  #    #","B":"#####  #    #  #####  #    #  #####",
  "C":" ##### #      #      #      #####","D":"#####  #    #  #    #  #    #  #####",
  "E":"###### #      #####  #      ######","F":"###### #      #####  #      #     ",
  "G":" ##### #      #  #### #    #  #### ","H":"#    # #    # ###### #    # #    #",
  "I":"######    #      #      #    ######","J":"     #      #      # #    #  #### ",
  "K":"#    # #  #   ##    #  #   #    #","L":"#      #      #      #      ######",
  "M":"#    # ##  ## # ## # #    # #    #","N":"#    # ##   # # #  # #  # # #   ##",
  "O":" ####  #    # #    # #    #  #### ","P":"#####  #    # #####  #      #     ",
  "Q":" ####  #    # #  # # #  #  #### #","R":"#####  #    # #####  #  #   #    #",
  "S":" ##### #      ####       # ##### ","T":"######    #      #      #      #  ",
  "U":"#    # #    # #    # #    #  #### ","V":"#    # #    # #    #  #  #    ##  ",
  "W":"#    # #    # # ## # ##  ## #    #","X":"#    #  #  #    ##    #  #  #    #",
  "Y":"#    #  #  #    ##     #      #   ","Z":"######     #    #    #    ######",
  "0":" ####  #   ## #  # # #   #  #### ","1":"  #    ##     #     #     #   ###",
  "2":" ####      #  ####  #      ######","3":" ####      #  ###       #  #### ",
  "4":"#   #  #   #  ######     #     # ","5":"###### #      #####      # ##### ",
  "6":" ####  #      ###### #    #  ####","7":"######     #    #    #    #    # ",
  "8":" ####  #    #  ####  #    #  ####","9":" ####  #    #  #####     #  ####",
  " ":"          "
}
function generate() {
  var t = text.value.toUpperCase()
  if (!t) { uni.showToast({ title: "\u8bf7\u8f93\u5165\u6587\u5b57", icon: "none" }); return }
  var lines = ["","","","","",""]
  for (var i = 0; i < t.length; i++) {
    var ch = font[t[i]] || font[" "]
    for (var j = 0; j < 6; j++) { lines[j] += ch.substr(j * 6, 6) + "  " }
  }
  asciiResult.value = lines.join("\n")
}
function copyText() { uni.setClipboardData({ data: asciiResult.value, success: function() { uni.showToast({ title: "\u5df2\u590d\u5236", icon: "success" }) } }) }
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }; generate() })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #1a1a2e, #16213e); }
.custom-nav { background: linear-gradient(135deg, #1a1a2e, #16213e); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.form-card { background: rgba(255,255,255,0.1); border-radius: 20rpx; padding: 24rpx; margin-bottom: 20rpx; }
.form-label { font-size: 26rpx; color: rgba(255,255,255,0.7); display: block; margin-bottom: 12rpx; }
.form-input { font-size: 32rpx; color: #fff; font-weight: 600; }
.gen-btn { background: linear-gradient(135deg, #00b894, #00cec9); border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 32rpx; }
.gen-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.result-card { background: rgba(255,255,255,0.1); border-radius: 20rpx; padding: 24rpx; margin-bottom: 24rpx; }
.ascii-scroll { max-height: 400rpx; }
.ascii-text { font-size: 16rpx; color: #00ff88; font-family: monospace; line-height: 1.2; white-space: pre; }
.copy-btn { display: block; background: #00b894; color: #fff; text-align: center; border-radius: 12rpx; padding: 16rpx; margin-top: 16rpx; font-size: 26rpx; }
.preset-card { background: rgba(255,255,255,0.05); border-radius: 16rpx; padding: 20rpx; }
.preset-title { font-size: 24rpx; color: rgba(255,255,255,0.6); display: block; margin-bottom: 12rpx; }
.preset-grid { display: flex; flex-wrap: wrap; gap: 8rpx; }
.preset-item { padding: 12rpx 20rpx; background: rgba(255,255,255,0.1); border-radius: 8rpx; color: #fff; font-size: 22rpx; }
</style>
