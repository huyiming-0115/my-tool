<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">抛硬币</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="coin-area">
        <view class="coin" :class="{ flipping: flipping }">
          <text class="coin-face">{{ result === "正" ? "☉" : result === "反" ? "☽" : "🧨" }}</text>
        </view>
      </view>
      <view class="flip-btn" :class="{ disabled: flipping }" @click="flip"><text>{{ flipping ? "翻转中..." : "抛硬币" }}</text></view>
      <view class="coin-stats" v-if="history.length">
        <text class="stats-title">统计 ({{ history.length }}次)</text>
        <view class="stats-row"><text>正面: {{ history.filter(function(h){return h==="正"}).length }}</text><text>反面: {{ history.filter(function(h){return h==="反"}).length }}</text></view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const result = ref("?")
const flipping = ref(false)
const history = ref([])
function flip() {
  if (flipping.value) return
  flipping.value = true
  var count = 0
  var timer = setInterval(function() { result.value = Math.random() > 0.5 ? "正" : "反"; count++ }, 100)
  setTimeout(function() { clearInterval(timer); flipping.value = false; history.value.unshift(result.value); if (history.value.length > 50) history.value.pop(); uni.vibrateShort({}) }, 1200)
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #f9ca24, #f0932b); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; display: flex; flex-direction: column; align-items: center; }
.coin-area { margin-bottom: 40rpx; }
.coin { width: 240rpx; height: 240rpx; border-radius: 50%; background: linear-gradient(135deg, #f9ca24, #f0932b); display: flex; align-items: center; justify-content: center; box-shadow: 0 8rpx 32rpx rgba(240,147,43,0.4); }
.coin.flipping { animation: coinFlip 0.15s infinite; }
@keyframes coinFlip { 0% { transform: rotateY(0); } 100% { transform: rotateY(180deg); } }
.coin-face { font-size: 100rpx; color: #fff; }
.flip-btn { width: 80%; background: linear-gradient(135deg, #f9ca24, #f0932b); border-radius: 16rpx; padding: 28rpx; text-align: center; margin-bottom: 32rpx; }
.flip-btn text { font-size: 32rpx; color: #fff; font-weight: 600; }
.flip-btn.disabled { opacity: 0.4; }
.coin-stats { background: #fff; border-radius: 20rpx; padding: 24rpx; width: 100%; box-sizing: border-box; }
.stats-title { font-size: 26rpx; color: #999; display: block; margin-bottom: 12rpx; }
.stats-row { display: flex; justify-content: space-around; font-size: 28rpx; color: #333; font-weight: 600; }
</style>