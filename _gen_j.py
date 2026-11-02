# -*- coding: utf-8 -*-
import os
base = "pkgTools/pages"
def w(name, content):
    with open(os.path.join(base, name, name + ".vue"), "w") as f:
        f.write(content)
    print("OK:", name)

# ===== recipebook =====
w("recipebook", """<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\\u2190</text><text class="nav-title">\\u98df\\u8c31\\u5927\\u5168</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="search-bar"><input class="search-input" v-model="keyword" placeholder="\\u641c\\u7d22\\u98df\\u8c31" /><text class="search-btn" @click="search">\\u641c\\u7d22</text></view>
      <view class="recipe-list">
        <view class="recipe-card" v-for="(r, i) in filteredRecipes" :key="i" @click="selected=r">
          <text class="recipe-name">{{ r.name }}</text>
          <text class="recipe-desc">{{ r.desc }}</text>
          <view class="recipe-tags"><text class="tag" v-for="(t, ti) in r.tags" :key="ti">{{ t }}</text></view>
        </view>
      </view>
      <view class="recipe-detail" v-if="selected">
        <text class="detail-name">{{ selected.name }}</text>
        <text class="detail-title\">\\u98df\\u6750</text>
        <text class="detail-text">{{ selected.ingredients }}</text>
        <text class="detail-title\">\\u6b65\\u9aa4</text>
        <text class="detail-text">{{ selected.steps }}</text>
        <text class="close-btn" @click="selected=null">\\u5173\\u95ed</text>
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
  {name:"\\u9ec4\\u7116\\u9e21", desc:"\\u5bb6\\u5e38\\u7f8e\\u5473\\u9e21\\u8089\\u83dc", tags:["\\u5bb6\\u5e38","\\u8089\\u7c7b"], ingredients:"\\u9e21\\u8089500\\u3001\\u571f\\u8c462\\u4e2a\\u3001\\u7ea2\\u6912\\u90e8\\u5206", steps:"1.\\u5207\\u5757\\u6d47\\u6ce1 2.\\u7092\\u9ec4\\u597d\\u5907 3.\\u52a0\\u6c34\\u711630\\u5206\\u949f"},
  {name:"\\u6842\\u82b1\\u7c73\\u7c89", desc:"\\u5357\\u65b9\\u7c73\\u7c89\\u7c89\\u7c89\\u9999\\u5473", tags:["\\u7c73\\u7c89","\\u5357\\u65b9"], ingredients:"\\u7c73\\u7c89500\\u3001\\u6842\\u82b1\\u90e8\\u5206\\u3001\\u7cd6\\u90e8\\u5206", steps:"1.\\u7c73\\u7c89\\u6d47\\u6ce1 2.\\u6842\\u82b1\\u6d47\\u6ce1 3.\\u5171\\u540c\\u7092\\u5236\\u5373\\u53ef"},
  {name:"\\u8170\\u679c\\u9ec4\\u7116\\u9e21", desc:"\\u53e4\\u5178\\u5bb6\\u5e38\\u53f0\\u5f0f\\u83dc", tags:["\\u53f0\\u5f0f","\\u8089\\u7c7b"], ingredients:"\\u8170\\u679c2\\u4e2a\\u3001\\u9e21\\u8089300\\u3001\\u8c46\\u5e72\\u90e8\\u5206", steps:"1.\\u8170\\u679c\\u5378\\u6839 2.\\u9e21\\u8089\\u7092\\u9ec4 3.\\u52a0\\u6c34\\u711620\\u5206\\u949f"},
  {name:"\\u6c99\\u62c9", desc:"\\u5065\\u5eb7\\u8f7b\\u98df\\u6c99\\u62c9\\u6c99\\u62c9", tags:["\\u5065\\u5eb7","\\u8f7b\\u98df"], ingredients:"\\u756a\\u83041\\u4e2a\\u3001\\u9ec4\\u74dc1\\u6839\\u3001\\u6c99\\u62c9\\u9171\\u90e8\\u5206", steps:"1.\\u9e21\\u86cb\\u7092\\u7740 2.\\u852c\\u83dc\\u5207\\u5757 3.\\u6405\\u62cc\\u5373\\u53ef"}
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
""")

