<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u968f\u673a\u6570\u636e\u751f\u6210</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="type-grid">
        <view class="type-card" v-for="(t, i) in types" :key="i" :class="{active: selected===i}" @click="selected=i">
          <text class="type-icon">{{ t.icon }}</text>
          <text class="type-name">{{ t.name }}</text>
        </view>
      </view>
      <view class="form-card"><text class="form-label">\u6570\u91cf: {{ count }}</text><slider :value="count" min="1" max="20" show-value @change="count=Number($event.detail.value)"/></view>
      <view class="calc-btn" @click="generate"><text>\u751f\u6210</text></view>
      <view class="result-card" v-if="results.length > 0">
        <view class="res-item" v-for="(r, i) in results" :key="i">{{ r }}</view>
        <text class="copy-btn" @click="copyAll">\u5168\u90e8\u590d\u5236</text>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const selected = ref(0)
const count = ref(5)
const results = ref([])
const types = [
  { icon: "\u2728", name: "\u59d3\u540d", fn: function() { var f=["\u5f20","\u674e","\u738b","\u8d75","\u5218","\u9648","\u6768","\u9ec4","\u5468","\u5434"]; var m=["\u4f1f","\u82b3","\u5a1f","\u6d01","\u6587","\u5f66","\u5609","\u6668","\u96e8","\u6b23"]; return f[Math.floor(Math.random()*f.length)]+m[Math.floor(Math.random()*m.length)] } },
  { icon: "\u2709", name: "\u90ae\u7bb1", fn: function() { var c="abcdefghijklmnopqrstuvwxyz1234567890"; var s=""; for(var i=0;i<8;i++) s+=c[Math.floor(Math.random()*c.length)]; return s+"@example.com" } },
  { icon: "\u260e", name: "\u624b\u673a\u53f7", fn: function() { var p=["130","131","132","133","134","135","136","137","138","139","150","151","152","153","155","156","157","158","159","180","181","182","183","185","186","187","188","189"]; var s=p[Math.floor(Math.random()*p.length)]; for(var i=0;i<8;i++) s+=Math.floor(Math.random()*10); return s } },
  { icon: "\u2708", name: "\u8eab\u4efd\u8bc1", fn: function() { var s=""; for(var i=0;i<18;i++) s+=Math.floor(Math.random()*10); return s } },
  { icon: "\u2600", name: "\u5730\u5740", fn: function() { var c=["\u5317\u4eac","\u4e0a\u6d77","\u5e7f\u5dde","\u6df1\u5733","\u676d\u5dde","\u6210\u90fd","\u6b66\u6c49","\u897f\u5b89","\u5357\u4eac","\u91cd\u5e86"]; var n=Math.floor(Math.random()*999+1); return c[Math.floor(Math.random()*c.length)]+"\u5e02\u6d77\u6dc0\u533a\u4e2d\u5173\u6751"+n+"\u53f7" } },
  { icon: "\u2615", name: "\u5bc6\u7801", fn: function() { var c="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%"; var s=""; for(var i=0;i<12;i++) s+=c[Math.floor(Math.random()*c.length)]; return s } }
]
function generate() { results.value = []; for (var i = 0; i < count.value; i++) results.value.push(types[selected.value].fn()) }
function copyAll() { uni.setClipboardData({ data: results.value.join("\n"), success: function() { uni.showToast({ title: "\u5df2\u590d\u5236", icon: "success" }) } }) }
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
.type-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16rpx; margin-bottom: 24rpx; }
.type-card { background: rgba(255,255,255,0.2); border-radius: 16rpx; padding: 20rpx; text-align: center; }
.type-card.active { background: #fff; }
.type-icon { font-size: 40rpx; display: block; }
.type-name { font-size: 22rpx; color: #fff; }
.type-card.active .type-name { color: #5a67d8; }
.form-card { background: #fff; border-radius: 20rpx; padding: 24rpx; margin-bottom: 20rpx; }
.form-label { font-size: 26rpx; color: #666; display: block; }
.calc-btn { background: linear-gradient(135deg, #5a67d8, #6b46c1); border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 32rpx; }
.calc-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.result-card { background: #fff; border-radius: 24rpx; padding: 24rpx; }
.res-item { padding: 12rpx 0; border-bottom: 2rpx solid #f0f0f0; font-size: 26rpx; color: #333; font-family: monospace; }
.copy-btn { display: block; background: #5a67d8; color: #fff; text-align: center; border-radius: 12rpx; padding: 16rpx; margin-top: 16rpx; font-size: 26rpx; }
</style>
