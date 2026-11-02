<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u6d77\u62a5\u6a21\u677f</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="template-row">
        <text class="tpl-label">\u6a21\u677f:</text>
        <scroll-view class="tpl-scroll" scroll-x>
          <view class="tpl-item" v-for="(t, i) in templates" :key="i" :class="{active: tplIdx===i}" @click="tplIdx=i" :style="{background: t.bg}">
            <text class="tpl-name">{{ t.name }}</text>
          </view>
        </scroll-view>
      </view>
      <view class="poster-preview" :style="{background: templates[tplIdx].bg}">
        <textarea class="poster-text" v-model="posterText" placeholder="\u8f93\u5165\u6587\u5b57..." maxlength="50"></textarea>
      </view>
      <view class="form-card"><text class="form-label">\u6587\u5b57\u989c\u8272</text><view class="color-row"><view class="color-dot" v-for="c in textColors" :key="c" :style="{background:c, border: textColor===c?'4rpx solid #333':'none'}" @click="textColor=c"></view></view></view>
      <view class="save-btn" @click="savePoster"><text>\u4fdd\u5b58\u6d77\u62a5</text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const tplIdx = ref(0)
const posterText = ref("\u4f60\u6700\u597d\u770b")
const textColor = ref("#ffffff")
const templates = [
  {name:"\u6d6a\u6f2b", bg:"linear-gradient(135deg, #667eea, #764ba2)"},
  {name:"\u6696\u9633", bg:"linear-gradient(135deg, #f6d365, #fda085)"},
  {name:"\u6d77\u6d0b", bg:"linear-gradient(135deg, #4facfe, #00f2fe)"},
  {name:"\u68ee\u7cfb", bg:"linear-gradient(135deg, #84fab0, #8fd3f4)"},
  {name:"\u591c\u665a", bg:"linear-gradient(135deg, #2d3436, #636e72)"},
  {name:"\u6d0b\u8471", bg:"linear-gradient(135deg, #f093fb, #f5576c)"}
]
const textColors = ["#ffffff","#000000","#ff6b6b","#feca57","#48dbfb","#ff9ff3"]
function savePoster() { uni.showToast({ title: "\u5df2\u4fdd\u5b58", icon: "success" }) }
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
.template-row { margin-bottom: 24rpx; }
.tpl-label { font-size: 26rpx; color: rgba(255,255,255,0.7); display: block; margin-bottom: 12rpx; }
.tpl-scroll { white-space: nowrap; }
.tpl-item { display: inline-block; width: 160rpx; height: 100rpx; border-radius: 12rpx; margin-right: 12rpx; text-align: center; line-height: 100rpx; }
.tpl-item.active { border: 4rpx solid #fff; }
.tpl-name { color: #fff; font-size: 24rpx; font-weight: 600; }
.poster-preview { width: 100%; height: 600rpx; border-radius: 24rpx; display: flex; align-items: center; justify-content: center; margin-bottom: 24rpx; }
.poster-text { width: 80%; text-align: center; font-size: 40rpx; font-weight: 700; color: #fff; background: transparent; }
.form-card { background: rgba(255,255,255,0.1); border-radius: 20rpx; padding: 24rpx; margin-bottom: 24rpx; }
.form-label { font-size: 26rpx; color: rgba(255,255,255,0.7); display: block; margin-bottom: 12rpx; }
.color-row { display: flex; gap: 16rpx; }
.color-dot { width: 48rpx; height: 48rpx; border-radius: 50%; }
.save-btn { background: linear-gradient(135deg, #00b894, #00cec9); border-radius: 16rpx; padding: 24rpx; text-align: center; }
.save-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
</style>
