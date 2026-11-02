<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u5f85\u529e\u6e05\u5355Pro</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="add-row"><input class="add-input" v-model="newTask" placeholder="\u6dfb\u52a0\u4efb\u52a1" @confirm="addTask" /><text class="add-btn" @click="addTask">+</text></view>
      <view class="filter-tabs"><text class="f-tab" :class="{active: filter==='all'}" @click="filter='all'">\u5168\u90e8</text><text class="f-tab" :class="{active: filter==='active'}" @click="filter='active'">\u672a\u5b8c\u6210</text><text class="f-tab" :class="{active: filter==='done'}" @click="filter='done'">\u5df2\u5b8c\u6210</text></view>
      <view class="task-list">
        <view class="task-item" v-for="(t, i) in filteredTasks" :key="t.id">
          <text class="task-check" @click="toggleTask(t.id)" :class="{checked: t.done}">{{ t.done?'\u2713':'' }}</text>
          <text class="task-text" :class="{done: t.done}">{{ t.text }}</text>
          <text class="task-priority" :class="'p'+t.priority">{{ ['\u4f4e','\u4e2d','\u9ad8'][t.priority] }}</text>
          <text class="task-del" @click="deleteTask(t.id)">\u00d7</text>
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
  {id:1, text:"\u5b8c\u6210\u9879\u76ee\u62a5\u544a", done:false, priority:2},
  {id:2, text:"\u56de\u590d\u90ae\u4ef6", done:false, priority:1},
  {id:3, text:"\u51c6\u5907\u4f1a\u8bae\u6750\u6599", done:true, priority:0}
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
