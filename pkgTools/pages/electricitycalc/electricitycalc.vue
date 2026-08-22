<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u7535\u8d39\u8ba1\u7b97\u5668</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="form-card"><text class="form-label">\u7528\u7535\u91cf (kWh)</text><input class="form-input" type="digit" v-model="kwh" placeholder="\u8f93\u5165\u7528\u7535\u91cf" /></view>
      <view class="form-card"><text class="form-label">\u9636\u68af\u7c7b\u578b</text><view class="tier-tabs"><text class="tier-tab" :class="{active: tierType==='monthly'}" @click="tierType='monthly'">\u6708\u7ea7</text><text class="tier-tab" :class="{active: tierType==='annual'}" @click="tierType='annual'">\u5e74\u7ea7</text></view></view>
      <view class="calc-btn" @click="calc"><text>\u8ba1\u7b97\u7535\u8d39</text></view>
      <view class="result-card" v-if="cost > 0">
        <text class="result-title">\u7535\u8d39\u660e\u7ec6</text>
        <view class="tier-detail" v-for="(t, i) in tierDetails" :key="i">
          <view class="tier-row"><text>\u7b2c{{ i+1 }}\u9636 ({{ t.range }})</text><text>{{ t.kwh }} kWh</text></view>
          <view class="tier-row"><text>\u5355\u4ef7: {{ t.rate }} \u5143/kWh</text><text>\u5c0f\u8ba1: {{ t.cost }} \u5143</text></view>
        </view>
        <view class="total-row"><text>\u5408\u8ba1</text><text class="total-val">{{ cost }} \u5143</text></view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const kwh = ref("")
const tierType = ref("monthly")
const cost = ref(0)
const tierDetails = ref([])
const monthlyTiers = [{limit:240,rate:0.49},{limit:400,rate:0.54},{limit:99999,rate:0.79}]
const annualTiers = [{limit:2880,rate:0.49},{limit:4800,rate:0.54},{limit:99999,rate:0.79}]
function calc() {
  const k = parseFloat(kwh.value) || 0
  if (k <= 0) { uni.showToast({ title: "\u8bf7\u8f93\u5165\u7528\u7535\u91cf", icon: "none" }); return }
  const tiers = tierType.value === "monthly" ? monthlyTiers : annualTiers
  let remaining = k, totalCost = 0, prevLimit = 0
  tierDetails.value = []
  for (let i = 0; i < tiers.length; i++) {
    const tier = tiers[i]
    const tierKwh = Math.min(remaining, tier.limit - prevLimit)
    if (tierKwh <= 0) break
    const tierCost = (tierKwh * tier.rate).toFixed(2)
    tierDetails.value.push({range: prevLimit+"-"+tier.limit, kwh: tierKwh.toFixed(1), rate: tier.rate.toFixed(2), cost: tierCost})
    totalCost += parseFloat(tierCost)
    remaining -= tierKwh
    prevLimit = tier.limit
    if (remaining <= 0) break
  }
  cost.value = totalCost.toFixed(2)
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #fbc2eb, #a6c1ee); }
.custom-nav { background: linear-gradient(135deg, #e17055, #fdcb6e); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.form-card { background: #fff; border-radius: 20rpx; padding: 24rpx; margin-bottom: 20rpx; }
.form-label { font-size: 26rpx; color: #666; display: block; margin-bottom: 12rpx; }
.form-input { font-size: 32rpx; color: #333; font-weight: 600; }
.tier-tabs { display: flex; gap: 16rpx; }
.tier-tab { padding: 12rpx 24rpx; border-radius: 12rpx; background: #f0f0f0; font-size: 26rpx; color: #666; }
.tier-tab.active { background: #e17055; color: #fff; }
.calc-btn { background: linear-gradient(135deg, #e17055, #fdcb6e); border-radius: 16rpx; padding: 24rpx; text-align: center; margin: 32rpx 0; }
.calc-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.result-card { background: #fff; border-radius: 24rpx; padding: 32rpx; }
.result-title { font-size: 30rpx; font-weight: 600; color: #333; display: block; margin-bottom: 20rpx; }
.tier-detail { border-bottom: 2rpx solid #f0f0f0; padding: 16rpx 0; }
.tier-row { display: flex; justify-content: space-between; font-size: 24rpx; color: #666; padding: 4rpx 0; }
.total-row { display: flex; justify-content: space-between; padding-top: 20rpx; font-size: 30rpx; font-weight: 700; }
.total-val { color: #e17055; }
</style>
