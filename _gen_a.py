# -*- coding: utf-8 -*-
import os
base = "pkgTools/pages"
def w(name, content):
    with open(os.path.join(base, name, name + ".vue"), "w") as f:
        f.write(content)
    print("OK:", name)

# ===== currencyconverter =====
w("currencyconverter", """<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\\u2190</text><text class="nav-title">\\u6c47\\u7387\\u8f6c\\u6362\\u5668</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="form-card"><text class="form-label">\\u91d1\\u989d</text><input class="form-input" type="digit" v-model="amount" placeholder="\\u8f93\\u5165\\u91d1\\u989d" /></view>
      <view class="currency-row">
        <picker class="curr-picker" :range="currencies" range-key="name" @change="fromIdx=Number($event.detail.value)">
          <text>{{ currencies[fromIdx].name }} \\u25bc</text>
        </picker>
        <text class="swap-btn" @click="swapCurr">\\u2194</text>
        <picker class="curr-picker" :range="currencies" range-key="name" @change="toIdx=Number($event.detail.value)">
          <text>{{ currencies[toIdx].name }} \\u25bc</text>
        </picker>
      </view>
      <view class="calc-btn" @click="convert"><text>\\u8f6c\\u6362</text></view>
      <view class="result-card" v-if="result">
        <text class="result-amount">{{ amount }} {{ currencies[fromIdx].code }}</text>
        <text class="result-arrow">\\u2193</text>
        <text class="result-val">{{ result }} {{ currencies[toIdx].code }}</text>
        <text class="result-rate">\\u6c47\\u7387: 1 {{ currencies[fromIdx].code }} = {{ rate }} {{ currencies[toIdx].code }}</text>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const amount = ref("")
const fromIdx = ref(0)
const toIdx = ref(1)
const result = ref("")
const rate = ref("")
const currencies = [
  {code:"CNY", name:"\\u4eba\\u6c11\\u5e01", rate:1},
  {code:"USD", name:"\\u7f8e\\u5143", rate:0.14},
  {code:"EUR", name:"\\u6b27\\u5143", rate:0.13},
  {code:"JPY", name:"\\u65e5\\u5143", rate:20.5},
  {code:"KRW", name:"\\u97e9\\u5143", rate:185},
  {code:"GBP", name:"\\u82f1\\u9551", rate:0.11},
  {code:"HKD", name:"\\u6e2f\\u5e01", rate:1.1},
  {code:"TWD", name:"\\u53f0\\u5e01", rate:4.5}
]
function convert() {
  const a = parseFloat(amount.value) || 0
  if (a <= 0) { uni.showToast({ title: "\\u8bf7\\u8f93\\u5165\\u91d1\\u989d", icon: "none" }); return }
  const r = currencies[toIdx.value].rate / currencies[fromIdx.value].rate
  rate.value = r.toFixed(4)
  result.value = (a * r).toFixed(2)
}
function swapCurr() { const t = fromIdx.value; fromIdx.value = toIdx.value; toIdx.value = t }
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
.form-card { background: #fff; border-radius: 20rpx; padding: 24rpx; margin-bottom: 20rpx; }
.form-label { font-size: 26rpx; color: #666; display: block; margin-bottom: 12rpx; }
.form-input { font-size: 36rpx; color: #333; font-weight: 600; }
.currency-row { display: flex; align-items: center; gap: 16rpx; margin-bottom: 24rpx; }
.curr-picker { flex: 1; background: #fff; border-radius: 16rpx; padding: 20rpx; text-align: center; font-size: 28rpx; }
.swap-btn { font-size: 36rpx; color: #fff; }
.calc-btn { background: linear-gradient(135deg, #5a67d8, #6b46c1); border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 32rpx; }
.calc-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.result-card { background: #fff; border-radius: 24rpx; padding: 32rpx; text-align: center; }
.result-amount { font-size: 28rpx; color: #999; display: block; }
.result-arrow { font-size: 32rpx; color: #5a67d8; display: block; margin: 8rpx 0; }
.result-val { font-size: 40rpx; font-weight: 700; color: #5a67d8; display: block; }
.result-rate { font-size: 22rpx; color: #999; display: block; margin-top: 12rpx; }
</style>
""")

