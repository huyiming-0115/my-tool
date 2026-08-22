<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u6c47\u7387\u8f6c\u6362\u5668</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="form-card"><text class="form-label">\u91d1\u989d</text><input class="form-input" type="digit" v-model="amount" placeholder="\u8f93\u5165\u91d1\u989d" /></view>
      <view class="currency-row">
        <picker class="curr-picker" :range="currencies" range-key="name" @change="fromIdx=Number($event.detail.value)">
          <text>{{ currencies[fromIdx].name }} \u25bc</text>
        </picker>
        <text class="swap-btn" @click="swapCurr">\u2194</text>
        <picker class="curr-picker" :range="currencies" range-key="name" @change="toIdx=Number($event.detail.value)">
          <text>{{ currencies[toIdx].name }} \u25bc</text>
        </picker>
      </view>
      <view class="calc-btn" @click="convert"><text>\u8f6c\u6362</text></view>
      <view class="result-card" v-if="result">
        <text class="result-amount">{{ amount }} {{ currencies[fromIdx].code }}</text>
        <text class="result-arrow">\u2193</text>
        <text class="result-val">{{ result }} {{ currencies[toIdx].code }}</text>
        <text class="result-rate">\u6c47\u7387: 1 {{ currencies[fromIdx].code }} = {{ rate }} {{ currencies[toIdx].code }}</text>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const amount = ref("")
const fromIdx = ref(0)
const toIdx = ref(1)
const result = ref("")
const rate = ref("")
const currencies = [
  {code:"CNY", name:"\u4eba\u6c11\u5e01", rate:1},
  {code:"USD", name:"\u7f8e\u5143", rate:0.14},
  {code:"EUR", name:"\u6b27\u5143", rate:0.13},
  {code:"JPY", name:"\u65e5\u5143", rate:20.5},
  {code:"KRW", name:"\u97e9\u5143", rate:185},
  {code:"GBP", name:"\u82f1\u9551", rate:0.11},
  {code:"HKD", name:"\u6e2f\u5e01", rate:1.1},
  {code:"TWD", name:"\u53f0\u5e01", rate:4.5}
]
function convert() {
  const a = parseFloat(amount.value) || 0
  if (a <= 0) { uni.showToast({ title: "\u8bf7\u8f93\u5165\u91d1\u989d", icon: "none" }); return }
  const r = currencies[toIdx.value].rate / currencies[fromIdx.value].rate
  rate.value = r.toFixed(4)
  result.value = (a * r).toFixed(2)
}
function swapCurr() { const t = fromIdx.value; fromIdx.value = toIdx.value; toIdx.value = t }
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
.form-card { background: #fff; border-radius: 20rpx; padding: 24rpx; margin-bottom: 20rpx; }
.form-label { font-size: 26rpx; color: #666; display: block; margin-bottom: 12rpx; }
.form-input { font-size: 36rpx; color: #333; font-weight: 600; }
.currency-row { display: flex; align-items: center; gap: 16rpx; margin-bottom: 24rpx; }
.curr-picker { flex: 1; background: #fff; border-radius: 16rpx; padding: 20rpx; text-align: center; font-size: 28rpx; }
.swap-btn { font-size: 36rpx; color: #fff; }
.calc-btn { background: linear-gradient(135deg, #5a67d8, #6b46c1); border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 32rpx; }
.calc-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.result-card { background: #fff; border-radius: 24rpx; padding: 32rpx; text-align: center; }
.result-amount { font-size: 28rpx; color: #999; display: block; }
.result-arrow { font-size: 32rpx; color: #5a67d8; display: block; margin: 8rpx 0; }
.result-val { font-size: 40rpx; font-weight: 700; color: #5a67d8; display: block; }
.result-rate { font-size: 22rpx; color: #999; display: block; margin-top: 12rpx; }
</style>
