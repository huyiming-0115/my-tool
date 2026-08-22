<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">节拍器</text><text class="nav-icon" @click="togglePlay">{{ playing ? "⏸" : "⏵" }}</text></view>
    </view>
    <view class="content">
      <view class="metro-display"><text class="bpm-val">{{ bpm }}</text><text class="bpm-label">BPM</text></view>
      <view class="metro-dot" :class="{ beat: beatActive }"></view>
      <view class="slider-row"><text class="slider-label">40</text><slider class="slider" :value="bpm" min="40" max="200" @change="bpm = $event.detail.value" block-size="20" /><text class="slider-label">200</text></view>
      <view class="quick-btns"><text class="qb" @click="bpm = 60">Largo</text><text class="qb" @click="bpm = 80">Andante</text><text class="qb" @click="bpm = 120">Allegro</text><text class="qb" @click="bpm = 160">Presto</text></view>
      <view class="play-btn" :class="{ playing }" @click="togglePlay"><text>{{ playing ? "停止" : "开始" }}</text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, watch, onUnmounted, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const bpm = ref(120)
const playing = ref(false)
const beatActive = ref(false)
var timer = null
function togglePlay() {
  playing.value = !playing.value
  if (playing.value) { startBeat() } else { clearInterval(timer); beatActive.value = false }
}
function startBeat() {
  clearInterval(timer)
  var interval = 60000 / bpm.value
  timer = setInterval(function() { beatActive.value = true; uni.vibrateShort({}); setTimeout(function() { beatActive.value = false }, 100) }, interval)
}
watch(bpm, function() { if (playing.value) startBeat() })
onUnmounted(function() { clearInterval(timer) })
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #00cec9, #81ecec); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 44rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; display: flex; flex-direction: column; align-items: center; }
.metro-display { text-align: center; margin-bottom: 32rpx; }
.bpm-val { font-size: 96rpx; font-weight: 700; color: #00cec9; display: block; }
.bpm-label { font-size: 24rpx; color: #999; }
.metro-dot { width: 60rpx; height: 60rpx; border-radius: 50%; background: #dfe6e9; margin-bottom: 32rpx; transition: background 0.1s; }
.metro-dot.beat { background: #00cec9; box-shadow: 0 0 20rpx #00cec9; }
.slider-row { display: flex; align-items: center; width: 100%; margin-bottom: 24rpx; }
.slider-label { font-size: 24rpx; color: #999; width: 60rpx; text-align: center; }
.slider { flex: 1; }
.quick-btns { display: flex; gap: 12rpx; width: 100%; margin-bottom: 32rpx; }
.qb { flex: 1; text-align: center; padding: 16rpx; background: #fff; border-radius: 12rpx; font-size: 24rpx; color: #666; }
.play-btn { width: 80%; background: linear-gradient(135deg, #00cec9, #81ecec); border-radius: 16rpx; padding: 28rpx; text-align: center; }
.play-btn text { font-size: 32rpx; color: #fff; font-weight: 600; }
.play-btn.playing { background: linear-gradient(135deg, #e17055, #d63031); }
</style>