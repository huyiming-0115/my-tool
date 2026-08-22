<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u6587\u5b57\u8f6c\u8bed\u97f3</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <textarea class="tts-input" v-model="text" placeholder="\u8f93\u5165\u8981\u8f6c\u5316\u4e3a\u8bed\u97f3\u7684\u6587\u5b57" auto-height></textarea>
      <view class="tts-controls">
        <view class="ctrl-row"><text class="ctrl-label">\u8bed\u8a00:</text><picker class="ctrl-picker" :range="langs" @change="lang=$event.detail.value"><text>{{ langs[lang] }} \u25bc</text></picker></view>
        <view class="ctrl-row"><text class="ctrl-label">\u901f\u5ea6: {{ speed }}</text><slider class="ctrl-slider" :value="speed" min="0.5" max="2" step="0.1" show-value @change="speed=Number($event.detail.value)"/></view>
        <view class="ctrl-row"><text class="ctrl-label">\u97f3\u8c03: {{ pitch }}</text><slider class="ctrl-slider" :value="pitch" min="0" max="2" step="0.1" show-value @change="pitch=Number($event.detail.value)"/></view>
      </view>
      <view class="tts-btn" @click="speak"><text>{{ speaking ? '\u64ad\u653e\u4e2d...' : '\u25b6 \u64ad\u653e' }}</text></view>
      <view class="tts-btn stop" v-if="speaking" @click="stop"><text>\u25a0 \u505c\u6b62</text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const text = ref("")
const lang = ref(0)
const speed = ref(1)
const pitch = ref(1)
const speaking = ref(false)
const langs = ["\u4e2d\u6587", "\u82f1\u6587", "\u65e5\u6587"]
function speak() {
  if (!text.value.trim()) { uni.showToast({ title: "\u8bf7\u8f93\u5165\u6587\u5b57", icon: "none" }); return }
  speaking.value = true
  const ctx = uni.createInnerAudioContext()
  ctx.src = "https://tts.baidu.com/text2audio?tex=" + encodeURIComponent(text.value) + "&cuid=baike&ctp=1&lan=zh&spd=" + Math.round(speed.value * 5) + "&pit=" + Math.round(pitch.value * 5) &vol=9&per=0"
  ctx.onEnded(function() { speaking.value = false; ctx.destroy() })
  ctx.onError(function() { speaking.value = false; uni.showToast({ title: "\u64ad\u653e\u5931\u8d25", icon: "none" }); ctx.destroy() })
  ctx.play()
}
function stop() {
  speaking.value = false
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #a1c4fd, #c2e9fb); }
.custom-nav { background: linear-gradient(135deg, #6c5ce7, #a29bfe); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.tts-input { background: #fff; border-radius: 20rpx; padding: 24rpx; font-size: 28rpx; min-height: 160rpx; margin-bottom: 24rpx; }
.tts-controls { background: #fff; border-radius: 20rpx; padding: 24rpx; margin-bottom: 24rpx; }
.ctrl-row { display: flex; align-items: center; gap: 16rpx; margin-bottom: 16rpx; }
.ctrl-label { font-size: 26rpx; color: #666; min-width: 100rpx; }
.ctrl-picker { flex: 1; background: #f8f8f8; border-radius: 12rpx; padding: 12rpx 16rpx; font-size: 26rpx; }
.ctrl-slider { flex: 1; }
.tts-btn { background: linear-gradient(135deg, #6c5ce7, #a29bfe); border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 16rpx; }
.tts-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.tts-btn.stop { background: #e17055; }
</style>
