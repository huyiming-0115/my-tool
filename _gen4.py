# -*- coding: utf-8 -*-
import os
base = "pkgTools/pages"
def w(name, content):
    with open(os.path.join(base, name, name + ".vue"), "w") as f:
        f.write(content)
    print("OK:", name)

# ===== dailypoem =====
w("dailypoem", """<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\\u2190</text><text class="nav-title">\\u6bcf\\u65e5\\u8bd7\\u8bcd</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="poem-card">
        <text class="poem-title">{{ poem.title }}</text>
        <text class="poem-author">{{ poem.author }} \\u00b7 {{ poem.dynasty }}</text>
        <view class="poem-body"><text class="poem-line" v-for="(line, i) in poem.lines" :key="i">{{ line }}</text></view>
        <view class="poem-desc" v-if="showDesc"><text>{{ poem.desc }}</text></view>
        <text class="toggle-btn" @click="showDesc=!showDesc">{{ showDesc ? '\\u6536\\u8d77\\u8bd1\\u6587' : '\\u67e5\\u770b\\u8bd1\\u6587' }}</text>
      </view>
      <view class="refresh-btn" @click="refresh"><text>\\u6362\\u4e00\\u9996</text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const poem = ref({title:"",author:"",dynasty:"",lines:[],desc:""})
const showDesc = ref(false)
const poems = [
  {title:"\\u9759\\u591c\\u601d",author:"\\u674e\\u767d",dynasty:"\\u5549",lines:["\\u5e8a\\u524d\\u660e\\u6708\\u5149","\\u7591\\u662f\\u5730\\u4e0a\\u971c","\\u4e3e\\u5934\\u671b\\u660e\\u6708","\\u4f4e\\u5934\\u601d\\u6545\\u4e61"],desc:"\\u8fd9\\u9996\\u8bd7\\u5199\\u7684\\u662f\\u5728\\u9759\\u8b60\\u7684\\u591c\\u665a\\uff0c\\u89c2\\u770b\\u660e\\u6708\\u7684\\u60c5\\u666f"},
  {title:"\\u767b\\u9e40\\u697c",author:"\\u738b\\u4e4b\\u6da3",dynasty:"\\u5549",lines:["\\u767d\\u65e5\\u4f0a\\u5c71\\u5c3d","\\u9ec4\\u6cb3\\u5165\\u6d77\\u6d41","\\u6b32\\u7a77\\u5343\\u91cc\\u76ee","\\u66f4\\u4e0a\\u4e00\\u5c42\\u697c"],desc:"\\u8fd9\\u9996\\u8bd7\\u8868\\u8fbe\\u4e86\\u8bd7\\u4eba\\u7684\\u626c\\u5fd7\\u594b\\u53d1\\u4e4b\\u60c5"},
  {title:"\\u6625\\u6653",author:"\\u5b5f\\u6d69\\u7136",dynasty:"\\u5549",lines:["\\u6625\\u7720\\u4e0d\\u89c9\\u6653","\\u5904\\u5904\\u95fb\\u557c\\u9e1f","\\u591c\\u6765\\u98ce\\u96e8\\u58f0","\\u82b1\\u843d\\u77e5\\u591a\\u5c11"],desc:"\\u8fd9\\u9996\\u8bd7\\u5199\\u6625\\u65e5\\u6e05\\u6668\\u7684\\u666f\\u8c22"},
  {title:"\\u5c71\\u5c45\\u79cb\\u665f",author:"\\u738b\\u7ef4",dynasty:"\\u5549",lines:["\\u7a7a\\u5c71\\u65b0\\u96e8\\u540e","\\u5929\\u6c14\\u6765\\u66ae\\u79cb","\\u660e\\u6708\\u67f4\\u95f4\\u7167","\\u6e05\\u6cc9\\u77f3\\u4e0a\\u6d41"],desc:"\\u8fd9\\u9996\\u8bd7\\u63cf\\u5199\\u7684\\u662f\\u5c71\\u95f4\\u79cb\\u591c\\u7684\\u7f8e\\u4e3d\\u666f\\u8272"},
  {title:"\\u6708\\u4e0b\\u72ec\\u914c",author:"\\u674e\\u767d",dynasty:"\\u5549",lines:["\\u82b1\\u95f4\\u4e00\\u58f6\\u9152","\\u72ec\\u914c\\u65e0\\u76f8\\u4eb2","\\u63ea\\u6708\\u6210\\u4e09\\u5f71","\\u6211\\u6b4c\\u6708\\u5f25\\u8fb9"],desc:"\\u8fd9\\u9996\\u8bd7\\u8868\\u8fbe\\u4e86\\u8bd7\\u4eba\\u72ec\\u5c45\\u5f02\\u4e61\\u7684\\u611f\\u60c5"}
]
function refresh() {
  showDesc.value = false
  poem.value = poems[Math.floor(Math.random() * poems.length)]
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }; refresh() })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #ffecd2, #fcb69f); }
.custom-nav { background: linear-gradient(135deg, #e17055, #fdcb6e); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.poem-card { background: #fff; border-radius: 24rpx; padding: 40rpx; text-align: center; margin-bottom: 32rpx; }
.poem-title { font-size: 36rpx; font-weight: 700; color: #333; display: block; margin-bottom: 8rpx; }
.poem-author { font-size: 24rpx; color: #999; display: block; margin-bottom: 24rpx; }
.poem-body { margin-bottom: 20rpx; }
.poem-line { font-size: 30rpx; color: #444; display: block; padding: 4rpx 0; line-height: 1.8; }
.poem-desc { background: #f8f8f8; border-radius: 16rpx; padding: 20rpx; font-size: 24rpx; color: #666; text-align: left; margin-top: 16rpx; }
.toggle-btn { font-size: 24rpx; color: #e17055; margin-top: 16rpx; display: inline-block; }
.refresh-btn { background: linear-gradient(135deg, #e17055, #fdcb6e); border-radius: 16rpx; padding: 24rpx; text-align: center; }
.refresh-btn text { color: #fff; font-size: 28rpx; font-weight: 600; }
</style>
""")

