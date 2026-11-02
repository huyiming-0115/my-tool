
<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">YAML-JSON互转</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="yj-tabs">
        <view class="yj-tab" :class="{active: mode==='yaml2json'}" @click="mode='yaml2json';convert"><text>YAML→JSON</text></view>
        <view class="yj-tab" :class="{active: mode==='json2yaml'}" @click="mode='json2yaml';convert"><text>JSON→YAML</text></view>
      </view>
      <view class="yj-card">
        <text class="yj-label">输入</text>
        <textarea class="yj-textarea" v-model="inputText" placeholder="在此粘贴内容..." />
      </view>
      <view class="yj-btn" @click="convert"><text>转换</text></view>
      <view class="yj-card" v-if="outputText">
        <view class="yj-result-header">
          <text class="yj-label">输出</text>
          <view class="yj-copy" @click="copyResult"><text>复制</text></view>
        </view>
        <scroll-view class="yj-output" scroll-y><text>{{outputText}}</text></scroll-view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const mode = ref("yaml2json")
const inputText = ref("")
const outputText = ref("")
function yaml2json(yaml) {
  var lines = yaml.split(/
?
/)
  var result = {}
  var current = result
  var stack = [{obj: result, indent: -1}]
  for (var i = 0; i < lines.length; i++) {
    var line = lines[i]
    if (!line.trim() || line.trim().charAt(0) === "#") continue
    var indent = line.search(/\S/)
    var content = line.trim()
    var colonIdx = content.indexOf(":")
    if (colonIdx < 0) continue
    var key = content.substring(0, colonIdx).trim()
    var value = content.substring(colonIdx + 1).trim()
    while (stack.length > 1 && stack[stack.length-1].indent >= indent) { stack.pop() }
    current = stack[stack.length-1].obj
    if (!value) {
      var newObj = {}
      current[key] = newObj
      stack.push({obj: newObj, indent: indent})
      current = newObj
    } else {
      if (value === "true") value = true
      else if (value === "false") value = false
      else if (!isNaN(value) && value !== "") value = Number(value)
      current[key] = value
    }
  }
  return JSON.stringify(result, null, 2)
}
function json2yaml(json) {
  var obj = JSON.parse(json)
  var lines = []
  function convert(o, indent) {
    var prefix = "  ".repeat(indent)
    if (typeof o === "object" && !Array.isArray(o)) {
      for (var k in o) {
        if (typeof o[k] === "object") {
          lines.push(prefix + k + ":")
          convert(o[k], indent + 1)
        } else {
          lines.push(prefix + k + ": " + o[k])
        }
      }
    }
  }
  convert(obj, 0)
  return lines.join("
")
}
function convert() {
  if (!inputText.value.trim()) return
  try {
    if (mode.value === "yaml2json") {
      outputText.value = yaml2json(inputText.value)
    } else {
      outputText.value = json2yaml(inputText.value)
    }
  } catch(e) {
    outputText.value = "转换错误: " + e.message
  }
}
function copyResult() {
  uni.setClipboardData({ data: outputText.value })
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #f6d365, #fda085); }
.custom-nav { background: linear-gradient(135deg, #f6d365, #fda085); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 32rpx; }
.yj-tabs { display: flex; background: rgba(255,255,255,0.2); border-radius: 16rpx; padding: 6rpx; margin-bottom: 24rpx; }
.yj-tab { flex: 1; text-align: center; padding: 16rpx; border-radius: 12rpx; }
.yj-tab text { color: rgba(255,255,255,0.7); font-size: 28rpx; }
.yj-tab.active { background: #fff; }
.yj-tab.active text { color: #fda085; font-weight: 600; }
.yj-card { background: rgba(255,255,255,0.2); border-radius: 20rpx; padding: 24rpx; margin-bottom: 20rpx; }
.yj-label { color: rgba(255,255,255,0.8); font-size: 26rpx; display: block; margin-bottom: 12rpx; }
.yj-textarea { background: rgba(255,255,255,0.2); border-radius: 12rpx; padding: 16rpx 20rpx; font-size: 26rpx; color: #fff; width: 100%; box-sizing: border-box; min-height: 200rpx; }
.yj-btn { background: #fff; border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 24rpx; }
.yj-btn text { color: #fda085; font-size: 32rpx; font-weight: 700; }
.yj-result-header { display: flex; justify-content: space-between; align-items: center; }
.yj-copy { background: rgba(255,255,255,0.3); padding: 8rpx 20rpx; border-radius: 8rpx; }
.yj-copy text { color: #fff; font-size: 24rpx; }
.yj-output { background: rgba(0,0,0,0.15); border-radius: 12rpx; padding: 16rpx; max-height: 400rpx; }
.yj-output text { color: rgba(255,255,255,0.9); font-size: 24rpx; line-height: 1.6; font-family: monospace; word-break: break-all; }
</style>
