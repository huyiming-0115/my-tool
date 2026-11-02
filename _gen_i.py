# -*- coding: utf-8 -*-
import os
base = "pkgTools/pages"
def w(name, content):
    with open(os.path.join(base, name, name + ".vue"), "w") as f:
        f.write(content)
    print("OK:", name)

# ===== unitconverter =====
w("unitconverter", """<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\\u2190</text><text class="nav-title">\\u5355\\u4f4d\\u6362\\u7b97\\u5168</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="cat-tabs"><text class="cat-tab" :class="{active: cat==='\\u957f\\u5ea6'}" @click="cat='\\u957f\\u5ea6'\">\\u957f\\u5ea6</text><text class="cat-tab" :class="{active: cat==='\\u91cd\\u91cf'}" @click="cat='\\u91cd\\u91cf'\">\\u91cd\\u91cf</text><text class="cat-tab" :class="{active: cat==='\\u6e29\\u5ea6'}" @click="cat='\\u6e29\\u5ea6'\">\\u6e29\\u5ea6</text><text class="cat-tab" :class="{active: cat==='\\u9762\\u79ef'}" @click="cat='\\u9762\\u79ef'\">\\u9762\\u79ef</text><text class="cat-tab" :class="{active: cat==='\\u901f\\u5ea6'}" @click="cat='\\u901f\\u5ea6'\">\\u901f\\u5ea6</text></view>
      <view class="form-card"><text class="form-label">\\u8f93\\u5165\\u503c</text><input class="form-input" type="digit" v-model="inputVal" /></view>
      <view class="form-card"><text class="form-label">\\u4ece</text><picker class="unit-picker" :range="units[cat]" @change="fromUnit=$event.detail.value"><text>{{ units[cat][fromUnit] }} \\u25bc</text></picker></view>
      <view class="form-card"><text class="form-label">\\u5230</text><picker class="unit-picker" :range="units[cat]" @change="toUnit=$event.detail.value"><text>{{ units[cat][toUnit] }} \\u25bc</text></picker></view>
      <view class="calc-btn" @click="convert"><text>\\u6362\\u7b97</text></view>
      <view class="result-card" v-if="result !== ''"><text class="result-val">{{ inputVal }} {{ units[cat][fromUnit] }} = {{ result }} {{ units[cat][toUnit] }}</text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const cat = ref("\\u957f\\u5ea6")
const inputVal = ref("1")
const fromUnit = ref(0)
const toUnit = ref(1)
const result = ref("")
const units = {
  "\\u957f\\u5ea6": ["\\u7c73","\\u5343\\u7c73","\\u5398\\u7c73","\\u82f1\\u5c3a","\\u82f1\\u5bf8","\\u7801"],
  "\\u91cd\\u91cd": ["\\u514b","\\u5343\\u514b","\\u65a4","\\u76ce\\u53f8","\\u78c5"],
  "\\u6e29\\u5ea6": ["\\u6444\\u6c0f\\u5ea6","\\u683c\\u91cc\\u58eb\\u5ea6","\\u5f00\\u5c14\\u6587"],
  "\\u9762\\u79ef": ["\\u5e73\\u65b9\\u7c73","\\u5e73\\u65b9\\u5343\\u7c73","\\u5e73\\u65b9\\u82f1\\u5c3a","\\u5e73\\u65b9\\u82f1\\u91cc","\\u516c\\u9877"],
  "\\u901f\\u5ea6": ["\\u7c73/\\u79d2","\\u5343\\u7c73/\\u5c0f\\u65f6","\\u82f1\\u91cc/\\u5c0f\\u65f6","\\u8282"]
}
const factors = {
  "\\u957f\\u5ea6": [1,1000,0.01,0.3048,0.0254,0.9144],
  "\\u91cd\\u91cd": [1,1000,0.002,0.0283495,0.453592],
  "\\u6e29\\u5ea6": [1,1,1],
  "\\u9762\\u79ef": [1,1000000,0.092903,2589988,4046.86],
  "\\u901f\\u5ea6": [1,3.6,0.277778,0.514444]
}
function convert() {
  const v = parseFloat(inputVal.value) || 0
  const f = factors[cat.value]
  result.value = (v * f[fromUnit.value] / f[toUnit.value]).toFixed(6)
}
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
.cat-tabs { display: flex; gap: 8rpx; margin-bottom: 24rpx; flex-wrap: wrap; }
.cat-tab { padding: 12rpx 20rpx; border-radius: 12rpx; background: rgba(255,255,255,0.2); color: #fff; font-size: 24rpx; }
.cat-tab.active { background: #fff; color: #5a67d8; }
.form-card { background: #fff; border-radius: 20rpx; padding: 24rpx; margin-bottom: 20rpx; }
.form-label { font-size: 26rpx; color: #666; display: block; margin-bottom: 12rpx; }
.form-input { font-size: 32rpx; color: #333; font-weight: 600; }
.unit-picker { background: #f8f8f8; border-radius: 12rpx; padding: 16rpx; font-size: 28rpx; }
.calc-btn { background: linear-gradient(135deg, #5a67d8, #6b46c1); border-radius: 16rpx; padding: 24rpx; text-align: center; margin: 32rpx 0; }
.calc-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.result-card { background: #fff; border-radius: 24rpx; padding: 32rpx; text-align: center; }
.result-val { font-size: 32rpx; font-weight: 700; color: #5a67d8; }
</style>
""")

