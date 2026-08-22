<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">拼音转换</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <textarea class="py-input" v-model="input" placeholder="输入中文..." maxlength="500" auto-height />
      <view class="py-output" v-if="pinyin"><text>{{ pinyin }}</text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, computed, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const input = ref("")
var pyMap = {"一":"yi","二":"er","三":"san","四":"si","五":"wu","六":"liu","七":"qi","八":"ba","九":"jiu","十":"shi","中":"zhong","国":"guo","人":"ren","大":"da","小":"xiao","学":"xue","生":"sheng","日":"ri","月":"yue","年":"nian","时":"shi","分":"fen","秒":"miao","天":"tian","地":"di","水":"shui","火":"huo","山":"shan","果":"guo","心":"xin","手":"shou","口":"kou","目":"mu","耳":"er","身":"shen","车":"che","马":"ma","鸟":"niao","鱼":"yu","虫":"chong","风":"feng","雨":"yu","雪":"xue","树":"shu","叶":"ye","花":"hua","草":"cao","竹":"zhu","梅":"mei","兰":"lan","菊":"ju","千":"qian","万":"wan","百":"bai","仟":"wan","亿":"yi"}
const pinyin = computed(function() { return input.value.split("").map(function(c) { return pyMap[c] || c }).join(" ") })
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #fd79a8, #e84393); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.py-input { width: 100%; min-height: 200rpx; background: #fff; border-radius: 20rpx; padding: 24rpx; font-size: 30rpx; box-sizing: border-box; margin-bottom: 24rpx; }
.py-output { background: #fff; border-radius: 20rpx; padding: 24rpx; font-size: 30rpx; color: #333; line-height: 1.8; }
</style>