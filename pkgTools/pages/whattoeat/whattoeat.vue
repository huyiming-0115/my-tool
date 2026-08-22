<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">今天吃什么</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="eat-card">
        <text class="eat-emoji">{{ emoji }}</text>
        <text class="eat-name">{{ food }}</text>
      </view>
      <view class="eat-btn" @click="pickFood"><text>{{ picking ? "思考中..." : "帮我选" }}</text></view>
      <view class="edit-section">
        <text class="section-title">自定义菜单 (每行一个)</text>
        <textarea class="food-input" v-model="foodList" placeholder="输入食物名称，每行一个" auto-height></textarea>
        <view class="save-btn" @click="saveList"><text>保存菜单</text></view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const defaultFoods = ["火锅","烧烤","麻辣烫","黄焖鸡","兰州拉面","沙县小吃","饺子","炒饭","盖浇饭","螺蛳粉","酸菜鱼","寿司","披萨","汉堡","炸鸡","寿司","米线","馄饨"]
const emojis = ["🍲","🍖","🌶️","🍗","🍜","🥟","🍱","🍛","🍝","🦪","🐟","🍣","🍕","🍔","🍟","🍙","🍲","🥣"]
const food = ref("点击下方按钮")
const emoji = ref("🤔")
const picking = ref(false)
const foodList = ref("")
let saved = []
function pickFood() {
  if (picking.value) return
  picking.value = true
  const list = saved.length > 0 ? saved : defaultFoods
  let count = 0
  const timer = setInterval(function() {
    const idx = Math.floor(Math.random() * list.length)
    food.value = list[idx]
    emoji.value = emojis[idx % emojis.length]
    count++
    if (count > 15) { clearInterval(timer); picking.value = false; uni.vibrateShort({}) }
  }, 80)
}
function saveList() {
  const arr = foodList.value.split("\n").map(function(s){return s.trim()}).filter(function(s){return s})
  if (arr.length < 2) { uni.showToast({ title: "至少输入2个食物", icon: "none" }); return }
  saved = arr
  uni.setStorageSync("whattoeat_list", arr)
  uni.showToast({ title: "已保存", icon: "success" })
}
function goBack() { uni.navigateBack() }
onMounted(function() {
  if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }
  const s = uni.getStorageSync("whattoeat_list")
  if (s && s.length > 0) { saved = s; foodList.value = s.join("\n") }
  else { foodList.value = defaultFoods.join("\n") }
})
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #ffecd2, #fcb69f); }
.custom-nav { background: linear-gradient(135deg, #ff6b6b, #ee5a24); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; display: flex; flex-direction: column; align-items: center; }
.eat-card { width: 100%; background: #fff; border-radius: 32rpx; padding: 60rpx 40rpx; text-align: center; box-shadow: 0 8rpx 32rpx rgba(238,90,36,0.15); margin-bottom: 40rpx; }
.eat-emoji { font-size: 120rpx; display: block; margin-bottom: 20rpx; }
.eat-name { font-size: 48rpx; color: #333; font-weight: 700; }
.eat-btn { width: 80%; background: linear-gradient(135deg, #ff6b6b, #ee5a24); border-radius: 16rpx; padding: 28rpx; text-align: center; margin-bottom: 40rpx; }
.eat-btn text { font-size: 32rpx; color: #fff; font-weight: 600; }
.edit-section { width: 100%; background: #fff; border-radius: 24rpx; padding: 32rpx; }
.section-title { font-size: 28rpx; color: #666; margin-bottom: 16rpx; display: block; }
.food-input { width: 100%; min-height: 200rpx; background: #f8f8f8; border-radius: 16rpx; padding: 20rpx; font-size: 28rpx; color: #333; margin-bottom: 20rpx; }
.save-btn { background: #ff6b6b; border-radius: 12rpx; padding: 20rpx; text-align: center; }
.save-btn text { color: #fff; font-size: 28rpx; font-weight: 600; }
</style>
