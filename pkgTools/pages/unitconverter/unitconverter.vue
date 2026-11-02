<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u5355\u4f4d\u6362\u7b97\u5168</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="cat-tabs"><text class="cat-tab" :class="{active: cat==='\u957f\u5ea6'}" @click="cat='\u957f\u5ea6'">\u957f\u5ea6</text><text class="cat-tab" :class="{active: cat==='\u91cd\u91cf'}" @click="cat='\u91cd\u91cf'">\u91cd\u91cf</text><text class="cat-tab" :class="{active: cat==='\u6e29\u5ea6'}" @click="cat='\u6e29\u5ea6'">\u6e29\u5ea6</text><text class="cat-tab" :class="{active: cat==='\u9762\u79ef'}" @click="cat='\u9762\u79ef'">\u9762\u79ef</text><text class="cat-tab" :class="{active: cat==='\u901f\u5ea6'}" @click="cat='\u901f\u5ea6'">\u901f\u5ea6</text></view>
      <view class="form-card"><text class="form-label">\u8f93\u5165\u503c</text><input class="form-input" type="digit" v-model="inputVal" /></view>
      <view class="form-card"><text class="form-label">\u4ece</text><picker class="unit-picker" :range="units[cat]" @change="fromUnit=$event.detail.value"><text>{{ units[cat][fromUnit] }} \u25bc</text></picker></view>
      <view class="form-card"><text class="form-label">\u5230</text><picker class="unit-picker" :range="units[cat]" @change="toUnit=$event.detail.value"><text>{{ units[cat][toUnit] }} \u25bc</text></picker></view>
      <view class="calc-btn" @click="convert"><text>\u6362\u7b97</text></view>
      <view class="result-card" v-if="result !== ''"><text class="result-val">{{ inputVal }} {{ units[cat][fromUnit] }} = {{ result }} {{ units[cat][toUnit] }}</text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const cat = ref("\u957f\u5ea6")
const inputVal = ref("1")
const fromUnit = ref(0)
const toUnit = ref(1)
const result = ref("")
const units = {
  "\u957f\u5ea6": ["\u7c73","\u5343\u7c73","\u5398\u7c73","\u82f1\u5c3a","\u82f1\u5bf8","\u7801"],
  "\u91cd\u91cd": ["\u514b","\u5343\u514b","\u65a4","\u76ce\u53f8","\u78c5"],
  "\u6e29\u5ea6": ["\u6444\u6c0f\u5ea6","\u683c\u91cc\u58eb\u5ea6","\u5f00\u5c14\u6587"],
  "\u9762\u79ef": ["\u5e73\u65b9\u7c73","\u5e73\u65b9\u5343\u7c73","\u5e73\u65b9\u82f1\u5c3a","\u5e73\u65b9\u82f1\u91cc","\u516c\u9877"],
  "\u901f\u5ea6": ["\u7c73/\u79d2","\u5343\u7c73/\u5c0f\u65f6","\u82f1\u91cc/\u5c0f\u65f6","\u8282"]
}
const factors = {
  "\u957f\u5ea6": [1,1000,0.01,0.3048,0.0254,0.9144],
  "\u91cd\u91cd": [1,1000,0.002,0.0283495,0.453592],
  "\u6e29\u5ea6": [1,1,1],
  "\u9762\u79ef": [1,1000000,0.092903,2589988,4046.86],
  "\u901f\u5ea6": [1,3.6,0.277778,0.514444]
}
function convert() {
  const v = parseFloat(inputVal.value) || 0
  const f = factors[cat.value]
  result.value = (v * f[fromUnit.value] / f[toUnit.value]).toFixed(6)
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #667eea, #764ba2); }
.custom-nav { background: linear-gradient(135deg, #5a67d8, #6b46c1); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.cat-tabs { display: flex; gap: 8rpx; margin-bottom: 24rpx; flex-wrap: wrap; }
.cat-tab { padding: 12rpx 20rpx; border-radius: 12rpx; background: rgba(255,255,255,0.2); color: #fff; font-size: 24rpx; }
.cat-tab.active { background: #fff; color: #5a67d8; }
.form-card { background: #fff; border-radius: 20rpx; padding: 24rpx; margin-bottom: 20rpx; }
.form-label { font-size: 26rpx; color: #666; display: block; margin-bottom: 12rpx; }
.form-input { font-size: 32rpx; color: #333; font-weight: 600; }
.unit-picker { background: #f8f8f8; border-radius: 12rpx; padding: 16rpx; font-size: 28rpx; }
.calc-btn { background: linear-gradient(135deg, #5a67d8, #6b46c1); border-radius: 16rpx; padding: 24rpx; text-align: center; margin: 32rpx 0; }
.calc-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.result-card { background: #fff; border-radius: 24rpx; padding: 32rpx; text-align: center; }
.result-val { font-size: 32rpx; font-weight: 700; color: #5a67d8; }
</style>
