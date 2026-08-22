<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">&#x2190;</text>
        <text class="nav-title">密码管理</text>
        <text class="nav-icon"> </text>
      </view>
    </view>
    <view class="content">
      <view class="search-bar">
        <input class="search-input" v-model="searchQuery" placeholder="搜索站点或用户名..." />
        <text class="add-btn" @click="showAddForm = true">+ 添加</text>
      </view>
      <view class="add-form" v-if="showAddForm">
        <view class="card">
          <view class="form-header">
            <text class="card-title">添加密码</text>
            <text class="close-btn" @click="showAddForm = false">&#x2715;</text>
          </view>
          <input class="form-input" v-model="newEntry.site" placeholder="站点名称" />
          <input class="form-input" v-model="newEntry.username" placeholder="用户名/邮箱" />
          <view class="password-gen-row">
            <input class="form-input gen-input" v-model="newEntry.password" placeholder="密码" />
            <text class="gen-btn" @click="generatePassword">生成</text>
          </view>
          <view class="submit-btn" @click="addEntry">
            <text class="btn-text">保存</text>
          </view>
        </view>
      </view>
      <view class="entry-list">
        <view class="empty-state" v-if="filteredEntries.length === 0">
          <text class="empty-icon">&#x1F512;</text>
          <text class="empty-text">暂无保存的密码</text>
        </view>
        <view class="entry-item" v-for="(entry, index) in filteredEntries" :key="entry.id">
          <view class="entry-info">
            <text class="entry-site">{{ entry.site }}</text>
            <text class="entry-username">{{ entry.username }}</text>
            <view class="entry-password-row">
              <text class="entry-password">{{ entry.visible ? entry.password : '********' }}</text>
              <text class="toggle-vis" @click="entry.visible = !entry.visible">{{ entry.visible ? '隐藏' : '显示' }}</text>
              <text class="copy-pw" @click="copyPassword(entry)">复制</text>
            </view>
          </view>
          <text class="delete-btn" @click="deleteEntry(entry.id)">&#x2715;</text>
        </view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, computed, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const entries = ref([])
