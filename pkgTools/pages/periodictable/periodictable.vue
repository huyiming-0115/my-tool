
<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">元素周期表</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="pt-search"><input class="pt-search-input" v-model="searchQuery" placeholder="搜索元素符号或名称" /></view>
      <view class="pt-grid">
        <view class="pt-element" v-for="el in filteredElements" :key="el.z" :style="{background: getCategoryColor(el.cat)}" @click="selectElement(el)">
          <text class="pt-z">{{el.z}}</text>
          <text class="pt-symbol">{{el.sym}}</text>
          <text class="pt-name">{{el.name}}</text>
        </view>
      </view>
      <view class="pt-detail" v-if="selected">
        <view class="pt-detail-header" :style="{background: getCategoryColor(selected.cat)}">
          <text class="pt-detail-z">{{selected.z}}</text>
          <text class="pt-detail-symbol">{{selected.sym}}</text>
        </view>
        <view class="pt-detail-body">
          <text class="pt-detail-name">{{selected.name}} ({{selected.en}})</text>
          <view class="pt-detail-row"><text>原子量</text><text>{{selected.mass}}</text></view>
          <view class="pt-detail-row"><text>类别</text><text>{{selected.cat}}</text></view>
          <view class="pt-detail-row"><text>电子排布</text><text>{{selected.config}}</text></view>
        </view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, computed, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const searchQuery = ref("")