# ===== pomodoropro =====
w("pomodoropro", """<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\\u2190</text><text class="nav-title">\\u756a\\u8304\\u949fPro</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="stats-overview">
        <view class="stat-card"><text class="stat-num\">{{ todayCount }}</text><text class=\"stat-label\">\\u4eca\\u65e5</text></view>
        <view class="stat-card"><text class="stat-num\">{{ weekCount }}</text><text class=\"stat-label\">\\u672c\\u5468</text></view>
        <view class="stat-card"><text class="stat-num\">{{ totalCount }}</text><text class=\"stat-label\">\\u603b\\u8ba1</text></view>
      </view>
      <view class="timer-section">
        <text class="timer-display">{{ displayTime }}</text>
        <text class="timer-status">{{ isBreak ? '\\u4f11\\u606f\\u4e2d' : '\\u4e13\\u6ce8\\u4e2d' }}</text>
        <view class="timer-btns">
          <text class="t-btn start" @click="toggleTimer">{{ running ? '\\u6682\\u505c' : '\\u5f00\\u59cb' }}</text>
          <text class="t-btn reset" @click="resetTimer">\\u91cd\\u7f6e</text>
        </view>
      </view>
      <view class="history-section">
        <text class="hist-title\">\\u6700\\u8fd1\\u8bb0\\u5f55</text>
        <view class="hist-item" v-for="(h, i) in history" :key="i">
          <text>{{ h.time }}</text>
          <text>{{ h.duration }}min</text>
          <text>{{ h.type }}</text>
        </view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, computed, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const todayCount = ref(5)
const weekCount = ref(23)
const totalCount = ref(156)
const totalSec = ref(25 * 60)
const running = ref(false)
const isBreak = ref(false)
let timer = null
const displayTime = computed(function() {
  var m = Math.floor(totalSec.value / 60), s = totalSec.value % 60
  return (m<10?"0":"")+m+":"+(s<10?"0":"")+s
})
const history = ref([
  {time:"10:30", duration:25, type:"\\u5b66\\u4e60"},
  {time:"11:00", duration:25, type:"\\u5de5\\u4f5c"},
  {time:"14:00", duration:25, type:"\\u9605\\u8bfb"},
  {time:"15:30", duration:25, type:"\\u5199\\u4f5c"}
])
function toggleTimer() {
  if (running.value) { clearInterval(timer); running.value = false; return }
  running.value = true
  timer = setInterval(function() {
    if (totalSec.value <= 0) {
      clearInterval(timer); running.value = false; uni.vibrateShort({})
      todayCount.value++; weekCount.value++; totalCount.value++
      isBreak.value = !isBreak.value
      totalSec.value = isBreak.value ? 5*60 : 25*60
    } else totalSec.value--
  }, 1000)
}
function resetTimer() { clearInterval(timer); running.value = false; isBreak.value = false; totalSec.value = 25*60 }
function goBack() { clearInterval(timer); uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #ff6b6b, #ee5a24); }
.custom-nav { background: linear-gradient(135deg, #e17055, #d63031); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.stats-overview { display: flex; gap: 16rpx; margin-bottom: 32rpx; }
.stat-card { flex: 1; background: rgba(255,255,255,0.2); border-radius: 20rpx; padding: 24rpx; text-align: center; }
.stat-num { font-size: 40rpx; font-weight: 700; color: #fff; display: block; }
.stat-label { font-size: 22rpx; color: rgba(255,255,255,0.8); }
.timer-section { background: #fff; border-radius: 24rpx; padding: 40rpx; text-align: center; margin-bottom: 24rpx; }
.timer-display { font-size: 80rpx; font-weight: 200; color: #e17055; display: block; font-family: monospace; }
.timer-status { font-size: 26rpx; color: #999; display: block; margin-bottom: 24rpx; }
.timer-btns { display: flex; gap: 16rpx; justify-content: center; }
.t-btn { padding: 20rpx 40rpx; border-radius: 12rpx; font-size: 26rpx; font-weight: 600; }
.t-btn.start { background: #e17055; color: #fff; }
.t-btn.reset { background: #f0f0f0; color: #666; }
.history-section { background: #fff; border-radius: 20rpx; padding: 24rpx; }
.hist-title { font-size: 26rpx; font-weight: 600; color: #333; display: block; margin-bottom: 16rpx; }
.hist-item { display: flex; justify-content: space-between; padding: 12rpx 0; border-bottom: 2rpx solid #f0f0f0; font-size: 24rpx; color: #666; }
</style>
""")

