<template>
  <view class="bmi-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">\u2190</text>
        <text class="nav-title">BMI计算</text>
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
          <text class="input-label">性别</text>
          <picker class="input-picker" :value="genderIdx" :range="genders" @change="onGenderChange">
            <text>{{ genders[genderIdx] }}</text>
          </picker>
        </view>
        <view class="input-row">
          <text class="input-label">年龄</text>
          <input class="input-field" v-model="age" type="digit" placeholder="请输入年龄" />
        </view>
        <button class="calc-btn" @click="calculate">计算 BMI</button>
      </view>

      <view class="result-card" v-if="bmiValue > 0">
        <text class="result-title">您的 BMI 结果</text>
        <text class="result-value">{{ bmiValue }}</text>
        <text class="result-category" :style="{ color: categoryColor }">{{ bmiCategory }}</text>
        <view class="result-bar">
          <view class="bar-segment" style="background: #3b82f6;">偏瘦</view>
          <view class="bar-segment" style="background: #10b981;">正常</view>
          <view class="bar-segment" style="background: #f59e0b;">偏胖</view>
          <view class="bar-segment" style="background: #ef4444;">肥胖</view>
        </view>
      </view>

      <view class="calorie-card" v-if="bmiValue > 0">
        <text class="calorie-title">每日建议热量</text>
        <view class="calorie-row">
          <text class="calorie-label">基础代谢率 (BMR)</text>
          <text class="calorie-value">{{ bmr }} 千卡</text>
        </view>
        <view class="calorie-row">
          <text class="calorie-label">久坐少动</text>
          <text class="calorie-value">{{ sedentary }} 千卡</text>
        </view>
        <view class="calorie-row">
          <text class="calorie-label">轻度活动</text>
          <text class="calorie-value">{{ light }} 千卡</text>
        </view>
        <view class="calorie-row">
          <text class="calorie-label">中度活动</text>
          <text class="calorie-value">{{ moderate }} 千卡</text>
        </view>
        <view class="calorie-row">
          <text class="calorie-label">高强度活动</text>
          <text class="calorie-value">{{ active }} 千卡</text>
        </view>
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
const bmiValue = ref(0)
const bmiCategory = ref("")
const categoryColor = ref("#10b981")
const bmr = ref(0)
const sedentary = ref(0)
const light = ref(0)
const moderate = ref(0)
const active = ref(0)

function goBack() { uni.navigateBack() }

function onGenderChange(e) { genderIdx.value = e.detail.value }

function calculate() {
  const h = parseFloat(height.value) / 100
  const w = parseFloat(weight.value)
  const a = parseFloat(age.value) || 25
  if (!h || !w || h <= 0 || w <= 0) {
    uni.showToast({ title: "请输入有效的身高体重", icon: "none" })
    return
  }
  const bmi = w / (h * h)
  bmiValue.value = bmi.toFixed(1)

  if (bmi < 18.5) { bmiCategory.value = "偏瘦"; categoryColor.value = "#3b82f6" }
  else if (bmi < 24) { bmiCategory.value = "正常"; categoryColor.value = "#10b981" }
  else if (bmi < 28) { bmiCategory.value = "偏胖"; categoryColor.value = "#f59e0b" }
  else { bmiCategory.value = "肥胖"; categoryColor.value = "#ef4444" }

  // BMR using Mifflin-St Jeor
  let base
  if (genderIdx.value === 0) {
    base = 10 * w + 6.25 * h * 100 - 5 * a + 5
  } else {
    base = 10 * w + 6.25 * h * 100 - 5 * a - 161
  }
  bmr.value = Math.round(base)
  sedentary.value = Math.round(base * 1.2)
  light.value = Math.round(base * 1.375)
  moderate.value = Math.round(base * 1.55)
  active.value = Math.round(base * 1.725)
}

onMounted(() => {
  if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }
})
</script>

<style lang="scss" scoped>
.bmi-page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #10b981, #34d399); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 32rpx; }
.input-card { background: #fff; border-radius: 24rpx; padding: 32rpx; margin-bottom: 24rpx; }
.input-row { display: flex; align-items: center; margin-bottom: 24rpx; }
.input-label { width: 160rpx; font-size: 28rpx; color: #666; flex-shrink: 0; }
.input-field { flex: 1; height: 80rpx; border: 2rpx solid #e5e7eb; border-radius: 12rpx; padding: 0 20rpx; font-size: 28rpx; }
.input-picker { flex: 1; height: 80rpx; line-height: 80rpx; border: 2rpx solid #e5e7eb; border-radius: 12rpx; padding: 0 20rpx; font-size: 28rpx; }
.calc-btn { background: linear-gradient(135deg, #10b981, #34d399); color: #fff; border-radius: 50rpx; font-size: 28rpx; margin-top: 16rpx; }
.result-card { background: #fff; border-radius: 24rpx; padding: 32rpx; margin-bottom: 24rpx; text-align: center; }
.result-title { font-size: 26rpx; color: #999; display: block; margin-bottom: 16rpx; }
.result-value { font-size: 72rpx; font-weight: 700; color: #333; display: block; }
.result-category { font-size: 32rpx; font-weight: 600; display: block; margin-top: 8rpx; }
.result-bar { display: flex; margin-top: 24rpx; border-radius: 12rpx; overflow: hidden; }
.bar-segment { flex: 1; padding: 12rpx 0; font-size: 22rpx; color: #fff; text-align: center; }
.calorie-card { background: #fff; border-radius: 24rpx; padding: 32rpx; }
.calorie-title { font-size: 28rpx; font-weight: 600; color: #333; margin-bottom: 20rpx; display: block; }
.calorie-row { display: flex; justify-content: space-between; align-items: center; padding: 16rpx 0; border-bottom: 2rpx solid #f9f9f9; }
.calorie-label { font-size: 26rpx; color: #666; }
.calorie-value { font-size: 28rpx; font-weight: 600; color: #10b981; }
</style>
