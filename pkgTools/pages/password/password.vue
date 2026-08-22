<template>
  <view class="pwd-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">←</text>
        <text class="nav-title">密码生成器</text>
        <text class="nav-icon empty"> </text>
      </view>
    </view>

    <view class="content">
      <view class="result-card">
        <text class="result-text" @click="copyPassword">{{ password }}</text>
        <view class="result-actions">
          <text class="action-btn" @click="copyPassword">复制</text>
          <text class="action-btn" @click="generate">刷新</text>
        </view>
      </view>

      <view class="strength-bar" v-if="password">
        <view class="strength-segment" :style="{ background: strengthColor }"></view>
        <text class="strength-text">强度: {{ strengthText }}</text>
      </view>

      <view class="options-card">
        <view class="opt-row">
          <text class="opt-label">密码长度</text>
          <slider class="opt-slider" :value="length" min="4" max="32" show-value @change="onLengthChange" />
        </view>

        <view class="opt-row">
          <text class="opt-label">包含大写字母 (A-Z)</text>
          <switch :checked="uppercase" @change="uppercase = $event.detail.value" color="#14b8a6" />
        </view>
        <view class="opt-row">
          <text class="opt-label">包含小写字母 (a-z)</text>
          <switch :checked="lowercase" @change="lowercase = $event.detail.value" color="#14b8a6" />
        </view>
        <view class="opt-row">
          <text class="opt-label">包含数字 (0-9)</text>
          <switch :checked="numbers" @change="numbers = $event.detail.value" color="#14b8a6" />
        </view>
        <view class="opt-row">
          <text class="opt-label">包含特殊字符 (!@#$)</text>
          <switch :checked="symbols" @change="symbols = $event.detail.value" color="#14b8a6" />
        </view>
      </view>

      <view class="batch-card">
        <text class="batch-title">批量生成</text>
        <view class="batch-row">
          <input class="batch-input" v-model="batchCount" type="number" placeholder="数量" />
          <button class="batch-btn" @click="generateBatch">生成</button>
        </view>
        <view class="batch-list" v-if="batchList.length > 0">
          <view class="batch-item" v-for="(item, idx) in batchList" :key="idx" @click="copyItem(item)">
            <text class="batch-text">{{ item }}</text>
            <text class="batch-copy">复制</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, watch, onMounted } from "vue"

const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const password = ref("")
const length = ref(16)
const uppercase = ref(true)
const lowercase = ref(true)
const numbers = ref(true)
const symbols = ref(true)
const batchCount = ref(5)
const batchList = ref([])

const strengthText = computed(() => {
  let score = 0
  if (password.value.length >= 8) score++
  if (password.value.length >= 12) score++
  if (password.value.length >= 16) score++
  if (/[A-Z]/.test(password.value)) score++
  if (/[a-z]/.test(password.value)) score++
  if (/[0-9]/.test(password.value)) score++
  if (/[^A-Za-z0-9]/.test(password.value)) score++
  if (score <= 2) return "弱"
  if (score <= 4) return "中"
  if (score <= 6) return "强"
  return "非常强"
})

const strengthColor = computed(() => {
  const t = strengthText.value
  if (t === "弱") return "#ef4444"
  if (t === "中") return "#f59e0b"
  if (t === "强") return "#10b981"
  return "#059669"
})

function generate() {
  let chars = ""
  if (uppercase.value) chars += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  if (lowercase.value) chars += "abcdefghijklmnopqrstuvwxyz"
  if (numbers.value) chars += "0123456789"
  if (symbols.value) chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
  if (!chars) { uni.showToast({ title: "请至少选择一种字符", icon: "none" }); return }
  let pwd = ""
  for (let i = 0; i < length.value; i++) {
    pwd += chars.charAt(Math.floor(Math.random() * chars.length))
  }
  password.value = pwd
}

function generateBatch() {
  const count = Math.min(parseInt(batchCount.value) || 5, 20)
  batchList.value = []
  for (let i = 0; i < count; i++) {
    let chars = ""
    if (uppercase.value) chars += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if (lowercase.value) chars += "abcdefghijklmnopqrstuvwxyz"
    if (numbers.value) chars += "0123456789"
    if (symbols.value) chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if (!chars) { chars = "abcdefghijklmnopqrstuvwxyz0123456789" }
    let pwd = ""
    for (let j = 0; j < length.value; j++) {
      pwd += chars.charAt(Math.floor(Math.random() * chars.length))
    }
    batchList.value.push(pwd)
  }
}

function copyPassword() {
  uni.setClipboardData({ data: password.value, success: () => uni.showToast({ title: "已复制", icon: "success" }) })
}

function copyItem(item) {
  uni.setClipboardData({ data: item, success: () => uni.showToast({ title: "已复制", icon: "success" }) })
}

function onLengthChange(e) { length.value = e.detail.value }

function goBack() { uni.navigateBack() }

watch([length, uppercase, lowercase, numbers, symbols], generate)

onMounted(() => {
  if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }
  generate()
})
</script>

<style lang="scss" scoped>
.pwd-page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #14b8a6, #06b6d4); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.result-card { background: #fff; border-radius: 24rpx; padding: 32rpx; margin-bottom: 24rpx; }
.result-text { font-size: 32rpx; font-weight: 600; color: #333; text-align: center; display: block; word-break: break-all; margin-bottom: 20rpx; min-height: 60rpx; }
.result-actions { display: flex; justify-content: center; gap: 24rpx; }
.action-btn { padding: 12rpx 40rpx; background: linear-gradient(135deg, #14b8a6, #06b6d4); color: #fff; border-radius: 30rpx; font-size: 26rpx; }
.strength-bar { display: flex; align-items: center; gap: 16rpx; padding: 0 24rpx; margin-bottom: 24rpx; }
.strength-segment { flex: 1; height: 8rpx; border-radius: 4rpx; }
.strength-text { font-size: 24rpx; color: #666; }
.options-card { background: #fff; border-radius: 24rpx; padding: 32rpx; margin-bottom: 24rpx; }
.opt-row { display: flex; align-items: center; justify-content: space-between; padding: 16rpx 0; border-bottom: 2rpx solid #f9f9f9; }
.opt-label { font-size: 28rpx; color: #333; }
.opt-slider { flex: 1; margin-left: 24rpx; }
.batch-card { background: #fff; border-radius: 24rpx; padding: 32rpx; }
.batch-title { font-size: 28rpx; font-weight: 600; color: #333; margin-bottom: 20rpx; display: block; }
.batch-row { display: flex; gap: 16rpx; margin-bottom: 20rpx; }
.batch-input { flex: 1; height: 72rpx; border: 2rpx solid #e5e7eb; border-radius: 12rpx; padding: 0 20rpx; font-size: 28rpx; }
.batch-btn { background: linear-gradient(135deg, #14b8a6, #06b6d4); color: #fff; border-radius: 12rpx; font-size: 26rpx; padding: 0 32rpx; }
.batch-list { max-height: 400rpx; overflow-y: auto; }
.batch-item { display: flex; align-items: center; justify-content: space-between; padding: 16rpx 0; border-bottom: 2rpx solid #f9f9f9; }
.batch-text { flex: 1; font-size: 26rpx; color: #666; word-break: break-all; margin-right: 16rpx; }
.batch-copy { font-size: 24rpx; color: #14b8a6; padding: 4rpx 16rpx; }
</style>