# ===== habittracker =====
w("habittracker", """<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\\u2190</text><text class="nav-title">\\u4e60\\u60ef\\u8ffd\\u8e2a</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="add-row"><input class="add-input" v-model="newHabit" placeholder="\\u65b0\\u4e60\\u60ef" /><text class="add-btn" @click="addHabit">+</text></view>
      <view class="habit-list">
        <view class="habit-card" v-for="(h, i) in habits" :key="i">
          <view class="habit-info"><text class="habit-name">{{ h.name }}</text><text class="habit-streak\">{{ h.streak }}\\u5929\\u8fde\\u7eed</text></view>
          <view class="habit-days">
            <text class="day-dot" :class="{done: d}" v-for="(d, di) in h.days" :key="di">{{ di+1 }}</text>
          </view>
          <text class="check-btn" @click="checkDay(i)">\\u4eca\\u65e5\\u6253\\u5361</text>
        </view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const newHabit = ref("")
const habits = ref([
  {name:"\\u65e9\\u8d77", streak:15, days:[true,true,true,true,true,true,false]},
  {name:"\\u8bfb\\u4e6630\\u5206\\u949f", streak:8, days:[true,true,false,true,true,false,false]},
  {name:"\\u559d\\u6c348\\u676f", streak:22, days:[true,true,true,true,true,true,true]},
  {name:"\\u8dd1\\u6b653km", streak:5, days:[true,false,true,false,true,false,false]}
])
function addHabit() {
  if (!newHabit.value.trim()) return
  habits.value.push({name: newHabit.value.trim(), streak: 0, days:[false,false,false,false,false,false,false]})
  newHabit.value = ""
}
function checkDay(i) { habits.value[i].days[0] = !habits.value[i].days[0] }
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #84fab0, #8fd3f4); }
.custom-nav { background: linear-gradient(135deg, #00b894, #55efc4); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.add-row { display: flex; gap: 16rpx; margin-bottom: 24rpx; }
.add-input { flex: 1; background: #fff; border-radius: 16rpx; padding: 20rpx 24rpx; font-size: 28rpx; }
.add-btn { background: #00b894; color: #fff; border-radius: 16rpx; width: 80rpx; display: flex; align-items: center; justify-content: center; font-size: 40rpx; font-weight: 700; }
.habit-list { display: flex; flex-direction: column; gap: 16rpx; }
.habit-card { background: #fff; border-radius: 20rpx; padding: 24rpx; }
.habit-info { display: flex; justify-content: space-between; margin-bottom: 16rpx; }
.habit-name { font-size: 28rpx; font-weight: 600; color: #333; }
.habit-streak { font-size: 24rpx; color: #00b894; font-weight: 600; }
.habit-days { display: flex; gap: 8rpx; margin-bottom: 16rpx; }
.day-dot { width: 48rpx; height: 48rpx; border-radius: 50%; background: #f0f0f0; display: flex; align-items: center; justify-content: center; font-size: 20rpx; color: #999; }
.day-dot.done { background: #00b894; color: #fff; }
.check-btn { display: block; text-align: center; padding: 16rpx; background: #f0f0f0; border-radius: 12rpx; font-size: 24rpx; color: #666; }
</style>
""")