# ===== textencrypt =====
w("textencrypt", """<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\\u2190</text><text class="nav-title">\\u6587\\u672c\\u52a0\\u5bc6\\u89e3\\u5bc6</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="mode-tabs"><text class="mode-tab" :class="{active: mode==='encrypt'}" @click="mode='encrypt'\">\\u52a0\\u5bc6</text><text class="mode-tab" :class="{active: mode==='decrypt'}" @click="mode='decrypt'\">\\u89e3\\u5bc6</text></view>
      <view class="form-card"><text class="form-label">\\u7b97\\u6cd5</text><picker class="algo-picker" :range="algorithms" @change="algo=$event.detail.value"><text>{{ algorithms[algo] }} \\u25bc</text></picker></view>
      <view class="form-card" v-if="algo===3"><text class="form-label">\\u5bc6\\u94a5</text><input class="form-input" v-model="key" placeholder="\\u8f93\\u5165\\u5bc6\\u94a5" /></view>
      <view class="form-card"><text class="form-label">{{ mode==='encrypt'?'\\u660e\\u6587':'\\u5bc6\\u6587' }}</text><textarea class="te-input" v-model="inputText" placeholder="\\u8f93\\u5165\\u6587\\u672c" auto-height></textarea></view>
      <view class="calc-btn" @click="process"><text>{{ mode==='encrypt'?'\\u52a0\\u5bc6':'\\u89e3\\u5bc6' }}</text></view>
      <view class="result-card" v-if="outputText"><text class="result-label">{{ mode==='encrypt'?'\\u5bc6\\u6587':'\\u660e\\u6587' }}</text><textarea class="result-area" :value="outputText" disabled></textarea><text class="copy-btn" @click="copyText">\\u590d\\u5236</text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const mode = ref("encrypt")
const algo = ref(0)
const key = ref("3")
const inputText = ref("")
const outputText = ref("")
const algorithms = ["Base64","URL\\u7f16\\u7801","\\u641c\\u9f3b\\u9f3b\\u7801","\\u51ef\\u6492\\u5bc6\\u7801","\\u6469\\u65af\\u7535\\u7801"]
function caesar(text, shift, decrypt) {
  if (decrypt) shift = -shift
  return text.split("").map(function(c) {
    if (c.match(/[a-z]/)) return String.fromCharCode((c.charCodeAt(0)-97+shift+26)%26+97)
    if (c.match(/[A-Z]/)) return String.fromCharCode((c.charCodeAt(0)-65+shift+26)%26+65)
    return c
  }).join("")
}
function morse(text, decrypt) {
  var map = {a:".-",b:"-...",c:"-.-.",d:"-..",e:".",f:"..-.",g:"--.",h:"....",i:"..",j:".---",k:"-.-",l:".-..",m:"--",n:"-.",o:"---",p:".--.",q:"--.-",r:".-.",s:"...",t:"-",u:"..-",v:"...-",w:".--",x:"-..-",y:"-.--",z:"--..","0":"-----","1":".----","2":"..---","3":"...--","4":"....-","5":"....-","6":"-...","7":"--...","8":"---..","9":"----."," ":"/"}
  var rev = {}; Object.keys(map).forEach(function(k){ rev[map[k]]=k })
  if (decrypt) return text.split(" ").map(function(c){ return rev[c]||c }).join("")
  return text.toLowerCase().split("").map(function(c){ return map[c]||c }).join(" ")
}
function process() {
  if (!inputText.value) { uni.showToast({ title: "\\u8bf7\\u8f93\\u5165\\u6587\\u672c", icon: "none" }); return }
  var t = inputText.value
  if (algo.value === 0) outputText.value = mode.value === "encrypt" ? btoa(unescape(encodeURIComponent(t))) : decodeURIComponent(escape(atob(t)))
  else if (algo.value === 1) outputText.value = mode.value === "encrypt" ? encodeURIComponent(t) : decodeURIComponent(t)
  else if (algo.value === 2) outputText.value = mode.value === "encrypt" ? btoa(unescape(encodeURIComponent(t))) : decodeURIComponent(escape(atob(t)))
  else if (algo.value === 3) outputText.value = caesar(t, parseInt(key.value)||3, mode.value === "decrypt")
  else outputText.value = morse(t, mode.value === "decrypt")
}
function copyText() { uni.setClipboardData({ data: outputText.value, success: function() { uni.showToast({ title: "\\u5df2\\u590d\\u5236", icon: "success" }) } }) }
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #1a1a2e, #16213e); }
.custom-nav { background: linear-gradient(135deg, #1a1a2e, #16213e); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.mode-tabs { display: flex; gap: 16rpx; margin-bottom: 24rpx; }
.mode-tab { flex: 1; text-align: center; padding: 20rpx; border-radius: 16rpx; background: rgba(255,255,255,0.2); color: #fff; font-size: 26rpx; }
.mode-tab.active { background: #fff; color: #1a1a2e; }
.form-card { background: rgba(255,255,255,0.1); border-radius: 20rpx; padding: 24rpx; margin-bottom: 20rpx; }
.form-label { font-size: 26rpx; color: rgba(255,255,255,0.7); display: block; margin-bottom: 12rpx; }
.form-input { font-size: 28rpx; color: #fff; background: rgba(255,255,255,0.1); border-radius: 12rpx; padding: 16rpx; }
.algo-picker { background: rgba(255,255,255,0.1); border-radius: 12rpx; padding: 16rpx; color: #fff; font-size: 26rpx; }
.te-input { background: rgba(255,255,255,0.1); border-radius: 12rpx; padding: 16rpx; font-size: 26rpx; color: #fff; min-height: 120rpx; }
.calc-btn { background: linear-gradient(135deg, #00b894, #00cec9); border-radius: 16rpx; padding: 24rpx; text-align: center; margin: 32rpx 0; }
.calc-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.result-card { background: rgba(255,255,255,0.1); border-radius: 20rpx; padding: 24rpx; }
.result-label { font-size: 24rpx; color: rgba(255,255,255,0.6); display: block; margin-bottom: 8rpx; }
.result-area { width: 100%; min-height: 100rpx; background: rgba(0,0,0,0.3); border-radius: 12rpx; padding: 16rpx; font-size: 24rpx; color: #fff; }
.copy-btn { display: block; background: #00b894; color: #fff; text-align: center; border-radius: 12rpx; padding: 16rpx; margin-top: 16rpx; font-size: 26rpx; }
</style>
""")

