<template>
  <view class="workout-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">\u2190</text>
        <text class="nav-title">训练计划</text>
        <text class="nav-icon" @click="openCreatePlan">+</text>
      </view>
    </view>

    <view class="content">
      <!-- 今日概览 -->
      <view class="today-card">
        <text class="today-date">{{ todayStr }}</text>
        <view class="today-stats">
          <view class="today-stat">
            <text class="ts-num">{{ todayWorkouts.length }}</text>
            <text class="ts-label">今日训练</text>
          </view>
          <view class="today-stat">
            <text class="ts-num">{{ todayDuration }}</text>
            <text class="ts-label">分钟</text>
          </view>
          <view class="today-stat">
            <text class="ts-num">{{ weeklyCount }}</text>
            <text class="ts-label">本周训练</text>
          </view>
        </view>
      </view>

      <!-- 训练计划列表 -->
      <view class="section-title">我的计划</view>
      <view class="plan-card" v-for="(plan, pIdx) in plans" :key="plan.id">
        <view class="plan-header">
          <text class="plan-name">{{ plan.name }}</text>
          <text class="plan-freq">{{ plan.frequency }}</text>
        </view>
        <view class="plan-exercises">
          <view class="exercise-tag" v-for="(ex, eIdx) in plan.exercises" :key="eIdx">
            <text>{{ ex }}</text>
          </view>
        </view>
        <view class="plan-actions">
          <text class="plan-btn" @click="startWorkout(pIdx)">开始训练</text>
          <text class="plan-btn danger" @click="deletePlan(pIdx)">删除</text>
        </view>
      </view>

      <!-- 今日训练记录 -->
      <view class="section-title">今日记录</view>
      <view class="record-card" v-for="(record, rIdx) in todayWorkouts" :key="rIdx">
        <view class="record-row1">
          <text class="record-name">{{ record.planName }}</text>
          <text class="record-duration">{{ record.duration }}分钟</text>
        </view>
        <text class="record-detail">{{ record.detail }}</text>
        <text class="record-time">{{ record.time }}</text>
      </view>
      <view class="empty-mini" v-if="todayWorkouts.length === 0">
        <text>今天还没有训练记录</text>
      </view>

      <!-- 历史记录 -->
      <view class="section-title">历史记录</view>
      <view class="history-item" v-for="(item, idx) in history" :key="idx">
        <text class="history-date">{{ item.date }}</text>
        <text class="history-plan">{{ item.planName }}</text>
        <text class="history-duration">{{ item.duration }}分钟</text>
      </view>
      <view class="empty-mini" v-if="history.length === 0">
        <text>暂无历史记录</text>
      </view>
    </view>

    <!-- 创建计划弹窗 -->
    <view v-if="showCreate" class="mask" @click="showCreate = false">
      <view class="create-panel" @click.stop>
        <view class="panel-head">
          <text class="panel-title">新建计划</text>
          <text class="panel-close" @click="showCreate = false">\u00d7</text>
        </view>
        <view class="panel-body">
          <view class="form-row">
            <text class="form-l">计划名称</text>
            <input class="form-input" v-model="newPlan.name" placeholder="如：胸肌训练" />
          </view>
          <view class="form-row">
            <text class="form-l">频率</text>
            <picker class="form-picker" :value="newPlanFreqIdx" :range="frequencies" @change="onFreqChange">
              <text>{{ frequencies[newPlanFreqIdx] }}</text>
            </picker>
          </view>
          <view class="form-row column">
            <text class="form-l">动作列表</text>
            <view class="ex-input-row">
              <input class="ex-input" v-model="exerciseInput" placeholder="输入动作名" @confirm="addExercise" />
              <text class="ex-add" @click="addExercise">+</text>
            </view>
            <view class="ex-list">
              <text class="ex-tag" v-for="(ex, idx) in newPlan.exercises" :key="idx" @click="removeExercise(idx)">
                {{ ex }} \u00d7
              </text>
            </view>
          </view>
          <view class="form-row column">
            <text class="form-l">快速模板</text>
            <view class="tpl-list">
              <view class="tpl-item" v-for="(tpl, idx) in workoutTemplates" :key="idx" @click="useWorkoutTemplate(tpl)">
                <text class="tpl-name">{{ tpl.name }}</text>
                <text class="tpl-meta">{{ tpl.exercises.length }} 个动作</text>
              </view>
            </view>
          </view>
        </view>
        <view class="panel-footer">
          <button class="btn-cancel" @click="showCreate = false">取消</button>
          <button class="btn-save" @click="createPlan">创建</button>
        </view>
      </view>
    </view>

    <!-- 开始训练弹窗 -->
    <view v-if="showWorkout" class="mask" @click="showWorkout = false">
      <view class="create-panel" @click.stop>
        <view class="panel-head">
          <text class="panel-title">{{ currentWorkoutPlan.name }}</text>
          <text class="panel-close" @click="showWorkout = false">\u00d7</text>
        </view>
        <view class="panel-body">
          <view class="timer-display">
            <text class="timer-text">{{ formatTime(workoutTimer) }}</text>
          </view>
          <view class="workout-ex-list">
            <view class="workout-ex" v-for="(ex, idx) in currentWorkoutPlan.exercises" :key="idx">
              <text class="workout-ex-name">{{ ex }}</text>
              <text class="workout-ex-check" @click="toggleExerciseDone(idx)" :class="{ done: currentWorkoutExDone[idx] }">
                {{ currentWorkoutExDone[idx] ? "\u2713" : "" }}
              </text>
            </view>
          </view>
        </view>
        <view class="panel-footer">
          <button class="btn-cancel" @click="cancelWorkout">取消</button>
          <button class="btn-save" @click="finishWorkout">完成训练</button>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue"