# ===== passwordgenerator =====
w("passwordgenerator", """<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\\u2190</text><text class="nav-title">\\u5bc6\\u7801\\u751f\\u6210\\u5668</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="opt-card"><text class="opt-label">\\u957f\\u5ea6: {{ length }}</text><slider :value="length" min="6" max="32" show-value @change="length=Number($event.detail.value)"/></view>
      <view class="opt-card">
        <view class="check-row"><checkbox :checked="useLower" @click="useLower=!useLower"/><text>\\u5c0f\\u5199\\u5b57\\u6bcd (a-z)</text></view>
        <view class="check-row"><checkbox :checked="useUpper" @click="useUpper=!useUpper"/><text>\\u5927\\u5199\\u5b57\\u6bcd (A-Z)</text></view>
        <view class="check-row"><checkbox :checked="useNum" @click="useNum=!useNum"/><text>\\u6570\\u5b57 (0-9)</text></view>
        <view class="check-row"><checkbox :checked="useSymbol" @click="useSymbol=!useSymbol"/><text>\\u7279\\u6b8a\\u5b57\\u7b26 (!@#$)</text></view>
      </view>
      <view class="gen-btn" @click="generate"><text>\\u751f\\u6210\\u5bc6\\u7801</text></view>
      <view class="result-card" v-if="password">
        <text class="pwd-text">{{ password }}</text>
        <view class="pwd-actions"><text class="pwd-btn" @click="copyPwd">\\u590d\\u5236</text><text class="pwd-btn regen" @click="generate">\\u91cd\\u65b0\\u751f\\u6210</text></view>
        <text class="strength-text" :style="{color: strengthColor}">{{ strengthText }}</text>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const length = ref(12)
const useLower = ref(true)
const useUpper = ref(true)
const useNum = ref(true)
const useSymbol = ref(false)
const password = ref("")
const strengthText = ref("")
const strengthColor = ref("#999")
function generate() {
  let chars = ""
  if (useLower.value) chars += "abcdefghijklmnopqrstuvwxyz"
  if (useUpper.value) chars += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  if (useNum.value) chars += "0123456789"
  if (useSymbol.value) chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
  if (!chars) { uni.showToast({ title: "\\u81f3\\u5c11\\u9009\\u4e00\\u79cd", icon: "none" }); return }
  let pwd = ""
  for (let i = 0; i < length.value; i++) pwd += chars[Math.floor(Math.random() * chars.length)]
  password.value = pwd
  const s = (useLower.value?1:0)+(useUpper.value?1:0)+(useNum.value?1:0)+(useSymbol.value?1:0)
  if (s >= 3 && length.value >= 12) { strengthText.value = "\\u5f3a"; strengthColor.value = "#00b894" }
  else if (s >= 2 && length.value >= 8) { strengthText.value = "\\u4e2d"; strengthColor.value = "#fdcb6e" }
  else { strengthText.value = "\\u5f31"; strengthColor.value = "#e17055" }
}
function copyPwd() {
  uni.setClipboardData({ data: password.value, success: function() { uni.showToast({ title: "\\u5df2\\u590d\\u5236", icon: "success" }) } })
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }; generate() })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #1e3c72, #2a5298); }
.custom-nav { background: linear-gradient(135deg, #1e3c72, #2a5298); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.opt-card { background: rgba(255,255,255,0.1); border-radius: 20rpx; padding: 24rpx; margin-bottom: 20rpx; }
.opt-label { font-size: 28rpx; color: #fff; display: block; margin-bottom: 12rpx; }
.check-row { display: flex; align-items: center; gap: 16rpx; padding: 12rpx 0; color: #fff; font-size: 26rpx; }
.gen-btn { background: linear-gradient(135deg, #00b894, #00cec9); border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 32rpx; }
.gen-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.result-card { background: #fff; border-radius: 24rpx; padding: 32rpx; text-align: center; }
.pwd-text { font-size: 28rpx; color: #333; font-family: monospace; word-break: break-all; display: block; margin-bottom: 20rpx; }
.pwd-actions { display: flex; gap: 16rpx; justify-content: center; margin-bottom: 16rpx; }
.pwd-btn { padding: 12rpx 24rpx; border-radius: 12rpx; background: #1e3c72; color: #fff; font-size: 24rpx; }
.pwd-btn.regen { background: #00b894; }
.strength-text { font-size: 24rpx; font-weight: 600; }
</style>
""")

