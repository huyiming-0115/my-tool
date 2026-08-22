# -*- coding: utf-8 -*-
import os
base = "pkgTools/pages"
def w(name, content):
    with open(os.path.join(base, name, name + ".vue"), "w") as f:
        f.write(content)
    print("OK:", name)

# ===== socialinsurance =====
w("socialinsurance", """<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\\u2190</text><text class="nav-title">\\u4e94\\u9669\\u4e00\\u91d1\\u8ba1\\u7b97\\u5668</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="form-card"><text class="form-label">\\u6708\\u85aa (\\u5143)</text><input class="form-input" type="digit" v-model="salary" placeholder="\\u8f93\\u5165\\u6708\\u85aa" /></view>
      <view class="form-card"><text class="form-label">\\u79ef\\u91d1\\u6bd4\\u4f8b (%): {{ fundRate }}</text><slider :value="fundRate" min="5" max="12" show-value @change="fundRate=Number($event.detail.value)"/></view>
      <view class="calc-btn" @click="calc"><text>\\u8ba1\\u7b97</text></view>
      <view class="result-card" v-if="total > 0">
        <view class="result-row"><text>\\u4e2a\\u4eba\\u627f\\u62c5:</text><text class="result-val">{{ personalTotal }} \\u5143</text></view>
        <view class="result-row"><text>\\u5355\\u4f4d\\u627f\\u62c5:</text><text class="result-val">{{ companyTotal }} \\u5143</text></view>
        <view class="result-row total"><text>\\u5408\\u8ba1:</text><text class="result-val">{{ total }} \\u5143</text></view>
        <view class="detail-list"><view class="detail-row" v-for="(d, i) in details" :key="i"><text>{{ d.name }}</text><text>{{ d.personal }}/{{ d.company }}</text></view></view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const salary = ref("")
const fundRate = ref(12)
const total = ref(0)
const personalTotal = ref(0)
const companyTotal = ref(0)
const details = ref([])
function calc() {
  const s = parseFloat(salary.value) || 0
  if (s <= 0) { uni.showToast({ title: "\\u8bf7\\u8f93\\u5165\\u6708\\u85aa", icon: "none" }); return }
  const f = fundRate.value / 100
  const rates = [
    {name:"\\u517b\\u8001\\u4fdd\\u9669", personal: 0.08, company: 0.16},
    {name:"\\u533b\\u7597\\u4fdd\\u9669", personal: 0.02, company: 0.08},
    {name:"\\u5931\\u4e1a\\u4fdd\\u9669", personal: 0.005, company: 0.005},
    {name:"\\u5de5\\u4f24\\u4fdd\\u9669", personal: 0, company: 0.004},
    {name:"\\u751f\\u80b2\\u4fdd\\u9669", personal: 0, company: 0.008},
    {name:"\\u4f4f\\u623f\\u516c\\u79ef\\u91d1", personal: f, company: f}
  ]
  details.value = rates.map(function(r) {
    return { name: r.name, personal: (s*r.personal).toFixed(2), company: (s*r.company).toFixed(2) }
  })
  personalTotal.value = details.value.reduce(function(a,b){return a+parseFloat(b.personal)},0).toFixed(2)
  companyTotal.value = details.value.reduce(function(a,b){return a+parseFloat(b.company)},0).toFixed(2)
  total.value = (parseFloat(personalTotal.value)+parseFloat(companyTotal.value)).toFixed(2)
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #a8edea, #fed6e3); }
.custom-nav { background: linear-gradient(135deg, #00b894, #00cec9); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.form-card { background: #fff; border-radius: 20rpx; padding: 24rpx; margin-bottom: 20rpx; }
.form-label { font-size: 26rpx; color: #666; display: block; margin-bottom: 12rpx; }
.form-input { font-size: 32rpx; color: #333; font-weight: 600; }
.calc-btn { background: linear-gradient(135deg, #00b894, #00cec9); border-radius: 16rpx; padding: 24rpx; text-align: center; margin: 32rpx 0; }
.calc-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.result-card { background: #fff; border-radius: 24rpx; padding: 32rpx; }
.result-row { display: flex; justify-content: space-between; padding: 12rpx 0; font-size: 28rpx; }
.result-row.total { border-top: 2rpx solid #eee; margin-top: 12rpx; padding-top: 20rpx; font-weight: 700; }
.result-val { color: #00b894; font-weight: 600; }
.detail-list { margin-top: 20rpx; border-top: 2rpx solid #f0f0f0; padding-top: 16rpx; }
.detail-row { display: flex; justify-content: space-between; font-size: 24rpx; color: #888; padding: 8rpx 0; }
</style>
""")

