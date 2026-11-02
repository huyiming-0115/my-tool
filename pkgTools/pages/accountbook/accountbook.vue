<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u8bb0\u8d26\u672c</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="summary-row">
        <view class="sum-card income"><text class="sum-val">{{ totalIncome }}</text><text class="sum-label">\u6536\u5165</text></view>
        <view class="sum-card expense"><text class="sum-val">{{ totalExpense }}</text><text class="sum-label">\u652f\u51fa</text></view>
        <view class="sum-card balance"><text class="sum-val">{{ balance }}</text><text class="sum-label">\u7ed3\u4f59</text></view>
      </view>
      <view class="add-row">
        <input class="add-input" v-model="newAmount" type="digit" placeholder="\u91d1\u989d" />
        <picker class="cat-picker" :range="categories" @change="catIdx=$event.detail.value"><text>{{ categories[catIdx] }} \u25bc</text></picker>
        <text class="add-btn" @click="addRecord">+</text>
      </view>
      <view class="record-list">
        <view class="record-item" v-for="(r, i) in records" :key="i">
          <text class="rec-cat">{{ r.cat }}</text>
          <text class="rec-amount" :class="{income: r.type==='in', expense: r.type==='out'}">{{ r.type==='in'?'+':'-' }}{{ r.amount }}</text>
        </view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const totalIncome = ref("3500")
const totalExpense = ref("1200")
const balance = ref("2300")
const newAmount = ref("")
const catIdx = ref(0)
const categories = ["\u996e\u98df","\u4ea4\u901a","\u8d2d\u7269","\u5a31\u4e50","\u5de5\u8d44","\u5176\u4ed6"]
const records = ref([
  {cat:"\u5de5\u8d44", amount:"5000", type:"in"},
  {cat:"\u996e\u98df", amount:"300", type:"out"},
  {cat:"\u4ea4\u901a", amount:"50", type:"out"},
  {cat:"\u8d2d\u7269", amount:"850", type:"out"}
])
function addRecord() {
  if (!newAmount.value) return
  records.value.unshift({cat: categories[catIdx.value], amount: newAmount.value, type: "out"})
  newAmount.value = ""
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #43e97b, #38f9d7); }
.custom-nav { background: linear-gradient(135deg, #00b894, #55efc4); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.summary-row { display: flex; gap: 16rpx; margin-bottom: 24rpx; }
.sum-card { flex: 1; background: #fff; border-radius: 20rpx; padding: 24rpx; text-align: center; }
.sum-val { font-size: 32rpx; font-weight: 700; display: block; }
.sum-label { font-size: 22rpx; color: #999; }
.income .sum-val { color: #00b894; }
.expense .sum-val { color: #e17055; }
.balance .sum-val { color: #0984e3; }
.add-row { display: flex; gap: 12rpx; margin-bottom: 24rpx; }
.add-input { flex: 1; background: #fff; border-radius: 16rpx; padding: 20rpx; font-size: 28rpx; }
.cat-picker { background: #fff; border-radius: 16rpx; padding: 20rpx; font-size: 26rpx; display: flex; align-items: center; }
.add-btn { background: #00b894; color: #fff; border-radius: 16rpx; width: 80rpx; display: flex; align-items: center; justify-content: center; font-size: 40rpx; font-weight: 700; }
.record-list { display: flex; flex-direction: column; gap: 12rpx; }
.record-item { background: #fff; border-radius: 16rpx; padding: 20rpx 24rpx; display: flex; justify-content: space-between; }
.rec-cat { font-size: 26rpx; color: #333; }
.rec-amount { font-size: 28rpx; font-weight: 600; }
.rec-amount.income { color: #00b894; }
.rec-amount.expense { color: #e17055; }
</style>
