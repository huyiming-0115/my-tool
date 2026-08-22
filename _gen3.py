# -*- coding: utf-8 -*-
import os
base = "pkgTools/pages"
def w(name, content):
    with open(os.path.join(base, name, name + ".vue"), "w") as f:
        f.write(content)
    print("OK:", name)

# ===== periodictable =====
w("periodictable", """<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\\u2190</text><text class="nav-title">\\u5143\\u7d20\\u5468\\u671f\\u8868</text><text class="nav-icon empty"> </text></view>
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
        <text class="ed-weight">\\u539f\\u5b50\\u91cf: {{ selected.weight }}</text>
        <text class="ed-group">\\u5206\\u7ec4: {{ selected.group }}</text>
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
  {num:1,symbol:"H",name:"\\u6c22",weight:"1.008",group:"s"},{num:2,symbol:"He",name:"\\u6c26",weight:"4.003",group:"p"},
  {num:3,symbol:"Li",name:"\\u9502",weight:"6.941",group:"s"},{num:4,symbol:"Be",name:"\\u94cd",weight:"9.012",group:"s"},
  {num:5,symbol:"B",name:"\\u787c",weight:"10.81",group:"p"},{num:6,symbol:"C",name:"\\u78b3",weight:"12.01",group:"p"},
  {num:7,symbol:"N",name:"\\u6c2e",weight:"14.01",group:"p"},{num:8,symbol:"O",name:"\\u6c27",weight:"16.00",group:"p"},
  {num:9,symbol:"F",name:"\\u6c1f",weight:"19.00",group:"p"},{num:10,symbol:"Ne",name:"\\u6c16",weight:"20.18",group:"p"},
  {num:11,symbol:"Na",name:"\\u94a0",weight:"22.99",group:"s"},{num:12,symbol:"Mg",name:"\\u9541",weight:"24.31",group:"s"},
  {num:13,symbol:"Al",name:"\\u94dd",weight:"26.98",group:"p"},{num:14,symbol:"Si",name:"\\u7845",weight:"28.09",group:"p"},
  {num:15,symbol:"P",name:"\\u78f7",weight:"30.97",group:"p"},{num:16,symbol:"S",name:"\\u786b",weight:"32.07",group:"p"},
  {num:17,symbol:"Cl",name:"\\u6c0f",weight:"35.45",group:"p"},{num:18,symbol:"Ar",name:"\\u6c29",weight:"39.95",group:"p"},
  {num:19,symbol:"K",name:"\\u94be",weight:"39.10",group:"s"},{num:20,symbol:"Ca",name:"\\u9499",weight:"40.08",group:"s"},
  {num:26,symbol:"Fe",name:"\\u94c1",weight:"55.85",group:"d"},{num:29,symbol:"Cu",name:"\\u94dc",weight:"63.55",group:"d"},
  {num:30,symbol:"Zn",name:"\\u950c",weight:"65.38",group:"d"},{num:47,symbol:"Ag",name:"\\u94f6",weight:"107.9",group:"d"},
  {num:79,symbol:"Au",name:"\\u91d1",weight:"197.0",group:"d"},{num:82,symbol:"Pb",name:"\\u94c5",weight:"207.2",group:"p"}
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
""")

