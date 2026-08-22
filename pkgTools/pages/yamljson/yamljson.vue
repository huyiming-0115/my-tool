<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">YAML-JSON\u4e92\u8f6c</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="mode-tabs"><text class="mode-tab" :class="{active: mode==='y2j'}" @click="mode='y2j'">YAML\u2192JSON</text><text class="mode-tab" :class="{active: mode==='j2y'}" @click="mode='j2y'">JSON\u2192YAML</text></view>
      <textarea class="io-input" v-model="inputText" :placeholder="mode==='y2j'?'\u8f93\u5165YAML':'\u8f93\u5165JSON'" auto-height></textarea>
      <view class="calc-btn" @click="convert"><text>\u8f6c\u6362</text></view>
      <view class="io-output" v-if="outputText"><textarea :value="outputText" disabled auto-height></textarea><text class="copy-btn" @click="copyText">\u590d\u5236</text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const mode = ref("y2j")
const inputText = ref("")
const outputText = ref("")
function yamlToJson(yaml) {
  try {
    const lines = yaml.split("\n")
    const obj = {}
    lines.forEach(function(line) {
      if (line.trim() && !line.trim().startsWith("#")) {
        const idx = line.indexOf(":")
        if (idx > -1) {
          const key = line.substring(0, idx).trim()
          const val = line.substring(idx + 1).trim()
          obj[key] = isNaN(val) ? val : Number(val)
        }
      }
    })
    return JSON.stringify(obj, null, 2)
  } catch(e) { return "\u89e3\u6790\u9519\u8bef: " + e.message }
}
function jsonToYaml(json) {
  try {
    const obj = JSON.parse(json)
    let yaml = ""
    Object.keys(obj).forEach(function(k) {
      yaml += k + ": " + obj[k] + "\n"
    })
    return yaml
  } catch(e) { return "\u89e3\u6790\u9519\u8bef: " + e.message }
}
function convert() {
  if (!inputText.value.trim()) { uni.showToast({ title: "\u8bf7\u8f93\u5165\u5185\u5bb9", icon: "none" }); return }
  outputText.value = mode.value === "y2j" ? yamlToJson(inputText.value) : jsonToYaml(inputText.value)
}
function copyText() {
  uni.setClipboardData({ data: outputText.value, success: function() { uni.showToast({ title: "\u5df2\u590d\u5236", icon: "success" }) } })
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #a18cd1, #fbc2eb); }
.custom-nav { background: linear-gradient(135deg, #6c5ce7, #a29bfe); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.mode-tabs { display: flex; gap: 16rpx; margin-bottom: 24rpx; }
.mode-tab { flex: 1; text-align: center; padding: 20rpx; border-radius: 16rpx; background: rgba(255,255,255,0.3); color: #fff; font-size: 26rpx; }
.mode-tab.active { background: #fff; color: #6c5ce7; }
.io-input { background: #fff; border-radius: 20rpx; padding: 24rpx; font-size: 26rpx; min-height: 200rpx; margin-bottom: 20rpx; }
.calc-btn { background: linear-gradient(135deg, #6c5ce7, #a29bfe); border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 24rpx; }
.calc-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.io-output { background: #fff; border-radius: 20rpx; padding: 24rpx; }
.io-output textarea { width: 100%; min-height: 200rpx; font-size: 24rpx; color: #333; }
.copy-btn { display: block; background: #6c5ce7; color: #fff; text-align: center; border-radius: 12rpx; padding: 16rpx; margin-top: 16rpx; font-size: 26rpx; }
</style>
