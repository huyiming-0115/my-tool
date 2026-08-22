<template>
  <view class="pick-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">随机抽签</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="input-card">
        <view class="input-row"><input class="item-input" v-model="newItem" placeholder="输入选项后回车" confirm-type="done" @confirm="addItem" /><text class="add-btn" @click="addItem">+</text></view>
        <view class="item-tags"><text class="tag" v-for="(item, idx) in items" :key="idx">{{ item }}<text class="tag-del" @click="items.splice(idx, 1)">×</text></text></view>
        <view class="empty-hint" v-if="!items.length"><text>至少添加 2 个选项</text></view>
      </view>
      <view class="result-area" v-if="result">
        <text class="result-label">天选之人</text>
        <text class="result-value">{{ result }}</text>
      </view>
      <view class="slot-machine" v-else-if="items.length >= 2">
        <view class="slot-display"><text class="slot-text">{{ rolling || '✨' }}</text></view>
      </view>
      <view class="pick-btn" :class="{ disabled: items.length < 2 }" @click="startRoll">
        <text>{{ rolling ? '抽取中...' : '开始抽取' }}</text>
      </view>
      <view class="quick-presets">
        <text class="preset-title">快速选择</text>
        <view class="preset-list">
          <text class="preset-item" @click="loadPreset('food')">吃什么</text>
          <text class="preset-item" @click="loadPreset('who')">谁来做</text>
          <text class="preset-item" @click="loadPreset('yesno')">是否</text>
        </view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const items = ref([])
const newItem = ref("")
const result = ref("")
const rolling = ref("")
function addItem() { if (newItem.value.trim()) { items.value.push(newItem.value.trim()); newItem.value = ""; result.value = "" } }
function startRoll() {
  if (items.value.length < 2 || rolling.value) return
  let count = 0
  const timer = setInterval(() => { rolling.value = items.value[Math.floor(Math.random() * items.value.length)]; count++ }, 80)
  setTimeout(() => { clearInterval(timer); result.value = items.value[Math.floor(Math.random() * items.value.length)]; rolling.value = ""; uni.vibrateShort({}) }, 1500)
}
function loadPreset(type) {
  if (type === 'food') items.value = ["烤肉饭", "麻辣烫", "糖醋排骨", "饼干夜宵", "小火锅"]
  else if (type === 'who') items.value = ["小明", "红红", "张三", "李四"]
  else if (type === 'yesno') items.value = ["是", "否"]
  result.value = ""
}
function goBack() { uni.navigateBack() }
onMounted(() => { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.pick-page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #f093fb, #f5576c); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.input-card { background: #fff; border-radius: 24rpx; padding: 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); margin-bottom: 24rpx; }
.input-row { display: flex; align-items: center; gap: 16rpx; margin-bottom: 16rpx; }
.item-input { flex: 1; height: 72rpx; background: #f5f7fb; border-radius: 16rpx; padding: 0 20rpx; font-size: 28rpx; }
.add-btn { width: 72rpx; height: 72rpx; line-height: 72rpx; text-align: center; background: linear-gradient(135deg, #f093fb, #f5576c); color: #fff; border-radius: 16rpx; font-size: 36rpx; }
.item-tags { display: flex; flex-wrap: wrap; gap: 12rpx; }
.tag { display: inline-flex; align-items: center; gap: 8rpx; padding: 12rpx 20rpx; background: #f0f0ff; color: #6c5ce7; border-radius: 30rpx; font-size: 26rpx; }
.tag-del { color: #999; font-size: 28rpx; }
.empty-hint { text-align: center; padding: 32rpx; font-size: 24rpx; color: #999; }
.result-area { background: linear-gradient(135deg, #f093fb, #f5576c); border-radius: 24rpx; padding: 48rpx; text-align: center; margin-bottom: 24rpx; }
.result-label { font-size: 24rpx; color: rgba(255,255,255,0.8); display: block; }
.result-value { font-size: 48rpx; color: #fff; font-weight: 700; display: block; margin-top: 16rpx; }
.slot-machine { background: #fff; border-radius: 24rpx; padding: 80rpx 40rpx; text-align: center; margin-bottom: 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.slot-text { font-size: 56rpx; color: #f5576c; font-weight: 700; }
.pick-btn { background: linear-gradient(135deg, #f093fb, #f5576c); border-radius: 16rpx; padding: 28rpx; text-align: center; margin-bottom: 24rpx; }
.pick-btn text { font-size: 32rpx; color: #fff; font-weight: 600; }
.pick-btn.disabled { opacity: 0.4; }
.quick-presets { background: #fff; border-radius: 24rpx; padding: 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.preset-title { font-size: 26rpx; color: #999; margin-bottom: 16rpx; display: block; }
.preset-list { display: flex; gap: 16rpx; }
.preset-item { padding: 12rpx 24rpx; background: #f5f5f5; border-radius: 20rpx; font-size: 26rpx; color: #666; }
</style>