# ===== todonotes =====
w("todonotes", """<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\\u2190</text><text class="nav-title">\\u5f85\\u529e\\u6e05\\u5355Pro</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="add-row"><input class="add-input" v-model="newTask" placeholder="\\u6dfb\\u52a0\\u4efb\\u52a1" @confirm="addTask" /><text class="add-btn" @click="addTask">+</text></view>
      <view class="filter-tabs"><text class="f-tab" :class="{active: filter==='all'}" @click="filter='all'\">\\u5168\\u90e8</text><text class="f-tab" :class="{active: filter==='active'}" @click="filter='active'\">\\u672a\\u5b8c\\u6210</text><text class="f-tab" :class="{active: filter==='done'}" @click="filter='done'\">\\u5df2\\u5b8c\\u6210</text></view>
      <view class="task-list">
        <view class="task-item" v-for="(t, i) in filteredTasks" :key="t.id">
          <text class="task-check" @click="toggleTask(t.id)" :class="{checked: t.done}">{{ t.done?'\\u2713':'' }}</text>
          <text class="task-text" :class="{done: t.done}">{{ t.text }}</text>
          <text class="task-priority\" :class=\"'p'+t.priority\">{{ ['\\u4f4e','\\u4e2d','\\u9ad8'][t.priority] }}</text>
          <text class="task-del" @click="deleteTask(t.id)">\\u00d7</text>
        </view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, computed, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const newTask = ref("")
const filter = ref("all")
const tasks = ref([
  {id:1, text:"\\u5b8c\\u6210\\u9879\\u76ee\\u62a5\\u544a", done:false, priority:2},
  {id:2, text:"\\u56de\\u590d\\u90ae\\u4ef6", done:false, priority:1},
  {id:3, text:"\\u51c6\\u5907\\u4f1a\\u8bae\\u6750\\u6599", done:true, priority:0}
])
const filteredTasks = computed(function() {
  if (filter.value === "active") return tasks.value.filter(function(t){return !t.done})
  if (filter.value === "done") return tasks.value.filter(function(t){return t.done})
  return tasks.value
})
function addTask() {
  if (!newTask.value.trim()) return
  tasks.value.unshift({id:Date.now(), text:newTask.value.trim(), done:false, priority:1})
  newTask.value = ""
}
function toggleTask(id) { var t = tasks.value.find(function(t){return t.id===id}); if (t) t.done = !t.done }
function deleteTask(id) { tasks.value = tasks.value.filter(function(t){return t.id!==id}) }
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
.add-row { display: flex; gap: 16rpx; margin-bottom: 20rpx; }
.add-input { flex: 1; background: #fff; border-radius: 16rpx; padding: 20rpx 24rpx; font-size: 28rpx; }
.add-btn { background: #5a67d8; color: #fff; border-radius: 16rpx; width: 80rpx; display: flex; align-items: center; justify-content: center; font-size: 40rpx; font-weight: 700; }
.filter-tabs { display: flex; gap: 12rpx; margin-bottom: 20rpx; }
.f-tab { flex: 1; text-align: center; padding: 16rpx; border-radius: 12rpx; background: rgba(255,255,255,0.2); color: #fff; font-size: 24rpx; }
.f-tab.active { background: #fff; color: #5a67d8; }
.task-list { display: flex; flex-direction: column; gap: 12rpx; }
.task-item { background: #fff; border-radius: 16rpx; padding: 20rpx 24rpx; display: flex; align-items: center; gap: 16rpx; }
.task-check { width: 40rpx; height: 40rpx; border-radius: 50%; border: 2rpx solid #ddd; display: flex; align-items: center; justify-content: center; font-size: 24rpx; color: #fff; }
.task-check.checked { background: #5a67d8; border-color: #5a67d8; }
.task-text { flex: 1; font-size: 26rpx; color: #333; }
.task-text.done { text-decoration: line-through; color: #999; }
.task-priority { font-size: 20rpx; padding: 4rpx 12rpx; border-radius: 8rpx; }
.task-priority.p0 { background: #f0f0f0; color: #999; }
.task-priority.p1 { background: #fff3cd; color: #856404; }
.task-priority.p2 { background: #f8d7da; color: #721c24; }
.task-del { font-size: 32rpx; color: #999; }
</style>
""")

