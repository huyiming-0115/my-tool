<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u7b14\u8bb0Pro</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="search-row"><input class="search-input" v-model="keyword" placeholder="\u641c\u7d22\u7b14\u8bb0" /><text class="add-note" @click="createNote">+</text></view>
      <view class="note-list">
        <view class="note-card" v-for="(n, i) in filteredNotes" :key="i" @click="editNote(n)">
          <text class="note-title">{{ n.title }}</text>
          <text class="note-preview">{{ n.content }}</text>
          <view class="note-meta"><text class="note-tag" v-for="(t, ti) in n.tags" :key="ti">{{ t }}</text><text class="note-date">{{ n.date }}</text></view>
        </view>
      </view>
      <view class="editor-card" v-if="editing">
        <input class="editor-title" v-model="editing.title" placeholder="\u6807\u9898" />
        <textarea class="editor-content" v-model="editing.content" placeholder="\u5185\u5bb9" auto-height></textarea>
        <view class="editor-actions"><text class="e-btn save" @click="saveNote">\u4fdd\u5b58</text><text class="e-btn cancel" @click="editing=null">\u53d6\u6d88</text></view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, computed, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const keyword = ref("")
const editing = ref(null)
const notes = ref([
  {title:"\u5de5\u4f5c\u8ba1\u5212", content:"\u672c\u5468\u5b8c\u6210\u9879\u76ee\u65b9\u6848", tags:["\u5de5\u4f5c"], date:"2024-01-15"},
  {title:"\u5b66\u4e60\u7b14\u8bb0", content:"Vue3 \u7ec4\u4ef6\u5f00\u53d1\u89c4\u8303", tags:["\u5b66\u4e60","\u6280\u672f"], date:"2024-01-14"},
  {title:"\u8d2d\u7269\u6e05\u5355", content:"\u7535\u8111\u3001\u9f20\u6807\u3001\u952e\u76d8", tags:["\u751f\u6d3b"], date:"2024-01-13"}
])
const filteredNotes = computed(function() {
  if (!keyword.value) return notes.value
  return notes.value.filter(function(n){return n.title.includes(keyword.value) || n.content.includes(keyword.value)})
})
function createNote() { editing.value = {title:"", content:"", tags:[], date:new Date().toLocaleDateString()} }
function editNote(n) { editing.value = Object.assign({}, n) }
function saveNote() {
  if (!editing.value.title) { uni.showToast({ title: "\u8bf7\u8f93\u5165\u6807\u9898", icon: "none" }); return }
  var idx = notes.value.findIndex(function(n){return n.title===editing.value.title})
  if (idx >= 0) notes.value[idx] = editing.value
  else notes.value.unshift(editing.value)
  editing.value = null
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #f6d365, #fda085); }
.custom-nav { background: linear-gradient(135deg, #f39c12, #e17055); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.search-row { display: flex; gap: 16rpx; margin-bottom: 24rpx; }
.search-input { flex: 1; background: #fff; border-radius: 16rpx; padding: 20rpx 24rpx; font-size: 28rpx; }
.add-note { background: #f39c12; color: #fff; border-radius: 16rpx; width: 80rpx; display: flex; align-items: center; justify-content: center; font-size: 40rpx; font-weight: 700; }
.note-list { display: flex; flex-direction: column; gap: 16rpx; }
.note-card { background: #fff; border-radius: 20rpx; padding: 24rpx; }
.note-title { font-size: 28rpx; font-weight: 600; color: #333; display: block; }
.note-preview { font-size: 24rpx; color: #666; display: block; margin: 8rpx 0; }
.note-meta { display: flex; gap: 8rpx; align-items: center; }
.note-tag { padding: 4rpx 12rpx; background: #fff3cd; border-radius: 8rpx; font-size: 20rpx; color: #856404; }
.note-date { margin-left: auto; font-size: 20rpx; color: #999; }
.editor-card { background: #fff; border-radius: 20rpx; padding: 24rpx; margin-top: 24rpx; }
.editor-title { font-size: 28rpx; font-weight: 600; color: #333; border-bottom: 2rpx solid #f0f0f0; padding-bottom: 16rpx; margin-bottom: 16rpx; }
.editor-content { width: 100%; min-height: 200rpx; font-size: 26rpx; color: #333; }
.editor-actions { display: flex; gap: 16rpx; margin-top: 16rpx; }
.e-btn { flex: 1; text-align: center; padding: 16rpx; border-radius: 12rpx; font-size: 26rpx; }
.e-btn.save { background: #f39c12; color: #fff; }
.e-btn.cancel { background: #f0f0f0; color: #666; }
</style>
