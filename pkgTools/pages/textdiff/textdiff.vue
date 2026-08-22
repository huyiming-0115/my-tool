<template><view class="page"><view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }"><view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">文本对比</text><text class="nav-icon" @click="compare">✅</text></view></view><view class="content"><view class="diff-row"><view class="diff-col"><text class="diff-label">旧文本</text><textarea class="diff-input" v-model="textA" placeholder="输入旧内容..." maxlength="1000" auto-height /></view><view class="diff-col"><text class="diff-label">新文本</text><textarea class="diff-input" v-model="textB" placeholder="输入新内容..." maxlength="1000" auto-height /></view></view><view class="diff-result" v-if="result.length"><view class="diff-line" v-for="(line, idx) in result" :key="idx" :class="line.type"><text>{{ line.text }}</text></view></view></view></view></template><script setup>import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const textA = ref(""); const textB = ref(""); const result = ref([])
function compare() {
  var a = textA.value.split("\n"); var b = textB.value.split("\n"); var r = []
  var max = Math.max(a.length, b.length)
  for (var i = 0; i < max; i++) {
    if (a[i] === b[i]) r.push({ type: "same", text: a[i] || "" })
    else { if (a[i]) r.push({ type: "removed", text: "- " + a[i] }); if (b[i]) r.push({ type: "added", text: "+ " + b[i] }) }
  }
  result.value = r
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script><style scoped>.page{min-height:100vh;background:#f5f7fb}.custom-nav{background:linear-gradient(135deg,#6c5ce7,#a29bfe);width:100%}.nav-row{height:88rpx;display:flex;align-items:center;padding:0 24rpx}.nav-icon{width:72rpx;text-align:center;font-size:48rpx;color:#fff;font-weight:700;flex-shrink:0}.nav-title{flex:1;text-align:center;font-size:32rpx;color:#fff;font-weight:600}.content{padding:24rpx}.diff-row{display:flex;gap:16rpx;margin-bottom:24rpx}.diff-col{flex:1}.diff-label{font-size:24rpx;color:#999;display:block;margin-bottom:8rpx}.diff-input{width:100%;min-height:200rpx;background:#fff;border-radius:16rpx;padding:16rpx;font-size:26rpx;box-sizing:border-box}.diff-result{background:#fff;border-radius:20rpx;padding:16rpx;font-family:monospace;font-size:24rpx}.diff-line{padding:8rpx 16rpx;border-radius:8rpx;margin-bottom:4rpx}.diff-line.addy{background:#d4edda;color:#155724}.diff-line.removed{background:#f8d7da;color:#721c24}.diff-line.same{color:#666}</style>