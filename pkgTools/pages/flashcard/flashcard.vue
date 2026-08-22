<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u95ea\u5361\u8bb0\u5fc6</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="fc-progress">{{ current+1 }}/{{ cards.length }}</view>
      <view class="fc-card" @click="flipped=!flipped" v-if="cards.length > 0">
        <view class="fc-inner" :class="{flip: flipped}">
          <text class="fc-front">{{ cards[current].front }}</text>
          <text class="fc-back">{{ cards[current].back }}</text>
        </view>
      </view>
      <view class="fc-actions" v-if="cards.length > 0">
        <text class="fc-btn prev" @click="prevCard">\u25c0 \u4e0a\u4e00\u5f20</text>
        <text class="fc-btn next" @click="nextCard">\u4e0b\u4e00\u5f20 \u25b6</text>
      </view>
      <view class="fc-add">
        <input class="fc-input" v-model="newFront" placeholder="\u6b63\u9762 (\u95ee\u9898)" />
        <input class="fc-input" v-model="newBack" placeholder="\u53cd\u9762 (\u7b54\u6848)" />
        <text class="fc-add-btn" @click="addCard">+ \u6dfb\u52a0\u5361\u7247</text>
      </view>
      <view class="empty" v-if="cards.length === 0"><text>\u8fd8\u6ca1\u6709\u5361\u7247\uff0c\u6dfb\u52a0\u7b2c\u4e00\u5f20\u5427</text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const cards = ref([{front:"\u4ec0\u4e48\u662fVue3?",back:"\u6700\u65b0\u7248\u672cVue\u6846\u67b6"},{front:"uni-app\u662f\u4ec0\u4e48?",back:"\u8de8\u5e73\u53f0\u5f00\u53d1\u6846\u67b6"}])
const current = ref(0)
const flipped = ref(false)
const newFront = ref("")
const newBack = ref("")
function nextCard() { if (current.value < cards.value.length-1) { current.value++; flipped.value = false } }
function prevCard() { if (current.value > 0) { current.value--; flipped.value = false } }
function addCard() {
  if (!newFront.value.trim() || !newBack.value.trim()) { uni.showToast({ title: "\u8bf7\u586b\u5199\u5b8c\u6574", icon: "none" }); return }
  cards.value.push({front: newFront.value.trim(), back: newBack.value.trim()})
  newFront.value = ""; newBack.value = ""
  uni.showToast({ title: "\u5df2\u6dfb\u52a0", icon: "success" })
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #4facfe, #00f2fe); }
.custom-nav { background: linear-gradient(135deg, #0984e3, #00cec9); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.fc-progress { text-align: center; font-size: 28rpx; color: rgba(255,255,255,0.8); margin-bottom: 20rpx; }
.fc-card { background: #fff; border-radius: 24rpx; padding: 80rpx 40rpx; text-align: center; min-height: 300rpx; display: flex; align-items: center; justify-content: center; margin-bottom: 32rpx; cursor: pointer; }
.fc-inner { transition: 0.3s; }
.fc-front { font-size: 36rpx; font-weight: 600; color: #333; display: block; }
.fc-back { font-size: 30rpx; color: #0984e3; display: none; }
.fc-inner.flip .fc-front { display: none; }
.fc-inner.flip .fc-back { display: block; }
.fc-actions { display: flex; gap: 16rpx; margin-bottom: 32rpx; }
.fc-btn { flex: 1; text-align: center; padding: 20rpx; border-radius: 16rpx; font-size: 26rpx; }
.fc-btn.prev { background: rgba(255,255,255,0.3); color: #fff; }
.fc-btn.next { background: #fff; color: #0984e3; }
.fc-add { background: rgba(255,255,255,0.2); border-radius: 20rpx; padding: 24rpx; display: flex; flex-direction: column; gap: 12rpx; }
.fc-input { background: #fff; border-radius: 12rpx; padding: 16rpx 20rpx; font-size: 26rpx; }
.fc-add-btn { background: #0984e3; color: #fff; text-align: center; border-radius: 12rpx; padding: 16rpx; font-size: 26rpx; }
.empty { text-align: center; padding: 60rpx; color: rgba(255,255,255,0.7); }
</style>
