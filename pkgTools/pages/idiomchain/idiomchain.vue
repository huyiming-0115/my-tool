<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u6210\u8bed\u63a5\u9f99</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="chain-display">
        <view class="chain-item" v-for="(c, i) in chain" :key="i">{{ c }}</view>
      </view>
      <view class="input-area">
        <input class="chain-input" v-model="input" placeholder="\u8f93\u5165\u4ee5\u4e0a\u4e00\u4e2a\u5b57\u5f00\u5934\u7684\u6210\u8bed" @confirm="submitWord" />
        <text class="submit-btn" @click="submitWord">\u63d0\u4ea4</text>
      </view>
      <view class="chain-stats"><text>\u957f\u5ea6: {{ chain.length }}</text><text class="hint-btn" @click="getHint">\u63d0\u793a</text></view>
      <text class="hint-text" v-if="hint">{{ hint }}</text>
      <view class="start-area" v-if="chain.length === 0">
        <text class="start-btn" @click="startChain">\u5f00\u59cb\u63a5\u9f99</text>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const chain = ref([])
const input = ref("")
const hint = ref("")
const idiomDB = ["\u4e00\u5fc3\u4e00\u610f","\u610f\u6c14\u98ce\u53d1","\u53d1\u6325\u5149\u5927","\u5927\u53d4\u91cd\u5e78","\u5e78\u798f\u7f8e\u6ee1","\u6ee1\u9762\u6625\u98ce","\u98ce\u5e73\u6d6a\u9759","\u9759\u9759\u7684\u5f85","\u5f85\u4eba\u4e50\u4e8b","\u4e8b\u534a\u529f\u500d","\u500d\u6599\u671f\u5f85","\u5f85\u65e5\u671f\u5f85","\u5f85\u4eba\u4e50\u4e8b","\u98ce\u5e73\u6d6a\u9759","\u9759\u4e0b\u5fc3\u6765","\u6765\u65e0\u660e\u65e5","\u65e5\u65b0\u6708\u5f02","\u5f02\u53e3\u540c\u58f0","\u58f0\u4e1c\u51fb\u897f","\u897f\u95e8\u6b63\u5f0f","\u5f0f\u5f0f\u76f8\u4f9d"]
function startChain() { chain.value = ["\u4e00\u5fc3\u4e00\u610f"] }
function submitWord() {
  if (!input.value.trim()) return
  var last = chain.value[chain.value.length - 1]
  var lastChar = last[last.length - 1]
  if (input.value[0] !== lastChar) { uni.showToast({ title: "\u5e94\u4ee5\u300c" + lastChar + "\u300d\u5f00\u5934", icon: "none" }); return }
  chain.value.push(input.value.trim())
  input.value = ""
  hint.value = ""
}
function getHint() {
  if (chain.value.length === 0) { startChain(); return }
  var last = chain.value[chain.value.length - 1]
  var lastChar = last[last.length - 1]
  var found = idiomDB.find(function(d) { return d[0] === lastChar && chain.value.indexOf(d) === -1 })
  hint.value = found || "\u6ca1\u627e\u5230\u53ef\u7528\u6210\u8bed"
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #f6d365, #fda085); }
.custom-nav { background: linear-gradient(135deg, #e17055, #f39c12); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.chain-display { background: rgba(255,255,255,0.3); border-radius: 20rpx; padding: 20rpx; margin-bottom: 24rpx; min-height: 100rpx; }
.chain-item { display: inline-block; background: #fff; padding: 12rpx 20rpx; border-radius: 12rpx; margin: 8rpx; font-size: 26rpx; color: #333; }
.input-area { display: flex; gap: 16rpx; margin-bottom: 16rpx; }
.chain-input { flex: 1; background: #fff; border-radius: 16rpx; padding: 20rpx 24rpx; font-size: 28rpx; }
.submit-btn { background: #e17055; color: #fff; border-radius: 16rpx; padding: 20rpx 32rpx; font-size: 28rpx; display: flex; align-items: center; }
.chain-stats { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16rpx; }
.chain-stats text { color: rgba(255,255,255,0.8); font-size: 24rpx; }
.hint-btn { padding: 8rpx 16rpx; background: rgba(255,255,255,0.3); border-radius: 8rpx; color: #fff; font-size: 22rpx; }
.hint-text { display: block; background: rgba(255,255,255,0.2); border-radius: 12rpx; padding: 16rpx; color: #fff; font-size: 26rpx; margin-bottom: 16rpx; }
.start-area { text-align: center; padding: 40rpx; }
.start-btn { display: inline-block; padding: 24rpx 60rpx; background: #fff; color: #e17055; border-radius: 16rpx; font-size: 30rpx; font-weight: 600; }
</style>