# ===== notepro =====
w("notepro", """<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\\u2190</text><text class="nav-title">\\u7b14\\u8bb0Pro</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="search-row"><input class="search-input" v-model="keyword" placeholder="\\u641c\\u7d22\\u7b14\\u8bb0" /><text class="add-note" @click="createNote">+</text></view>
      <view class="note-list">
        <view class="note-card" v-for="(n, i) in filteredNotes" :key="i" @click="editNote(n)">
          <text class="note-title">{{ n.title }}</text>
          <text class="note-preview">{{ n.content }}</text>
          <view class="note-meta"><text class="note-tag" v-for="(t, ti) in n.tags" :key="ti">{{ t }}</text><text class="note-date">{{ n.date }}</text></view>
        </view>
      </view>
      <view class="editor-card" v-if="editing">
        <input class="editor-title" v-model="editing.title" placeholder="\\u6807\\u9898" />
        <textarea class="editor-content" v-model="editing.content" placeholder="\\u5185\\u5bb9" auto-height></textarea>
        <view class="editor-actions"><text class="e-btn save" @click="saveNote">\\u4fdd\\u5b58</text><text class="e-btn cancel" @click="editing=null">\\u53d6\\u6d88</text></view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, computed, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const keyword = ref("")
const editing = ref(null)
const notes = ref([
  {title:"\\u5de5\\u4f5c\\u8ba1\\u5212", content:"\\u672c\\u5468\\u5b8c\\u6210\\u9879\\u76ee\\u65b9\\u6848", tags:["\\u5de5\\u4f5c"], date:"2024-01-15"},
  {title:"\\u5b66\\u4e60\\u7b14\\u8bb0", content:"Vue3 \\u7ec4\\u4ef6\\u5f00\\u53d1\\u89c4\\u8303", tags:["\\u5b66\\u4e60","\\u6280\\u672f"], date:"2024-01-14"},
  {title:"\\u8d2d\\u7269\\u6e05\\u5355", content:"\\u7535\\u8111\\u3001\\u9f20\\u6807\\u3001\\u952e\\u76d8", tags:["\\u751f\\u6d3b"], date:"2024-01-13"}
])
const filteredNotes = computed(function() {
  if (!keyword.value) return notes.value
  return notes.value.filter(function(n){return n.title.includes(keyword.value) || n.content.includes(keyword.value)})
})
function createNote() { editing.value = {title:"", content:"", tags:[], date:new Date().toLocaleDateString()} }
function editNote(n) { editing.value = Object.assign({}, n) }
function saveNote() {
  if (!editing.value.title) { uni.showToast({ title: "\\u8bf7\\u8f93\\u5165\\u6807\\u9898", icon: "none" }); return }
  var idx = notes.value.findIndex(function(n){return n.title===editing.value.title})
  if (idx >= 0) notes.value[idx] = editing.value
  else notes.value.unshift(editing.value)
  editing.value = null
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #f6d365, #fda085); }
.custom-nav { background: linear-gradient(135deg, #f39c12, #e17055); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.search-row { display: flex; gap: 16rpx; margin-bottom: 24rpx; }
.search-input { flex: 1; background: #fff; border-radius: 16rpx; padding: 20rpx 24rpx; font-size: 28rpx; }
.add-note { background: #f39c12; color: #fff; border-radius: 16rpx; width: 80rpx; display: flex; align-items: center; justify-content: center; font-size: 40rpx; font-weight: 700; }
.note-list { display: flex; flex-direction: column; gap: 16rpx; }
.note-card { background: #fff; border-radius: 20rpx; padding: 24rpx; }
.note-title { font-size: 28rpx; font-weight: 600; color: #333; display: block; }
.note-preview { font-size: 24rpx; color: #666; display: block; margin: 8rpx 0; }
.note-meta { display: flex; gap: 8rpx; align-items: center; }
.note-tag { padding: 4rpx 12rpx; background: #fff3cd; border-radius: 8rpx; font-size: 20rpx; color: #856404; }
.note-date { margin-left: auto; font-size: 20rpx; color: #999; }
.editor-card { background: #fff; border-radius: 20rpx; padding: 24rpx; margin-top: 24rpx; }
.editor-title { font-size: 28rpx; font-weight: 600; color: #333; border-bottom: 2rpx solid #f0f0f0; padding-bottom: 16rpx; margin-bottom: 16rpx; }
.editor-content { width: 100%; min-height: 200rpx; font-size: 26rpx; color: #333; }
.editor-actions { display: flex; gap: 16rpx; margin-top: 16rpx; }
.e-btn { flex: 1; text-align: center; padding: 16rpx; border-radius: 12rpx; font-size: 26rpx; }
.e-btn.save { background: #f39c12; color: #fff; }
.e-btn.cancel { background: #f0f0f0; color: #666; }
</style>
""")

print("batch2 done")