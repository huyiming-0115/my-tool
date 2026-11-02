<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">SQL\u683c\u5f0f\u5316</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="mode-tabs"><text class="mode-tab" :class="{active: mode==='beautify'}" @click="mode='beautify'">\u7f8e\u5316</text><text class="mode-tab" :class="{active: mode==='minify'}" @click="mode='minify'">\u538b\u7f29</text></view>
      <textarea class="sql-input" v-model="sqlText" placeholder="SELECT * FROM users WHERE id=1" auto-height></textarea>
      <view class="calc-btn" @click="format"><text>\u8f6c\u6362</text></view>
      <view class="result-card" v-if="result"><textarea class="result-area" :value="result" disabled auto-height></textarea><text class="copy-btn" @click="copyText">\u590d\u5236</text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const mode = ref("beautify")
const sqlText = ref("SELECT id,name,age FROM users WHERE age>18 ORDER BY id DESC")
const result = ref("")
function format() {
  if (!sqlText.value.trim()) { uni.showToast({ title: "\u8bf7\u8f93\u5165SQL", icon: "none" }); return }
  let sql = sqlText.value.trim()
  if (mode.value === "beautify") {
    sql = sql.replace(/\s+/g, " ")
    sql = sql.replace(/\s*(SELECT|FROM|WHERE|ORDER BY|GROUP BY|HAVING|JOIN|LEFT JOIN|RIGHT JOIN|INNER JOIN|ON|AND|OR|INSERT INTO|UPDATE|DELETE FROM|VALUES|SET)\s+/gi, "\n$1 ")
    sql = sql.replace(/\s*(,)\s*/g, ",\n  ")
    result.value = sql.trim()
  } else {
    result.value = sql.replace(/\s+/g, " ").replace(/\s*([(),=<>])\s*/g, "$1").trim()
  }
}
function copyText() { uni.setClipboardData({ data: result.value, success: function() { uni.showToast({ title: "\u5df2\u590d\u5236", icon: "success" }) } }) }
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #1e3c72, #2a5298); }
.custom-nav { background: linear-gradient(135deg, #1e3c72, #2a5298); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.mode-tabs { display: flex; gap: 16rpx; margin-bottom: 24rpx; }
.mode-tab { flex: 1; text-align: center; padding: 20rpx; border-radius: 16rpx; background: rgba(255,255,255,0.2); color: #fff; font-size: 26rpx; }
.mode-tab.active { background: #fff; color: #1e3c72; }
.sql-input { background: rgba(255,255,255,0.95); border-radius: 16rpx; padding: 24rpx; font-size: 24rpx; min-height: 200rpx; font-family: monospace; margin-bottom: 20rpx; }
.calc-btn { background: linear-gradient(135deg, #00b894, #00cec9); border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 24rpx; }
.calc-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.result-card { background: #fff; border-radius: 20rpx; padding: 24rpx; }
.result-area { width: 100%; min-height: 200rpx; font-size: 24rpx; font-family: monospace; color: #333; background: #f8f8f8; border-radius: 12rpx; padding: 16rpx; }
.copy-btn { display: block; background: #1e3c72; color: #fff; text-align: center; border-radius: 12rpx; padding: 16rpx; margin-top: 16rpx; font-size: 26rpx; }
</style>