const searchQuery = ref("")
const showAddForm = ref(false)
const newEntry = ref({ site: "", username: "", password: "" })
const filteredEntries = computed(function() {
  if (!searchQuery.value) return entries.value
  const q = searchQuery.value.toLowerCase()
  return entries.value.filter(function(e) {
    return e.site.toLowerCase().includes(q) || e.username.toLowerCase().includes(q)
  })
})
function goBack() { uni.navigateBack() }
function loadEntries() {
  const stored = uni.getStorageSync("password_entries")
  if (stored) {
    entries.value = JSON.parse(stored).map(function(e) {
      return Object.assign({}, e, { visible: false })
    })
  }
}
function saveEntries() {
  uni.setStorageSync("password_entries", JSON.stringify(entries.value.map(function(e) {
    return { id: e.id, site: e.site, username: e.username, password: e.password }
  })))
}
function generatePassword() {
  const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*"
  let pw = ""
  for (let i = 0; i < 16; i++) {
    pw += chars.charAt(Math.floor(Math.random() * chars.length))
  }
  newEntry.value.password = pw
}
function addEntry() {
  if (!newEntry.value.site || !newEntry.value.password) {
    uni.showToast({ title: "请填写站点和密码", icon: "none" })
    return
  }
  entries.value.push({
    id: Date.now().toString(),
    site: newEntry.value.site,
    username: newEntry.value.username,
    password: newEntry.value.password,
    visible: false
  })
  saveEntries()
  newEntry.value = { site: "", username: "", password: "" }
  showAddForm.value = false
  uni.showToast({ title: "保存成功", icon: "success" })
}
function deleteEntry(id) {
  uni.showModal({
    title: "确认删除",
    content: "确定要删除此密码吗？",
    success: function(res) {
      if (res.confirm) {
        entries.value = entries.value.filter(function(e) { return e.id !== id })
        saveEntries()
        uni.showToast({ title: "已删除", icon: "none" })
      }
    }
  })
}
function copyPassword(entry) {
  uni.setClipboardData({
    data: entry.password,
    success: function() {
      uni.showToast({ title: "密码已复制", icon: "success" })
    }
  })
}
onMounted(function() {
  if (!uni.getStorageSync("isLoggedIn")) {
    uni.reLaunch({ url: "/pages/login/login" })
    return
  }
  loadEntries()
})
</script>
<style scoped>
.page { min-height: 100vh; background: #f5f7fb }
.custom-nav { background: linear-gradient(135deg, #06b6d4, #0891b2); width: 100% }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx }
.nav-icon { width: 72rpx; text-align: center; font-size: 44rpx; color: #fff; font-weight: 700; flex-shrink: 0 }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600 }
.content { padding: 24rpx }
.search-bar { display: flex; align-items: center; gap: 16rpx; margin-bottom: 24rpx }
.search-input { flex: 1; height: 80rpx; background: #fff; border-radius: 12rpx; padding: 0 24rpx; font-size: 28rpx; box-shadow: 0 2rpx 8rpx rgba(0,0,0,0.04) }
.add-btn { background: linear-gradient(135deg, #06b6d4, #0891b2); color: #fff; font-size: 26rpx; padding: 20rpx 24rpx; border-radius: 12rpx; font-weight: 600 }
.card { background: #fff; border-radius: 16rpx; padding: 32rpx; box-shadow: 0 2rpx 12rpx rgba(0,0,0,0.06) }
.card-title { font-size: 30rpx; font-weight: 600; color: #1f2937 }
.form-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20rpx }
.close-btn { font-size: 32rpx; color: #9ca3af; padding: 4rpx 12rpx }
.form-input { width: 100%; height: 80rpx; background: #f9fafb; border-radius: 10rpx; padding: 0 20rpx; font-size: 28rpx; color: #374151; margin-bottom: 16rpx; box-sizing: border-box }
.password-gen-row { display: flex; align-items: center; gap: 12rpx; margin-bottom: 16rpx }
.gen-input { flex: 1; margin-bottom: 0 }
.gen-btn { background: #cffafe; color: #0891b2; font-size: 26rpx; padding: 16rpx 24rpx; border-radius: 10rpx; font-weight: 600; flex-shrink: 0 }
.submit-btn { background: linear-gradient(135deg, #06b6d4, #0891b2); border-radius: 12rpx; padding: 24rpx; text-align: center; margin-top: 8rpx }
.btn-text { color: #fff; font-size: 28rpx; font-weight: 600 }
.entry-list { margin-top: 8rpx }
.empty-state { display: flex; flex-direction: column; align-items: center; padding: 80rpx 0 }
.empty-icon { font-size: 80rpx }
.empty-text { font-size: 26rpx; color: #9ca3af; margin-top: 16rpx }
.entry-item { background: #fff; border-radius: 16rpx; padding: 24rpx; margin-bottom: 16rpx; display: flex; align-items: flex-start; justify-content: space-between; box-shadow: 0 2rpx 8rpx rgba(0,0,0,0.04) }
.entry-info { flex: 1 }
.entry-site { font-size: 30rpx; font-weight: 600; color: #1f2937; display: block }
.entry-username { font-size: 26rpx; color: #6b7280; display: block; margin-top: 4rpx; margin-bottom: 8rpx }
.entry-password-row { display: flex; align-items: center; gap: 16rpx }
.entry-password { font-size: 26rpx; color: #374151; font-family: monospace }
.toggle-vis { font-size: 24rpx; color: #06b6d4; padding: 4rpx 12rpx; background: #ecfeff; border-radius: 6rpx }
.copy-pw { font-size: 24rpx; color: #06b6d4; padding: 4rpx 12rpx; background: #ecfeff; border-radius: 6rpx }
.delete-btn { font-size: 28rpx; color: #ef4444; padding: 8rpx 16rpx; margin-left: 12rpx }
</style>