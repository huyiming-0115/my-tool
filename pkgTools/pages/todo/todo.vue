<template>
  <view class="todo-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">\u2190</text>
        <text class="nav-title">待办清单</text>
        <text class="nav-icon empty"> </text>
      </view>
    </view>

    <view class="content">
      <view class="stats-row">
        <view class="stat-card">
          <text class="stat-num">{{ totalTasks }}</text>
          <text class="stat-label">全部</text>
        </view>
        <view class="stat-card">
          <text class="stat-num" style="color:#22c55e;">{{ completedTasks }}</text>
          <text class="stat-label">已完成</text>
        </view>
        <view class="stat-card">
          <text class="stat-num" style="color:#f59e0b;">{{ pendingTasks }}</text>
          <text class="stat-label">进行中</text>
        </view>
      </view>

      <view class="input-bar">
        <input class="todo-input" v-model="newTask" placeholder="添加新任务..." @confirm="addTask" />
        <text class="add-btn" @click="addTask">+</text>
      </view>

      <view class="filter-tabs">
        <text class="filter-tab" :class="{ active: filter === 'all' }" @click="filter = 'all'">全部</text>
        <text class="filter-tab" :class="{ active: filter === 'pending' }" @click="filter = 'pending'">未完成</text>
        <text class="filter-tab" :class="{ active: filter === 'done' }" @click="filter = 'done'">已完成</text>
      </view>

      <view class="task-list">
        <view class="task-item" v-for="(task, idx) in filteredTasks" :key="task.id">
          <text class="task-check" @click="toggleTask(task.id)" :class="{ checked: task.done }">{{ task.done ? "\u2713" : "" }}</text>
          <text class="task-text" :class="{ done: task.done }">{{ task.text }}</text>
          <text class="task-del" @click="deleteTask(task.id)">\u00d7</text>
        </view>
      </view>

      <view class="empty" v-if="filteredTasks.length === 0">
        <text class="empty-emoji">📋</text>
        <text class="empty-title">暂无任务</text>
        <text class="empty-desc">{{ filter === 'all' ? '添加第一个任务吧' : (filter === 'done' ? '还没有完成的任务' : '没有待办任务') }}</text>
      </view>

      <view class="clear-bar" v-if="completedTasks > 0">
        <text class="clear-btn" @click="clearCompleted">清除已完成 ({{ completedTasks }})</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from "vue"

const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const tasks = ref([])
const newTask = ref("")
const filter = ref("all")

const totalTasks = computed(() => tasks.value.length)
const completedTasks = computed(() => tasks.value.filter(t => t.done).length)
const pendingTasks = computed(() => tasks.value.filter(t => !t.done).length)

const filteredTasks = computed(() => {
  if (filter.value === "pending") return tasks.value.filter(t => !t.done)
  if (filter.value === "done") return tasks.value.filter(t => t.done)
  return tasks.value
})

function goBack() { uni.navigateBack() }

function addTask() {
  const text = newTask.value.trim()
  if (!text) {
    uni.showToast({ title: "请输入任务内容", icon: "none" })
    return
  }
  tasks.value.unshift({ id: Date.now(), text: text, done: false })
  newTask.value = ""
  saveTasks()
}

function toggleTask(id) {
  const task = tasks.value.find(t => t.id === id)
  if (task) {
    task.done = !task.done
    saveTasks()
  }
}

function deleteTask(id) {
  tasks.value = tasks.value.filter(t => t.id !== id)
  saveTasks()
}

function clearCompleted() {
  uni.showModal({
    title: "清除已完成",
    content: "确定清除所有已完成的任务？",
    success: (res) => {
      if (res.confirm) {
        tasks.value = tasks.value.filter(t => !t.done)
        saveTasks()
      }
    },
  })
}

function saveTasks() {
  uni.setStorageSync("todo_tasks", JSON.stringify(tasks.value))
}

onMounted(() => {
  if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }
  const saved = uni.getStorageSync("todo_tasks")
  if (saved) {
    try { tasks.value = JSON.parse(saved) } catch (e) { tasks.value = [] }
  }
})
</script>

<style lang="scss" scoped>
.todo-page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #84cc16, #22c55e); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.stats-row { display: flex; gap: 16rpx; margin-bottom: 24rpx; }
.stat-card { flex: 1; background: #fff; border-radius: 20rpx; padding: 24rpx; text-align: center; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.stat-num { font-size: 36rpx; font-weight: 700; color: #333; display: block; }
.stat-label { font-size: 22rpx; color: #999; margin-top: 4rpx; display: block; }
.input-bar { display: flex; align-items: center; gap: 16rpx; margin-bottom: 24rpx; }
.todo-input { flex: 1; height: 80rpx; background: #fff; border-radius: 40rpx; padding: 0 28rpx; font-size: 28rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.add-btn { width: 80rpx; height: 80rpx; background: linear-gradient(135deg, #84cc16, #22c55e); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 40rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.filter-tabs { display: flex; gap: 12rpx; margin-bottom: 24rpx; }
.filter-tab { padding: 12rpx 28rpx; background: #fff; border-radius: 30rpx; font-size: 24rpx; color: #666; }
.filter-tab.active { background: linear-gradient(135deg, #84cc16, #22c55e); color: #fff; }
.task-list { background: #fff; border-radius: 24rpx; padding: 8rpx 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.task-item { display: flex; align-items: center; padding: 20rpx 0; border-bottom: 2rpx solid #f9f9f9; }
.task-item:last-child { border-bottom: none; }
.task-check { width: 40rpx; height: 40rpx; border-radius: 50%; border: 2rpx solid #ddd; display: flex; align-items: center; justify-content: center; margin-right: 16rpx; font-size: 22rpx; color: #fff; flex-shrink: 0; }
.task-check.checked { background: #22c55e; border-color: #22c55e; }
.task-text { flex: 1; font-size: 28rpx; color: #333; }
.task-text.done { text-decoration: line-through; color: #999; }
.task-del { width: 48rpx; height: 48rpx; display: flex; align-items: center; justify-content: center; font-size: 32rpx; color: #ccc; }
.empty { text-align: center; padding: 80rpx 40rpx; }
.empty-emoji { font-size: 80rpx; display: block; }
.empty-title { font-size: 28rpx; color: #333; margin-top: 24rpx; display: block; }
.empty-desc { font-size: 24rpx; color: #999; margin-top: 12rpx; display: block; }
.clear-bar { text-align: center; margin-top: 32rpx; }
.clear-btn { font-size: 24rpx; color: #ef4444; padding: 12rpx 32rpx; }
</style>
