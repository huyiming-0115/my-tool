<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">塔罗牌</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="tarot-area">
        <view class="tarot-card" :class="{ flipped: flipped }" @click="draw">
          <view class="card-front" v-if="flipped"><text class="card-name">{{ card.name }}</text><text class="card-desc">{{ card.meaning }}</text></view>
          <view class="card-back" v-else><text class="card-back-icon">♈</text><text class="card-tap">点击抽卡</text></view>
        </view>
      </view>
      <view class="draw-btn" @click="draw"><text>{{ flipped ? "再抽一张" : "开始抽卡" }}</text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const flipped = ref(false)
const card = ref({ name: "", meaning: "" })
const cards = [
  { name: "恶魔", meaning: "激情、诱惑、知识的幻象" },
  { name: "女祠师", meaning: "直觉、秘密、美女" },
  { name: "女皇", meaning: "丰收、母爱、天空" },
  { name: "皇帝", meaning: "权威、稳定、父爱" },
  { name: "教皇", meaning: "信仰、传统、感情" },
  { name: "爱人", meaning: "爱情、和谐、感情" },
  { name: "战车", meaning: "胜利、冲动、挑战" },
  { name: "力量", meaning: "勇气、耐心、激情" },
  { name: "转轮", meaning: "命运、转换、变化" },
  { name: "正义", meaning: "公正、决定、清醒" },
  { name: "倒挂人", meaning: "等待、放下、战略" },
  { name: "死亡", meaning: "结束、转变、重生" },
  { name: "节制", meaning": "平衡、耐心、合作" },
  { name: "暗黑塔", meaning: "恐惧、危机、诱惑" },
  { name: "星星", meaning: "希望、光明、合作" },
  { name: "月亮", meaning: "恐惧、幻觉、意识" },
  { name: "太阳", meaning: "成功、快乐、光明" },
  { name: "审判", meaning: "反省、决定、改变" },
  { name: "世界", meaning: "完成、成就、幸福" }
]
function draw() {
  flipped.value = false
  setTimeout(function() { card.value = cards[Math.floor(Math.random() * cards.length)]; flipped.value = true; uni.vibrateShort({}) }, 300)
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #5f27cd, #a29bfe); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; display: flex; flex-direction: column; align-items: center; }
.tarot-area { margin-bottom: 40rpx; }
.tarot-card { width: 320rpx; height: 500rpx; border-radius: 20rpx; box-shadow: 0 8rpx 32rpx rgba(95,39,205,0.3); transition: transform 0.6s; transform-style: preserve-3d; }
.tarot-card.flipped { transform: rotateY(180deg); }
.card-front, .card-back { position: absolute; width: 100%; height: 100%; border-radius: 20rpx; display: flex; flex-direction: column; align-items: center; justify-content: center; backface-visibility: hidden; }
.card-front { background: linear-gradient(135deg, #5f27cd, #a29bfe); transform: rotateY(180deg); }
.card-back { background: linear-gradient(135deg, #2d3436, #636e72); }
.card-name { font-size: 40rpx; color: #fff; font-weight: 700; margin-bottom: 24rpx; }
.card-desc { font-size: 26rpx; color: rgba(255,255,255,0.8); text-align: center; padding: 0 32rpx; }
.card-back-icon { font-size: 80rpx; color: #f9ca24; }
.card-tap { font-size: 24rpx; color: rgba(255,255,255,0.6); margin-top: 16rpx; }
.draw-btn { width: 80%; background: linear-gradient(135deg, #5f27cd, #a29bfe); border-radius: 16rpx; padding: 28rpx; text-align: center; }
.draw-btn text { font-size: 32rpx; color: #fff; font-weight: 600; }
</style>