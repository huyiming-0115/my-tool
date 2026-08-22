<template>
  <view class="currency-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">\u2190</text>
        <text class="nav-title">汇率查询</text>
        <text class="nav-icon empty"> </text>
      </view>
    </view>

    <view class="content">
      <view class="rate-card">
        <text class="rate-title">基准汇率</text>
        <text class="rate-base">1 {{ baseCurrency }} = {{ rateValue }} {{ targetCurrency }}</text>
        <text class="rate-update">{{ updateTime }}</text>
      </view>

      <view class="converter-card">
        <view class="conv-row">
          <view class="conv-item">
            <text class="conv-label">持有货币</text>
            <view class="conv-input-wrap">
              <input class="conv-input" v-model="amount" type="digit" placeholder="0" @input="convert" />
              <picker class="conv-picker" :value="baseIdx" :range="currencies" range-key="label" @change="onBaseChange">
                <text>{{ baseCurrency }}</text>
              </picker>
            </view>
          </view>
        </view>

        <view class="conv-swap" @click="swapCurrency">
          <text class="swap-icon">⇅</text>
        </view>

        <view class="conv-row">
          <view class="conv-item">
            <text class="conv-label">兑换货币</text>
            <view class="conv-input-wrap">
              <text class="conv-result">{{ convertedAmount }}</text>
              <picker class="conv-picker" :value="targetIdx" :range="currencies" range-key="label" @change="onTargetChange">
                <text>{{ targetCurrency }}</text>
              </picker>
            </view>
          </view>
        </view>
      </view>

      <view class="table-card">
        <text class="table-title">常用货币汇率 (基准: {{ baseCurrency }})</text>
        <view class="table-header">
          <text class="th th-code">货币</text>
          <text class="th th-name">名称</text>
          <text class="th th-rate">汇率</text>
        </view>
        <view class="table-row" v-for="(item, idx) in rateTable" :key="idx">
          <text class="td td-code">{{ item.code }}</text>
          <text class="td td-name">{{ item.name }}</text>
          <text class="td td-rate">{{ item.rate }}</text>
        </view>
      </view>

      <button class="refresh-btn" @click="fetchRates">刷新汇率</button>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from "vue"

const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const amount = ref("1")
const baseIdx = ref(0)
const targetIdx = ref(1)
const baseCurrency = ref("USD")
const targetCurrency = ref("CNY")
const rateValue = ref("--")
const convertedAmount = ref("--")
const updateTime = ref("")
const rates = ref({})
const rateTable = ref([])

const currencies = [
  { code: "USD", name: "美元", label: "USD-美元" },
  { code: "CNY", name: "人民币", label: "CNY-人民币" },
  { code: "EUR", name: "欧元", label: "EUR-欧元" },
  { code: "JPY", name: "日元", label: "JPY-日元" },
  { code: "GBP", name: "英镑", label: "GBP-英镑" },
  { code: "KRW", name: "韩元", label: "KRW-韩元" },
  { code: "HKD", name: "港币", label: "HKD-港币" },
  { code: "TWD", name: "台币", label: "TWD-台币" },
  { code: "AUD", name: "澳元", label: "AUD-澳元" },
  { code: "CAD", name: "加元", label: "CAD-加元" },
  { code: "SGD", name: "新加坡元", label: "SGD-新加坡元" },
  { code: "CHF", name: "瑞士法郎", label: "CHF-瑞士法郎" },
  { code: "THB", name: "泰铢", label: "THB-泰铢" },
]

function goBack() { uni.navigateBack() }

function onBaseChange(e) {
  baseIdx.value = e.detail.value
  baseCurrency.value = currencies[e.detail.value].code
  fetchRates()
}

function onTargetChange(e) {
  targetIdx.value = e.detail.value
  targetCurrency.value = currencies[e.detail.value].code
  convert()
}

