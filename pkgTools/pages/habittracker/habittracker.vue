<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u4e60\u60ef\u8ffd\u8e2a</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="add-row"><input class="add-input" v-model="newHabit" placeholder="\u65b0\u4e60\u60ef" /><text class="add-btn" @click="addHabit">+</text></view>
      <view class="habit-list">
        <view class="habit-card" v-for="(h, i) in habits" :key="i">
          <view class="habit-info"><text class="habit-name">{{ h.name }}</text><text class="habit-streak">{{ h.streak }}\u5929\u8fde\u7eed</text></view>
          <view class="habit-days">
            <text class="day-dot" :class="{done: d}" v-for="(d, di) in h.days" :key="di">{{ di+1 }}</text>
          </view>
          <text class="check-btn" @click="checkDay(i)">\u4eca\u65e5\u6253\u5361</text>
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
  {name:"\u65e9\u8d77", streak:15, days:[true,true,true,true,true,true,false]},
  {name:"\u8bfb\u4e6630\u5206\u949f", streak:8, days:[true,true,false,true,true,false,false]},
  {name:"\u559d\u6c348\u676f", streak:22, days:[true,true,true,true,true,true,true]},
  {name:"\u8dd1\u6b653km", streak:5, days:[true,false,true,false,true,false,false]}
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
