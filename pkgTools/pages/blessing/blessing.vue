<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u8282\u65e5\u795d\u798f</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="form-card"><text class="form-label">\u5bf9\u65b9\u59d3\u540d</text><input class="form-input" v-model="name" placeholder="\u8f93\u5165\u59d3\u540d" /></view>
      <view class="form-card"><text class="form-label">\u8282\u65e5</text><view class="festival-row"><text class="fest-btn" :class="{active: festival==='\u6625\u8282'}" @click="festival='\u6625\u8282'">\u6625\u8282</text><text class="fest-btn" :class="{active: festival==='\u751f\u65e5'}" @click="festival='\u751f\u65e5'">\u751f\u65e5</text><text class="fest-btn" :class="{active: festival==='\u6625\u8054'}" @click="festival='\u6625\u8054'">\u6625\u8054</text><text class="fest-btn" :class="{active: festival==='\u611f\u6069'}" @click="festival='\u611f\u6069'">\u611f\u6069</text><text class="fest-btn" :class="{active: festival==='\u7ed3\u5a5a'}" @click="festival='\u7ed3\u5a5a'">\u7ed3\u5a5a</text></view></view>
      <view class="gen-btn" @click="generate"><text>\u751f\u6210\u795d\u798f</text></view>
      <view class="result-card" v-if="blessing">
        <text class="blessing-text">{{ blessing }}</text>
        <text class="copy-btn" @click="copyText">\u590d\u5236\u795d\u798f</text>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const name = ref("")
const festival = ref("\u6625\u8282")
const blessing = ref("")
const blessings = {
  "\u6625\u8282": ["\u65b0\u5e74\u5feb\u4e50\uff0c{name}\uff0c\u795d\u4f60\u65b0\u7684\u4e00\u5e74\u5e73\u5b89\u559c\u4e50\uff0c\u4e07\u4e8b\u5982\u610f\uff01","\u6625\u8282\u5230\uff0c{name}\uff0c\u795d\u4f60\u5e74\u5e74\u6709\u4eca\u65e5\uff0c\u6708\u6708\u6709\u4eca\u665a\uff01","\u795d{name}\u65b0\u5e74\u5feb\u4e50\uff0c\u5409\u7965\u5982\u610f\uff0c\u5e78\u798f\u5168\u7f51\uff01"],
  "\u751f\u65e5": ["{name}\uff0c\u751f\u65e5\u5feb\u4e50\uff01\u795d\u4f60\u6bcf\u5929\u90fd\u8fd9\u4e48\u5f00\u5fc3\uff01","\u795d{name}\u751f\u65e5\u5feb\u4e50\uff0c\u5e78\u798f\u5065\u5eb7\uff0c\u4e07\u4e8b\u987a\u5fc3\uff01","{name}\uff0c\u751f\u65e5\u5feb\u4e50\uff01\u613f\u4f60\u7684\u6bcf\u4e00\u5929\u90fd\u5145\u6ee1\u9633\u5149\uff01"],
  "\u6625\u8054": ["\u795d{name}\u6625\u8054\u5feb\u4e50\uff0c\u5409\u7965\u5982\u610f\uff0c\u5e73\u5b89\u559c\u4e50\uff01","{name}\uff0c\u6625\u8282\u5feb\u4e50\uff0c\u795d\u4f60\u5409\u661f\u9ad8\u7167\uff0c\u5e78\u798f\u7f8e\u6ee1\uff01"],
  "\u611f\u6069": ["{name}\uff0c\u611f\u6069\u6709\u4f60\uff0c\u795d\u4f60\u5e78\u798f\u5065\u5eb7\uff01","\u795d{name}\u611f\u6069\u8282\u5feb\u4e50\uff0c\u611f\u6069\u751f\u6d3b\u4e2d\u7684\u6bcf\u4e00\u4efd\u7f8e\u597d\uff01"],
  "\u7ed3\u5a5a": ["\u795d{name}\u65b0\u5a5a\u5feb\u4e50\uff0c\u767d\u5934\u5055\u8001\uff0c\u559c\u7ed3\u8f89\u5e74\uff01","{name}\uff0c\u795d\u4f60\u4eec\u559c\u7ed3\u8f89\u5e74\uff0c\u5e73\u5b89\u559c\u4e50\uff01"]
}
function generate() {
  var n = name.value || "\u670b\u53cb"
  var arr = blessings[festival.value]
  blessing.value = arr[Math.floor(Math.random()*arr.length)].replace("{name}", n)
}
function copyText() { uni.setClipboardData({ data: blessing.value, success: function() { uni.showToast({ title: "\u5df2\u590d\u5236", icon: "success" }) } }) }
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
.festival-row { display: flex; gap: 12rpx; flex-wrap: wrap; }
.fest-btn { padding: 12rpx 24rpx; border-radius: 12rpx; background: #f0f0f0; font-size: 24rpx; color: #666; }
.fest-btn.active { background: #e84393; color: #fff; }
.gen-btn { background: linear-gradient(135deg, #e84393, #fd79a8); border-radius: 16rpx; padding: 24rpx; text-align: center; margin: 32rpx 0; }
.gen-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.result-card { background: #fff; border-radius: 24rpx; padding: 32rpx; text-align: center; }
.blessing-text { font-size: 30rpx; color: #333; line-height: 1.8; display: block; margin-bottom: 20rpx; }
.copy-btn { display: inline-block; padding: 16rpx 32rpx; background: #e84393; color: #fff; border-radius: 12rpx; font-size: 26rpx; }
</style>
