<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">Markdown\u7f16\u8f91\u5668</text><text class="nav-icon" @click="preview=!preview">{{ preview ? '\u270e' : '\u270e' }}</text></view>
    </view>
    <view class="content">
      <view class="toolbar">
        <text class="tool-btn" @click="insertText('**','**')">B</text>
        <text class="tool-btn" @click="insertText('*','*')">I</text>
        <text class="tool-btn" @click="insertText('# ','')">H1</text>
        <text class="tool-btn" @click="insertText('## ','')">H2</text>
        <text class="tool-btn" @click="insertText('- ','')">\u2022</text>
        <text class="tool-btn" @click="insertText('[](url)',')')">\u270e</text>
        <text class="tool-btn" @click="insertText('> ','')">\u2753</text>
      </view>
      <textarea class="md-input" v-model="mdText" placeholder="\u8f93\u5165Markdown\u6587\u672c..." v-show="!preview" auto-height></textarea>
      <view class="md-preview" v-if="preview"><rich-text :nodes="renderedHtml"></rich-text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, computed, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const mdText = ref("# \u6b22\u8fce\u4f7f\u7528\n\n**\u52a0\u7c97** \u548c *\u659c\u4f53*\n\n- \u5217\u8868\u98791\n- \u5217\u8868\u98792\n\n> \u5f15\u7528\u6587\u672c")
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
  return html.replace(/
/g, "<br/>")
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