const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const plans = ref([])
const records = ref([])
const showCreate = ref(false)
const showWorkout = ref(false)
const newPlan = ref({ name: "", frequency: "每周3次", exercises: [] })
const newPlanFreqIdx = ref(0)
const frequencies = ["每周1次", "每周2次", "每周3次", "每周4次", "每周5次", "每周6次", "每天"]
const exerciseInput = ref("")
const currentWorkoutPlan = ref({ name: "", exercises: [] })
const currentWorkoutExDone = ref([])
const workoutTimer = ref(0)
let timerInterval = null

const workoutTemplates = [
  { name: "胸肌+三头", exercises: ["卧推", "上斜哑铃推举", "龙门架夹胸", "绳索下压", "仰卧臂屈伸"] },
  { name: "背部+二头", exercises: ["引体向上", "杠铃划船", "高位下拉", "哑铃弯举", "锤式弯举"] },
  { name: "腿部训练", exercises: ["深蹲", "腿举", "腿弯举", "腿屈伸", "提踵"] },
  { name: "肩部训练", exercises: ["哑铃推举", "侧平举", "前平举", "俯身飞鸟", "面拉"] },
  { name: "全身训练", exercises: ["深蹲", "卧推", "硬拉", "引体向上", "推举"] },
]

const todayStr = computed(() => {
  const d = new Date()
  return (d.getMonth() + 1) + "月" + d.getDate() + "日 " + ["周日", "周一", "周二", "周三", "周四", "周五", "周六"][d.getDay()]
})

const todayWorkouts = computed(() => {
  const today = new Date().toISOString().slice(0, 10)
  return records.value.filter(r => r.date === today)
})

const todayDuration = computed(() => {
  return todayWorkouts.value.reduce((sum, r) => sum + r.duration, 0)
})

const weeklyCount = computed(() => {
  const now = new Date()
  const startOfWeek = new Date(now)
  startOfWeek.setDate(now.getDate() - now.getDay())
  startOfWeek.setHours(0, 0, 0, 0)
  return records.value.filter(r => new Date(r.date) >= startOfWeek).length
})

const history = computed(() => {
  return records.value.filter(r => r.date !== new Date().toISOString().slice(0, 10)).slice(0, 20)
})

function goBack() {
  if (showWorkout.value) { cancelWorkout(); return }
  uni.navigateBack()
}

function openCreatePlan() {
  newPlan.value = { name: "", frequency: "每周3次", exercises: [] }
  newPlanFreqIdx.value = 2
  exerciseInput.value = ""
  showCreate.value = true
}

function onFreqChange(e) {
  newPlanFreqIdx.value = e.detail.value
  newPlan.value.frequency = frequencies[e.detail.value]
}

function addExercise() {
  const name = exerciseInput.value.trim()
  if (name) {
    newPlan.value.exercises.push(name)
    exerciseInput.value = ""
  }
}

function removeExercise(idx) {
  newPlan.value.exercises.splice(idx, 1)
}

function useWorkoutTemplate(tpl) {
  newPlan.value.name = tpl.name
  newPlan.value.exercises = [...tpl.exercises]
}