# ===== bodyfitness =====
w("bodyfitness", """<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\\u2190</text><text class="nav-title">\\u4f53\\u8102\\u7387\\u8ba1\\u7b97</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="form-card">
        <view class="gender-row"><text class="gender-btn" :class="{active: gender==='male'}" @click="gender='male'">\\u7537</text><text class="gender-btn" :class="{active: gender==='female'}" @click="gender='female'">\\u5973</text></view>
      </view>
      <view class="form-card"><text class="form-label">\\u8eab\\u9ad8 (cm)</text><input class="form-input" type="digit" v-model="height" /></view>
      <view class="form-card"><text class="form-label">\\u4f53\\u91cd (kg)</text><input class="form-input" type="digit" v-model="weight" /></view>
      <view class="form-card"><text class="form-label">\\u8170\\u56f4 (cm)</text><input class="form-input" type="digit" v-model="waist" /></view>
      <view class="form-card"><text class="form-label">\\u5e74\\u9f84</text><input class="form-input" type="number" v-model="age" /></view>
      <view class="calc-btn" @click="calc"><text>\\u8ba1\\u7b97</text></view>
      <view class="result-card" v-if="bmi">
        <view class="res-row"><text>BMI:</text><text class="res-val">{{ bmi }}</text></view>
        <view class="res-row"><text>\\u4f53\\u8102\\u7387:</text><text class="res-val">{{ bodyFat }}%</text></view>
        <view class="res-row"><text>\\u57fa\\u7840\\u4ee3\\u8c22:</text><text class="res-val">{{ bmr }} kcal</text></view>
        <view class="res-row"><text>\\u6bcf\\u65e5\\u6d88\\u8017(TDEE):</text><text class="res-val">{{ tdee }} kcal</text></view>
        <text class="res-tip">{{ tip }}</text>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const gender = ref("male")
const height = ref("")
const weight = ref("")
const waist = ref("")
const age = ref("")
const bmi = ref("")
const bodyFat = ref("")
const bmr = ref("")
const tdee = ref("")
const tip = ref("")
function calc() {
  const h = parseFloat(height.value), w = parseFloat(weight.value)
  const waistVal = parseFloat(waist.value), a = parseFloat(age.value)
  if (!h || !w) { uni.showToast({ title: "\\u8bf7\\u8f93\\u5165\\u8eab\\u9ad8\\u4f53\\u91cd", icon: "none" }); return }
  bmi.value = (w / ((h/100) ** 2)).toFixed(1)
  if (waistVal && a) {
    if (gender.value === "male") bodyFat.value = ((1.2 * parseFloat(bmi.value)) + (0.23 * a) - 16.2).toFixed(1)
    else bodyFat.value = ((1.2 * parseFloat(bmi.value)) + (0.23 * a) - 5.4).toFixed(1)
  } else bodyFat.value = (parseFloat(bmi.value) * 1.2 + (gender.value==="male"?16.2:5.4)).toFixed(1)
  bmr.value = gender.value === "male" ? (10*w + 6.25*h - 5*a + 5).toFixed(0) : (10*w + 6.25*h - 5*a - 161).toFixed(0)
  tdee.value = (parseFloat(bmr.value) * 1.55).toFixed(0)
  const b = parseFloat(bmi.value)
  if (b < 18.5) tip.value = "\\u504f\\u7626\\uff0c\\u5efa\\u8bae\\u589e\\u91cd\\u589e\\u808c"
  else if (b < 24) tip.value = "\\u6b63\\u5e38\\uff0c\\u4fdd\\u6301\\u73b0\\u72b6"
  else if (b < 28) tip.value = "\\u504f\\u80a5\\uff0c\\u5efa\\u8bae\\u9002\\u5f53\\u51cf\\u8102"
  else tip.value = "\\u80a5\\u80d6\\uff0c\\u5efa\\u8bae\\u5236\\u5b9a\\u51cf\\u8102\\u8ba1\\u5212"
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #f093fb, #f5576c); }
.custom-nav { background: linear-gradient(135deg, #e84393, #fd79a8); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.form-card { background: #fff; border-radius: 20rpx; padding: 24rpx; margin-bottom: 20rpx; }
.form-label { font-size: 26rpx; color: #666; display: block; margin-bottom: 12rpx; }
.form-input { font-size: 32rpx; color: #333; font-weight: 600; }
.gender-row { display: flex; gap: 16rpx; }
.gender-btn { flex: 1; text-align: center; padding: 16rpx; border-radius: 12rpx; background: #f0f0f0; font-size: 28rpx; }
.gender-btn.active { background: #e84393; color: #fff; }
.calc-btn { background: linear-gradient(135deg, #e84393, #fd79a8); border-radius: 16rpx; padding: 24rpx; text-align: center; margin: 32rpx 0; }
.calc-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.result-card { background: #fff; border-radius: 24rpx; padding: 32rpx; }
.res-row { display: flex; justify-content: space-between; padding: 12rpx 0; font-size: 28rpx; }
.res-val { color: #e84393; font-weight: 700; }
.res-tip { display: block; margin-top: 16rpx; padding: 16rpx; background: #fff0f5; border-radius: 12rpx; font-size: 24rpx; color: #e84393; }
</style>
""")