# ===== electricitycalc =====
w("electricitycalc", """<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\\u2190</text><text class="nav-title">\\u7535\\u8d39\\u8ba1\\u7b97\\u5668</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="form-card"><text class="form-label">\\u7528\\u7535\\u91cf (kWh)</text><input class="form-input" type="digit" v-model="kwh" placeholder="\\u8f93\\u5165\\u7528\\u7535\\u91cf" /></view>
      <view class="form-card"><text class="form-label">\\u9636\\u68af\\u7c7b\\u578b</text><view class="tier-tabs"><text class="tier-tab" :class="{active: tierType==='monthly'}" @click="tierType='monthly'">\\u6708\\u7ea7</text><text class="tier-tab" :class="{active: tierType==='annual'}" @click="tierType='annual'">\\u5e74\\u7ea7</text></view></view>
      <view class="calc-btn" @click="calc"><text>\\u8ba1\\u7b97\\u7535\\u8d39</text></view>
      <view class="result-card" v-if="cost > 0">
        <text class="result-title">\\u7535\\u8d39\\u660e\\u7ec6</text>
        <view class="tier-detail" v-for="(t, i) in tierDetails" :key="i">
          <view class="tier-row"><text>\\u7b2c{{ i+1 }}\\u9636 ({{ t.range }})</text><text>{{ t.kwh }} kWh</text></view>
          <view class="tier-row"><text>\\u5355\\u4ef7: {{ t.rate }} \\u5143/kWh</text><text>\\u5c0f\\u8ba1: {{ t.cost }} \\u5143</text></view>
        </view>
        <view class="total-row"><text>\\u5408\\u8ba1</text><text class="total-val">{{ cost }} \\u5143</text></view>
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
  if (k <= 0) { uni.showToast({ title: "\\u8bf7\\u8f93\\u5165\\u7528\\u7535\\u91cf", icon: "none" }); return }
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
""")

# ===== cncapital =====
w("cncapital", """<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\\u2190</text><text class="nav-title">\\u5927\\u5199\\u91d1\\u989d\\u8f6c\\u6362</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="form-card"><text class="form-label">\\u8f93\\u5165\\u91d1\\u989d</text><input class="form-input" type="digit" v-model="amount" placeholder="\\u5982: 12345.67" /></view>
      <view class="calc-btn" @click="convert"><text>\\u8f6c\\u6362</text></view>
      <view class="result-card" v-if="result">
        <text class="result-label">\\u4e2d\\u6587\\u5927\\u5199</text>
        <text class="result-text">{{ result }}</text>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const amount = ref("")
const result = ref("")
const digits = ["\\u96f6","\\u58f9","\\u8d30","\\u53c1","\\u8086","\\u4f0d","\\u9646","\\u67d2","\\u634c","\\u7396"]
const units = ["", "\\u62fe", "\\u4f70", "\\u4edf", "\\u4e07", "\\u62fe", "\\u4f70", "\\u4edf", "\\u4ebf"]
function convert() {
  const val = parseFloat(amount.value)
  if (isNaN(val) || val < 0) { uni.showToast({ title: "\\u8bf7\\u8f93\\u5165\\u6709\\u6548\\u91d1\\u989d", icon: "none" }); return }
  if (val > 999999999999.99) { uni.showToast({ title: "\\u91d1\\u989d\\u8fc7\\u5927", icon: "none" }); return }
  const parts = val.toFixed(2).split(".")
  const intPart = parts[0]
  const decPart = parts[1]
  let chinese = ""
  let zeroFlag = false
  const len = intPart.length
  for (let i = 0; i < len; i++) {
    const n = parseInt(intPart[i])
    const pos = len - i - 1
    if (n === 0) { zeroFlag = true }
    else {
      if (zeroFlag) { chinese += "\\u96f6"; zeroFlag = false }
      chinese += digits[n] + units[pos % 8]
    }
    if (pos === 4 && zeroFlag) { chinese += "\\u4e07"; zeroFlag = false }
    if (pos === 8) { chinese += "\\u4ebf"; zeroFlag = false }
  }
  if (!chinese) chinese = "\\u96f6"
  chinese += "\\u5143"
  if (decPart[0] === "0" && decPart[1] === "0") chinese += "\\u6574"
  else {
    if (decPart[0] !== "0") chinese += digits[parseInt(decPart[0])] + "\\u89d2"
    if (decPart[1] !== "0") chinese += digits[parseInt(decPart[1])] + "\\u5206"
  }
  result.value = chinese
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #ffecd2, #fcb69f); }
.custom-nav { background: linear-gradient(135deg, #e17055, #fdcb6e); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.form-card { background: #fff; border-radius: 20rpx; padding: 24rpx; margin-bottom: 20rpx; }
.form-label { font-size: 26rpx; color: #666; display: block; margin-bottom: 12rpx; }
.form-input { font-size: 36rpx; color: #333; font-weight: 600; }
.calc-btn { background: linear-gradient(135deg, #e17055, #fdcb6e); border-radius: 16rpx; padding: 24rpx; text-align: center; margin: 32rpx 0; }
.calc-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.result-card { background: #fff; border-radius: 24rpx; padding: 32rpx; text-align: center; }
.result-label { font-size: 24rpx; color: #999; display: block; margin-bottom: 12rpx; }
.result-text { font-size: 36rpx; color: #e17055; font-weight: 700; line-height: 1.6; }
</style>
""")

print("batch2 done")