function createPlan() {
  if (!newPlan.value.name.trim()) {
    uni.showToast({ title: "请输入计划名称", icon: "none" })
    return
  }
  if (newPlan.value.exercises.length === 0) {
    uni.showToast({ title: "请至少添加一个动作", icon: "none" })
    return
  }
  plans.value.push({
    id: Date.now(),
    name: newPlan.value.name,
    frequency: newPlan.value.frequency,
    exercises: [...newPlan.value.exercises],
  })
  saveData()
  showCreate.value = false
}

function deletePlan(idx) {
  uni.showModal({
    title: "删除计划",
    content: "确定删除此计划？",
    success: (res) => {
      if (res.confirm) { plans.value.splice(idx, 1); saveData() }
    },
  })
}

function startWorkout(idx) {
  currentWorkoutPlan.value = plans.value[idx]
  currentWorkoutExDone.value = plans.value[idx].exercises.map(() => false)
  workoutTimer.value = 0
  showWorkout.value = true
  timerInterval = setInterval(() => { workoutTimer.value++ }, 1000)
}

function toggleExerciseDone(idx) {
  currentWorkoutExDone.value[idx] = !currentWorkoutExDone.value[idx]
}

function cancelWorkout() {
  clearInterval(timerInterval)
  showWorkout.value = false
}

function finishWorkout() {
  clearInterval(timerInterval)
  const duration = Math.max(1, Math.round(workoutTimer.value / 60))
  const doneCount = currentWorkoutExDone.value.filter(Boolean).length
  const totalEx = currentWorkoutPlan.value.exercises.length
  const today = new Date().toISOString().slice(0, 10)
  const now = new Date()
  records.value.unshift({
    date: today,
    planName: currentWorkoutPlan.value.name,
    duration: duration,
    detail: "完成 " + doneCount + "/" + totalEx + " 个动作",
    time: now.getHours() + ":" + String(now.getMinutes()).padStart(2, "0"),
  })
  saveData()
  showWorkout.value = false
  uni.showToast({ title: "训练完成！辛苦了", icon: "success" })
}

function formatTime(seconds) {
  const m = Math.floor(seconds / 60)
  const s = seconds % 60
  return String(m).padStart(2, "0") + ":" + String(s).padStart(2, "0")
}

function saveData() {
  uni.setStorageSync("workout_plans", JSON.stringify(plans.value))
  uni.setStorageSync("workout_records", JSON.stringify(records.value))
}

onUnmounted(() => { clearInterval(timerInterval) })

onMounted(() => {
  if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }
  const savedPlans = uni.getStorageSync("workout_plans")
  if (savedPlans) { try { plans.value = JSON.parse(savedPlans) } catch (e) {} }
  const savedRecords = uni.getStorageSync("workout_records")
  if (savedRecords) { try { records.value = JSON.parse(savedRecords) } catch (e) {} }
})
</script>