# ===== idiom =====
w("idiom", """<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\\u2190</text><text class="nav-title">\\u6210\\u8bed\\u8bcd\\u5178</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="search-bar"><input class="search-input" v-model="keyword" placeholder="\\u641c\\u7d22\\u6210\\u8bed" @input="search" /><text class="search-btn" @click="search">\\u641c\\u7d22</text></view>
      <view class="idiom-list">
        <view class="idiom-card" v-for="(item, i) in results" :key="i">
          <text class="ic-word">{{ item.word }}</text>
          <text class="ic-pinyin">{{ item.pinyin }}</text>
          <text class="ic-meaning">{{ item.meaning }}</text>
        </view>
      </view>
      <view class="empty" v-if="results.length === 0"><text>\\u6ca1\\u6709\\u627e\\u5230\\u76f8\\u5173\\u6210\\u8bed</text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const keyword = ref("")
const results = ref([])
const idioms = [
  {word:"\\u4e00\\u5c71\\u4e0d\\u5bb9\\u4e8c\\u864e",pinyin:"y\\u012b sh\\u0101n b\\u00f9 r\\u00f3ng \\u00e8r h\\u01d4",meaning:"\\u4e24\\u864e\\u4e0d\\u80fd\\u5171\\u5b58\\uff0c\\u6bd4\\u55bb\\u4e24\\u4e2a\\u5f3a\\u654c\\u4e0d\\u80fd\\u5171\\u5b58"},
  {word:"\\u4e94\\u82b1\\u516b\\u95e8",pinyin:"w\\u01d4 hu\\u0101 b\\u0101 m\\u00e9n",meaning:"\\u5f62\\u5bb9\\u5408\\u79cd\\u591a\\u6837\\uff0c\\u53d1\\u5c55\\u4e0d\\u660e\\u786e"},
  {word:"\\u4eba\\u5c71\\u4eba\\u6d77",pinyin:"r\\u00e9n sh\\u0101n r\\u00e9n h\\u01d0i",meaning:"\\u5f62\\u5bb9\\u4eba\\u6c14\\u96c6\\u4e2d\\uff0c\\u4eba\\u6570\\u6781\\u591a"},
  {word:"\\u5929\\u5730\\u957f\\u4e45",pinyin:"ti\\u0101n d\\u00ec ch\\u00e1ng ji\\u01d4",meaning:"\\u5f62\\u5bb9\\u65f6\\u95f4\\u6781\\u5176\\u4e45\\u8fdc"},
  {word:"\\u4e07\\u53d8\\u4e0d\\u79bb\\u5176\\u5b97",pinyin:"w\\u00e0n bi\\u00e0n b\\u00f9 l\\u00ed q\\u00ed z\\u014dng",meaning:"\\u5f62\\u5bb9\\u867d\\u7136\\u53d8\\u5316\\u5f88\\u5927\\uff0c\\u4f46\\u672c\\u8d28\\u6ca1\\u6709\\u53d8"},
  {word:"\\u4e00\\u5fc3\\u4e00\\u610f",pinyin:"y\\u012b x\\u012bn y\\u012b y\\u00ec",meaning:"\\u5fc3\\u5ff5\\u4e00\\uff0c\\u4e0d\\u5206\\u5fc3"},
  {word:"\\u5343\\u519b\\u4e07\\u9a6c",pinyin:"qi\\u0101n j\\u016bn w\\u00e0n m\\u01d0",meaning:"\\u5f62\\u5bb9\\u884c\\u519b\\u7eb5\\u6a2a\\uff0c\\u58ee\\u89c2\\u6c14\\u52bf"},
  {word:"\\u4e09\\u987e\\u8305\\u5e90",pinyin:"s\\u0101n g\\u00f9 m\\u00e1o l\\u00fa",meaning:"\\u6bd4\\u55bb\\u7740\\u7740\\u5b9d\\u8d1d\\u5730\\u89d2\\u65b9\\u5207"},
  {word:"\\u6795\\u4e2d\\u5e15\\u9999",pinyin:"zh\\u011bn zh\\u014dng p\\u00e0 xi\\u0101ng",meaning:"\\u6bd4\\u55bb\\u5e38\\u5e38\\u60f3\\u5230\\u67d0\\u4e8b\\u800c\\u4e0d\\u5982\\u610f"},
  {word:"\\u9f99\\u98de\\u51e4\\u821e",pinyin:"l\\u00f3ng f\\u0113i f\\u00e8ng w\\u01d4",meaning:"\\u5f62\\u5bb9\\u4e66\\u6cd5\\u7cbe\\u5de7\\uff0c\\u8c61\\u5f81\\u5409\\u7965"}
]
function search() {
  const k = keyword.value.trim()
  if (!k) { results.value = []; return }
  results.value = idioms.filter(function(i){return i.word.includes(k) || i.pinyin.includes(k.toLowerCase())})
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #f6d365, #fda085); }
.custom-nav { background: linear-gradient(135deg, #e17055, #f39c12); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.search-bar { display: flex; gap: 16rpx; margin-bottom: 32rpx; }
.search-input { flex: 1; background: #fff; border-radius: 16rpx; padding: 20rpx 24rpx; font-size: 28rpx; }
.search-btn { background: #e17055; color: #fff; border-radius: 16rpx; padding: 20rpx 32rpx; font-size: 28rpx; display: flex; align-items: center; }
.idiom-list { display: flex; flex-direction: column; gap: 16rpx; }
.idiom-card { background: #fff; border-radius: 20rpx; padding: 24rpx; }
.ic-word { font-size: 36rpx; font-weight: 700; color: #333; display: block; }
.ic-pinyin { font-size: 24rpx; color: #999; display: block; margin: 4rpx 0; }
.ic-meaning { font-size: 26rpx; color: #666; display: block; }
.empty { text-align: center; padding: 60rpx; color: rgba(255,255,255,0.7); }
</style>
""")

