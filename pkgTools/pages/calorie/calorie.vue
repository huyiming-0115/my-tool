<template>
  <view class="calorie-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">←</text>
        <text class="nav-title">热量计算</text>
        <text class="nav-icon empty"> </text>
      </view>
    </view>

    <view class="content">
      <view class="input-card">
        <view class="input-row">
          <text class="input-label">身高 (cm)</text>
          <input class="input-field" v-model="height" type="digit" placeholder="请输入身高" />
        </view>
        <view class="input-row">
          <text class="input-label">体重 (kg)</text>
          <input class="input-field" v-model="weight" type="digit" placeholder="请输入体重" />
        </view>
        <view class="input-row">
          <text class="input-label">年龄</text>
          <input class="input-field" v-model="age" type="digit" placeholder="请输入年龄" />
        </view>
        <view class="input-row">
          <text class="input-label">性别</text>
          <picker class="input-picker" :value="genderIdx" :range="genders" @change="onGenderChange">
            <text>{{ genders[genderIdx] }}</text>
          </picker>
        </view>
        <view class="input-row">
          <text class="input-label">活动量</text>
          <picker class="input-picker" :value="activityIdx" :range="activityLevels" range-key="label" @change="onActivityChange">
            <text>{{ activityLevels[activityIdx].label }}</text>
          </picker>
        </view>
        <view class="input-row">
          <text class="input-label">目标</text>
          <picker class="input-picker" :value="goalIdx" :range="goals" range-key="label" @change="onGoalChange">
            <text>{{ goals[goalIdx].label }}</text>
          </picker>
        </view>
        <button class="calc-btn" @click="calculate">计算热量</button>
      </view>

      <view class="result-card" v-if="bmr > 0">
        <text class="result-title">计算结果</text>
        <view class="result-grid">
          <view class="result-item">
            <text class="item-value">{{ bmr }}</text>
            <text class="item-label">基础代谢 (千卡)</text>
          </view>
          <view class="result-item">
            <text class="item-value">{{ tdee }}</text>
            <text class="item-label">维持体重 (千卡)</text>
          </view>
          <view class="result-item highlight">
            <text class="item-value">{{ targetCal }}</text>
            <text class="item-label">{{ goals[goalIdx].label }} (千卡)</text>
          </view>
        </view>
      </view>

      <view class="tips-card" v-if="bmr > 0">
        <text class="tips-title">建议</text>
        <text class="tips-text">• 每日蛋白质摄入: {{ protein }}g</text>
        <text class="tips-text">• 建议饮水量: {{ water }}L</text>
        <text class="tips-text">• {{ advice }}</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from "vue"

const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const height = ref("")
const weight = ref("")
const age = ref("")
const genderIdx = ref(0)
const genders = ["男", "女"]
const activityIdx = ref(0)
const activityLevels = [
  { label: "久坐不动 (办公室工作)", value: 1.2 },
  { label: "轻度活动 (每周1-3次)", value: 1.375 },
  { label: "中度活动 (每周3-5次)", value: 1.55 },
  { label: "高强度 (每周6-7次)", value: 1.725 },
  { label: "极高强度 (体力劳动)", value: 1.9 },
]
const goalIdx = ref(1)
const goals = [
  { label: "快速减重 (-500千卡)", offset: -500 },
  { label: "缓慢减重 (-300千卡)", offset: -300 },
  { label: "维持体重", offset: 0 },
  { label: "缓慢增重 (+300千卡)", offset: 300 },
  { label: "快速增重 (+500千卡)", offset: 500 },
]
const bmr = ref(0)
const tdee = ref(0)
const targetCal = ref(0)
const protein = ref(0)
const water = ref(0)
const advice = ref("")

function goBack() { uni.navigateBack() }
function onGenderChange(e) { genderIdx.value = e.detail.value }
function onActivityChange(e) { activityIdx.value = e.detail.value }
function onGoalChange(e) { goalIdx.value = e.detail.value }

function calculate() {
  const h = parseFloat(height.value)
  const w = parseFloat(weight.value)
  const a = parseFloat(age.value) || 25
  if (!h || !w || h <= 0 || w <= 0) {
    uni.showToast({ title: "请输入有效的身高体重", icon: "none" })
    return
  }
  // Mifflin-St Jeor BMR
  let base
  if (genderIdx.value === 0) {
    base = 10 * w + 6.25 * h - 5 * a + 5
  } else {
    base = 10 * w + 6.25 * h - 5 * a - 161
  }
  bmr.value = Math.round(base)
  tdee.value = Math.round(base * activityLevels[activityIdx.value].value)
  targetCal.value = tdee.value + goals[goalIdx.value].offset
  if (targetCal.value < bmr.value * 0.8) {
    targetCal.value = Math.round(bmr.value * 0.8)
  }
  protein.value = Math.round(w * 1.6)
  water.value = (w * 0.033).toFixed(1)
  if (goalIdx.value <= 1) {
    advice.value = "控制饮食+适量运动，建议力量训练保持肌肉"
  } else if (goalIdx.value === 2) {
    advice.value = "保持当前饮食和运动习惯，定期监测体重"
  } else {
    advice.value = "增加优质碳水和蛋白质摄入，配合力量训练"
  }
}

onMounted(() => {
  if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }
})
</script>

<style lang="scss" scoped>
.calorie-page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #f97316, #fb923c); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 32rpx; }
.input-card { background: #fff; border-radius: 24rpx; padding: 32rpx; margin-bottom: 24rpx; }
.input-row { display: flex; align-items: center; margin-bottom: 24rpx; }
.input-label { width: 180rpx; font-size: 28rpx; color: #666; flex-shrink: 0; }
.input-field { flex: 1; height: 80rpx; border: 2rpx solid #e5e7eb; border-radius: 12rpx; padding: 0 20rpx; font-size: 28rpx; }
.input-picker { flex: 1; height: 80rpx; line-height: 80rpx; border: 2rpx solid #e5e7eb; border-radius: 12rpx; padding: 0 20rpx; font-size: 26rpx; }
.calc-btn { background: linear-gradient(135deg, #f97316, #fb923c); color: #fff; border-radius: 50rpx; font-size: 28rpx; margin-top: 16rpx; }
.result-card { background: #fff; border-radius: 24rpx; padding: 32rpx; margin-bottom: 24rpx; }
.result-title { font-size: 28rpx; font-weight: 600; color: #333; margin-bottom: 24rpx; display: block; text-align: center; }
.result-grid { display: flex; justify-content: space-between; }
.result-item { flex: 1; text-align: center; padding: 16rpx; }
.result-item.highlight { background: linear-gradient(135deg, #f97316, #fb923c); border-radius: 16rpx; }
.result-item.highlight .item-value { color: #fff; }
.result-item.highlight .item-label { color: rgba(255,255,255,0.85); }
.item-value { font-size: 36rpx; font-weight: 700; color: #f97316; display: block; }
.item-label { font-size: 20rpx; color: #999; margin-top: 8rpx; display: block; }
.tips-card { background: #fff; border-radius: 24rpx; padding: 32rpx; }
.tips-title { font-size: 28rpx; font-weight: 600; color: #333; margin-bottom: 16rpx; display: block; }
.tips-text { font-size: 26rpx; color: #666; line-height: 1.8; display: block; }
</style>
