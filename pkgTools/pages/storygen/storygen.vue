<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u968f\u673a\u6545\u4e8b\u751f\u6210</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="form-card"><text class="form-label">\u4e3b\u89d2\u540d\u5b57</text><input class="form-input" v-model="hero" placeholder="\u5f20\u4e09" /></view>
      <view class="form-card"><text class="form-label">\u573a\u666f</text><view class="tag-row"><text class="tag" :class="{active: scene==='\u53e4\u4ee3'}" @click="scene='\u53e4\u4ee3'">\u53e4\u4ee3</text><text class="tag" :class="{active: scene==='\u73b0\u4ee3'}" @click="scene='\u73b0\u4ee3'">\u73b0\u4ee3</text><text class="tag" :class="{active: scene==='\u672a\u6765'}" @click="scene='\u672a\u6765'">\u672a\u6765</text><text class="tag" :class="{active: scene==='\u5947\u5e7b'}" @click="scene='\u5947\u5e7b'">\u5947\u5e7b</text></view></view>
      <view class="form-card"><text class="form-label">\u60c5\u8282</text><view class="tag-row"><text class="tag" :class="{active: plot==='\u5192\u9669'}" @click="plot='\u5192\u9669'">\u5192\u9669</text><text class="tag" :class="{active: plot==='\u7231\u60c5'}" @click="plot='\u7231\u60c5'">\u7231\u60c5</text><text class="tag" :class="{active: plot==='\u60ac\u7591'}" @click="plot='\u60ac\u7591'">\u60ac\u7591</text><text class="tag" :class="{active: plot==='\u559c\u5267'}" @click="plot='\u559c\u5267'">\u559c\u5267</text></view></view>
      <view class="gen-btn" @click="generate"><text>\u751f\u6210\u6545\u4e8b</text></view>
      <view class="result-card" v-if="story"><text class="story-text">{{ story }}</text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const hero = ref("\u5c0f\u660e")
const scene = ref("\u53e4\u4ee3")
const plot = ref("\u5192\u9669")
const story = ref("")
const openings = { "\u53e4\u4ee3":"\u5728\u4e00\u4e2a\u9057\u8bb8\u7684\u53e4\u4ee3\u57ce\u90b1\uff0c","\u73b0\u4ee3":"\u5728\u7e41\u534e\u7684\u5927\u90fd\u5e02\u91cc\uff0c","\u672a\u6765":"\u57282099\u5e74\u7684\u667a\u80fd\u57ce\u5e02\uff0c","\u5947\u5e7b":"\u5728\u4e00\u4e2a\u795e\u79d8\u7684\u5f02\u4e16\u754c\uff0c" }
const middles = { "\u5192\u9669":"{hero}\u610f\u5916\u53d1\u73b0\u4e86\u4e00\u5f20\u79d8\u5bc6\u5730\u56fe\uff0c\u4e8e\u662f\u5f00\u59cb\u4e86\u4e00\u573a\u60ca\u5fc3\u52a8\u9b44\u7684\u5192\u9669\u3002","\u7231\u60c5":"{hero}\u9082\u9005\u4e86\u4e00\u4f4d\u7f8e\u4e3d\u7684\u5f02\u60c5\u4eba\uff0c\u4e24\u4eba\u4e4b\u95f4\u4ea7\u751f\u4e86\u7f9f\u52d2\u7684\u7231\u60c5\u3002","\u60ac\u7591":"{hero}\u6536\u5230\u4e86\u4e00\u5c01\u795e\u79d8\u7684\u60ac\u7591\u4fe1\uff0c\u5f00\u59cb\u4e86\u8ffd\u67e5\u771f\u76f8\u7684\u4e4b\u65c5\u3002","\u559c\u5267":"{hero}\u7684\u751f\u6d3b\u5145\u6ee1\u4e86\u5404\u79cd\u65e0\u6545\u7684\u559c\u5267\u60c5\u8282\u3002" }
const endings = { "\u5192\u9669":"\u6700\u7ec8\uff0c{hero}\u6210\u529f\u627e\u5230\u4e86\u9057\u8bb8\u7684\u5b9d\u85cf\uff0c\u5f53\u4e0a\u4e86\u4eba\u751f\u5dc5\u5cf0\u3002","\u7231\u60c5":"\u7ecf\u8fc7\u4e00\u7cfb\u5217\u6ce2\u6298\uff0c{hero}\u7ec8\u4e8e\u548c\u5fc3\u7231\u7684\u4eba\u5728\u4e00\u8d77\u4e86\u3002","\u60ac\u7591":"\u7ec8\u4e8e\uff0c{hero}\u62ff\u5230\u4e86\u5173\u952e\u8bc1\u636e\uff0c\u771f\u76f8\u5927\u767d\u3002","\u559c\u5267":"\u6700\u540e\u6210\u4e86\u4e00\u4e2a\u5e7d\u9ed8\u800c\u610f\u5916\u7684\u7ed3\u5c40\u3002" }
function generate() {
  story.value = openings[scene.value].replace("{hero}", hero.value) + middles[plot.value].replace("{hero}", hero.value) + endings[plot.value].replace("{hero}", hero.value)
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
.form-card { background: #fff; border-radius: 20rpx; padding: 24rpx; margin-bottom: 20rpx; }
.form-label { font-size: 26rpx; color: #666; display: block; margin-bottom: 12rpx; }
.form-input { font-size: 32rpx; color: #333; font-weight: 600; }
.tag-row { display: flex; gap: 12rpx; flex-wrap: wrap; }
.tag { padding: 12rpx 24rpx; border-radius: 12rpx; background: #f0f0f0; font-size: 24rpx; color: #666; }
.tag.active { background: #6c5ce7; color: #fff; }
.gen-btn { background: linear-gradient(135deg, #6c5ce7, #a29bfe); border-radius: 16rpx; padding: 24rpx; text-align: center; margin: 32rpx 0; }
.gen-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.result-card { background: #fff; border-radius: 24rpx; padding: 32rpx; }
.story-text { font-size: 28rpx; color: #333; line-height: 1.8; }
</style>