# ===== todayinhistory =====
w("todayinhistory", """<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\\u2190</text><text class="nav-title">\\u5386\\u53f2\\u4eca\\u65e5</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <text class="today-date\">{{ todayStr }}</text>
      <view class="event-list">
        <view class="event-card" v-for="(e, i) in events" :key="i">
          <text class="event-year">{{ e.year }}\\u5e74</text>
          <text class="event-text">{{ e.text }}</text>
        </view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const todayStr = ref("")
const events = ref([])
const allEvents = {
  "1/1":[{year:1912,text:"\\u4e2d\\u534e\\u6c11\\u56fd\\u6210\\u7acb"},{year:1979,text:"\\u4e2d\\u7f8e\\u5efa\\u4ea4"}],
  "5/4":[{year:1919,text:"\\u4e94\\u56db\\u8fd0\\u52a8\\u7206\\u53d1"}],
  "7/1":[{year:1921,text:"\\u4e2d\\u56fd\\u5171\\u4ea7\\u515a\\u6210\\u7acb"},{year:1997,text:"\\u9999\\u6e2f\\u56de\\u5f52"}],
  "8/1":[{year:1927,text:"\\u5357\\u660c\\u8d77\\u4e49"}],
  "10/1":[{year:1949,text:"\\u4e2d\\u534e\\u4eba\\u6c11\\u5171\\u548c\\u56fd\\u6210\\u7acb"}],
  "12/26":[{year:1893,text:"\\u6bdb\\u6cfd\\u4e1c\\u8bde\\u8fb0"}]
}
onMounted(function() {
  if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }
  const d = new Date()
  const key = (d.getMonth()+1) + "/" + d.getDate()
  todayStr.value = d.getFullYear() + "\\u5e74" + (d.getMonth()+1) + "\\u6708" + d.getDate() + "\\u65e5"
  events.value = allEvents[key] || [{year:d.getFullYear()-100,text:"\\u8fd9\\u4e00\\u5929\\u4e5f\\u6709\\u5f88\\u591a\\u6545\\u4e8b\\u53d1\\u751f"}]
})
function goBack() { uni.navigateBack() }
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #a18cd1, #fbc2eb); }
.custom-nav { background: linear-gradient(135deg, #6c5ce7, #a29bfe); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.today-date { font-size: 36rpx; font-weight: 700; color: #fff; text-align: center; display: block; margin-bottom: 32rpx; }
.event-list { display: flex; flex-direction: column; gap: 20rpx; }
.event-card { background: #fff; border-radius: 20rpx; padding: 28rpx; display: flex; align-items: center; gap: 24rpx; }
.event-year { font-size: 32rpx; font-weight: 700; color: #6c5ce7; min-width: 120rpx; }
.event-text { font-size: 28rpx; color: #333; flex: 1; }
</style>
""")

