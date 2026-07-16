<template>
  <view class="my-page">
    <!-- 顶部用户区 -->
    <view class="profile-header">
      <view class="bg-grad"></view>
      <view class="header-body" style="padding-right: 180rpx;">
        <view class="avatar-wrap">
          <text class="avatar-text">{{ username.charAt(0).toUpperCase() }}</text>
        </view>
        <view class="user-meta">
          <text class="user-name">{{ username }}</text>
          <text class="user-id">账号：{{ userId }}</text>
        </view>
        <text class="settings-icon" @click="goSettings">⚙️</text>
      </view>

      <view class="stat-cards">
        <view class="stat-card">
          <text class="stat-v">{{ notesCount }}</text>
          <text class="stat-l">笔记</text>
        </view>
        <view class="stat-card">
          <text class="stat-v">{{ travelCount }}</text>
          <text class="stat-l">计划</text>
        </view>
        <view class="stat-card">
          <text class="stat-v">{{ daysCount }}</text>
          <text class="stat-l">记录天</text>
        </view>
      </view>
    </view>

    <!-- 工具分组 -->
    <view class="tools-section">
      <text class="section-title">常用工具</text>
      <view class="tool-grid">
        <view class="tool-item" @click="goNotes">
          <view class="tool-circle" style="background: linear-gradient(135deg,#f59e0b,#ef4444);">
            <text>📝</text>
          </view>
          <text class="tool-name">笔记</text>
          <text class="tool-sub">{{ notesCount }} 篇</text>
        </view>

        <view class="tool-item" @click="goTravel">
          <view class="tool-circle" style="background: linear-gradient(135deg,#4a6cf7,#7c3aed);">
            <text>🗺️</text>
          </view>
          <text class="tool-name">旅游计划</text>
          <text class="tool-sub">{{ travelCount }} 项</text>
        </view>

        <view class="tool-item" @click="goDeveloping">
          <view class="tool-circle" style="background: linear-gradient(135deg,#10b981,#06b6d4);">
            <text>🍅</text>
          </view>
          <text class="tool-name">番茄钟</text>
          <text class="tool-sub">专注</text>
        </view>

        <view class="tool-item" @click="goDeveloping">
          <view class="tool-circle" style="background: linear-gradient(135deg,#ec4899,#f43f5e);">
            <text>🎯</text>
          </view>
          <text class="tool-name">打卡</text>
          <text class="tool-sub">习惯</text>
        </view>
      </view>
    </view>

    <!-- 其他功能 -->
    <view class="menu-section">
      <text class="section-title">其他</text>
      <view class="menu-list">
        <view class="menu-item" @click="goDeveloping">
          <text class="menu-icon">📦</text>
          <text class="menu-text">数据备份</text>
          <text class="menu-arrow">›</text>
        </view>
        <view class="menu-item" @click="goDeveloping">
          <text class="menu-icon">🎨</text>
          <text class="menu-text">主题外观</text>
          <text class="menu-arrow">›</text>
        </view>
        <view class="menu-item" @click="goDeveloping">
          <text class="menu-icon">💡</text>
          <text class="menu-text">意见反馈</text>
          <text class="menu-arrow">›</text>
        </view>
        <view class="menu-item" @click="goDeveloping">
          <text class="menu-icon">ℹ️</text>
          <text class="menu-text">关于</text>
          <text class="menu-arrow">›</text>
        </view>
      </view>
    </view>

    <!-- 退出登录 -->
    <view class="logout-section">
      <button class="logout-btn" @click="handleLogout">退出登录</button>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from "vue"

const username = ref("旅行者")
const userId = ref("U10086")
const notesCount = ref(0)
const travelCount = ref(0)
const daysCount = ref(0)

const goDeveloping = () => uni.showToast({ title: "功能开发中...", icon: "none" })
const goSettings = () => uni.showToast({ title: "设置开发中...", icon: "none" })

const goNotes = () => { uni.navigateTo({ url: "/pkgTools/pages/notes/home" }) }
const goTravel = () => { uni.navigateTo({ url: "/pkgTools/pages/travel/travel" }) }

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

const countDays = () => {
  try {
    const stored = uni.getStorageSync("myNotes")
    if (!stored) return 0
    const notes = JSON.parse(stored)
    if (!Array.isArray(notes)) return 0
    const set = new Set()
    notes.forEach((n) => { if (n.createdAt) set.add(n.createdAt.slice(0, 10)) })
    return set.size
  } catch (e) { return 0 }
}

