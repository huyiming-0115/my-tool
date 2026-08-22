<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">Markdown 预览</text><text class="nav-icon" @click="showPreview = !showPreview">{{ showPreview ? "✎" : "📝" }}</text></view>
    </view>
    <view class="content">
      <view v-if="!showPreview" class="md-edit"><textarea class="md-input" v-model="input" placeholder="输入 Markdown 文本..." maxlength="5000" auto-height /></view>
      <view v-else class="md-preview">
        <view class="md-render" v-for="(line, idx) in rendered" :key="idx">
          <text class="md-h1" v-if="line.startsWith('# ')">{{ line.slice(2) }}</text>
          <text class="md-h2" v-else-if="line.startsWith('## ')">{{ line.slice(3) }}</text>
          <text class="md-h3" v-else-if="line.startsWith('### ')">{{ line.slice(4) }}</text>
          <text class="md-bold" v-else-if="line.startsWith('**')">{{ line.slice(2, -2) }}</text>
          <text class="md-list" v-else-if="line.startsWith('- ')">{{ line }}</text>
          <text class="md-normal" v-else>{{ line }}</text>
        </view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, computed, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const input = ref("")
const showPreview = ref(false)
const rendered = computed(function() { return input.value.split("\n") })
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #636e72, #2d3436); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 44rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.md-input { width: 100%; min-height: 500rpx; background: #fff; border-radius: 20rpx; padding: 24rpx; font-size: 28rpx; font-family: monospace; box-sizing: border-box; }
.md-preview { background: #fff; border-radius: 20rpx; padding: 32rpx; }
.md-render { margin-bottom: 16rpx; }
.md-h1 { font-size: 36rpx; font-weight: 700; color: #2d3436; display: block; margin: 16rpx 0; }
.md-h2 { font-size: 32rpx; font-weight: 700; color: #333; display: block; margin: 12rpx 0; }
.md-h3 { font-size: 28rpx; font-weight: 600; color: #555; display: block; margin: 8rpx 0; }
.md-bold { font-weight: 700; font-size: 28rpx; color: #333; display: block; }
.md-list { font-size: 28rpx; color: #555; display: block; }
.md-normal { font-size: 28rpx; color: #333; display: block; line-height: 1.6; }
</style>