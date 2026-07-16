<template>
  <view class="home-container">
    <view class="home-header">
      <view class="bg-grad"></view>
      <view class="header-content">
        <text class="app-name">我的工具箱</text>
        <text class="app-desc">高效工作 · 轻松生活</text>
      </view>
    </view>

    <view class="tools-grid">
      <view class="tool-card" @click="goTravel">
        <view class="tool-icon" style="background: linear-gradient(135deg, #4a6cf7, #7c3aed);">
          <text>🗺️</text>
        </view>
        <text class="tool-name">旅游计划</text>
        <text class="tool-desc">查看旅行文档</text>
      </view>

      <view class="tool-card" @click="goNotes">
        <view class="tool-icon" style="background: linear-gradient(135deg, #f59e0b, #ef4444);">
          <text>📝</text>
        </view>
        <text class="tool-name">笔记</text>
        <text class="tool-desc">记录灵感</text>
      </view>

      <view class="tool-card" @click="goDeveloping">
        <view class="tool-icon" style="background: linear-gradient(135deg, #10b981, #06b6d4);">
          <text>🍅</text>
        </view>
        <text class="tool-name">番茄钟</text>
        <text class="tool-desc">专注时间</text>
      </view>

      <view class="tool-card" @click="goDeveloping">
        <view class="tool-icon" style="background: linear-gradient(135deg, #ec4899, #f43f5e);">
          <text>🎯</text>
        </view>
        <text class="tool-name">习惯打卡</text>
        <text class="tool-desc">养成好习惯</text>
      </view>
    </view>

    <view v-if="username" class="user-bar">
      <text class="user-text">当前用户：{{ username }}</text>
      <text class="logout-text" @click="handleLogout">退出</text>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from "vue"

const username = ref("")

const goTravel = () => {
  uni.navigateTo({ url: "/pkgTools/pages/travel/travel" })
}

const goDeveloping = () => {
  uni.showToast({ title: '功能开发中...', icon: 'none' })
}

const goNotes = () => {
  uni.navigateTo({ url: "/pkgTools/pages/notes/home" })
}

const handleLogout = () => {
  uni.showModal({
    title: "退出登录",
    content: "确定退出？",
    success: (res) => {
      if (res.confirm) {
        uni.removeStorageSync("isLoggedIn")
        uni.reLaunch({ url: "/pages/login/login" })
      }
    },
  })
}

onMounted(() => {
  username.value = uni.getStorageSync("username") || ""
})
</script>

<style lang="scss" scoped>
.home-container {
  min-height: 100vh;
  background: #f5f7fb;
  padding-bottom: 40rpx;
}

.home-header {
  position: relative;
  padding: 100rpx 40rpx 60rpx;
  overflow: hidden;
}

.bg-grad {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #4a6cf7 0%, #7c3aed 100%);
  z-index: 0;
}

.header-content {
  position: relative;
  z-index: 1;
}

.app-name {
  font-size: 40rpx;
  color: #fff;
  font-weight: 700;
  display: block;
}

.app-desc {
  font-size: 26rpx;
  color: rgba(255, 255, 255, 0.75);
  margin-top: 12rpx;
  display: block;
}

.tools-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24rpx;
  padding: 40rpx 32rpx;
}

.tool-card {
  background: #fff;
  border-radius: 24rpx;
  padding: 36rpx 28rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.04);
  transition: transform 0.15s;
}

.tool-card:active {
  transform: scale(0.95);
}

.tool-icon {
  width: 96rpx;
  height: 96rpx;
  border-radius: 24rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20rpx;
}

.tool-icon text {
  font-size: 44rpx;
}

.tool-name {
  font-size: 28rpx;
  font-weight: 600;
  color: #333;
  margin-bottom: 8rpx;
}

.tool-desc {
  font-size: 22rpx;
  color: #999;
}

.user-bar {
  margin-top: 40rpx;
  padding: 0 32rpx;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-text {
  font-size: 24rpx;
  color: #999;
}

.logout-text {
  font-size: 24rpx;
  color: #ef4444;
  padding: 4rpx 16rpx;
}
</style>