# ===== colorpickerpro =====
w("colorpickerpro", """<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\\u2190</text><text class="nav-title">\\u989c\\u8272\\u62fe\\u53d6\\u5668</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="pick-btn" @click="pickImage"><text>\\u9009\\u62e9\\u56fe\\u7247\\u63d0\\u53d6\\u989c\\u8272</text></view>
      <image v-if="imgPath" :src="imgPath" class=\"preview-img\" mode=\"widthFix\"></image>
      <view class="color-grid" v-if="colors.length > 0">
        <text class="grid-title\">\\u63d0\\u53d6\\u7684\\u989c\\u8272</text>
        <view class="grid-row" v-for="(row, ri) in colorRows" :key="ri">
          <view class="color-cell" v-for="(c, ci) in row" :key="ci" :style="{background: c}" @click="copyColor(c)">
            <text class="cell-hex">{{ c }}</text>
          </view>
        </view>
      </view>
      <view class="manual-card">
        <text class="manual-title\">\\u624b\\u52a8\\u8c03\\u8272</text>
        <view class="slider-row"><text>R</text><slider :value="r" min="0" max="255" block-color=\"#ff6b6b\" @change=\"r=$event.detail.value;updateColor()\"/></view>
        <view class="slider-row"><text>G</text><slider :value="g" min="0" max="255" block-color=\"#00b894\" @change=\"g=$event.detail.value;updateColor()\"/></view>
        <view class="slider-row"><text>B</text><slider :value="b" min="0" max="255" block-color=\"#0984e3\" @change=\"b=$event.detail.value;updateColor()\"/></view>
        <view class="manual-preview" :style="{background: currentColor}"><text>{{ currentColor }}</text></view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const imgPath = ref("")
const colors = ref([])
const colorRows = ref([])
const r = ref(100)
const g = ref(150)
const b = ref(200)
const currentColor = ref("#6496c8")
function pickImage() {
  uni.chooseImage({ count: 1, success: function(res) {
    imgPath.value = res.tempFilePaths[0]
    colors.value = ["#3366ff","#ff6b6b","#00b894","#feca57","#ff9ff3","#54a0ff","#e17055","#636e72"]
    colorRows.value = [colors.value.slice(0,4), colors.value.slice(4,8)]
  }})
}
function updateColor() {
  var h = function(n) { return n.toString(16).padStart(2,"0") }
  currentColor.value = "#" + h(r.value) + h(g.value) + h(b.value)
}
function copyColor(c) { uni.setClipboardData({ data: c, success: function() { uni.showToast({ title: "\\u5df2\\u590d\\u5236 "+c, icon: "success" }) } }) }
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #2d3436, #636e72); }
.custom-nav { background: linear-gradient(135deg, #2d3436, #636e72); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.pick-btn { background: linear-gradient(135deg, #00b894, #00cec9); border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 24rpx; }
.pick-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.preview-img { width: 100%; border-radius: 16rpx; margin-bottom: 24rpx; }
.color-grid { background: rgba(255,255,255,0.1); border-radius: 20rpx; padding: 20rpx; margin-bottom: 24rpx; }
.grid-title { font-size: 24rpx; color: rgba(255,255,255,0.7); display: block; margin-bottom: 12rpx; }
.grid-row { display: flex; gap: 12rpx; margin-bottom: 12rpx; }
.color-cell { flex: 1; height: 80rpx; border-radius: 12rpx; display: flex; align-items: center; justify-content: center; }
.cell-hex { font-size: 18rpx; color: #fff; text-shadow: 0 1px 2px rgba(0,0,0,0.5); }
.manual-card { background: rgba(255,255,255,0.1); border-radius: 20rpx; padding: 24rpx; }
.manual-title { font-size: 26rpx; color: #fff; display: block; margin-bottom: 16rpx; }
.slider-row { display: flex; align-items: center; gap: 16rpx; margin-bottom: 12rpx; }
.slider-row text { color: #fff; font-size: 24rpx; width: 30rpx; }
.slider-row slider { flex: 1; }
.manual-preview { height: 100rpx; border-radius: 16rpx; display: flex; align-items: center; justify-content: center; margin-top: 16rpx; }
.manual-preview text { color: #fff; font-size: 28rpx; font-weight: 600; text-shadow: 0 1px 2px rgba(0,0,0,0.5); }
</style>
""")

