<template><view class="page"><view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }"><view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">密码强度</text><text class="nav-icon empty"> </text></view></view><view class="content"><input class="ps-input" v-model="password" placeholder="输入密码..." password @input="check" /><view class="ps-bar"><view class="ps-fill" :style="{ width: score + '%', background: color }"></view></view><view class="ps-label" :style="{ color: color }">{{ level }}</view><view class="ps-checks"><view class="ps-check" v-for="c in checks" :key="c.label"><text :class="c.pass ? 'pass' : 'fail'">{{ c.pass ? "✓" : "✗" }} {{ c.label }}</text></view></view></view></view></template><script setup>import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const password = ref(""); const score = ref(0); const level = ref("未输入"); const color = ref("#ddd")
const checks = ref([{label:"至少8个字符",pass:false},{label:"包含大写字母",pass:false},{label:"包含小写字母",pass:false},{label:"包含数字",pass:false},{label:"包含特殊符号",pass:false}])
function check() {
  var p = password.value; var s = 0
  var len = p.length >= 8; var upper = /[A-Z]/.test(p); var lower = /[a-z]/.test(p); var num = /\d/.test(p); var sym = /[^A-Za-z0-9]/.test(p)
  checks.value = [{label:"至少8个字符",pass:len},{label:"包含大写字母",pass:upper},{label:"包含小写字母",pass:lower},{label:"包含数字",pass:num},{label:"包含特殊符号",pass:sym}]
  if (len) s += 20; if (upper) s += 20; if (lower) s += 20; if (num) s += 20; if (sym) s += 20
  score.value = s
  if (s <= 20) { level.value = "很弱"; color.value = "#e17055" }
  else if (s <= 40) { level.value = "弱"; color.value = "#fdcb6e" }
  else if (s <= 60) { level.value = "中等"; color.value = "#74b9ff" }
  else if (s <= 80) { level.value = "强"; color.value = "#00b894" }
  else { level.value = "非常强"; color.value = "#00cec9" }
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script><style scoped>.page{min-height:100vh;background:#f5f7fb}.custom-nav{background:linear-gradient(135deg,#e84393,#fd79a8);width:100%}.nav-row{height:88rpx;display:flex;align-items:center;padding:0 24rpx}.nav-icon{width:72rpx;text-align:center;font-size:48rpx;color:#fff;font-weight:700;flex-shrink:0}.nav-title{flex:1;text-align:center;font-size:32rpx;color:#fff;font-weight:600}.content{padding:24rpx}.ps-input{width:100%;height:80rpx;background:#fff;border-radius:16rpx;padding:0 24rpx;font-size:30rpx;box-sizing:border-box;margin-bottom:24rpx}.ps-bar{width:100%;height:24rpx;background:#eee;border-radius:12rpx;overflow:hidden;margin-bottom:16rpx}.ps-fill{height:100%;border-radius:12rpx;transition:all 0.3s}.ps-label{font-size:28rpx;font-weight:700;margin-bottom:24rpx}.ps-checks{background:#fff;border-radius:20rpx;padding:16rpx 24rpx}.ps-check{padding:12rpx 0;font-size:26rpx;color:#666}.ps-check .pass{color:#00b894}.ps-check .fail{color:#e17055}</style>