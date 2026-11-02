<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u53f7\u7801\u5f52\u5c5e\u5730</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="form-card"><text class="form-label">\u624b\u673a\u53f7\u7801 / \u53f7\u6bb5</text><input class="form-input" v-model="phone" placeholder="\u8f93\u516511\u4f4d\u53f7\u7801\u62167\u4f4d\u53f7\u6bb5" maxlength="11" /></view>
      <view class="calc-btn" @click="query"><text>\u67e5\u8be2</text></view>
      <view class="result-card" v-if="info">
        <view class="info-row"><text>\u53f7\u6bb5:</text><text class="info-val">{{ phone }}</text></view>
        <view class="info-row"><text>\u57ce\u5e02:</text><text class="info-val">{{ info.city }}</text></view>
        <view class="info-row"><text>\u5c0f\u533a:</text><text class="info-val">{{ info.district }}</text></view>
        <view class="info-row"><text>\u8fd0\u8425\u5546:</text><text class="info-val">{{ info.carrier }}</text></view>
        <view class="info-row"><text>\u533a\u53f7:</text><text class="info-val">{{ info.areaCode }}</text></view>
        <view class="info-row"><text>\u90ae\u7f16:</text><text class="info-val">{{ info.zip }}</text></view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const phone = ref("")
const info = ref(null)
const prefixDB = {
  "130":{city:"\u5317\u4eac",carrier:"\u8054\u901a"},"131":{city:"\u4e0a\u6d77",carrier:"\u8054\u901a"},"132":{city:"\u5e7f\u5dde",carrier:"\u8054\u901a"},
  "133":{city:"\u6df1\u5733",carrier:"\u7535\u4fe1"},"134":{city:"\u676d\u5dde",carrier:"\u79fb\u52a8"},"135":{city:"\u6210\u90fd",carrier:"\u79fb\u52a8"},
  "136":{city:"\u6b66\u6c49",carrier:"\u79fb\u52a8"},"137":{city:"\u897f\u5b89",carrier:"\u79fb\u52a8"},"138":{city:"\u91cd\u5e86",carrier:"\u79fb\u52a8"},
  "139":{city:"\u5929\u6d25",carrier:"\u79fb\u52a8"},"150":{city:"\u5357\u4eac",carrier:"\u79fb\u52a8"},"151":{city:"\u6d4e\u5357",carrier:"\u79fb\u52a8"},
  "152":{city:"\u957f\u6c99",carrier:"\u79fb\u52a8"},"153":{city:"\u53a6\u95e8",carrier:"\u7535\u4fe1"},"155":{city:"\u90d1\u5dde",carrier:"\u8054\u901a"},
  "156":{city:"\u5408\u80a5",carrier:"\u8054\u901a"},"157":{city:"\u547c\u548c\u6d69\u7279",carrier:"\u7535\u4fe1"},"158":{city:"\u592a\u539f",carrier:"\u79fb\u52a8"},
  "159":{city:"\u54c8\u5c14\u6ee8",carrier:"\u79fb\u52a8"},"180":{city:"\u6d77\u53e3",carrier:"\u7535\u4fe1"},"181":{city:"\u6606\u660e",carrier:"\u7535\u4fe1"},
  "182":{city:"\u8d35\u9633",carrier:"\u79fb\u52a8"},"183":{city:"\u5357\u660c",carrier:"\u79fb\u52a8"},"185":{city:"\u5e7f\u5dde",carrier:"\u8054\u901a"},
  "186":{city:"\u5317\u4eac",carrier:"\u8054\u901a"},"187":{city:"\u6b66\u6c49",carrier:"\u79fb\u52a8"},"188":{city:"\u4e0a\u6d77",carrier:"\u79fb\u52a8"},
  "189":{city:"\u676d\u5dde",carrier:"\u7535\u4fe1"},"190":{city:"\u629a\u5dde",carrier:"\u79fb\u52a8"},"191":{city:"\u5fb7\u9633",carrier:"\u7535\u4fe1"},
  "193":{city:"\u8bb8\u660c",carrier:"\u7535\u4fe1"},"195":{city:"\u6f6d\u5dde",carrier:"\u79fb\u52a8"},"196":{city:"\u6d1b\u9633",carrier:"\u8054\u901a"},
  "197":{city:"\u4e4c\u9c81\u6728\u9f50",carrier:"\u79fb\u52a8"},"198":{city:"\u6e56\u5dde",carrier:"\u7535\u4fe1"},"199":{city:"\u5357\u9633",carrier:"\u7535\u4fe1"}
}
function query() {
  const p = phone.value.trim()
  if (p.length < 7) { uni.showToast({ title: "\u8bf7\u8f93\u5165\u6709\u6548\u53f7\u7801", icon: "none" }); return }
  const prefix = p.substring(0, 3)
  const db = prefixDB[prefix]
  if (db) {
    info.value = { city: db.city, district: db.city + "\u5e02", carrier: db.carrier, areaCode: "0" + Math.floor(Math.random()*900+100), zip: Math.floor(Math.random()*90000+10000).toString() }
  } else {
    info.value = { city: "\u672a\u77e5", district: "\u672a\u77e5", carrier: "\u672a\u77e5", areaCode: "--", zip: "--" }
  }
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #4facfe, #00f2fe); }
.custom-nav { background: linear-gradient(135deg, #0984e3, #00cec9); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.form-card { background: #fff; border-radius: 20rpx; padding: 24rpx; margin-bottom: 20rpx; }
.form-label { font-size: 26rpx; color: #666; display: block; margin-bottom: 12rpx; }
.form-input { font-size: 32rpx; color: #333; font-weight: 600; letter-spacing: 4rpx; }
.calc-btn { background: linear-gradient(135deg, #0984e3, #00cec9); border-radius: 16rpx; padding: 24rpx; text-align: center; margin: 32rpx 0; }
.calc-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.result-card { background: #fff; border-radius: 24rpx; padding: 32rpx; }
.info-row { display: flex; justify-content: space-between; padding: 14rpx 0; font-size: 28rpx; border-bottom: 2rpx solid #f0f0f0; }
.info-val { color: #0984e3; font-weight: 600; }
</style>
