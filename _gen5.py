# -*- coding: utf-8 -*-
import os
base = "pkgTools/pages"
def w(name, content):
    with open(os.path.join(base, name, name + ".vue"), "w") as f:
        f.write(content)
    print("OK:", name)

# ===== csvparser =====
w("csvparser", """<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\\u2190</text><text class="nav-title">CSV\\u89e3\\u6790\\u5668</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <textarea class="csv-input" v-model="csvText" placeholder="\\u7c98\\u8d34CSV\\u6570\\u636e\\u5230\\u8fd9\\u91cc" auto-height></textarea>
      <view class="opt-row">
        <text class="opt-label">\\u5206\\u9694\\u7b26:</text>
        <text class="sep-btn" :class="{active: sep==','}" @click="sep=','">\\u9017\\u53f7</text>
        <text class="sep-btn" :class="{active: sep=='\\t'}" @click="sep='\\t'">Tab</text>
        <text class="sep-btn" :class="{active: sep==';'}" @click="sep=';'">\\u5206\\u53f7</text>
      </view>
      <view class="calc-btn" @click="parse"><text>\\u89e3\\u6790</text></view>
      <scroll-view class="table-scroll" scroll-x scroll-y v-if="rows.length > 0">
        <view class="csv-table">
          <view class="csv-row header"><text class="csv-cell" v-for="(h, i) in rows[0]" :key="i">{{ h }}</text></view>
          <view class="csv-row" v-for="(row, ri) in rows.slice(1)" :key="ri"><text class="csv-cell" v-for="(cell, ci) in row" :key="ci">{{ cell }}</text></view>
        </view>
      </scroll-view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const csvText = ref("")
const sep = ref(",")
const rows = ref([])
function parse() {
  if (!csvText.value.trim()) { uni.showToast({ title: "\\u8bf7\\u8f93\\u5165CSV\\u6570\\u636e", icon: "none" }); return }
  const lines = csvText.value.trim().split("\\n")
  rows.value = lines.map(function(line) { return line.split(sep.value) })
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #fa709a, #fee140); }
.custom-nav { background: linear-gradient(135deg, #e84393, #fdcb6e); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.csv-input { background: #fff; border-radius: 20rpx; padding: 24rpx; font-size: 26rpx; min-height: 200rpx; margin-bottom: 20rpx; }
.opt-row { display: flex; align-items: center; gap: 12rpx; margin-bottom: 20rpx; }
.opt-label { color: rgba(255,255,255,0.8); font-size: 26rpx; }
.sep-btn { padding: 12rpx 24rpx; border-radius: 12rpx; background: rgba(255,255,255,0.3); color: #fff; font-size: 24rpx; }
.sep-btn.active { background: #fff; color: #e84393; }
.calc-btn { background: linear-gradient(135deg, #e84393, #fdcb6e); border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 24rpx; }
.calc-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.table-scroll { max-height: 60vh; background: #fff; border-radius: 16rpx; overflow: auto; }
.csv-table { min-width: 100%; }
.csv-row { display: flex; }
.csv-row.header { background: #f8f8f8; }
.csv-cell { min-width: 160rpx; padding: 16rpx; font-size: 24rpx; border: 1rpx solid #eee; flex-shrink: 0; }
.csv-row.header .csv-cell { font-weight: 700; }
</style>
""")

# ===== yamljson =====
w("yamljson", """<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\\u2190</text><text class="nav-title">YAML-JSON\\u4e92\\u8f6c</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="mode-tabs"><text class="mode-tab" :class="{active: mode==='y2j'}" @click="mode='y2j'\">YAML\\u2192JSON</text><text class="mode-tab" :class="{active: mode==='j2y'}" @click="mode='j2y'\">JSON\\u2192YAML</text></view>
      <textarea class="io-input" v-model="inputText" :placeholder=\"mode==='y2j'?'\\u8f93\\u5165YAML':'\\u8f93\\u5165JSON'\" auto-height></textarea>
      <view class="calc-btn" @click="convert"><text>\\u8f6c\\u6362</text></view>
      <view class="io-output" v-if="outputText"><textarea :value="outputText" disabled auto-height></textarea><text class="copy-btn" @click="copyText">\\u590d\\u5236</text></view>
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
    const lines = yaml.split("\\n")
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
  } catch(e) { return "\\u89e3\\u6790\\u9519\\u8bef: " + e.message }
}
function jsonToYaml(json) {
  try {
    const obj = JSON.parse(json)
    let yaml = ""
    Object.keys(obj).forEach(function(k) {
      yaml += k + ": " + obj[k] + "\\n"
    })
    return yaml
  } catch(e) { return "\\u89e3\\u6790\\u9519\\u8bef: " + e.message }
}
function convert() {
  if (!inputText.value.trim()) { uni.showToast({ title: "\\u8bf7\\u8f93\\u5165\\u5185\\u5bb9", icon: "none" }); return }
  outputText.value = mode.value === "y2j" ? yamlToJson(inputText.value) : jsonToYaml(inputText.value)
}
function copyText() {
  uni.setClipboardData({ data: outputText.value, success: function() { uni.showToast({ title: "\\u5df2\\u590d\\u5236", icon: "success" }) } })
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
""")

