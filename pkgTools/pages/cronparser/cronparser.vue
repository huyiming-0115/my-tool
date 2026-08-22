<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">Cron 解析</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="cron-input-row"><input class="cron-input" v-model="cron" placeholder="* * * * *" @input="parse" /><text class="cron-btn" @click="parse">解析</text></view>
      <view class="cron-fields">
        <view class="field"><text class="field-name">分</text><text class="field-val">{{ fields[0] }}</text></view>
        <view class="field"><text class="field-name">时</text><text class="field-val">{{ fields[1] }}</text></view>
        <view class="field"><text class="field-name">日</text><text class="field-val">{{ fields[2] }}</text></view>
        <view class="field"><text class="field-name">月</text><text class="field-val">{{ fields[3] }}</text></view>
        <view class="field"><text class="field-name">周</text><text class="field-val">{{ fields[4] }}</text></view>
      </view>
      <view class="cron-result" v-if="description"><text>{{ description }}</text></view>
      <view class="cron-presets">
        <text class="preset-title">常用表达式</text>
        <view class="preset-list">
          <text class="preset-item" v-for="(p, idx) in presets" :key="idx" @click="cron = p.val; parse()">{{ p.name }}</text>
        </view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const cron = ref("*/5 * * * *")
const fields = ref(["*", "*", "*", "*", "*"])
const description = ref("")
const presets = [
  { name: "每5分钟", val: "*/5 * * * *" },
  { name: "每小时", val: "0 * * * *" },
  { name: "每天早上8点", val: "0 8 * * *" },
  { name: "每周一上午9点", val: "0 9 * * 1" },
  { name: "每月1号凌晨", val: "0 0 1 * *" }
]
function parse() {
  var parts = cron.value.trim().split(/\s+/)
  if (parts.length === 5) {
    fields.value = parts
    description.value = "表达式有效"
  } else {
    description.value = "格式错误，需要5个字段"
  }
}
parse()
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #0984e3, #74b9ff); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.cron-input-row { display: flex; gap: 16rpx; margin-bottom: 24rpx; }
.cron-input { flex: 1; height: 80rpx; background: #fff; border-radius: 16rpx; padding: 0 20rpx; font-size: 28rpx; font-family: monospace; }
.cron-btn { padding: 0 32rpx; background: #0984e3; border-radius: 16rpx; line-height: 80rpx; color: #fff; font-size: 26rpx; }
.cron-fields { display: flex; gap: 12rpx; margin-bottom: 24rpx; }
.field { flex: 1; background: #fff; border-radius: 16rpx; padding: 16rpx; text-align: center; }
.field-name { font-size: 22rpx; color: #999; display: block; }
.field-val { font-size: 28rpx; color: #333; font-weight: 600; display: block; margin-top: 4rpx; }
.cron-result { background: #fff; border-radius: 16rpx; padding: 20rpx; margin-bottom: 24rpx; font-size: 26rpx; color: #333; }
.cron-presets { background: #fff; border-radius: 16rpx; padding: 20rpx; }
.preset-title { font-size: 26rpx; color: #999; display: block; margin-bottom: 12rpx; }
.preset-list { display: flex; flex-wrap: wrap; gap: 12rpx; }
.preset-item { padding: 12rpx 20rpx; background: #f0f0ff; border-radius: 20rpx; font-size: 24rpx; color: #6c5ce7; }
</style>