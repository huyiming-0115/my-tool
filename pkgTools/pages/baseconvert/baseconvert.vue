<template>
  <view class="bc-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">进制转换</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="input-card">
        <view class="form-row"><text class="form-l">输入数值</text><input class="form-input" v-model="inputVal" placeholder="输入数字" /></view>
        <view class="form-row"><text class="form-l">输入进制</text>
          <view class="base-btns"><text class="base-btn" :class="{ active: fromBase === 2 }" @click="fromBase = 2; convert()">2</text><text class="base-btn" :class="{ active: fromBase === 8 }" @click="fromBase = 8; convert()">8</text><text class="base-btn" :class="{ active: fromBase === 10 }" @click="fromBase = 10; convert()">10</text><text class="base-btn" :class="{ active: fromBase === 16 }" @click=" fromBase = 16; convert()">16</text></view>
        </view>
      </view>
      <view class="result-card">
        <view class="res-item"><text class="res-base">二进制 (BIN)</text><text class="res-val" @click="copy(results.bin)">{{ results.bin }}</text></view>
        <view class="res-item"><text class="res-base">八进制 (OCT)</text><text class="res-val" @click="copy(results.oct)">{{ results.oct }}</text></view>
        <view class="res-item"><text class="res-base">十进制 (DEC)</text><text class="res-val" @click="copy(results.dec)">{{ results.dec }}</text></view>
        <view class="res-item"><text class="res-base">十六进制 (HEX)</text><text class="res-val" @click="copy(results.hex)">{{ results.hex }}</text></view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, reactive, watch, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const inputVal = ref("")
const fromBase = ref(10)
const results = reactive({ bin: "0", oct: "0", dec: "0", hex: "0" })
function convert() {
  try {
    const dec = parseInt(inputVal.value || "0", fromBase.value)
    if (isNaN(dec)) { results.bin = results.oct = results.dec = results.hex = "Error"; return }
    results.bin = dec.toString(2)
    results.oct = dec.toString(8)
    results.dec = dec.toString(10)
    results.hex = dec.toString(16).toUpperCase()
  } catch (e) { results.bin = results.oct = results.dec = results.hex = "Error" }
}
watch(inputVal, convert)
function copy(v) { uni.setClipboardData({ data: v, success: () => uni.showToast({ title: "已复制", icon: "success" }) }) }
function goBack() { uni.navigateBack() }
onMounted(() => { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.bc-page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #6c5ce7, #a29bfe); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.input-card { background: #fff; border-radius: 24rpx; padding: 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); margin-bottom: 24rpx; }
.form-row { padding: 20rpx 0; border-bottom: 2rpx solid #f8f8f8; }
.form-row:last-child { border-bottom: none; }
.form-l { font-size: 28rpx; color: #333; display: block; margin-bottom: 16rpx; font-weight: 500; }
.form-input { width: 100%; height: 72rpx; font-size: 32rpx; border: 2rpx solid #e5e7eb; border-radius: 12rpx; padding: 0 16rpx; box-sizing: border-box; }
.base-btns { display: flex; gap: 16rpx; }
.base-btn { flex: 1; text-align: center; padding: 16rpx; background: #f5f5f5; border-radius: 12rpx; font-size: 28rpx; color: #666; }
.base-btn.active { background: linear-gradient(135deg, #6c5ce7, #a29bfe); color: #fff; }
.result-card { background: #fff; border-radius: 24rpx; padding: 8rpx 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.res-item { display: flex; align-items: center; padding: 24rpx 0; border-bottom: 2rpx solid #f8f8f8; }
.res-item:last-child { border-bottom: none; }
.res-base { font-size: 26rpx; color: #999; width: 180rpx; flex-shrink: 0; }
.res-val { flex: 1; font-size: 30rpx; color: #333; font-family: monospace; text-align: right; }
</style>
