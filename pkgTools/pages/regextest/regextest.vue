<template>
  <view class="rx-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">正则测试</text><text class="nav-icon" @click="showCheatsheet = !showCheatsheet">?</text></view>
    </view>
    <view class="content">
      <view class="rx-card">
        <view class="rx-label">正则表达式</view>
        <view class="rx-input-row"><input class="rx-input" v-model="pattern" placeholder="例如: \d{11}" @input="testRx" /><text class="rx-flags">
          <text class="flag" :class="{ active: flags.g }" @click="flags.g = !flags.g; testRx()">g</text>
          <text class="flag" :class="{ active: flags.i }" @click="flags.i = !flags.i; testRx()">i</text>
          <text class="flag" :class="{ active: flags.m }" @click="flags.m = !flags.m; testRx()">m</text>
        </text></view>
      </view>
      <view class="rx-card">
        <view class="rx-label">测试文本</view>
        <textarea class="rx-text" v-model="testStr" placeholder="输入要匹配的文本..." @input="testRx" auto-height maxlength="2000" />
      </view>
      <view class="rx-card" v-if="pattern">
        <view class="rx-label">匹配结果 <text class="rx-count" v-if="matches.length">({{ matches.length }}个)</text></view>
        <view class="rx-result" v-if="matches.length">
          <text class="rx-match" v-for="(m, idx) in matches" :key="idx">[{{ idx + 1 }}] {{ m }}</text>
        </view>
        <view class="rx-no-match" v-else><text>无匹配</text></view>
      </view>
    </view>
    <view v-if="showCheatsheet" class="mask" @click="showCheatsheet = false">
      <view class="cs-panel" @click.stop>
        <view class="cs-head"><text class="cs-title">常用正则</text><text class="cs-close" @click="showCheatsheet = false">×</text></view>
        <scroll-view class="cs-list" scroll-y>
          <view class="cs-item" v-for="(item, idx) in cheatsheet" :key="idx" @click="pattern = item.rx; testRx()">
            <text class="cs-name">{{ item.name }}</text>
            <text class="cs-rx">{{ item.rx }}</text>
          </view>
        </scroll-view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, reactive, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const pattern = ref("")
const testStr = ref("")
const matches = ref([])
const flags = reactive({ g: true, i: false, m: false })
const showCheatsheet = ref(false)
const cheatsheet = [
  { name: "手机号", rx: "^1[3-9]\\d{9}$" },
  { name: "邮箱", rx: "^[\\w.-]+@[\\w.-]+\\.\\w+$" },
  { name: "身份证", rx: "^\\d{17}[\\dXx]$" },
  { name: "URL", rx: "^https?://.+" },
  { name: "整数", rx: "^-?\\d+$" },
  { name: "正整数", rx: "^[1-9]\\d*$" },
  { name: "中文", rx: "^[\\u4e00-\\u9fff]+$" },
  { name: "日期(YYYY-MM-DD)", rx: "^\\d{4}-\\d{2}-\\d{2}$" },
  { name: "IPv4地址", rx: "^\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}$" },
  { name: "车牌号", rx: "^[\\u4e00-\\u9fff][A-Z][A-Z0-9]{5}$" }
]
function testRx() {
  if (!pattern.value) { matches.value = []; return }
  try {
    const f = (flags.g ? "g" : "") + (flags.i ? "i" : "") + (flags.m ? "m" : "")
    const rx = new RegExp(pattern.value, f)
    if (flags.g) { matches.value = testStr.value.match(rx) || [] }
    else { const m = testStr.value.match(rx); matches.value = m ? [m[0]] : [] }
  } catch (e) { matches.value = [] }
}
function goBack() { uni.navigateBack() }
onMounted(() => { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.rx-page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #fd79a8, #e84393); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.rx-card { background: #fff; border-radius: 24rpx; padding: 24rpx; margin-bottom: 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.rx-label { font-size: 26rpx; color: #999; margin-bottom: 12rpx; display: block; }
.rx-count { color: #e84393; }
.rx-input-row { display: flex; align-items: center; gap: 16rpx; }
.rx-input { flex: 1; height: 72rpx; font-size: 28rpx; font-family: monospace; border: 2rpx solid #e5e7eb; border-radius: 12rpx; padding: 0 16rpx; }
.rx-flags { display: flex; gap: 8rpx; }
.flag { width: 48rpx; height: 48rpx; line-height: 48rpx; text-align: center; background: #f5f5f5; border-radius: 8rpx; font-size: 24rpx; color: #666; }
.flag.active { background: #e84393; color: #fff; }
.rx-text { width: 100%; min-height: 200rpx; font-size: 28rpx; line-height: 1.6; }
.rx-result { display: flex; flex-direction: column; gap: 8rpx; }
.rx-match { font-size: 26rpx; color: #333; background: #f0fff4; padding: 12rpx 16rpx; border-radius: 8rpx; font-family: monospace; }
.rx-no-match { text-align: center; padding: 32rpx; font-size: 26rpx; color: #999; }
.mask { position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 999; display: flex; align-items: flex-end; }
.cs-panel { width: 100%; max-height: 70vh; background: #fff; border-radius: 32rpx 32rpx 0 0; display: flex; flex-direction: column; }
.cs-head { display: flex; justify-content: space-between; align-items: center; padding: 28rpx 32rpx; border-bottom: 2rpx solid #f0f0f0; }
.cs-title { font-size: 30rpx; font-weight: 600; }
.cs-close { font-size: 40rpx; color: #999; }
.cs-list { max-height: 60vh; padding: 8rpx 32rpx; }
.cs-item { padding: 20rpx 0; border-bottom: 2rpx solid #f8f8f8; }
.cs-name { font-size: 26rpx; color: #333; font-weight: 600; display: block; margin-bottom: 4rpx; }
.cs-rx { font-size: 24rpx; color: #e84393; font-family: monospace; display: block; }
</style>
