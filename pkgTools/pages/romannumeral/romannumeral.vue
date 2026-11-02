<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u7f57\u9a6c\u6570\u5b57\u8f6c\u6362</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="mode-tabs"><text class="mode-tab" :class="{active: mode==='toRoman'}" @click="mode='toRoman'">\u6570\u5b57\u2192\u7f57\u9a6c</text><text class="mode-tab" :class="{active: mode==='toNum'}" @click="mode='toNum'">\u7f57\u9a6c\u2192\u6570\u5b57</text></view>
      <view class="form-card"><text class="form-label">{{ mode==='toRoman' ? '\u8f93\u5165\u6570\u5b57 (1-3999)' : '\u8f93\u5165\u7f57\u9a6c\u6570\u5b57' }}</text><input class="form-input" v-model="input" :placeholder="mode==='toRoman'?'\u5982: 2024':'\u5982: MMXXIV'" /></view>
      <view class="calc-btn" @click="convert"><text>\u8f6c\u6362</text></view>
      <view class="result-card" v-if="result"><text class="result-text">{{ result }}</text></view>
      <view class="ref-table"><text class="ref-title">\u5e38\u7528\u5bf9\u7167</text><view class="ref-grid"><text class="ref-item" v-for="(r, i) in refList" :key="i">{{ r }}</text></view></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const mode = ref("toRoman")
const input = ref("")
const result = ref("")
const refList = ["I=1","IV=4","V=5","IX=9","X=10","L=50","C=100","D=500","M=1000"]
const romanMap = [[1000,"M"],[900,"CM"],[500,"D"],[400,"CD"],[100,"C"],[90,"XC"],[50,"L"],[40,"XL"],[10,"X"],[9,"IX"],[5,"V"],[4,"IV"],[1,"I"]]
function toRoman(num) {
  let r = ""
  romanMap.forEach(function(m) { while (num >= m[0]) { r += m[1]; num -= m[0] } })
  return r
}
function toNum(s) {
  const map = {I:1,V:5,X:10,L:50,C:100,D:500,M:1000}
  let n = 0
  for (let i = 0; i < s.length; i++) { map[s[i]] < map[s[i+1]] ? n -= map[s[i]] : n += map[s[i]] }
  return n
}
function convert() {
  if (mode.value === "toRoman") {
    const n = parseInt(input.value)
    if (n < 1 || n > 3999) { uni.showToast({ title: "1-3999", icon: "none" }); return }
    result.value = toRoman(n)
  } else {
    const n = toNum(input.value.toUpperCase())
    result.value = n > 0 ? n : "\u65e0\u6548"
  }
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
.mode-tabs { display: flex; gap: 16rpx; margin-bottom: 24rpx; }
.mode-tab { flex: 1; text-align: center; padding: 20rpx; border-radius: 16rpx; background: rgba(255,255,255,0.3); color: #fff; font-size: 24rpx; }
.mode-tab.active { background: #fff; color: #e84393; }
.form-card { background: #fff; border-radius: 20rpx; padding: 24rpx; margin-bottom: 20rpx; }
.form-label { font-size: 26rpx; color: #666; display: block; margin-bottom: 12rpx; }
.form-input { font-size: 32rpx; color: #333; font-weight: 600; }
.calc-btn { background: linear-gradient(135deg, #e84393, #fd79a8); border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 32rpx; }
.calc-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.result-card { background: #fff; border-radius: 24rpx; padding: 40rpx; text-align: center; margin-bottom: 24rpx; }
.result-text { font-size: 48rpx; font-weight: 700; color: #e84393; }
.ref-table { background: rgba(255,255,255,0.2); border-radius: 20rpx; padding: 20rpx; }
.ref-title { font-size: 24rpx; color: #fff; display: block; margin-bottom: 12rpx; }
.ref-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8rpx; }
.ref-item { background: rgba(255,255,255,0.3); border-radius: 8rpx; padding: 12rpx; text-align: center; font-size: 22rpx; color: #fff; }
</style>