# ===== translator =====
w("translator", """<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\\u2190</text><text class="nav-title">\\u7ffb\\u8bd1\\u5de5\\u5177</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="lang-row">
        <picker class="lang-picker" :range="langs" range-key="name" @change="fromLang=Number($event.detail.value)"><text>{{ langs[fromLang].name }} \\u25bc</text></picker>
        <text class="swap-btn" @click="swapLang">\\u2194</text>
        <picker class="lang-picker" :range="langs" range-key="name" @change="toLang=Number($event.detail.value)"><text>{{ langs[toLang].name }} \\u25bc</text></picker>
      </view>
      <textarea class="tr-input" v-model="inputText" placeholder="\\u8f93\\u5165\\u8981\\u7ffb\\u8bd1\\u7684\\u6587\\u672c" auto-height></textarea>
      <view class="tr-btn" @click="translate"><text>\\u7ffb\\u8bd1</text></view>
      <view class="tr-result" v-if="outputText"><text>{{ outputText }}</text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const inputText = ref("")
const outputText = ref("")
const fromLang = ref(0)
const toLang = ref(1)
const langs = [{name:"\\u4e2d\\u6587",code:"zh"},{name:"\\u82f1\\u6587",code:"en"},{name:"\\u65e5\\u6587",code:"ja"},{name:"\\u97e9\\u6587",code:"ko"},{name:"\\u6cd5\\u6587",code:"fr"},{name:"\\u5fb7\\u6587",code:"de"},{name:"\\u897f\\u73ed\\u7259\\u6587",code:"es"}]
const dict = {
  "hello":"\\u4f60\\u597d","world":"\\u4e16\\u754c","thank":"\\u8c22\\u8c22","love":"\\u7231","friend":"\\u670b\\u53cb",
  "\\u4f60\\u597d":"hello","\\u4e16\\u754c":"world","\\u8c22\\u8c22":"thank you","\\u7231":"love","\\u670b\\u53cb":"friend"
}
function translate() {
  if (!inputText.value.trim()) { uni.showToast({ title: "\\u8bf7\\u8f93\\u5165\\u6587\\u672c", icon: "none" }); return }
  const key = inputText.value.trim().toLowerCase()
  outputText.value = dict[key] || "\\u7ffb\\u8bd1\\u7ed3\\u679c: " + inputText.value + " (" + langs[fromLang.value].name + "\\u2192" + langs[toLang.value].name + ")"
}
function swapLang() { const t = fromLang.value; fromLang.value = toLang.value; toLang.value = t }
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #a1c4fd, #c2e9fb); }
.custom-nav { background: linear-gradient(135deg, #0984e3, #74b9ff); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.lang-row { display: flex; align-items: center; gap: 16rpx; margin-bottom: 24rpx; }
.lang-picker { flex: 1; background: #fff; border-radius: 16rpx; padding: 20rpx; text-align: center; font-size: 28rpx; }
.swap-btn { font-size: 36rpx; color: #fff; }
.tr-input { background: #fff; border-radius: 20rpx; padding: 24rpx; font-size: 28rpx; min-height: 160rpx; margin-bottom: 24rpx; }
.tr-btn { background: linear-gradient(135deg, #0984e3, #74b9ff); border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 24rpx; }
.tr-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.tr-result { background: #fff; border-radius: 20rpx; padding: 24rpx; font-size: 28rpx; color: #333; }
</style>
""")

