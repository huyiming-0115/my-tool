<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u968f\u673a\u51b3\u5b9a\u5668</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="wheel-container">
        <view class="wheel" :style="{transform: 'rotate('+rotation+'deg)', transition: spinning?'2s ease-out':'none'}">
          <view class="wheel-section" v-for="(opt, i) in options" :key="i" :style="{transform: 'rotate('+(i*360/options.length)+'deg)', background: wheelColors[i%wheelColors.length]}">
            <text class="wheel-text">{{ opt }}</text>
          </view>
        </view>
        <view class="wheel-pointer">\u25b2</view>
      </view>
      <text class="result-text" v-if="result">{{ result }}</text>
      <view class="spin-btn" @click="spin"><text>{{ spinning ? '\u8f6c\u52a8\u4e2d...' : '\u5f00\u59cb\u8f6c\u52a8' }}</text></view>
      <view class="options-edit">
        <text class="section-title">\u9009\u9879 (\u6bcf\u884c\u4e00\u4e2a)</text>
        <textarea class="opt-input" v-model="optionsText" placeholder="\u8f93\u5165\u9009\u9879" auto-height></textarea>
        <text class="save-btn" @click="saveOptions">\u4fdd\u5b58</text>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const defaultOpts = ["\u662f","\u5426","\u518d\u60f3\u60f3","\u5f53\u7136","\u4e0d\u884c","\u53ef\u4ee5"]
const options = ref(defaultOpts.slice())
const optionsText = ref(defaultOpts.join("\n"))
const rotation = ref(0)
const spinning = ref(false)
const result = ref("")
const wheelColors = ["#ff6b6b","#feca57","#48dbfb","#ff9ff3","#54a0ff","#5f27cd","#00d2d3","#ff9f43"]
function spin() {
  if (spinning.value) return
  spinning.value = true
  result.value = ""
  const spins = 5 + Math.random() * 5
  const idx = Math.floor(Math.random() * options.value.length)
  rotation.value += spins * 360 + (360 - idx * (360 / options.value.length))
  setTimeout(function() {
    spinning.value = false
    result.value = "\u2728 " + options.value[idx]
    uni.vibrateShort({})
  }, 2000)
}
function saveOptions() {
  const arr = optionsText.value.split("\n").map(function(s){return s.trim()}).filter(function(s){return s})
  if (arr.length < 2) { uni.showToast({ title: "\u81f3\u5c112\u4e2a\u9009\u9879", icon: "none" }); return }
  options.value = arr
  uni.showToast({ title: "\u5df2\u4fdd\u5b58", icon: "success" })
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #f6d365, #fda085); }
.custom-nav { background: linear-gradient(135deg, #f39c12, #e17055); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; display: flex; flex-direction: column; align-items: center; }
.wheel-container { position: relative; width: 500rpx; height: 500rpx; margin-bottom: 32rpx; }
.wheel { width: 100%; height: 100%; border-radius: 50%; position: relative; overflow: hidden; border: 8rpx solid #fff; box-shadow: 0 8rpx 32rpx rgba(0,0,0,0.2); }
.wheel-section { position: absolute; width: 50%; height: 50%; top: 0; left: 50%; transform-origin: 0 100%; display: flex; align-items: flex-start; justify-content: center; padding-top: 40rpx; }
.wheel-text { font-size: 22rpx; color: #fff; font-weight: 700; }
.wheel-pointer { position: absolute; top: -20rpx; left: 50%; transform: translateX(-50%); font-size: 40rpx; color: #e17055; }
.result-text { font-size: 40rpx; font-weight: 700; color: #fff; margin-bottom: 24rpx; }
.spin-btn { width: 80%; background: linear-gradient(135deg, #f39c12, #e17055); border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 32rpx; }
.spin-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.options-edit { width: 100%; background: rgba(255,255,255,0.3); border-radius: 20rpx; padding: 24rpx; }
.section-title { font-size: 26rpx; color: #fff; display: block; margin-bottom: 12rpx; }
.opt-input { width: 100%; background: #fff; border-radius: 12rpx; padding: 16rpx; font-size: 26rpx; min-height: 120rpx; margin-bottom: 12rpx; }
.save-btn { display: block; background: #f39c12; color: #fff; text-align: center; border-radius: 12rpx; padding: 16rpx; font-size: 26rpx; }
</style>
