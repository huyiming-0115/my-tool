
<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">随机决定器</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="dw-input-row">
        <input class="dw-input" v-model="newOption" placeholder="输入选项" @keyup.enter="addOption" />
        <view class="dw-add-btn" @click="addOption"><text>+</text></view>
      </view>
      <view class="dw-options-list">
        <view class="dw-option-tag" v-for="(opt, i) in options" :key="i">
          <text>{{opt}}</text>
          <text class="dw-remove" @click="removeOption(i)">×</text>
        </view>
      </view>
      <view class="dw-wheel-container">
        <view class="dw-wheel" :style="{transform: 'rotate('+rotation+'deg)', transitionDuration: spinning?s+'s':'0s'}">
          <view class="dw-slice" v-for="(opt, i) in options" :key="i" :style="{transform: 'rotate('+(i*(360/options.length))+'deg)', background: wheelColors[i % wheelColors.length]}">
            <text class="dw-slice-text">{{opt}}</text>
          </view>
        </view>
        <view class="dw-pointer">▲</view>
      </view>
      <view class="dw-btn" :class="{disabled: spinning || options.length<2}" @click="spin"><text>{{spinning ? "转动中..." : "开始"}}</text></view>
      <view class="dw-result" v-if="result"><text>结果: {{result}}</text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const options = ref(["吃火锅", "吃烧烤", "吃日料", "吃西餐", "吃川菜"])
const newOption = ref("")
const rotation = ref(0)
const spinning = ref(false)
const s = ref(3)
const result = ref("")
const wheelColors = ["#ff6b6b","#feca57","#48dbfb","#ff9ff3","#54a0ff","#5f27cd","#01a3a4","#f368e0"]
function addOption() {
  if (!newOption.value.trim()) return
  options.value.push(newOption.value.trim())
  newOption.value = ""
}
function removeOption(i) { options.value.splice(i, 1) }
function spin() {
  if (spinning.value || options.value.length < 2) return
  spinning.value = true
  result.value = ""
  var extraSpins = 5 + Math.random() * 3
  var sliceAngle = 360 / options.value.length
  var targetIdx = Math.floor(Math.random() * options.value.length)
  var targetAngle = 360 - (targetIdx * sliceAngle + sliceAngle / 2)
  rotation.value += extraSpins * 360 + targetAngle
  s.value = 3 + Math.random() * 2
  setTimeout(function() {
    spinning.value = false
    result.value = options.value[targetIdx]
  }, s.value * 1000)
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #f7971e, #ffd200); }
.custom-nav { background: linear-gradient(135deg, #f7971e, #ffd200); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 32rpx; }
.dw-input-row { display: flex; gap: 12rpx; margin-bottom: 20rpx; }
.dw-input { flex: 1; background: rgba(255,255,255,0.3); border-radius: 16rpx; padding: 16rpx 20rpx; font-size: 28rpx; color: #fff; }
.dw-add-btn { width: 72rpx; height: 72rpx; background: #fff; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
.dw-add-btn text { color: #f7971e; font-size: 40rpx; font-weight: 700; }
.dw-options-list { display: flex; flex-wrap: wrap; gap: 12rpx; margin-bottom: 32rpx; }
.dw-option-tag { background: rgba(255,255,255,0.3); border-radius: 30rpx; padding: 8rpx 20rpx; display: flex; align-items: center; gap: 8rpx; }
.dw-option-tag text { color: #fff; font-size: 26rpx; }
.dw-remove { color: rgba(255,255,255,0.6); font-size: 32rpx; }
.dw-wheel-container { position: relative; width: 500rpx; height: 500rpx; margin: 0 auto 32rpx; }
.dw-wheel { width: 100%; height: 100%; border-radius: 50%; position: relative; overflow: hidden; transition: transform cubic-bezier(0.17,0.67,0.12,0.99); box-shadow: 0 8rpx 32rpx rgba(0,0,0,0.2); }
.dw-slice { position: absolute; width: 50%; height: 50%; transform-origin: 100% 100%; top: 0; right: 50%; display: flex; align-items: flex-start; justify-content: center; padding-top: 40rpx; }
.dw-slice-text { color: #fff; font-size: 24rpx; font-weight: 700; text-shadow: 0 2rpx 4rpx rgba(0,0,0,0.3); }
.dw-pointer { position: absolute; top: -20rpx; left: 50%; transform: translateX(-50%); color: #fff; font-size: 48rpx; z-index: 10; }
.dw-btn { background: #fff; border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 20rpx; }
.dw-btn text { color: #f7971e; font-size: 32rpx; font-weight: 700; }
.dw-btn.disabled { opacity: 0.5; }
.dw-result { text-align: center; background: rgba(255,255,255,0.3); border-radius: 16rpx; padding: 20rpx; }
.dw-result text { color: #fff; font-size: 36rpx; font-weight: 700; }
</style>
