
<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">闪卡记忆</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="fc-progress"><text>{{current+1}} / {{cards.length}}</text></view>
      <view class="fc-card" :class="{flipped: isFlipped}" @click="isFlipped=!isFlipped" v-if="cards.length">
        <view class="fc-card-inner">
          <view class="fc-card-face fc-front"><text class="fc-label">正面</text><text class="fc-text">{{cards[current]?.front || ''}}</text></view>
          <view class="fc-card-face fc-back"><text class="fc-label">背面</text><text class="fc-text">{{cards[current]?.back || ''}}</text></view>
        </view>
      </view>
      <view class="fc-hint" v-if="cards.length"><text>点击卡片翻转</text></view>
      <view class="fc-nav-btns">
        <view class="fc-nav-btn" :class="{disabled: current<=0}" @click="prev"><text>上一张</text></view>
        <view class="fc-nav-btn" :class="{disabled: current>=cards.length-1}" @click="next"><text>下一张</text></view>
      </view>
      <view class="fc-actions">
        <view class="fc-action" @click="showAdd=true"><text>+ 添加卡片</text></view>
        <view class="fc-action" @click="shuffle"><text>🔀 打乱</text></view>
      </view>
      <view class="fc-add-modal" v-if="showAdd">
        <view class="fc-add-box">
          <text class="fc-add-title">添加新卡片</text>
          <input class="fc-add-input" v-model="newFront" placeholder="正面内容" />
          <input class="fc-add-input" v-model="newBack" placeholder="背面内容" />
          <view class="fc-add-btns">
            <view class="fc-add-btn" @click="showAdd=false"><text>取消</text></view>
            <view class="fc-add-btn primary" @click="addCard"><text>添加</text></view>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const cards = ref([
  {front:"Apple",back:"苹果"},
  {front:"Butterfly",back:"蝴蝶"},
  {front:"Catastrophe",back:"灾难"},
  front:"Ephemeral",back:"短暂的"},
  {front:"Serendipity",back:"意外之喜"}
])
const current = ref(0)
const isFlipped = ref(false)
const showAdd = ref(false)
const newFront = ref("")
const newBack = ref("")
function next() {
  if (current.value < cards.value.length - 1) { current.value++; isFlipped.value = false }
}
function prev() {
  if (current.value > 0) { current.value--; isFlipped.value = false }
}
function shuffle() {
  cards.value = cards.value.slice().sort(function() { return Math.random() - 0.5 })
  current.value = 0
  isFlipped.value = false
}
function addCard() {
  if (!newFront.value || !newBack.value) return
  cards.value.push({front: newFront.value, back: newBack.value})
  newFront.value = ""
  newBack.value = ""
  showAdd.value = false
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #a8edea, #fed6e3); }
.custom-nav { background: linear-gradient(135deg, #a8edea, #fed6e3); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #555; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #555; font-weight: 600; }
.content { padding: 32rpx; }
.fc-progress { text-align: center; margin-bottom: 24rpx; }
.fc-progress text { color: #888; font-size: 28rpx; }
.fc-card { perspective: 1000rpx; height: 400rpx; margin-bottom: 16rpx; }
.fc-card-inner { position: relative; width: 100%; height: 100%; transition: transform 0.6s; transform-style: preserve-3d; }
.fc-card.flipped .fc-card-inner { transform: rotateY(180deg); }
.fc-card-face { position: absolute; inset: 0; backface-visibility: hidden; border-radius: 24rpx; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 40rpx; }
.fc-front { background: linear-gradient(135deg, #667eea, #764ba2); }
.fc-back { background: linear-gradient(135deg, #f093fb, #f5576c); transform: rotateY(180deg); }
.fc-label { color: rgba(255,255,255,0.6); font-size: 24rpx; margin-bottom: 20rpx; }
.fc-text { color: #fff; font-size: 40rpx; font-weight: 700; text-align: center; }
.fc-hint { text-align: center; margin-bottom: 24rpx; }
.fc-hint text { color: #999; font-size: 24rpx; }
.fc-nav-btns { display: flex; gap: 20rpx; margin-bottom: 24rpx; }
.fc-nav-btn { flex: 1; text-align: center; padding: 20rpx; background: rgba(102,126,234,0.1); border-radius: 16rpx; }
.fc-nav-btn text { color: #667eea; font-size: 28rpx; font-weight: 600; }
.fc-nav-btn.disabled { opacity: 0.3; }
.fc-actions { display: flex; gap: 20rpx; }
.fc-action { flex: 1; text-align: center; padding: 20rpx; background: rgba(255,255,255,0.5); border-radius: 16rpx; }
.fc-action text { color: #555; font-size: 28rpx; }
.fc-add-modal { position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 999; }
.fc-add-box { background: #fff; border-radius: 24rpx; padding: 40rpx; width: 80%; }
.fc-add-title { font-size: 32rpx; font-weight: 700; color: #333; display: block; margin-bottom: 24rpx; }
.fc-add-input { background: #f5f5f5; border-radius: 12rpx; padding: 16rpx 20rpx; font-size: 28rpx; margin-bottom: 16rpx; }
.fc-add-btns { display: flex; gap: 16rpx; margin-top: 24rpx; }
.fc-add-btn { flex: 1; text-align: center; padding: 16rpx; background: #eee; border-radius: 12rpx; }
.fc-add-btn text { color: #666; font-size: 28rpx; }
.fc-add-btn.primary { background: #667eea; }
.fc-add-btn.primary text { color: #fff; }
</style>