# ===== markdowneditor =====
w("markdowneditor", """<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\\u2190</text><text class="nav-title">Markdown\\u7f16\\u8f91\\u5668</text><text class="nav-icon" @click="preview=!preview">{{ preview ? '\\u270e' : '\\u270e' }}</text></view>
    </view>
    <view class="content">
      <view class="toolbar">
        <text class="tool-btn" @click="insertText('**','**')">B</text>
        <text class="tool-btn" @click="insertText('*','*')">I</text>
        <text class="tool-btn" @click="insertText('# ','')">H1</text>
        <text class="tool-btn" @click="insertText('## ','')">H2</text>
        <text class="tool-btn" @click="insertText('- ','')">\\u2022</text>
        <text class="tool-btn" @click="insertText('[](url)',')')">\\u270e</text>
        <text class="tool-btn" @click="insertText('> ','')">\\u2753</text>
      </view>
      <textarea class="md-input" v-model="mdText" placeholder="\\u8f93\\u5165Markdown\\u6587\\u672c..." v-show="!preview" auto-height></textarea>
      <view class="md-preview" v-if="preview"><rich-text :nodes="renderedHtml"></rich-text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, computed, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const mdText = ref("# \\u6b22\\u8fce\\u4f7f\\u7528\\n\\n**\\u52a0\\u7c97** \\u548c *\\u659c\\u4f53*\\n\\n- \\u5217\\u8868\\u98791\\n- \\u5217\\u8868\\u98792\\n\\n> \\u5f15\\u7528\\u6587\\u672c")
const preview = ref(false)
const renderedHtml = computed(function() {
  let html = mdText.value
  html = html.replace(/^### (.+)$/gm, "<h3>$1</h3>")
  html = html.replace(/^## (.+)$/gm, "<h2>$1</h2>")
  html = html.replace(/^# (.+)$/gm, "<h1>$1</h1>")
  html = html.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
  html = html.replace(/\*(.+?)\*/g, "<em>$1</em>")
  html = html.replace(/^- (.+)$/gm, "<li>$1</li>")
  html = html.replace(/^> (.+)$/gm, "<blockquote>$1</blockquote>")
  return html.replace(/\n/g, "<br/>")
})
function insertText(before, after) {
  const ta = document.querySelector("textarea")
  if (ta) { mdText.value += before + after }
  else { mdText.value += before }
}
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
.content { padding: 20rpx; }
.toolbar { display: flex; gap: 8rpx; margin-bottom: 16rpx; flex-wrap: wrap; }
.tool-btn { padding: 12rpx 20rpx; background: rgba(255,255,255,0.1); border-radius: 8rpx; color: #fff; font-size: 24rpx; font-weight: 600; }
.md-input { background: rgba(255,255,255,0.95); border-radius: 16rpx; padding: 24rpx; font-size: 26rpx; min-height: 60vh; font-family: monospace; }
.md-preview { background: #fff; border-radius: 16rpx; padding: 24rpx; min-height: 60vh; font-size: 26rpx; }
</style>
""")

print("batch1 done")