<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u98df\u8c31\u5927\u5168</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="search-bar"><input class="search-input" v-model="keyword" placeholder="\u641c\u7d22\u98df\u8c31" /><text class="search-btn" @click="search">\u641c\u7d22</text></view>
      <view class="recipe-list">
        <view class="recipe-card" v-for="(r, i) in filteredRecipes" :key="i" @click="selected=r">
          <text class="recipe-name">{{ r.name }}</text>
          <text class="recipe-desc">{{ r.desc }}</text>
          <view class="recipe-tags"><text class="tag" v-for="(t, ti) in r.tags" :key="ti">{{ t }}</text></view>
        </view>
      </view>
      <view class="recipe-detail" v-if="selected">
        <text class="detail-name">{{ selected.name }}</text>
        <text class="detail-title">\u98df\u6750</text>
        <text class="detail-text">{{ selected.ingredients }}</text>
        <text class="detail-title">\u6b65\u9aa4</text>
        <text class="detail-text">{{ selected.steps }}</text>
        <text class="close-btn" @click="selected=null">\u5173\u95ed</text>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, computed, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const keyword = ref("")
const selected = ref(null)
const recipes = ref([
  {name:"\u9ec4\u7116\u9e21", desc:"\u5bb6\u5e38\u7f8e\u5473\u9e21\u8089\u83dc", tags:["\u5bb6\u5e38","\u8089\u7c7b"], ingredients:"\u9e21\u8089500\u3001\u571f\u8c462\u4e2a\u3001\u7ea2\u6912\u90e8\u5206", steps:"1.\u5207\u5757\u6d47\u6ce1 2.\u7092\u9ec4\u597d\u5907 3.\u52a0\u6c34\u711630\u5206\u949f"},
  {name:"\u6842\u82b1\u7c73\u7c89", desc:"\u5357\u65b9\u7c73\u7c89\u7c89\u7c89\u9999\u5473", tags:["\u7c73\u7c89","\u5357\u65b9"], ingredients:"\u7c73\u7c89500\u3001\u6842\u82b1\u90e8\u5206\u3001\u7cd6\u90e8\u5206", steps:"1.\u7c73\u7c89\u6d47\u6ce1 2.\u6842\u82b1\u6d47\u6ce1 3.\u5171\u540c\u7092\u5236\u5373\u53ef"},
  {name:"\u8170\u679c\u9ec4\u7116\u9e21", desc:"\u53e4\u5178\u5bb6\u5e38\u53f0\u5f0f\u83dc", tags:["\u53f0\u5f0f","\u8089\u7c7b"], ingredients:"\u8170\u679c2\u4e2a\u3001\u9e21\u8089300\u3001\u8c46\u5e72\u90e8\u5206", steps:"1.\u8170\u679c\u5378\u6839 2.\u9e21\u8089\u7092\u9ec4 3.\u52a0\u6c34\u711620\u5206\u949f"},
  {name:"\u6c99\u62c9", desc:"\u5065\u5eb7\u8f7b\u98df\u6c99\u62c9\u6c99\u62c9", tags:["\u5065\u5eb7","\u8f7b\u98df"], ingredients:"\u756a\u83041\u4e2a\u3001\u9ec4\u74dc1\u6839\u3001\u6c99\u62c9\u9171\u90e8\u5206", steps:"1.\u9e21\u86cb\u7092\u7740 2.\u852c\u83dc\u5207\u5757 3.\u6405\u62cc\u5373\u53ef"}
])
const filteredRecipes = computed(function() {
  if (!keyword.value) return recipes.value
  return recipes.value.filter(function(r){return r.name.includes(keyword.value) || r.tags.some(function(t){return t.includes(keyword.value)})})
})
function search() {}
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
.content { padding: 40rpx; }
.search-bar { display: flex; gap: 16rpx; margin-bottom: 24rpx; }
.search-input { flex: 1; background: #fff; border-radius: 16rpx; padding: 20rpx 24rpx; font-size: 28rpx; }
.search-btn { background: #e84393; color: #fff; border-radius: 16rpx; padding: 20rpx 32rpx; font-size: 28rpx; display: flex; align-items: center; }
.recipe-list { display: flex; flex-direction: column; gap: 16rpx; }
.recipe-card { background: #fff; border-radius: 20rpx; padding: 24rpx; }
.recipe-name { font-size: 30rpx; font-weight: 600; color: #333; display: block; }
.recipe-desc { font-size: 24rpx; color: #999; display: block; margin: 8rpx 0; }
.recipe-tags { display: flex; gap: 8rpx; flex-wrap: wrap; }
.tag { padding: 6rpx 12rpx; background: #fff0f5; border-radius: 8rpx; font-size: 20rpx; color: #e84393; }
.recipe-detail { margin-top: 24rpx; background: #fff; border-radius: 20rpx; padding: 32rpx; }
.detail-name { font-size: 32rpx; font-weight: 700; color: #333; display: block; margin-bottom: 16rpx; }
.detail-title { font-size: 26rpx; font-weight: 600; color: #e84393; display: block; margin: 16rpx 0 8rpx; }
.detail-text { font-size: 24rpx; color: #666; line-height: 1.8; }
.close-btn { display: block; text-align: center; padding: 16rpx; background: #f0f0f0; border-radius: 12rpx; font-size: 26rpx; color: #666; margin-top: 20rpx; }
</style>