<style lang="scss" scoped>
.workout-page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #ef4444, #dc2626); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.today-card { background: linear-gradient(135deg, #ef4444, #dc2626); border-radius: 24rpx; padding: 32rpx; margin-bottom: 24rpx; }
.today-date { font-size: 26rpx; color: rgba(255,255,255,0.8); display: block; }
.today-stats { display: flex; justify-content: space-around; margin-top: 24rpx; }
.today-stat { text-align: center; }
.ts-num { font-size: 40rpx; color: #fff; font-weight: 700; display: block; }
.ts-label { font-size: 22rpx; color: rgba(255,255,255,0.7); margin-top: 4rpx; display: block; }
.section-title { font-size: 28rpx; font-weight: 600; color: #333; margin: 24rpx 0 16rpx; }
.plan-card { background: #fff; border-radius: 24rpx; padding: 28rpx; margin-bottom: 16rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.plan-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16rpx; }
.plan-name { font-size: 28rpx; font-weight: 600; color: #333; }
.plan-freq { font-size: 22rpx; color: #ef4444; background: #fef2f2; padding: 4rpx 16rpx; border-radius: 20rpx; }
.plan-exercises { display: flex; flex-wrap: wrap; gap: 8rpx; margin-bottom: 16rpx; }
.exercise-tag { font-size: 22rpx; color: #666; background: #f5f5f5; padding: 6rpx 16rpx; border-radius: 20rpx; }
.plan-actions { display: flex; gap: 24rpx; }
.plan-btn { font-size: 24rpx; color: #ef4444; }
.plan-btn.danger { color: #999; }
.record-card { background: #fff; border-radius: 20rpx; padding: 24rpx; margin-bottom: 12rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.record-row1 { display: flex; justify-content: space-between; align-items: center; }
.record-name { font-size: 26rpx; font-weight: 600; color: #333; }
.record-duration { font-size: 24rpx; color: #ef4444; font-weight: 600; }
.record-detail { font-size: 22rpx; color: #666; margin-top: 8rpx; display: block; }
.record-time { font-size: 20rpx; color: #999; margin-top: 4rpx; display: block; }
.history-item { display: flex; justify-content: space-between; align-items: center; padding: 16rpx 0; border-bottom: 2rpx solid #f9f9f9; }
.history-date { font-size: 24rpx; color: #999; width: 140rpx; }
.history-plan { flex: 1; font-size: 24rpx; color: #333; }
.history-duration { font-size: 24rpx; color: #ef4444; }
.empty-mini { text-align: center; padding: 32rpx; font-size: 24rpx; color: #999; }
.mask { position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 999; display: flex; align-items: flex-end; }
.create-panel { width: 100%; background: #fff; border-radius: 32rpx 32rpx 0 0; max-height: 80vh; display: flex; flex-direction: column; }
.panel-head { display: flex; justify-content: space-between; align-items: center; padding: 28rpx 32rpx; border-bottom: 2rpx solid #f0f0f0; }
.panel-title { font-size: 30rpx; font-weight: 600; color: #1a1a1a; }
.panel-close { font-size: 40rpx; color: #999; padding: 4rpx 8rpx; }
.panel-body { flex: 1; padding: 12rpx 32rpx; overflow-y: auto; }
.form-row { display: flex; align-items: center; padding: 20rpx 0; border-bottom: 2rpx solid #f8f8f8; }
.form-row.column { flex-direction: column; align-items: flex-start; gap: 12rpx; }
.form-l { font-size: 26rpx; color: #333; width: 140rpx; flex-shrink: 0; font-weight: 500; }
.form-input { flex: 1; font-size: 28rpx; color: #333; height: 56rpx; }
.form-picker { flex: 1; height: 56rpx; line-height: 56rpx; font-size: 26rpx; }
.ex-input-row { display: flex; align-items: center; gap: 12rpx; width: 100%; }
.ex-input { flex: 1; height: 64rpx; border: 2rpx solid #e5e7eb; border-radius: 12rpx; padding: 0 16rpx; font-size: 26rpx; }
.ex-add { width: 64rpx; height: 64rpx; background: #ef4444; color: #fff; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 32rpx; }
.ex-list { display: flex; flex-wrap: wrap; gap: 8rpx; }
.ex-tag { font-size: 22rpx; color: #ef4444; background: #fef2f2; padding: 6rpx 16rpx; border-radius: 20rpx; }
.tpl-list { display: flex; flex-direction: column; gap: 12rpx; width: 100%; }
.tpl-item { padding: 16rpx 20rpx; background: #f8f9ff; border-radius: 12rpx; display: flex; justify-content: space-between; align-items: center; }
.tpl-name { font-size: 26rpx; color: #333; font-weight: 500; }
.tpl-meta { font-size: 22rpx; color: #999; }
.panel-footer { display: flex; gap: 24rpx; padding: 24rpx 32rpx; border-top: 2rpx solid #f0f0f0; }
.btn-cancel { flex: 1; height: 80rpx; line-height: 80rpx; border-radius: 40rpx; background: #f5f5f5; color: #666; font-size: 28rpx; border: none; }
.btn-cancel::after { border: none; }
.btn-save { flex: 1; height: 80rpx; line-height: 80rpx; border-radius: 40rpx; background: linear-gradient(135deg, #ef4444, #dc2626); color: #fff; font-size: 28rpx; font-weight: 600; border: none; }
.btn-save::after { border: none; }
.timer-display { text-align: center; padding: 32rpx; }
.timer-text { font-size: 72rpx; font-weight: 700; color: #ef4444; font-variant-numeric: tabular-nums; }
.workout-ex-list { display: flex; flex-direction: column; gap: 12rpx; }
.workout-ex { display: flex; align-items: center; justify-content: space-between; padding: 16rpx 20rpx; background: #f9f9f9; border-radius: 12rpx; }
.workout-ex-name { font-size: 26rpx; color: #333; }
.workout-ex-check { width: 44rpx; height: 44rpx; border-radius: 50%; border: 2rpx solid #ddd; display: flex; align-items: center; justify-content: center; font-size: 24rpx; color: #fff; }
.workout-ex-check.done { background: #ef4444; border-color: #ef4444; }
</style>