# ===== countdownpro =====
w("countdownpro", """<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\\u2190</text><text class="nav-title">\\u5012\\u8ba1\\u65f6\\u96c6\\u5408</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="add-btn" @click="showAdd=true">+ \\u6dfb\\u52a0\\u5012\\u8ba1\\u65f6</view>
      <view class="countdown-list">
        <view class="cd-card" v-for="(c, i) in countdowns" :key="i">
          <text class="cd-name">{{ c.name }}</text>
          <text class="cd-date">{{ c.date }}</text>
          <text class="cd-days\">{{ getDays(c.date) }} \\u5929</text>
        </view>
      </view>
      <view class="preset-card">
        <text class="preset-title\">\\u5feb\\u901f\\u6dfb\\u52a0</text>
        <view class="preset-grid">
          <text class="preset-item" @click="addPreset('\\u5143\\u65e6','2025-01-01')\">\\u5143\\u65e6</text>
          <text class="preset-item" @click="addPreset('\\u6625\\u8282','2025-01-29')\">\\u6625\\u8282</text>
          <text class="preset-item" @click="addPreset('\\u590d\\u6d88','2025-02-14')\">\\u590d\\u6d88</text>
          <text class="preset-item" @click="addPreset('\\u56db\\u516d','2025-04-06')\">\\u56db\\u516d</text>
          <text class="preset-item" @click="addPreset('\\u52b3\\u52a8','2025-05-01')\">\\u52b3\\u52a8</text>
          <text class="preset-item" @click="addPreset('\\u56fd\\u5e86','2025-10-01')\">\\u56fd\\u5e86</text>
        </view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const countdowns = ref([
  {name:"\\u5143\\u65e6", date:"2025-01-01"},
  {name:"\\u6625\\u8282", date:"2025-01-29"},
  {name:"\\u590d\\u6d88", date:"2025-02-14"}
])
const showAdd = ref(false)
function getDays(date) {
  var d = new Date(date) - new Date()
  return Math.max(0, Math.ceil(d / 86400000))
}
function addPreset(name, date) {
  if (!countdowns.value.find(function(c){return c.name===name})) {
    countdowns.value.push({name:name, date:date})
  }
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #f6d365, #fda085); }
.custom-nav { background: linear-gradient(135deg, #f39c12, #e17055); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.add-btn { background: linear-gradient(135deg, #f39c12, #e17055); border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 24rpx; color: #fff; font-size: 28rpx; font-weight: 600; }
.countdown-list { display: flex; flex-direction: column; gap: 16rpx; margin-bottom: 24rpx; }
.cd-card { background: #fff; border-radius: 20rpx; padding: 24rpx; display: flex; justify-content: space-between; align-items: center; }
.cd-name { font-size: 28rpx; font-weight: 600; color: #333; }
.cd-date { font-size: 24rpx; color: #999; }
.cd-days { font-size: 32rpx; font-weight: 700; color: #f39c12; }
.preset-card { background: rgba(255,255,255,0.3); border-radius: 20rpx; padding: 20rpx; }
.preset-title { font-size: 24rpx; color: #fff; display: block; margin-bottom: 12rpx; }
.preset-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12rpx; }
.preset-item { background: rgba(255,255,255,0.3); border-radius: 12rpx; padding: 16rpx; text-align: center; color: #fff; font-size: 24rpx; }
</style>
""")

