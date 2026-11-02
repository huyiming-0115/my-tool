
<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">电费计算器</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="ec-tabs"><view class="ec-tab" :class="{active: mode==='month'}" @click="mode='month'"><text>按月</text></view><view class="ec-tab" :class="{active: mode==='year'}" @click="mode='year'"><text>按年</text></view></view>
      <view class="ec-card">
        <text class="ec-label">用电量（度/kWh）</text>
        <input class="ec-input" type="digit" v-model="usage" placeholder="请输入用电量" />
      </view>
      <view class="ec-card">
        <text class="ec-label">地区类型</text>
        <view class="ec-radio-row"><view class="ec-radio" :class="{active: type==='urban'}" @click="type='urban'"><text>城镇居民</text></view><view class="ec-radio" :class="{active: type==='rural'}" @click="type='rural'"><text>农村居民</text></view></view>
      </view>
      <view class="ec-btn" @click="calculate"><text>计算电费</text></view>
      <view class="ec-result" v-if="showResult">
        <text class="ec-result-title">阶梯电价明细</text>
        <view class="ec-tier" v-for="(t, i) in tiers" :key="i">
          <view class="ec-tier-header"><text>{{t.name}}</text><text>{{t.range}}</text></view>
          <view class="ec-tier-row"><text>用电量: {{t.usage}} 度</text><text>单价: {{t.price}}元</text><text>小计: {{t.cost}}元</text></view>
        </view>
        <view class="ec-total"><text>合计电费</text><text>{{totalCost}} 元</text></view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, reactive, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const usage = ref("")
const mode = ref("month")
const type = ref("urban")
const showResult = ref(false)
const tiers = ref([])
const totalCost = ref("0")
function calculate() {
  var u = parseFloat(usage.value) || 0
  if (u <= 0) return
  var limits = mode.value === "month" ? [240, 400, 99999] : [2880, 4800, 99999]
  var prices = type.value === "urban" ? [0.52, 0.57, 0.82] : [0.51, 0.56, 0.81]
  var names = ["第一阶梯", "第二阶梯", "第三阶梯"]
  var ranges = mode.value === "month" ? ["0-240度", "241-400度", "401度以上"] : ["0-2880度", "2881-4800度", "4801度以上"]
  var remaining = u
  var result = []
  var total = 0
  var prev = 0
  for (var i = 0; i < 3; i++) {
    var tierUsage = Math.min(remaining, limits[i] - prev)
    if (tierUsage <= 0) break
    var cost = (tierUsage * prices[i]).toFixed(2)
    result.push({ name: names[i], range: ranges[i], usage: tierUsage.toFixed(0), price: prices[i].toFixed(2), cost: cost })
    total += parseFloat(cost)
    remaining -= tierUsage
    prev = limits[i]
    if (remaining <= 0) break
  }
  tiers.value = result
  totalCost.value = total.toFixed(2)
  showResult.value = true
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #f093fb, #f5576c); }
.custom-nav { background: linear-gradient(135deg, #f093fb, #f5576c); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 32rpx; }
.ec-tabs { display: flex; background: rgba(255,255,255,0.2); border-radius: 16rpx; padding: 6rpx; margin-bottom: 24rpx; }
.ec-tab { flex: 1; text-align: center; padding: 16rpx; border-radius: 12rpx; }
.ec-tab text { color: rgba(255,255,255,0.7); font-size: 28rpx; }
.ec-tab.active { background: #fff; }
.ec-tab.active text { color: #f5576c; font-weight: 600; }
.ec-card { background: rgba(255,255,255,0.15); border-radius: 20rpx; padding: 24rpx; margin-bottom: 20rpx; }
.ec-label { color: rgba(255,255,255,0.8); font-size: 26rpx; display: block; margin-bottom: 12rpx; }
.ec-input { background: rgba(255,255,255,0.2); border-radius: 12rpx; padding: 16rpx 20rpx; font-size: 32rpx; color: #fff; font-weight: 600; }
.ec-radio-row { display: flex; gap: 16rpx; }
.ec-radio { flex: 1; text-align: center; padding: 16rpx; background: rgba(255,255,255,0.1); border-radius: 12rpx; }
.ec-radio text { color: rgba(255,255,255,0.7); font-size: 28rpx; }
.ec-radio.active { background: #fff; }
.ec-radio.active text { color: #f5576c; font-weight: 600; }
.ec-btn { background: #fff; border-radius: 16rpx; padding: 24rpx; text-align: center; margin: 32rpx 0; }
.ec-btn text { color: #f5576c; font-size: 32rpx; font-weight: 700; }
.ec-result { background: rgba(255,255,255,0.15); border-radius: 20rpx; padding: 28rpx; }
.ec-result-title { color: #fff; font-size: 30rpx; font-weight: 700; display: block; margin-bottom: 20rpx; }
.ec-tier { background: rgba(255,255,255,0.1); border-radius: 16rpx; padding: 20rpx; margin-bottom: 16rpx; }
.ec-tier-header { display: flex; justify-content: space-between; margin-bottom: 8rpx; }
.ec-tier-header text { color: #fff; font-size: 28rpx; font-weight: 600; }
.ec-tier-row { display: flex; justify-content: space-between; }
.ec-tier-row text { color: rgba(255,255,255,0.7); font-size: 24rpx; }
.ec-total { display: flex; justify-content: space-between; padding-top: 16rpx; border-top: 1rpx solid rgba(255,255,255,0.3); }
.ec-total text { color: #fff; font-size: 32rpx; font-weight: 700; }
</style>
