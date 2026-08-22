<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">&#x2190;</text>
        <text class="nav-title">PDF合并</text>
        <text class="nav-icon"> </text>
      </view>
    </view>
    <view class="content">
      <view class="card">
        <text class="card-title">选择PDF文件</text>
        <text class="card-desc">选择多个PDF文件进行合并</text>
        <view class="btn-primary" @click="selectFiles">
          <text class="btn-text">+ 添加文件</text>
        </view>
      </view>
      <view class="file-list" v-if="files.length > 0">
        <text class="section-title">文件列表 ({{ files.length }}个)</text>
        <view class="file-item" v-for="(file, index) in files" :key="index">
          <view class="file-info">
            <text class="file-icon">PDF</text>
            <view class="file-detail">
              <text class="file-name">{{ file.name }}</text>
              <text class="file-size">{{ file.size }}</text>
            </view>
          </view>
          <view class="file-actions">
            <text class="action-btn" @click="moveUp(index)" v-if="index > 0">&#x25B2;</text>
            <text class="action-btn" @click="moveDown(index)" v-if="index < files.length - 1">&#x25BC;</text>
            <text class="action-btn delete" @click="removeFile(index)">&#x2715;</text>
          </view>
        </view>
      </view>
      <view class="btn-merge" v-if="files.length >= 2" @click="mergeFiles">
        <text class="btn-text">开始合并 ({{ files.length }}个文件)</text>
      </view>
      <view class="empty-state" v-if="files.length === 0">
        <text class="empty-icon">&#x1F4C4;</text>
        <text class="empty-text">暂无文件，点击上方按钮添加</text>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const files = ref([])
const sampleFiles = [
  { name: "项目报告.pdf", size: "2.4 MB" },
  { name: "合同文件.pdf", size: "1.8 MB" },
  { name: "财务报表.pdf", size: "3.1 MB" },
  { name: "技术文档.pdf", size: "5.2 MB" },
  { name: "用户手册.pdf", size: "1.2 MB" }
]
function goBack() { uni.navigateBack() }
function selectFiles() {
  const remaining = sampleFiles.filter(f => !files.value.find(s => s.name === f.name))
  if (remaining.length === 0) {
    uni.showToast({ title: "已添加所有示例文件", icon: "none" })
    return
  }
  const pick = remaining[Math.floor(Math.random() * remaining.length)]
  files.value.push(pick)
  uni.showToast({ title: "已添加: " + pick.name, icon: "none" })
}
function moveUp(index) {
  if (index === 0) return
  const item = files.value.splice(index, 1)[0]
  files.value.splice(index - 1, 0, item)
}
function moveDown(index) {
  if (index >= files.value.length - 1) return
  const item = files.value.splice(index, 1)[0]
  files.value.splice(index + 1, 0, item)
}
function removeFile(index) {
  files.value.splice(index, 1)
}
function mergeFiles() {
  uni.showLoading({ title: "正在合并..." })
  setTimeout(function() {
    uni.hideLoading()
    uni.showToast({ title: "合并成功!", icon: "success" })
    files.value = []
  }, 1500)
}
onMounted(function() {
  if (!uni.getStorageSync("isLoggedIn")) {
    uni.reLaunch({ url: "/pages/login/login" })
    return
  }
})
</script>
<style scoped>
.page { min-height: 100vh; background: #f5f7fb }
.custom-nav { background: linear-gradient(135deg, #ef4444, #dc2626); width: 100% }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx }
.nav-icon { width: 72rpx; text-align: center; font-size: 44rpx; color: #fff; font-weight: 700; flex-shrink: 0 }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600 }
.content { padding: 24rpx }
.card { background: #fff; border-radius: 16rpx; padding: 32rpx; margin-bottom: 24rpx; box-shadow: 0 2rpx 12rpx rgba(0,0,0,0.06) }
.card-title { font-size: 32rpx; font-weight: 600; color: #1f2937 }
.card-desc { font-size: 26rpx; color: #6b7280; margin-top: 8rpx; display: block }
.btn-primary { background: linear-gradient(135deg, #ef4444, #dc2626); border-radius: 12rpx; padding: 24rpx; text-align: center; margin-top: 24rpx }
.btn-text { color: #fff; font-size: 28rpx; font-weight: 600 }
.file-list { background: #fff; border-radius: 16rpx; padding: 24rpx; margin-bottom: 24rpx; box-shadow: 0 2rpx 12rpx rgba(0,0,0,0.06) }
.section-title { font-size: 28rpx; font-weight: 600; color: #374151; margin-bottom: 16rpx; display: block }
.file-item { display: flex; align-items: center; justify-content: space-between; padding: 20rpx 0; border-bottom: 1rpx solid #f3f4f6 }
.file-item:last-child { border-bottom: none }
.file-info { display: flex; align-items: center; flex: 1 }
.file-icon { background: #fee2e2; color: #ef4444; font-size: 20rpx; font-weight: 700; padding: 8rpx 12rpx; border-radius: 8rpx; margin-right: 16rpx }
.file-detail { display: flex; flex-direction: column }
.file-name { font-size: 28rpx; color: #1f2937 }
.file-size { font-size: 24rpx; color: #9ca3af; margin-top: 4rpx }
.file-actions { display: flex; align-items: center; gap: 16rpx }
.action-btn { font-size: 28rpx; color: #6b7280; padding: 8rpx 12rpx }
.action-btn.delete { color: #ef4444 }
.btn-merge { background: linear-gradient(135deg, #ef4444, #dc2626); border-radius: 12rpx; padding: 28rpx; text-align: center; margin-top: 8rpx }
.empty-state { display: flex; flex-direction: column; align-items: center; padding: 80rpx 0 }
.empty-icon { font-size: 80rpx }
.empty-text { font-size: 26rpx; color: #9ca3af; margin-top: 16rpx }
</style>