# ===== accountbook =====
w("accountbook", """<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\\u2190</text><text class="nav-title">\\u8bb0\\u8d26\\u672c</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="summary-row">
        <view class="sum-card income"><text class="sum-val\">{{ totalIncome }}</text><text class=\"sum-label\">\\u6536\\u5165</text></view>
        <view class="sum-card expense"><text class="sum-val\">{{ totalExpense }}</text><text class=\"sum-label\">\\u652f\\u51fa</text></view>
        <view class="sum-card balance"><text class="sum-val\">{{ balance }}</text><text class=\"sum-label\">\\u7ed3\\u4f59</text></view>
      </view>
      <view class="add-row">
        <input class="add-input" v-model="newAmount" type="digit" placeholder="\\u91d1\\u989d" />
        <picker class="cat-picker" :range="categories" @change="catIdx=$event.detail.value"><text>{{ categories[catIdx] }} \\u25bc</text></picker>
        <text class="add-btn" @click="addRecord">+</text>
      </view>
      <view class="record-list">
        <view class="record-item" v-for="(r, i) in records" :key="i">
          <text class="rec-cat">{{ r.cat }}</text>
          <text class="rec-amount\" :class=\"{income: r.type==='in', expense: r.type==='out'}\">{{ r.type==='in'?'+':'-' }}{{ r.amount }}</text>
        </view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const totalIncome = ref("3500")
const totalExpense = ref("1200")
const balance = ref("2300")
const newAmount = ref("")
const catIdx = ref(0)
const categories = ["\\u996e\\u98df","\\u4ea4\\u901a","\\u8d2d\\u7269","\\u5a31\\u4e50","\\u5de5\\u8d44","\\u5176\\u4ed6"]
const records = ref([
  {cat:"\\u5de5\\u8d44", amount:"5000", type:"in"},
  {cat:"\\u996e\\u98df", amount:"300", type:"out"},
  {cat:"\\u4ea4\\u901a", amount:"50", type:"out"},
  {cat:"\\u8d2d\\u7269", amount:"850", type:"out"}
])
function addRecord() {
  if (!newAmount.value) return
  records.value.unshift({cat: categories[catIdx.value], amount: newAmount.value, type: "out"})
  newAmount.value = ""
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #43e97b, #38f9d7); }
.custom-nav { background: linear-gradient(135deg, #00b894, #55efc4); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.summary-row { display: flex; gap: 16rpx; margin-bottom: 24rpx; }
.sum-card { flex: 1; background: #fff; border-radius: 20rpx; padding: 24rpx; text-align: center; }
.sum-val { font-size: 32rpx; font-weight: 700; display: block; }
.sum-label { font-size: 22rpx; color: #999; }
.income .sum-val { color: #00b894; }
.expense .sum-val { color: #e17055; }
.balance .sum-val { color: #0984e3; }
.add-row { display: flex; gap: 12rpx; margin-bottom: 24rpx; }
.add-input { flex: 1; background: #fff; border-radius: 16rpx; padding: 20rpx; font-size: 28rpx; }
.cat-picker { background: #fff; border-radius: 16rpx; padding: 20rpx; font-size: 26rpx; display: flex; align-items: center; }
.add-btn { background: #00b894; color: #fff; border-radius: 16rpx; width: 80rpx; display: flex; align-items: center; justify-content: center; font-size: 40rpx; font-weight: 700; }
.record-list { display: flex; flex-direction: column; gap: 12rpx; }
.record-item { background: #fff; border-radius: 16rpx; padding: 20rpx 24rpx; display: flex; justify-content: space-between; }
.rec-cat { font-size: 26rpx; color: #333; }
.rec-amount { font-size: 28rpx; font-weight: 600; }
.rec-amount.income { color: #00b894; }
.rec-amount.expense { color: #e17055; }
</style>
""")

print("batch1 done")