onMounted(() => {
  username.value = uni.getStorageSync("username") || "旅行者"
  try {
    const stored = uni.getStorageSync("myNotes")
    notesCount.value = stored ? JSON.parse(stored).length : 0
  } catch (e) { notesCount.value = 0 }
  try {
    const stored = uni.getStorageSync("travelPlans")
    travelCount.value = stored ? JSON.parse(stored).length : 0
  } catch (e) { travelCount.value = 0 }
  daysCount.value = countDays()
})
</script>

<style lang="scss" scoped>
.my-page { min-height: 100vh; background: #f5f7fb; padding-bottom: 40rpx; }

.profile-header { position: relative; padding: 60rpx 40rpx 32rpx; overflow: hidden; }
.bg-grad { position: absolute; inset: 0; background: linear-gradient(135deg, #4a6cf7, #7c3aed); z-index: 0; }
.header-body { position: relative; z-index: 1; display: flex; align-items: center; margin-bottom: 40rpx; padding-right: 140rpx; box-sizing: border-box; }
.avatar-wrap {
  width: 110rpx; height: 110rpx; border-radius: 50%;
  background: rgba(255,255,255,0.25); border: 4rpx solid rgba(255,255,255,0.6);
  display: flex; align-items: center; justify-content: center; margin-right: 24rpx; flex-shrink: 0;
}
.avatar-text { font-size: 44rpx; color: #fff; font-weight: 700; }
.user-meta { flex: 1; }
.user-name { font-size: 34rpx; color: #fff; font-weight: 700; display: block; }
.user-id { font-size: 22rpx; color: rgba(255,255,255,0.7); margin-top: 4rpx; display: block; }
.settings-icon {
  font-size: 36rpx; width: 64rpx; height: 64rpx; line-height: 64rpx; text-align: center;
  border-radius: 50%; background: rgba(255,255,255,0.2);
}

.stat-cards { position: relative; z-index: 1; display: flex; gap: 16rpx; }
.stat-card {
  flex: 1; background: rgba(255,255,255,0.15); backdrop-filter: blur(8rpx);
  border-radius: 20rpx; padding: 24rpx 0; text-align: center;
  border: 2rpx solid rgba(255,255,255,0.25);
}
.stat-v { font-size: 36rpx; color: #fff; font-weight: 700; display: block; }
.stat-l { font-size: 22rpx; color: rgba(255,255,255,0.75); display: block; margin-top: 8rpx; }

.tools-section { padding: 32rpx 32rpx 0; }
.section-title { font-size: 28rpx; color: #999; font-weight: 500; margin-bottom: 20rpx; display: block; letter-spacing: 1rpx; }
.tool-grid {
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 24rpx;
  background: #fff; border-radius: 24rpx; padding: 32rpx 16rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04);
}
.tool-item { display: flex; flex-direction: column; align-items: center; }
.tool-item:active { transform: scale(0.92); transition: transform 0.1s; }
.tool-circle { width: 88rpx; height: 88rpx; border-radius: 22rpx; display: flex; align-items: center; justify-content: center; margin-bottom: 12rpx; }
.tool-circle text { font-size: 40rpx; }
.tool-name { font-size: 24rpx; color: #333; font-weight: 500; margin-bottom: 4rpx; }
.tool-sub { font-size: 20rpx; color: #999; }

.menu-section { padding: 32rpx 32rpx 0; }
.menu-list { background: #fff; border-radius: 24rpx; padding: 0 28rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.menu-item { display: flex; align-items: center; padding: 28rpx 0; border-bottom: 2rpx solid #f5f5f5; }
.menu-item:last-child { border-bottom: none; }
.menu-item:active { opacity: 0.7; }
.menu-icon { font-size: 32rpx; margin-right: 20rpx; flex-shrink: 0; }
.menu-text { font-size: 28rpx; color: #333; flex: 1; }
.menu-arrow { font-size: 32rpx; color: #ccc; font-weight: 300; }

.logout-section { padding: 40rpx 32rpx 0; }
.logout-btn {
  height: 88rpx; line-height: 88rpx; border-radius: 44rpx;
  background: #fff; color: #ef4444; font-size: 28rpx; font-weight: 500; border: 2rpx solid #f5e5e5;
}
.logout-btn::after { border: none; }
</style>
