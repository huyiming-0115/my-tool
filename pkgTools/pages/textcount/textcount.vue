<template>
  <view class="tc-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">文字统计</text><text class="nav-icon" @click="textContent = ''">🗑</text></view>
    </view>
    <view class="content">
      <view class="stats-bar">
        <view class="stat-chip"><text class="s-num">{{ stats.chars }}</text><text class="s-l">总字数</text></view>
        <view class="stat-chip"><text class="s-no-space">{{ stats.noSpace }}</text><text class="s-l">去空</text></view>
        <view class="stat-chip"><text class="s-cn">{{ stats.chinese }}</text><text class="s-l">中文</text></view>
        <view class="stat-chip"><text class="s-en">{{ stats.english }}</text><text class="s-l">英文</text></view>
        <view class="stat-chip"><text class="s-num2">{{ stats.numbers }}</text><text class="s-l">数字</text></view>
        <view class="stat-chip"><text class="s-line">{{ stats.lines }}</text><text class="s-l">行数</text></view>
      </view>
      <textarea class="tc-input" v-model="textContent" placeholder="请输入或粘贴文本内容..." maxlength="10000" auto-height />
      <view class="extra-stats"><text>标点符号: {{ stats.punctuation }} · 空格: {{ stats.spaces }}</text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, computed, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const textContent = ref("")
const stats = computed(() => {
  const t = textContent.value
  return {
    chars: t.length,
    noSpace: t.replace(/\s/g, "").length,
    chinese: (t.match(/[一-龥]/g) || []).length,
    english: (t.match(/[a-zA-Z]/g) || []).length,
    numbers: (t.match(/[0-9]/g) || []).length,
    lines: t ? t.split("\n").length : 0,
    punctuation: (t.match(/[、。，！？；：""''（）《》【】]/g) || []).length,
    spaces: (t.match(/\s/g) || []).length
  }
})
function goBack() { uni.navigateBack() }
onMounted(() => { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.tc-page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #f6d365, #fda085); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 44rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.stats-bar { display: flex; flex-wrap: wrap; gap: 12rpx; margin-bottom: 24rpx; }
.stat-chip { flex: 1; min-width: 28%; background: #fff; border-radius: 16rpx; padding: 16rpx; text-align: center; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.s-num, .s-no-space, .s-cn, .s-en, .s-num2, .s-line { font-size: 36rpx; font-weight: 700; display: block; }
.s-num { color: #f6d365; } .s-no-space { color: #fda085; } .s-cn { color: #667eea; } .s-en { color: #10b981; } .s-num2 { color: #f5576c; } .s-line { color: #8b5cf6; }
.s-l { font-size: 20rpx; color: #999; display: block; margin-top: 4rpx; }
.tc-input { width: 100%; min-height: 400rpx; background: #fff; border-radius: 24rpx; padding: 24rpx; font-size: 28rpx; line-height: 1.8; box-sizing: border-box; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); margin-bottom: 16rpx; }
.extra-stats { text-align: center; font-size: 24rpx; color: #999; }
</style>
