<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">JSON Path\u67e5\u8be2</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="form-card"><text class="form-label">JSON \u6570\u636e</text><textarea class="jp-input" v-model="jsonText" placeholder='{"name":"\u5f20\u4e09","age":25}' auto-height></textarea></view>
      <view class="form-card"><text class="form-label">Path \u8868\u8fbe\u5f0f</text><input class="form-input" v-model="pathExpr" placeholder="$.name" /></view>
      <view class="calc-btn" @click="query"><text>\u67e5\u8be2</text></view>
      <view class="result-card" v-if="result !== null">
        <text class="result-label">\u7ed3\u679c</text>
        <textarea class="result-area" :value="result" disabled></textarea>
      </view>
      <view class="hint-card"><text class="hint-title">\u5e38\u7528\u8bed\u6cd5</text><text class="hint-item">$.key \u2192 \u53d6\u503c</text><text class="hint-item">$..key \u2192 \u904d\u5386</text><text class="hint-item">$.arr[0] \u2192 \u6570\u7ec4</text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const jsonText = ref('{"name":"\u5f20\u4e09","age":25,"city":"\u5317\u4eac"}')
const pathExpr = ref("$.name")
const result = ref(null)
function query() {
  try {
    const obj = JSON.parse(jsonText.value)
    const path = pathExpr.value.trim().replace("$.", "").replace("$", "")
    const keys = path.split(".").filter(function(k){return k})
    let val = obj
    keys.forEach(function(k) { val = val[k] })
    result.value = typeof val === "object" ? JSON.stringify(val, null, 2) : String(val)
  } catch(e) { result.value = "\u9519\u8bef: " + e.message }
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #2d3436, #636e72); }
.custom-nav { background: linear-gradient(135deg, #2d3436, #636e72); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.form-card { background: rgba(255,255,255,0.1); border-radius: 20rpx; padding: 24rpx; margin-bottom: 20rpx; }
.form-label { font-size: 26rpx; color: rgba(255,255,255,0.7); display: block; margin-bottom: 12rpx; }
.jp-input { background: rgba(255,255,255,0.1); border-radius: 12rpx; padding: 16rpx; font-size: 24rpx; color: #fff; min-height: 160rpx; font-family: monospace; }
.form-input { font-size: 28rpx; color: #fff; background: rgba(255,255,255,0.1); border-radius: 12rpx; padding: 16rpx; font-family: monospace; }
.calc-btn { background: linear-gradient(135deg, #00b894, #00cec9); border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 32rpx; }
.calc-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.result-card { background: rgba(255,255,255,0.1); border-radius: 20rpx; padding: 24rpx; margin-bottom: 24rpx; }
.result-label { font-size: 24rpx; color: rgba(255,255,255,0.6); display: block; margin-bottom: 8rpx; }
.result-area { background: rgba(0,0,0,0.3); border-radius: 12rpx; padding: 16rpx; font-size: 24rpx; color: #fff; min-height: 100rpx; width: 100%; font-family: monospace; }
.hint-card { background: rgba(255,255,255,0.05); border-radius: 16rpx; padding: 20rpx; }
.hint-title { font-size: 24rpx; color: rgba(255,255,255,0.6); display: block; margin-bottom: 12rpx; }
.hint-item { font-size: 22rpx; color: rgba(255,255,255,0.5); display: block; padding: 4rpx 0; font-family: monospace; }
</style>
