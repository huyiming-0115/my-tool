<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">CSV\u89e3\u6790\u5668</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <textarea class="csv-input" v-model="csvText" placeholder="\u7c98\u8d34CSV\u6570\u636e\u5230\u8fd9\u91cc" auto-height></textarea>
      <view class="opt-row">
        <text class="opt-label">\u5206\u9694\u7b26:</text>
        <text class="sep-btn" :class="{active: sep==','}" @click="sep=','">\u9017\u53f7</text>
        <text class="sep-btn" :class="{active: sep=='\t'}" @click="sep='\t'">Tab</text>
        <text class="sep-btn" :class="{active: sep==';'}" @click="sep=';'">\u5206\u53f7</text>
      </view>
      <view class="calc-btn" @click="parse"><text>\u89e3\u6790</text></view>
      <scroll-view class="table-scroll" scroll-x scroll-y v-if="rows.length > 0">
        <view class="csv-table">
          <view class="csv-row header"><text class="csv-cell" v-for="(h, i) in rows[0]" :key="i">{{ h }}</text></view>
          <view class="csv-row" v-for="(row, ri) in rows.slice(1)" :key="ri"><text class="csv-cell" v-for="(cell, ci) in row" :key="ci">{{ cell }}</text></view>
        </view>
      </scroll-view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const csvText = ref("")
const sep = ref(",")
const rows = ref([])
function parse() {
  if (!csvText.value.trim()) { uni.showToast({ title: "\u8bf7\u8f93\u5165CSV\u6570\u636e", icon: "none" }); return }
  const lines = csvText.value.trim().split("\n")
  rows.value = lines.map(function(line) { return line.split(sep.value) })
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #fa709a, #fee140); }
.custom-nav { background: linear-gradient(135deg, #e84393, #fdcb6e); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.csv-input { background: #fff; border-radius: 20rpx; padding: 24rpx; font-size: 26rpx; min-height: 200rpx; margin-bottom: 20rpx; }
.opt-row { display: flex; align-items: center; gap: 12rpx; margin-bottom: 20rpx; }
.opt-label { color: rgba(255,255,255,0.8); font-size: 26rpx; }
.sep-btn { padding: 12rpx 24rpx; border-radius: 12rpx; background: rgba(255,255,255,0.3); color: #fff; font-size: 24rpx; }
.sep-btn.active { background: #fff; color: #e84393; }
.calc-btn { background: linear-gradient(135deg, #e84393, #fdcb6e); border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 24rpx; }
.calc-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.table-scroll { max-height: 60vh; background: #fff; border-radius: 16rpx; overflow: auto; }
.csv-table { min-width: 100%; }
.csv-row { display: flex; }
.csv-row.header { background: #f8f8f8; }
.csv-cell { min-width: 160rpx; padding: 16rpx; font-size: 24rpx; border: 1rpx solid #eee; flex-shrink: 0; }
.csv-row.header .csv-cell { font-weight: 700; }
</style>
