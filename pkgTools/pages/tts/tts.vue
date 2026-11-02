
<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">文字转语音</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="tts-card">
        <text class="tts-label">输入文本</text>
        <textarea class="tts-textarea" v-model="text" placeholder="输入要转换为语音的文字..." maxlength="500" />
        <text class="tts-count">{{text.length}}/500</text>
      </view>
      <view class="tts-card">
        <text class="tts-label">语音设置</text>
        <view class="tts-setting">
          <text class="tts-setting-label">语速 {{rate}}</text>
          <slider class="tts-slider" :value="rate" min="0.5" max="2" step="0.1" show-value @change="rate=parseFloat($event.detail.value.toFixed(1))" />
        </view>
        <view class="tts-setting">
          <text class="tts-setting-label">音调 {{pitch}}</text>
          <slider class="tts-slider" :value="pitch" min="0.5" max="2" step="0.1" show-value @change="pitch=parseFloat($event.detail.value.toFixed(1))" />
        </view>
        <view class="tts-setting">
          <text class="tts-setting-label">音量 {{volume}}</text>
          <slider class="tts-slider" :value="volume" min="0" max="1" step="0.1" show-value @change="volume=parseFloat($event.detail.value.toFixed(1))" />
        </view>
      </view>
      <view class="tts-controls">
        <view class="tts-btn" :class="{disabled: !text || speaking}" @click="speak">{{speaking ? "播放中..." : "播放"}}</view>
        <view class="tts-btn stop" @click="stop">停止</view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted, onUnmounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const text = ref("")
const rate = ref(1)
const pitch = ref(1)
const volume = ref(1)
const speaking = ref(false)
const innerAudioContext = ref(null)
function speak() {
  if (!text.value || speaking.value) return
  speaking.value = true
  if (innerAudioContext.value) {
    innerAudioContext.value.destroy()
  }
  var ctx = uni.createInnerAudioContext()
  innerAudioContext.value = ctx
  ctx.src = "https://tts.baidu.com/text2audio?tex=" + encodeURIComponent(text.value) + "&cuid=baidu_speech_demo&lan=zh&ctp=1&pdt=1&spd=" + Math.round(rate.value * 5) + "&pit=" + Math.round(pitch.value * 5) + "&vol=" + Math.round(volume.value * 10)
  ctx.onError(function() {
    speaking.value = false
    uni.showToast({ title: "播放失败", icon: "none" })
  })
  ctx.onEnded(function() { speaking.value = false })
  ctx.play()
}
function stop() {
  if (innerAudioContext.value) {
    innerAudioContext.value.stop()
    speaking.value = false
  }
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
onUnmounted(function() { if (innerAudioContext.value) innerAudioContext.value.destroy() })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #a18cd1, #fbc2eb); }
.custom-nav { background: linear-gradient(135deg, #a18cd1, #fbc2eb); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 32rpx; }
.tts-card { background: rgba(255,255,255,0.2); border-radius: 20rpx; padding: 24rpx; margin-bottom: 20rpx; position: relative; }
.tts-label { color: rgba(255,255,255,0.8); font-size: 26rpx; display: block; margin-bottom: 12rpx; }
.tts-textarea { background: rgba(255,255,255,0.2); border-radius: 12rpx; padding: 16rpx 20rpx; font-size: 28rpx; color: #fff; width: 100%; box-sizing: border-box; min-height: 160rpx; }
.tts-count { position: absolute; bottom: 36rpx; right: 44rpx; color: rgba(255,255,255,0.5); font-size: 22rpx; }
.tts-setting { margin-bottom: 16rpx; }
.tts-setting-label { color: rgba(255,255,255,0.8); font-size: 26rpx; display: block; margin-bottom: 8rpx; }
.tts-slider { width: 100%; }
.tts-controls { display: flex; gap: 20rpx; margin-top: 24rpx; }
.tts-btn { flex: 1; background: #fff; border-radius: 16rpx; padding: 24rpx; text-align: center; }
.tts-btn text { color: #a18cd1; font-size: 32rpx; font-weight: 700; }
.tts-btn.disabled { opacity: 0.5; }
.tts-btn.stop { background: rgba(255,255,255,0.3); }
.tts-btn.stop text { color: #fff; }
</style>