function swapCurrency() {
  const tmpIdx = baseIdx.value
  baseIdx.value = targetIdx.value
  targetIdx.value = tmpIdx
  baseCurrency.value = currencies[baseIdx.value].code
  targetCurrency.value = currencies[targetIdx.value].code
  fetchRates()
}

function convert() {
  const r = rates.value[targetCurrency.value]
  if (!r) { convertedAmount.value = "--"; return }
  const amt = parseFloat(amount.value) || 0
  convertedAmount.value = (amt * r).toFixed(2)
}

function fetchRates() {
  uni.showLoading({ title: "加载中..." })
  uni.request({
    url: "https://api.frankfurter.app/latest?from=" + baseCurrency.value,
    success: (res) => {
      uni.hideLoading()
      const data = res.data
      if (data && data.rates) {
        rates.value = data.rates
        const r = data.rates[targetCurrency.value]
        if (r) {
          rateValue.value = r.toFixed(4)
          updateTime.value = "更新时间: " + data.date
        }
        buildTable()
        convert()
      }
    },
    fail: () => {
      uni.hideLoading()
      uni.showToast({ title: "获取失败，请检查网络", icon: "none" })
    }
  })
}

function buildTable() {
  const list = []
  for (const cur of currencies) {
    if (cur.code === baseCurrency.value) continue
    const r = rates.value[cur.code]
    if (r) list.push({ code: cur.code, name: cur.name, rate: r.toFixed(4) })
  }
  rateTable.value = list
}

onMounted(() => {
  if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }
  fetchRates()
})
</script>

<style lang="scss" scoped>
.currency-page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #8b5cf6, #a855f7); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 32rpx; }
.rate-card { background: linear-gradient(135deg, #8b5cf6, #a855f7); border-radius: 24rpx; padding: 32rpx; margin-bottom: 24rpx; text-align: center; }
.rate-title { font-size: 24rpx; color: rgba(255,255,255,0.8); display: block; }
.rate-base { font-size: 36rpx; color: #fff; font-weight: 700; margin: 12rpx 0; display: block; }
.rate-update { font-size: 22rpx; color: rgba(255,255,255,0.7); display: block; }
.converter-card { background: #fff; border-radius: 24rpx; padding: 32rpx; margin-bottom: 24rpx; }
.conv-row { margin-bottom: 16rpx; }
.conv-label { font-size: 24rpx; color: #999; margin-bottom: 12rpx; display: block; }
.conv-input-wrap { display: flex; align-items: center; gap: 16rpx; }
.conv-input { flex: 1; height: 80rpx; border: 2rpx solid #e5e7eb; border-radius: 12rpx; padding: 0 20rpx; font-size: 32rpx; font-weight: 600; }
.conv-result { flex: 1; height: 80rpx; line-height: 80rpx; font-size: 32rpx; font-weight: 600; color: #8b5cf6; }
.conv-picker { padding: 12rpx 20rpx; background: #f5f5f5; border-radius: 12rpx; font-size: 28rpx; font-weight: 600; }
.conv-swap { text-align: center; margin: 16rpx 0; }
.swap-icon { font-size: 40rpx; color: #8b5cf6; }
.table-card { background: #fff; border-radius: 24rpx; padding: 24rpx; margin-bottom: 24rpx; }
.table-title { font-size: 26rpx; font-weight: 600; color: #333; margin-bottom: 16rpx; display: block; }
.table-header { display: flex; padding: 12rpx 0; border-bottom: 2rpx solid #f0f0f0; }
.table-row { display: flex; padding: 16rpx 0; border-bottom: 2rpx solid #f9f9f9; }
.th, .td { flex: 1; text-align: center; }
.th { font-size: 22rpx; color: #999; font-weight: 600; }
.td { font-size: 26rpx; color: #333; }
.td-code { font-weight: 600; }
.refresh-btn { background: linear-gradient(135deg, #8b5cf6, #a855f7); color: #fff; border-radius: 50rpx; font-size: 28rpx; }
</style>