# ===== flashcard =====
w("flashcard", """<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\\u2190</text><text class="nav-title">\\u95ea\\u5361\\u8bb0\\u5fc6</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="fc-progress\">{{ current+1 }}/{{ cards.length }}</view>
      <view class="fc-card" @click="flipped=!flipped" v-if="cards.length > 0">
        <view class="fc-inner" :class="{flip: flipped}">
          <text class="fc-front\">{{ cards[current].front }}</text>
          <text class="fc-back\">{{ cards[current].back }}</text>
        </view>
      </view>
      <view class="fc-actions" v-if="cards.length > 0">
        <text class="fc-btn prev" @click="prevCard">\\u25c0 \\u4e0a\\u4e00\\u5f20</text>
        <text class="fc-btn next" @click="nextCard">\\u4e0b\\u4e00\\u5f20 \\u25b6</text>
      </view>
      <view class="fc-add">
        <input class="fc-input" v-model="newFront" placeholder="\\u6b63\\u9762 (\\u95ee\\u9898)" />
        <input class="fc-input" v-model="newBack" placeholder="\\u53cd\\u9762 (\\u7b54\\u6848)" />
        <text class="fc-add-btn" @click="addCard">+ \\u6dfb\\u52a0\\u5361\\u7247</text>
      </view>
      <view class="empty" v-if="cards.length === 0"><text>\\u8fd8\\u6ca1\\u6709\\u5361\\u7247\\uff0c\\u6dfb\\u52a0\\u7b2c\\u4e00\\u5f20\\u5427</text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const cards = ref([{front:"\\u4ec0\\u4e48\\u662fVue3?",back:"\\u6700\\u65b0\\u7248\\u672cVue\\u6846\\u67b6"},{front:"uni-app\\u662f\\u4ec0\\u4e48?",back:"\\u8de8\\u5e73\\u53f0\\u5f00\\u53d1\\u6846\\u67b6"}])
const current = ref(0)
const flipped = ref(false)
const newFront = ref("")
const newBack = ref("")
function nextCard() { if (current.value < cards.value.length-1) { current.value++; flipped.value = false } }
function prevCard() { if (current.value > 0) { current.value--; flipped.value = false } }
function addCard() {
  if (!newFront.value.trim() || !newBack.value.trim()) { uni.showToast({ title: "\\u8bf7\\u586b\\u5199\\u5b8c\\u6574", icon: "none" }); return }
  cards.value.push({front: newFront.value.trim(), back: newBack.value.trim()})
  newFront.value = ""; newBack.value = ""
  uni.showToast({ title: "\\u5df2\\u6dfb\\u52a0", icon: "success" })
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
.fc-progress { text-align: center; font-size: 28rpx; color: rgba(255,255,255,0.8); margin-bottom: 20rpx; }
.fc-card { background: #fff; border-radius: 24rpx; padding: 80rpx 40rpx; text-align: center; min-height: 300rpx; display: flex; align-items: center; justify-content: center; margin-bottom: 32rpx; cursor: pointer; }
.fc-inner { transition: 0.3s; }
.fc-front { font-size: 36rpx; font-weight: 600; color: #333; display: block; }
.fc-back { font-size: 30rpx; color: #0984e3; display: none; }
.fc-inner.flip .fc-front { display: none; }
.fc-inner.flip .fc-back { display: block; }
.fc-actions { display: flex; gap: 16rpx; margin-bottom: 32rpx; }
.fc-btn { flex: 1; text-align: center; padding: 20rpx; border-radius: 16rpx; font-size: 26rpx; }
.fc-btn.prev { background: rgba(255,255,255,0.3); color: #fff; }
.fc-btn.next { background: #fff; color: #0984e3; }
.fc-add { background: rgba(255,255,255,0.2); border-radius: 20rpx; padding: 24rpx; display: flex; flex-direction: column; gap: 12rpx; }
.fc-input { background: #fff; border-radius: 12rpx; padding: 16rpx 20rpx; font-size: 26rpx; }
.fc-add-btn { background: #0984e3; color: #fff; text-align: center; border-radius: 12rpx; padding: 16rpx; font-size: 26rpx; }
.empty { text-align: center; padding: 60rpx; color: rgba(255,255,255,0.7); }
</style>
""")

print("batch3 done")