
<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">CSV解析器</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="cp-card">
        <text class="cp-label">粘贴CSV数据</text>
        <textarea class="cp-textarea" v-model="csvInput" placeholder="姓名,年龄,城市&#10;张三,25,北京&#10;李四,30,上海" />
      </view>
      <view class="cp-options">
        <text class="cp-label">分隔符</text>
        <view class="cp-delimiters">
          <view class="cp-del" :class="{active: delimiter===','}" @click="delimiter=','"><text>逗号</text></view>
          <view class="cp-del" :class:{active: delimiter==='	'}" @click="delimiter='	'"><text>制表符</text></view>
          <view class="cp-del" :class="{active: delimiter===';'}" @click="delimiter=';'"><text>分号</text></view>
          <view class="cp-del" :class="{active: delimiter==='|'}" @click="delimiter='|'"><text>竖线</text></view>
        </view>
      </view>
      <view class="cp-btn" @click="parse"><text>解析</text></view>
      <view class="cp-result" v-if="headers.length">
        <view class="cp-result-header">
          <text class="cp-result-title">解析结果 ({{rows.length}}行)</text>
          <view class="cp-copy" @click="copyResult"><text>复制JSON</text></view>
        </view>
        <scroll-view class="cp-table" scroll-x>
          <view class="cp-row cp-header">
            <view class="cp-cell" v-for="(h, i) in headers" :key="i"><text>{{h}}</text></view>
          </view>
          <view class="cp-row" v-for="(row, ri) in rows.slice(0, 20)" :key="ri">
            <view class="cp-cell" v-for="(cell, ci) in row" :key="ci"><text>{{cell}}</text></view>
          </view>
        </scroll-view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const csvInput = ref("")
const delimiter = ref(",")
const headers = ref([])
const rows = ref([])
function parse() {
  if (!csvInput.value.trim()) return
  var lines = csvInput.value.trim().split(/
?
/)
  if (lines.length === 0) return
  headers.value = lines[0].split(delimiter.value).map(function(h) { return h.trim() })
  rows.value = lines.slice(1).map(function(line) {
    return line.split(delimiter.value).map(function(c) { return c.trim() })
  })
}
function copyResult() {
  var json = JSON.stringify(rows.value.map(function(row) {
    var obj = {}
    headers.value.forEach(function(h, i) { obj[h] = row[i] || "" })
    return obj
  }), null, 2)
  uni.setClipboardData({ data: json })
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #4facfe, #00f2fe); }
.custom-nav { background: linear-gradient(135deg, #4facfe, #00f2fe); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 32rpx; }
.cp-card { background: rgba(255,255,255,0.2); border-radius: 20rpx; padding: 24rpx; margin-bottom: 20rpx; }
.cp-label { color: rgba(255,255,255,0.8); font-size: 26rpx; display: block; margin-bottom: 12rpx; }
.cp-textarea { background: rgba(255,255,255,0.2); border-radius: 12rpx; padding: 16rpx 20rpx; font-size: 26rpx; color: #fff; width: 100%; box-sizing: border-box; min-height: 200rpx; }
.cp-options { margin-bottom: 20rpx; }
.cp-delimiters { display: flex; gap: 12rpx; }
.cp-del { flex: 1; text-align: center; padding: 12rpx; background: rgba(255,255,255,0.15); border-radius: 12rpx; }
.cp-del text { color: rgba(255,255,255,0.7); font-size: 26rpx; }
.cp-del.active { background: #fff; }
.cp-del.active text { color: #4facfe; font-weight: 600; }
.cp-btn { background: #fff; border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 24rpx; }
.cp-btn text { color: #4facfe; font-size: 32rpx; font-weight: 700; }
.cp-result { background: rgba(255,255,255,0.2); border-radius: 20rpx; padding: 24rpx; }
.cp-result-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16rpx; }
.cp-result-title { color: #fff; font-size: 28rpx; font-weight: 600; }
.cp-copy { background: rgba(255,255,255,0.3); padding: 8rpx 20rpx; border-radius: 8rpx; }
.cp-copy text { color: #fff; font-size: 24rpx; }
.cp-table { white-space: nowrap; }
.cp-row { display: flex; border-bottom: 1rpx solid rgba(255,255,255,0.1); }
.cp-row.cp-header { background: rgba(255,255,255,0.15); }
.cp-cell { min-width: 200rpx; padding: 16rpx; }
.cp-cell text { color: #fff; font-size: 26rpx; }
</style>