# ===== cardvalidate =====
w("cardvalidate", """<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\\u2190</text><text class="nav-title">\\u94f6\\u884c\\u5361\\u6821\\u9a8c</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="form-card"><text class="form-label">\\u94f6\\u884c\\u5361\\u53f7</text><input class="form-input" type="number" v-model="cardNo" placeholder="\\u8f93\\u5165\\u5361\\u53f7" maxlength="19" /></view>
      <view class="calc-btn" @click="validate"><text>\\u6821\\u9a8c</text></view>
      <view class="result-card" v-if="result">
        <text class="result-label">\\u6821\\u9a8c\\u7ed3\\u679c</text>
        <text class="result-valid" v-if="result.valid" style="color:#00b894;">\\u2714 \\u6709\\u6548\\u7684\\u5361\\u53f7</text>
        <text class="result-valid" v-else style="color:#e17055;">\\u2718 \\u65e0\\u6548\\u7684\\u5361\\u53f7</text>
        <text class="result-text\">\\u5361\\u7c7b\\u578b: {{ result.type }}</text>
        <text class=\"result-text\">\\u4f4d\\u6570: {{ cardNo.length }}</text>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const cardNo = ref("")
const result = ref(null)
function luhnCheck(num) {
  let sum = 0, alt = false
  for (let i = num.length - 1; i >= 0; i--) {
    let n = parseInt(num[i])
    if (alt) { n *= 2; if (n > 9) n -= 9 }
    sum += n; alt = !alt
  }
  return sum % 10 === 0
}
function getCardType(num) {
  if (/^4/.test(num)) return "Visa"
  if (/^5[1-5]/.test(num)) return "MasterCard"
  if (/^62/.test(num)) return "\\u94f6\\u8054"
  if (/^9558/.test(num)) return "\\u5de5\\u5546\\u94f6\\u884c"
  if (/^6222|^6223/.test(num)) return "\\u4e2d\\u65b9\\u94f6\\u884c"
  return "\\u672a\\u77e5"
}
function validate() {
  const num = cardNo.value.replace(/\s/g, "")
  if (!num || num.length < 13) { uni.showToast({ title: "\\u8bf7\\u8f93\\u5165\\u6709\\u6548\\u5361\\u53f7", icon: "none" }); return }
  result.value = { valid: luhnCheck(num), type: getCardType(num) }
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
.form-input { font-size: 32rpx; color: #333; font-weight: 600; letter-spacing: 4rpx; }
.calc-btn { background: linear-gradient(135deg, #e84393, #fd79a8); border-radius: 16rpx; padding: 24rpx; text-align: center; margin: 32rpx 0; }
.calc-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.result-card { background: #fff; border-radius: 24rpx; padding: 32rpx; text-align: center; }
.result-label { font-size: 24rpx; color: #999; display: block; margin-bottom: 12rpx; }
.result-valid { font-size: 32rpx; font-weight: 700; display: block; margin-bottom: 16rpx; }
.result-text { font-size: 26rpx; color: #666; display: block; padding: 4rpx 0; }
</style>
""")

# ===== imagetobase64 =====
w("imagetobase64", """<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\\u2190</text><text class="nav-title">\\u56fe\\u7247\\u8f6cBase64</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="pick-btn" @click="pickImage"><text>\\u9009\\u62e9\\u56fe\\u7247</text></view>
      <image v-if="imgPath" :src="imgPath" class=\"preview-img\" mode=\"widthFix\"></image>
      <view class="result-card" v-if="base64Result">
        <text class="result-label">Base64 \\u7f16\\u7801</text>
        <textarea class=\"b64-output\" :value=\"base64Result\" disabled auto-height></textarea>
        <text class="copy-btn" @click="copyText">\\u590d\\u5236</text>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const imgPath = ref("")
const base64Result = ref("")
function pickImage() {
  uni.chooseImage({
    count: 1,
    success: function(res) {
      imgPath.value = res.tempFilePaths[0]
      uni.getFileSystemManager().readFile({
        filePath: res.tempFilePaths[0],
        encoding: "base64",
        success: function(r) {
          base64Result.value = "data:image/jpeg;base64," + r.data
        }
      })
    }
  })
}
function copyText() {
  uni.setClipboardData({ data: base64Result.value, success: function() { uni.showToast({ title: "\\u5df2\\u590d\\u5236", icon: "success" }) } })
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
.pick-btn { background: linear-gradient(135deg, #00b894, #55efc4); border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 32rpx; }
.pick-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.preview-img { width: 100%; border-radius: 16rpx; margin-bottom: 24rpx; }
.result-card { background: #fff; border-radius: 24rpx; padding: 32rpx; }
.result-label { font-size: 26rpx; color: #666; display: block; margin-bottom: 12rpx; }
.b64-output { width: 100%; background: #f8f8f8; border-radius: 12rpx; padding: 16rpx; font-size: 20rpx; color: #666; min-height: 120rpx; }
.copy-btn { display: block; background: #00b894; color: #fff; text-align: center; border-radius: 12rpx; padding: 16rpx; margin-top: 16rpx; font-size: 26rpx; }
</style>
""")

print("batch4 done")