const selected = ref(null)
const elements = [
  {z:1,sym:"H",name:"氢",en:"Hydrogen",mass:"1.008",cat:"非金属",config:"1s¹"},{z:2,sym:"He",name:"氦",en:"Helium",mass:"4.003",cat:"稀有气体",config:"1s²"},
  {z:3,sym:"Li",name:"锂",en:"Lithium",mass:"6.941",cat:"碱金属",config:"[He]2s¹"},{z:4,sym:"Be",name:"铍",en:"Beryllium",mass:"9.012",cat:"碱土金属",config:"[He]2s²"},
  {z:5,sym:"B",name:"硼",en:"Boron",mass:"10.81",cat:"类金属",config:"[He]2s²2p¹"},{z:6,sym:"C",name:"碳",en:"Carbon",mass:"12.01",cat:"非金属",config:"[He]2s²2p²"},
  {z:7,sym:"N",name:"氮",en:"Nitrogen",mass:"14.01",cat:"非金属",config:"[He]2s²2p³"},{z:8,sym:"O",name:"氧",en:"Oxygen",mass:"16.00",cat:"非金属",config:"[He]2s²2p⁴"},
  {z:9,sym:"F",name:"氟",en:"Fluorine",mass:"19.00",cat:"卤素",config:"[He]2s²2p⁵"},{z:10,sym:"Ne",name:"氖",en:"Neon",mass:"20.18",cat:"稀有气体",config:"[He]2s²2p⁶"},
  {z:11,sym:"Na",name:"钠",en:"Sodium",mass:"22.99",cat:"碱金属",config:"[Ne]3s¹"},{z:12,sym:"Mg",name:"镁",en:"Magnesium",mass:"24.31",cat:"碱土金属",config:"[Ne]3s²"},
  {z:13,sym:"Al",name:"铝",en:"Aluminum",mass:"26.98",cat:"贫金属",config:"[Ne]3s²3p¹"},{z:14,sym:"Si",name:"硅",en:"Silicon",mass:"28.09",cat:"类金属",config:"[Ne]3s²3p²"},
  {z:15,sym:"P",name:"磷",en:"Phosphorus",mass:"30.97",cat:"非金属",config:"[Ne]3s²3p³"},{z:16,sym:"S",name:"硫",en:"Sulfur",mass:"32.07",cat:"非金属",config:"[Ne]3s²3p⁴"},
  {z:17,sym:"Cl",name:"氯",en:"Chlorine",mass:"35.45",cat:"卤素",config:"[Ne]3s²3p⁵"},{z:18,sym:"Ar",name:"氩",en:"Argon",mass:"39.95",cat:"稀有气体",config:"[Ne]3s²3p⁶"},
  {z:19,sym:"K",name:"钾",en:"Potassium",mass:"39.10",cat:"碱金属",config:"[Ar]4s¹"},{z:20,sym:"Ca",name:"钙",en:"Calcium",mass:"40.08",cat:"碱土金属",config:"[Ar]4s²"},
  {z:26,sym:"Fe",name:"铁",en:"Iron",mass:"55.85",cat:"过渡金属",config:"[Ar]3d⁶4s²"},{z:29,sym:"Cu",name:"铜",en:"Copper",mass:"63.55",cat:"过渡金属",config:"[Ar]3d¹⁰4s¹"},
  {z:30,sym:"Zn",name:"锌",en:"Zinc",mass:"65.38",cat:"过渡金属",config:"[Ar]3d¹⁰4s²"},{z:47,sym:"Ag",name:"银",en:"Silver",mass:"107.87",cat:"过渡金属",config:"[Kr]4d¹⁰5s¹"},
  {z:79,sym:"Au",name:"金",en:"Gold",mass:"196.97",cat:"过渡金属",config:"[Xe]4f¹⁴5d¹⁰6s¹"},{z:82,sym:"Pb",name:"铅",en:"Lead",mass:"207.2",cat:"贫金属",config:"[Xe]4f¹⁴5d¹⁰6s²6p²"},
  {z:92,sym:"U",name:"铀",en:"Uranium",mass:"238.03",cat:"锕系元素",config:"[Rn]5f³6d¹7s²"}
]
const categoryColors = {
  "碱金属":"#ff6b6b","碱土金属":"#ffa94d","过渡金属":"#ffd43b","贫金属":"#69db7c",
  "类金属":"#4dabf7","非金属":"#74c0fc","卤素":"#9775fa","稀有气体":"#f783ac",
  "锕系元素":"#e599f7"
}
const filteredElements = computed(function() {
  if (!searchQuery.value) return elements
  var q = searchQuery.value.toLowerCase()
  return elements.filter(function(e) {
    return e.sym.toLowerCase().indexOf(q) >= 0 || e.name.indexOf(q) >= 0 || e.z.toString() === q
  })
})
function getCategoryColor(cat) { return categoryColors[cat] || "#868e96" }
function selectElement(el) { selected.value = el }
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #a18cd1, #fbc2eb); }
.custom-nav { background: linear-gradient(135deg, #a18cd1, #fbc2eb); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.pt-search { margin-bottom: 20rpx; }
.pt-search-input { background: rgba(255,255,255,0.3); border-radius: 16rpx; padding: 16rpx 24rpx; font-size: 28rpx; color: #fff; }
.pt-grid { display: grid; grid-template-columns: repeat(6, 1fr); gap: 8rpx; }
.pt-element { border-radius: 8rpx; padding: 8rpx 4rpx; text-align: center; }
.pt-z { color: rgba(255,255,255,0.6); font-size: 16rpx; display: block; }
.pt-symbol { color: #fff; font-size: 28rpx; font-weight: 700; display: block; }
.pt-name { color: rgba(255,255,255,0.8); font-size: 16rpx; display: block; }
.pt-detail { margin-top: 24rpx; background: rgba(255,255,255,0.2); border-radius: 20rpx; overflow: hidden; }
.pt-detail-header { padding: 24rpx; text-align: center; }
.pt-detail-z { color: rgba(255,255,255,0.7); font-size: 24rpx; display: block; }
.pt-detail-symbol { color: #fff; font-size: 60rpx; font-weight: 700; display: block; }
.pt-detail-body { padding: 24rpx; }
.pt-detail-name { color: #fff; font-size: 30rpx; font-weight: 600; display: block; margin-bottom: 16rpx; }
.pt-detail-row { display: flex; justify-content: space-between; padding: 8rpx 0; }
.pt-detail-row text { color: rgba(255,255,255,0.8); font-size: 26rpx; }
</style>
