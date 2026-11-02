<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u5e74\u9f84\u8ba1\u7b97\u5668</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="form-card"><text class="form-label">\u51fa\u751f\u65e5\u671f</text><input class="form-input" type="date" v-model="birthDate" /></view>
      <view class="calc-btn" @click="calc"><text>\u8ba1\u7b97</text></view>
      <view class="result-card" v-if="age">
        <view class="age-main"><text class="age-num">{{ age }}</text><text class="age-unit">\u5c81</text></view>
        <view class="age-detail">
          <text>\u5171 {{ totalDays }} \u5929</text>
          <text>{{ totalHours }} \u5c0f\u65f6</text>
        </view>
        <view class="age-info">
          <view class="info-row"><text>\u661f\u5ea7:</text><text>{{ zodiacSign }}</text></view>
          <view class="info-row"><text>\u751f\u8096:</text><text>{{ chineseZodiac }}</text></view>
          <view class="info-row"><text>\u4e0b\u4e00\u4e2a\u751f\u65e5:</text><text>{{ nextBirthday }}</text></view>
          <view class="info-row"><text>\u751f\u65e5\u5012\u8ba1\u65f6:</text><text>{{ birthdayCountdown }} \u5929</text></view>
        </view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const birthDate = ref("")
const age = ref("")
const totalDays = ref("")
const totalHours = ref("")
const zodiacSign = ref("")
const chineseZodiac = ref("")
const nextBirthday = ref("")
const birthdayCountdown = ref("")
const signs = ["\u725b\u5994","\u53cc\u5b50","\u5de8\u87f9","\u72ee\u5b50","\u5904\u5973","\u5929\u79e4","\u5929\u874e","\u5c04\u624b","\u6469\u7faf","\u6c34\u74f6","\u53cc\u9c7c","\u767d\u7f8a"]
const animals = ["\u732b","\u72d7","\u732a","\u9f20","\u725b","\u864e","\u5154","\u9f99","\u86c7","\u9a6c","\u7f8a","\u7334"]
function calc() {
  if (!birthDate.value) { uni.showToast({ title: "\u8bf7\u9009\u62e9\u65e5\u671f", icon: "none" }); return }
  const b = new Date(birthDate.value)
  const now = new Date()
  const diff = now - b
  totalDays.value = Math.floor(diff / 86400000)
  totalHours.value = Math.floor(diff / 3600000)
  let years = now.getFullYear() - b.getFullYear()
  if (now.getMonth() < b.getMonth() || (now.getMonth() === b.getMonth() && now.getDate() < b.getDate())) years--
  age.value = years
  zodiacSign.value = signs[now.getMonth()]
  chineseZodiac.value = animals[(b.getFullYear() - 4) % 12]
  let next = new Date(now.getFullYear(), b.getMonth(), b.getDate())
  if (next < now) next.setFullYear(next.getFullYear() + 1)
  nextBirthday.value = next.toLocaleDateString()
  birthdayCountdown.value = Math.floor((next - now) / 86400000)
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #a18cd1, #fbc2eb); }
.custom-nav { background: linear-gradient(135deg, #6c5ce7, #a29bfe); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.form-card { background: #fff; border-radius: 20rpx; padding: 24rpx; margin-bottom: 20rpx; }
.form-label { font-size: 26rpx; color: #666; display: block; margin-bottom: 12rpx; }
.form-input { font-size: 32rpx; color: #333; font-weight: 600; }
.calc-btn { background: linear-gradient(135deg, #6c5ce7, #a29bfe); border-radius: 16rpx; padding: 24rpx; text-align: center; margin: 32rpx 0; }
.calc-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.result-card { background: #fff; border-radius: 24rpx; padding: 32rpx; text-align: center; }
.age-main { margin-bottom: 20rpx; }
.age-num { font-size: 80rpx; font-weight: 700; color: #6c5ce7; }
.age-unit { font-size: 32rpx; color: #999; margin-left: 8rpx; }
.age-detail { font-size: 24rpx; color: #999; margin-bottom: 24rpx; display: flex; justify-content: center; gap: 24rpx; }
.age-info { text-align: left; border-top: 2rpx solid #f0f0f0; padding-top: 20rpx; }
.info-row { display: flex; justify-content: space-between; padding: 10rpx 0; font-size: 26rpx; color: #666; }
</style>
