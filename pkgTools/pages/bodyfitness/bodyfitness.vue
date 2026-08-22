<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u4f53\u8102\u7387\u8ba1\u7b97</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="form-card">
        <view class="gender-row"><text class="gender-btn" :class="{active: gender==='male'}" @click="gender='male'">\u7537</text><text class="gender-btn" :class="{active: gender==='female'}" @click="gender='female'">\u5973</text></view>
      </view>
      <view class="form-card"><text class="form-label">\u8eab\u9ad8 (cm)</text><input class="form-input" type="digit" v-model="height" /></view>
      <view class="form-card"><text class="form-label">\u4f53\u91cd (kg)</text><input class="form-input" type="digit" v-model="weight" /></view>
      <view class="form-card"><text class="form-label">\u8170\u56f4 (cm)</text><input class="form-input" type="digit" v-model="waist" /></view>
      <view class="form-card"><text class="form-label">\u5e74\u9f84</text><input class="form-input" type="number" v-model="age" /></view>
      <view class="calc-btn" @click="calc"><text>\u8ba1\u7b97</text></view>
      <view class="result-card" v-if="bmi">
        <view class="res-row"><text>BMI:</text><text class="res-val">{{ bmi }}</text></view>
        <view class="res-row"><text>\u4f53\u8102\u7387:</text><text class="res-val">{{ bodyFat }}%</text></view>
        <view class="res-row"><text>\u57fa\u7840\u4ee3\u8c22:</text><text class="res-val">{{ bmr }} kcal</text></view>
        <view class="res-row"><text>\u6bcf\u65e5\u6d88\u8017(TDEE):</text><text class="res-val">{{ tdee }} kcal</text></view>
        <text class="res-tip">{{ tip }}</text>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const gender = ref("male")
const height = ref("")
const weight = ref("")
const waist = ref("")
const age = ref("")
const bmi = ref("")
const bodyFat = ref("")
const bmr = ref("")
const tdee = ref("")
const tip = ref("")
function calc() {
  const h = parseFloat(height.value), w = parseFloat(weight.value)
  const waistVal = parseFloat(waist.value), a = parseFloat(age.value)
  if (!h || !w) { uni.showToast({ title: "\u8bf7\u8f93\u5165\u8eab\u9ad8\u4f53\u91cd", icon: "none" }); return }
  bmi.value = (w / ((h/100) ** 2)).toFixed(1)
  if (waistVal && a) {
    if (gender.value === "male") bodyFat.value = ((1.2 * parseFloat(bmi.value)) + (0.23 * a) - 16.2).toFixed(1)
    else bodyFat.value = ((1.2 * parseFloat(bmi.value)) + (0.23 * a) - 5.4).toFixed(1)
  } else bodyFat.value = (parseFloat(bmi.value) * 1.2 + (gender.value==="male"?16.2:5.4)).toFixed(1)
  bmr.value = gender.value === "male" ? (10*w + 6.25*h - 5*a + 5).toFixed(0) : (10*w + 6.25*h - 5*a - 161).toFixed(0)
  tdee.value = (parseFloat(bmr.value) * 1.55).toFixed(0)
  const b = parseFloat(bmi.value)
  if (b < 18.5) tip.value = "\u504f\u7626\uff0c\u5efa\u8bae\u589e\u91cd\u589e\u808c"
  else if (b < 24) tip.value = "\u6b63\u5e38\uff0c\u4fdd\u6301\u73b0\u72b6"
  else if (b < 28) tip.value = "\u504f\u80a5\uff0c\u5efa\u8bae\u9002\u5f53\u51cf\u8102"
  else tip.value = "\u80a5\u80d6\uff0c\u5efa\u8bae\u5236\u5b9a\u51cf\u8102\u8ba1\u5212"
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #f093fb, #f5576c); }
.custom-nav { background: linear-gradient(135deg, #e84393, #fd79a8); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.form-card { background: #fff; border-radius: 20rpx; padding: 24rpx; margin-bottom: 20rpx; }
.form-label { font-size: 26rpx; color: #666; display: block; margin-bottom: 12rpx; }
.form-input { font-size: 32rpx; color: #333; font-weight: 600; }
.gender-row { display: flex; gap: 16rpx; }
.gender-btn { flex: 1; text-align: center; padding: 16rpx; border-radius: 12rpx; background: #f0f0f0; font-size: 28rpx; }
.gender-btn.active { background: #e84393; color: #fff; }
.calc-btn { background: linear-gradient(135deg, #e84393, #fd79a8); border-radius: 16rpx; padding: 24rpx; text-align: center; margin: 32rpx 0; }
.calc-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.result-card { background: #fff; border-radius: 24rpx; padding: 32rpx; }
.res-row { display: flex; justify-content: space-between; padding: 12rpx 0; font-size: 28rpx; }
.res-val { color: #e84393; font-weight: 700; }
.res-tip { display: block; margin-top: 16rpx; padding: 16rpx; background: #fff0f5; border-radius: 12rpx; font-size: 24rpx; color: #e84393; }
</style>
