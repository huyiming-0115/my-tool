<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u5143\u7d20\u5468\u671f\u8868</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="pt-grid">
        <view class="pt-element" v-for="(el, i) in elements" :key="i" :style="{background: groupColors[el.group]}" @click="selected=el">
          <text class="el-num">{{ el.num }}</text>
          <text class="el-symbol">{{ el.symbol }}</text>
          <text class="el-name">{{ el.name }}</text>
        </view>
      </view>
      <view class="el-detail" v-if="selected">
        <text class="ed-symbol">{{ selected.symbol }}</text>
        <text class="ed-name">{{ selected.name }} ({{ selected.num }})</text>
        <text class="ed-weight">\u539f\u5b50\u91cf: {{ selected.weight }}</text>
        <text class="ed-group">\u5206\u7ec4: {{ selected.group }}</text>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const selected = ref(null)
const groupColors = {s:"#ff6b6b",p:"#feca57",d:"#48dbfb",f:"#ff9ff3"}
const elements = [
  {num:1,symbol:"H",name:"\u6c22",weight:"1.008",group:"s"},{num:2,symbol:"He",name:"\u6c26",weight:"4.003",group:"p"},
  {num:3,symbol:"Li",name:"\u9502",weight:"6.941",group:"s"},{num:4,symbol:"Be",name:"\u94cd",weight:"9.012",group:"s"},
  {num:5,symbol:"B",name:"\u787c",weight:"10.81",group:"p"},{num:6,symbol:"C",name:"\u78b3",weight:"12.01",group:"p"},
  {num:7,symbol:"N",name:"\u6c2e",weight:"14.01",group:"p"},{num:8,symbol:"O",name:"\u6c27",weight:"16.00",group:"p"},
  {num:9,symbol:"F",name:"\u6c1f",weight:"19.00",group:"p"},{num:10,symbol:"Ne",name:"\u6c16",weight:"20.18",group:"p"},
  {num:11,symbol:"Na",name:"\u94a0",weight:"22.99",group:"s"},{num:12,symbol:"Mg",name:"\u9541",weight:"24.31",group:"s"},
  {num:13,symbol:"Al",name:"\u94dd",weight:"26.98",group:"p"},{num:14,symbol:"Si",name:"\u7845",weight:"28.09",group:"p"},
  {num:15,symbol:"P",name:"\u78f7",weight:"30.97",group:"p"},{num:16,symbol:"S",name:"\u786b",weight:"32.07",group:"p"},
  {num:17,symbol:"Cl",name:"\u6c0f",weight:"35.45",group:"p"},{num:18,symbol:"Ar",name:"\u6c29",weight:"39.95",group:"p"},
  {num:19,symbol:"K",name:"\u94be",weight:"39.10",group:"s"},{num:20,symbol:"Ca",name:"\u9499",weight:"40.08",group:"s"},
  {num:26,symbol:"Fe",name:"\u94c1",weight:"55.85",group:"d"},{num:29,symbol:"Cu",name:"\u94dc",weight:"63.55",group:"d"},
  {num:30,symbol:"Zn",name:"\u950c",weight:"65.38",group:"d"},{num:47,symbol:"Ag",name:"\u94f6",weight:"107.9",group:"d"},
  {num:79,symbol:"Au",name:"\u91d1",weight:"197.0",group:"d"},{num:82,symbol:"Pb",name:"\u94c5",weight:"207.2",group:"p"}
]
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #89f7fe, #66a6ff); }
.custom-nav { background: linear-gradient(135deg, #0984e3, #74b9ff); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 20rpx; }
.pt-grid { display: grid; grid-template-columns: repeat(6, 1fr); gap: 8rpx; }
.pt-element { border-radius: 12rpx; padding: 12rpx 4rpx; text-align: center; }
.el-num { font-size: 16rpx; color: rgba(255,255,255,0.7); display: block; }
.el-symbol { font-size: 32rpx; color: #fff; font-weight: 700; display: block; }
.el-name { font-size: 18rpx; color: rgba(255,255,255,0.9); display: block; }
.el-detail { margin-top: 20rpx; background: #fff; border-radius: 24rpx; padding: 32rpx; text-align: center; }
.ed-symbol { font-size: 80rpx; font-weight: 900; color: #0984e3; display: block; }
.ed-name { font-size: 32rpx; font-weight: 600; display: block; margin: 8rpx 0; }
.ed-weight, .ed-group { font-size: 26rpx; color: #666; display: block; }
</style>
