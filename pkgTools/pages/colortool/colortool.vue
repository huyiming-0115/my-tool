<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u989c\u8272\u8f6c\u6362\u5de5\u5177</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="color-preview" :style="{background: hexValue}"></view>
      <view class="form-card"><text class="form-label">HEX</text><input class="form-input" v-model="hexValue" placeholder="#3366ff" /></view>
      <view class="rgb-row">
        <view class="rgb-item"><text>R</text><input type="number" v-model="r" min="0" max="255" /></view>
        <view class="rgb-item"><text>G</text><input type="number" v-model="g" min="0" max="255" /></view>
        <view class="rgb-item"><text>B</text><input type="number" v-model="b" min="0" max="255" /></view>
      </view>
      <view class="convert-btn" @click="convert"><text>\u4e92\u8f6c</text></view>
      <view class="color-values">
        <text class="cv-item">HEX: {{ hexValue }}</text>
        <text class="cv-item">RGB: rgb({{ r }}, {{ g }}, {{ b }})</text>
        <text class="cv-item">HSL: hsl({{ h }}, {{ s }}%, {{ l }}%)</text>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const hexValue = ref("#3366ff")
const r = ref(51)
const g = ref(102)
const b = ref(255)
const h = ref(225)
const s = ref(100)
const l = ref(60)
function convert() {
  let hex = hexValue.value.replace("#", "")
  if (hex.length === 3) hex = hex[0]+hex[0]+hex[1]+hex[1]+hex[2]+hex[2]
  if (hex.length !== 6) { uni.showToast({ title: "\u65e0\u6548HEX", icon: "none" }); return }
  r.value = parseInt(hex.substr(0,2), 16)
  g.value = parseInt(hex.substr(2,2), 16)
  b.value = parseInt(hex.substr(4,2), 16)
  const rn = r.value/255, gn = g.value/255, bn = b.value/255
  const max = Math.max(rn,gn,bn), min = Math.min(rn,gn,bn)
  let hh = 0
  if (max === min) hh = 0
  else if (max === rn) hh = ((gn-bn)/(max-min)) % 6
  else if (max === gn) hh = (bn-rn)/(max-min) + 2
  else hh = (rn-gn)/(max-min) + 4
  hh = Math.round(hh * 60)
  if (hh < 0) hh += 360
  const ll = (max+min)/2
  const ss = max === min ? 0 : ll > 0.5 ? (2*max-2*min)/(2-2*ll) : (2*max-2*min)/(2*ll)
  h.value = hh; s.value = Math.round(ss*100); l.value = Math.round(ll*100)
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }; convert() })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #2d3436, #636e72); }
.custom-nav { background: linear-gradient(135deg, #2d3436, #636e72); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.color-preview { width: 100%; height: 200rpx; border-radius: 20rpx; margin-bottom: 24rpx; border: 4rpx solid rgba(255,255,255,0.2); }
.form-card { background: rgba(255,255,255,0.1); border-radius: 20rpx; padding: 24rpx; margin-bottom: 20rpx; }
.form-label { font-size: 26rpx; color: rgba(255,255,255,0.7); display: block; margin-bottom: 12rpx; }
.form-input { font-size: 32rpx; color: #fff; font-weight: 600; }
.rgb-row { display: flex; gap: 16rpx; margin-bottom: 20rpx; }
.rgb-item { flex: 1; background: rgba(255,255,255,0.1); border-radius: 16rpx; padding: 16rpx; text-align: center; }
.rgb-item text { font-size: 24rpx; color: rgba(255,255,255,0.7); display: block; }
.rgb-item input { color: #fff; font-size: 28rpx; font-weight: 600; }
.convert-btn { background: linear-gradient(135deg, #0984e3, #74b9ff); border-radius: 16rpx; padding: 20rpx; text-align: center; margin-bottom: 24rpx; }
.convert-btn text { color: #fff; font-size: 28rpx; font-weight: 600; }
.color-values { background: rgba(255,255,255,0.1); border-radius: 16rpx; padding: 20rpx; }
.cv-item { display: block; font-size: 24rpx; color: rgba(255,255,255,0.8); padding: 8rpx 0; font-family: monospace; }
</style>
