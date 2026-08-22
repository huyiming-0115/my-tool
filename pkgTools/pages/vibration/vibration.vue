<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u9707\u52a8\u9a6c\u8fbe</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <text class="section-title">\u9009\u62e9\u6a21\u5f0f</text>
      <view class="vib-grid">
        <view class="vib-card" v-for="(p, i) in patterns" :key="i" :class="{ active: selected === i }" @click="selected = i">
          <text class="vib-emoji">{{ p.emoji }}</text>
          <text class="vib-name">{{ p.name }}</text>
        </view>
      </view>
      <view class="vib-btn" @click="startVib" v-if="selected >= 0">
        <text>{{ vibing ? '\u9707\u52a8\u4e2d...' : '\u5f00\u59cb\u9707\u52a8' }}</text>
      </view>
      <view class="custom-section">
        <text class="section-title">\u81ea\u5b9a\u4e49\u6a21\u5f0f (\u6bcf\u884c\u4e00\u4e2a\uff0c\u5355\u4f4dms)</text>
        <textarea class="vib-input" v-model="customPattern" placeholder="\u5982:\n500\n200\n500\n200\n1000" auto-height></textarea>
        <view class="vib-btn custom" @click="startCustom"><text>\u64ad\u653e\u81ea\u5b9a\u4e49</text></view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const selected = ref(-1)
const vibing = ref(false)
const customPattern = ref("")
const patterns = [
  { emoji: "\u26a1", name: "\u77ed\u4fc3", pattern: [100] },
  { emoji: "\U0001f50b", name: "\u8fde\u7eed", pattern: [200, 100, 200] },
  { emoji: "\u2764\ufe0f", name: "\u5fc3\u8df3", pattern: [300, 150, 300, 150, 600] },
  { emoji: "\U0001f514", name: "\u94c3\u58f0", pattern: [500, 200, 500] },
  { emoji: "\U0001f680", name: "\u52a0\u901f", pattern: [100, 50, 100, 50, 100, 50, 300] },
  { emoji: "\u23f0", name: "\u50ac\u4fc3", pattern: [100, 100, 100, 100, 100, 100, 500] }
]
function startVib() {
  if (selected.value < 0) return
  vibing.value = true
  const pat = patterns[selected.value].pattern
  let i = 0
  function next() {
    if (i >= pat.length) { vibing.value = false; return }
    if (i % 2 === 0) uni.vibrateLong({})
    else uni.vibrateShort({})
    i++
    setTimeout(next, pat[i-1])
  }
  next()
}
function startCustom() {
  const arr = customPattern.value.split("\n").map(function(s){return parseInt(s.trim())}).filter(function(n){return n > 0})
  if (arr.length === 0) { uni.showToast({ title: "\u8bf7\u8f93\u5165\u6709\u6548\u6a21\u5f0f", icon: "none" }); return }
  vibing.value = true
  let i = 0
  function next() {
    if (i >= arr.length) { vibing.value = false; return }
    if (i % 2 === 0) uni.vibrateLong({})
    else uni.vibrateShort({})
    i++
    setTimeout(next, arr[i-1])
  }
  next()
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #f093fb, #f5576c); }
.custom-nav { background: linear-gradient(135deg, #e84393, #fd79a8); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.section-title { font-size: 28rpx; color: rgba(255,255,255,0.9); display: block; margin-bottom: 16rpx; }
.vib-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16rpx; margin-bottom: 32rpx; }
.vib-card { background: rgba(255,255,255,0.2); border-radius: 20rpx; padding: 24rpx; text-align: center; }
.vib-card.active { background: #fff; }
.vib-emoji { font-size: 48rpx; display: block; margin-bottom: 8rpx; }
.vib-name { font-size: 24rpx; color: #fff; }
.vib-card.active .vib-name { color: #e84393; }
.vib-btn { background: linear-gradient(135deg, #e84393, #fd79a8); border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 24rpx; }
.vib-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.vib-btn.custom { background: rgba(255,255,255,0.3); }
.custom-section { background: rgba(255,255,255,0.2); border-radius: 20rpx; padding: 24rpx; }
.vib-input { width: 100%; background: #fff; border-radius: 12rpx; padding: 16rpx; font-size: 26rpx; min-height: 120rpx; margin-bottom: 16rpx; }
</style>
