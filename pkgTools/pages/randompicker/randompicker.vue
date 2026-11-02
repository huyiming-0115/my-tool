<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u968f\u673a\u70b9\u540d\u5668</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="input-bar">
        <input class="rp-input" v-model="newName" placeholder="\u8f93\u5165\u59d3\u540d" @confirm="addName" />
        <text class="add-btn" @click="addName">+</text>
      </view>
      <view class="name-tags">
        <text class="name-tag" v-for="(name, i) in names" :key="i" @click="removeName(i)">{{ name }} \u00d7</text>
      </view>
      <view class="result-display" v-if="picked">
        <text class="picked-name">{{ picked }}</text>
      </view>
      <view class="pick-btn" :class="{spinning: spinning}" @click="pick" v-if="names.length > 0">
        <text>{{ spinning ? '\u6325\u8f6c\u4e2d...' : '\u5f00\u59cb\u70b9\u540d' }}</text>
      </view>
      <view class="quick-btns">
        <text class="quick-btn" @click="loadClass">\u5feb\u901f\u586b\u5165\u73ed\u7ea7</text>
        <text class="quick-btn" @click="clearAll">\u6e05\u7a7a</text>
      </view>
      <view class="empty" v-if="names.length === 0"><text>\u6dfb\u52a0\u59d3\u540d\u540e\u5f00\u59cb\u70b9\u540d</text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const names = ref([])
const newName = ref("")
const picked = ref("")
const spinning = ref(false)
function addName() {
  if (!newName.value.trim()) return
  names.value.push(newName.value.trim())
  newName.value = ""
}
function removeName(i) { names.value.splice(i, 1) }
function pick() {
  if (spinning.value || names.value.length === 0) return
  spinning.value = true
  picked.value = ""
  let count = 0
  const timer = setInterval(function() {
    picked.value = names.value[Math.floor(Math.random() * names.value.length)]
    count++
    if (count > 20) { clearInterval(timer); spinning.value = false; uni.vibrateShort({}) }
  }, 80)
}
function loadClass() {
  names.value = ["\u5f20\u4e09","\u674e\u56db","\u738b\u4e94","\u8d75\u516d","\u94b1\u4e03","\u5b59\u516b","\u5468\u4e5d","\u5434\u5341"]
}
function clearAll() { names.value = []; picked.value = "" }
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #667eea, #764ba2); }
.custom-nav { background: linear-gradient(135deg, #5a67d8, #6b46c1); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.input-bar { display: flex; gap: 16rpx; margin-bottom: 24rpx; }
.rp-input { flex: 1; background: #fff; border-radius: 16rpx; padding: 20rpx 24rpx; font-size: 28rpx; }
.add-btn { background: #5a67d8; color: #fff; border-radius: 16rpx; width: 80rpx; display: flex; align-items: center; justify-content: center; font-size: 40rpx; font-weight: 700; }
.name-tags { display: flex; flex-wrap: wrap; gap: 12rpx; margin-bottom: 32rpx; }
.name-tag { background: rgba(255,255,255,0.2); color: #fff; padding: 12rpx 20rpx; border-radius: 12rpx; font-size: 24rpx; }
.result-display { background: rgba(255,255,255,0.15); border-radius: 24rpx; padding: 40rpx; text-align: center; margin-bottom: 32rpx; }
.picked-name { font-size: 48rpx; font-weight: 700; color: #fff; }
.pick-btn { background: linear-gradient(135deg, #00b894, #00cec9); border-radius: 16rpx; padding: 28rpx; text-align: center; margin-bottom: 24rpx; }
.pick-btn text { color: #fff; font-size: 32rpx; font-weight: 600; }
.pick-btn.spinning { opacity: 0.6; }
.quick-btns { display: flex; gap: 16rpx; }
.quick-btn { flex: 1; text-align: center; padding: 16rpx; background: rgba(255,255,255,0.2); border-radius: 12rpx; color: #fff; font-size: 24rpx; }
.empty { text-align: center; padding: 60rpx; color: rgba(255,255,255,0.6); }
</style>
