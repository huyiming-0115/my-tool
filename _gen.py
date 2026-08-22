# -*- coding: utf-8 -*-
import os, json

base = "pkgTools/pages"

def w(name, content):
    path = os.path.join(base, name, name + ".vue")
    with open(path, "w") as f:
        f.write(content)
    print("OK:", name)

# ===== ledscroll =====
w("ledscroll", """<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\\u2190</text><text class="nav-title">\\u624b\\u6301\\u5f39\\u5e55</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <input class="ls-input" v-model="text" placeholder="\\u8f93\\u5165\\u5f39\\u5e55\\u6587\\u5b57" maxlength="50" />
      <view class="opts-row"><text class="opt-label">\\u5b57\\u4f53\\u989c\\u8272:</text><view class="color-dot" v-for="c in colors" :key="c" :style="{background:c, border: fontColor===c?'4rpx solid #333':'none'}" @click="fontColor=c"></view></view>
      <view class="opts-row"><text class="opt-label">\\u80cc\\u666f:</text><view class="color-dot" v-for="c in bgColors" :key="c" :style="{background:c, border: bgColor===c?'4rpx solid #333':'none'}" @click="bgColor=c"></view></view>
      <view class="opts-row"><text class="opt-label">\\u901f\\u5ea6:</text><slider class="ls-slider" :value="speed" min="1" max="10" show-value @change="speed=Number($event.detail.value)"/></view>
      <view class="ls-btn" @click="showLed=true"><text>\\u5f00\\u59cb\\u5f39\\u5e55</text></view>
    </view>
    <view class="led-fullscreen" v-if="showLed" :style="{background: bgColor}">
      <view class="led-scroll-container" :style="{animationDuration: (11-speed)*0.3+'s'}">
        <text class="led-text" :style="{color: fontColor, textShadow: '0 0 20rpx '+fontColor}">{{ text || '\\u6b22\\u8fce\\u4f7f\\u7528' }}</text>
      </view>
      <view class="led-close" @click="showLed=false">\\u00d7</view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const text = ref("")
const speed = ref(5)
const fontColor = ref("#00ff00")
const bgColor = ref("#000000")
const showLed = ref(false)
const colors = ["#00ff00","#ff0000","#ffff00","#00ffff","#ff00ff","#ffffff","#ff8800"]
const bgColors = ["#000000","#000088","#008800","#880000","#440044"]
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #0f0c29, #302b63); }
.custom-nav { background: linear-gradient(135deg, #0f0c29, #302b63); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.ls-input { background: rgba(255,255,255,0.1); border-radius: 16rpx; padding: 20rpx 24rpx; font-size: 28rpx; color: #fff; margin-bottom: 24rpx; }
.opts-row { display: flex; align-items: center; gap: 16rpx; margin-bottom: 20rpx; flex-wrap: wrap; }
.opt-label { color: rgba(255,255,255,0.7); font-size: 26rpx; }
.color-dot { width: 48rpx; height: 48rpx; border-radius: 50%; }
.ls-slider { flex: 1; }
.ls-btn { background: linear-gradient(135deg, #00b894, #00cec9); border-radius: 16rpx; padding: 24rpx; text-align: center; margin-top: 32rpx; }
.ls-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.led-fullscreen { position: fixed; inset: 0; z-index: 9999; display: flex; align-items: center; justify-content: center; overflow: hidden; }
.led-scroll-container { animation: ledScroll linear infinite; white-space: nowrap; }
.led-text { font-size: 80rpx; font-weight: 900; letter-spacing: 8rpx; }
@keyframes ledScroll { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
.led-close { position: absolute; top: 40rpx; right: 40rpx; font-size: 60rpx; color: rgba(255,255,255,0.5); z-index: 10000; }
</style>
""")