# ===== jwtparser =====
w("jwtparser", """<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\\u2190</text><text class="nav-title">JWT\\u89e3\\u6790\\u5668</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <textarea class="jwt-input" v-model="jwtText" placeholder="\\u7c98\\u8d34JWT Token" auto-height></textarea>
      <view class="calc-btn" @click="parse"><text>\\u89e3\\u6790</text></view>
      <view class="result-card" v-if="header">
        <text class="section-title\">\\u2728 Header</text>
        <textarea class="json-output" :value="header" disabled></textarea>
        <text class="section-title\">\\u2728 Payload</text>
        <textarea class="json-output" :value="payload" disabled></textarea>
        <text class="section-title\">\\u2728 Signature</text>
        <text class="sig-text">{{ signature }}</text>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const jwtText = ref("")
const header = ref("")
const payload = ref("")
const signature = ref("")
function base64UrlDecode(str) {
  try {
    str = str.replace(/-/g, "+").replace(/_/g, "/")
    while (str.length % 4) str += "="
    return decodeURIComponent(escape(atob(str)))
  } catch(e) { return "\\u89e3\\u7801\\u5931\\u8d25" }
}
function parse() {
  const parts = jwtText.value.trim().split(".")
  if (parts.length !== 3) { uni.showToast({ title: "\\u65e0\\u6548\\u7684JWT\\u683c\\u5f0f", icon: "none" }); return }
  header.value = JSON.stringify(JSON.parse(base64UrlDecode(parts[0])), null, 2)
  payload.value = JSON.stringify(JSON.parse(base64UrlDecode(parts[1])), null, 2)
  signature.value = parts[2]
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #fad0c4, #ffd1ff); }
.custom-nav { background: linear-gradient(135deg, #e17055, #fd79a8); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.jwt-input { background: #fff; border-radius: 20rpx; padding: 24rpx; font-size: 24rpx; min-height: 160rpx; margin-bottom: 20rpx; }
.calc-btn { background: linear-gradient(135deg, #e17055, #fd79a8); border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 24rpx; }
.calc-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.result-card { background: #fff; border-radius: 24rpx; padding: 32rpx; }
.section-title { font-size: 28rpx; font-weight: 600; color: #333; display: block; margin: 16rpx 0 8rpx; }
.json-output { width: 100%; background: #f8f8f8; border-radius: 12rpx; padding: 16rpx; font-size: 22rpx; color: #333; min-height: 120rpx; }
.sig-text { font-size: 20rpx; color: #999; word-break: break-all; }
</style>
""")

# ===== colorblind =====
w("colorblind", """<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\\u2190</text><text class="nav-title">\\u8272\\u76f2\\u6d4b\\u8bd5</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <text class=\"test-title\">\\u7b2c{{ current+1 }}\\u9898 / {{ tests.length }}</text>
      <view class=\"cb-plate\" :style=\"{ background: tests[current].bg }\" @click=\"showAnswer=!showAnswer\">
        <text class=\"cb-number\" :style=\"{ color: tests[current].fg }\">{{ showAnswer ? tests[current].num : '?' }}</text>
      </view>
      <text class=\"cb-hint\">{{ showAnswer ? '\\u70b9\\u51fb\\u7eed\\u7eed\\u4e0b\\u4e00\\u9898' : '\\u70b9\\u51fb\\u67e5\\u770b\\u7b54\\u6848' }}</text>
      <view class=\"cb-actions\">
        <text class=\"cb-btn\" @click=\"prevTest\" v-if=\"current > 0\">\\u4e0a\\u4e00\\u9898</text>
        <text class=\"cb-btn next\" @click=\"nextTest\" v-if=\"current < tests.length-1\">\\u4e0b\\u4e00\\u9898</text>
        <text class=\"cb-btn next\" v-else @click=\"reset\">\\u91cd\\u65b0\\u5f00\\u59cb</text>
      </view>
      <view class=\"cb-result\" v-if=\"current === tests.length-1 && showAnswer\">
        <text>\\u6d4b\\u8bd5\\u5b8c\\u6210\\uff01\\u5982\\u679c\\u4f60\\u80fd\\u770b\\u6e05\\u6240\\u6709\\u6570\\u5b57\\uff0c\\u8bf4\\u660e\\u4f60\\u7684\\u89c6\\u529b\\u5f88\\u597d\\u3002</text>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const current = ref(0)
const showAnswer = ref(false)
const tests = [
  { num: "74", bg: "#4a90d9", fg: "#f5a623" },
  { num: "6", bg: "#7ed321", fg: "#d0021b" },
  { num: "29", bg: "#f5a623", fg: "#4a90d9" },
  { num: "8", bg: "#d0021b", fg: "#7ed321" },
  { num: "42", fg: "#4a90d9", bg: "#f5a623" }
]
function nextTest() { if (current.value < tests.length-1) { current.value++; showAnswer.value = false } }
function prevTest() { if (current.value > 0) { current.value--; showAnswer.value = false } }
function reset() { current.value = 0; showAnswer.value = false }
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #ff9a9e, #fecfef); }
.custom-nav { background: linear-gradient(135deg, #e84393, #fd79a8); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; text-align: center; }
.test-title { font-size: 30rpx; color: #fff; font-weight: 600; display: block; margin-bottom: 32rpx; }
.cb-plate { width: 400rpx; height: 400rpx; border-radius: 50%; margin: 0 auto 32rpx; display: flex; align-items: center; justify-content: center; box-shadow: 0 8rpx 32rpx rgba(0,0,0,0.15); }
.cb-number { font-size: 120rpx; font-weight: 900; }
.cb-hint { font-size: 26rpx; color: rgba(255,255,255,0.8); display: block; margin-bottom: 24rpx; }
.cb-actions { display: flex; gap: 16rpx; justify-content: center; }
.cb-btn { padding: 20rpx 40rpx; border-radius: 16rpx; background: rgba(255,255,255,0.3); color: #fff; font-size: 26rpx; }
.cb-btn.next { background: #fff; color: #e84393; }
.cb-result { margin-top: 32rpx; background: #fff; border-radius: 20rpx; padding: 24rpx; font-size: 26rpx; color: #333; }
</style>
""")

print("batch5 done")