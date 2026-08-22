<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">摩斯电码</text><text class="nav-icon" @click="swap">⇄</text></view>
    </view>
    <view class="content">
      <view class="mode-tabs"><text class="mode-tab" :class="{ active: mode === 'encode' }" @click="mode = 'encode'; convert()">文→摩</text><text class="mode-tab" :class="{ active: mode === 'decode' }" @click="mode = 'decode'; convert()">摩→文</text></view>
      <view class="io-card"><text class="io-label">{{ mode === 'encode' ? '原文' : '摩斯电码' }}</text><textarea class="io-input" v-model="input" placeholder="..." auto-height maxlength="1000" /></view>
      <view class="io-card"><view class="io-head"><text class="io-label">{{ mode === 'encode' ? '摩斯电码' : '原文' }}</text><text class="copy-btn" @click="copy(output)">复制</text></view><textarea class="io-input result" :value="output" auto-height readonly /></view>
    </view>
  </view>
</template>
<script setup>
import { ref, watch, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const mode = ref("encode")
const input = ref("")
const output = ref("")
var map = {A:".-",B:"-...",C:"-.-.",D:"-..",E:".",F:"..-.",G:"--.",H:"....",I:"..",J:".---",K:"-.-",L:".-..",M:"--",N:"-.",O:"---",P:".--.",Q:"--.-",R:".-.",S:"...",T:"-",U:"..-",V:"...-",W:".--",X:"-..-",Y:"-.--",Z:"--..",0:"-----",1:".----",2:"..---",3:"...--",4:"....-",5:".....",6:"-....",7:"--...",8:"---..",9:"----.", ".":".-.-.-",",":"--..--","?":"..--.."}
var rmap = {}
for (var k in map) rmap[map[k]] = k
function convert() {
  if (mode.value === "encode") { output.value = input.value.toUpperCase().split("").map(function(c) { return map[c] || c }).join(" ") }
  else { output.value = input.value.split(" ").map(function(c) { return rmap[c] || c }).join("") }
}
watch(input, convert)
watch(mode, convert)
function swap() { mode.value = mode.value === "encode" ? "decode" : "encode"; var t = input.value; input.value = output.value; output.value = t }
function copy(v) { uni.setClipboardData({ data: v, success: function() { uni.showToast({ title: "已复制", icon: "success" }) } }) }
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #e17055, #d63031); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.mode-tabs { display: flex; gap: 16rpx; margin-bottom: 24rpx; }
.mode-tab { flex: 1; text-align: center; padding: 20rpx; background: #fff; border-radius: 16rpx; font-size: 26rpx; color: #666; }
.mode-tab.active { background: linear-gradient(135deg, #e17055, #d63031); color: #fff; }
.io-card { background: #fff; border-radius: 24rpx; padding: 24rpx; margin-bottom: 24rpx; }
.io-head { display: flex; justify-content: space-between; align-items: center; }
.io-label { font-size: 26rpx; color: #999; display: block; margin-bottom: 12rpx; }
.copy-btn { font-size: 24rpx; color: #e17055; }
.io-input { width: 100%; min-height: 150rpx; font-size: 28rpx; }
.io-input.result { background: #f8f9fa; border-radius: 12rpx; padding: 16rpx; }
</style>