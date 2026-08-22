<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u4e94\u9669\u4e00\u91d1\u8ba1\u7b97\u5668</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="form-card"><text class="form-label">\u6708\u85aa (\u5143)</text><input class="form-input" type="digit" v-model="salary" placeholder="\u8f93\u5165\u6708\u85aa" /></view>
      <view class="form-card"><text class="form-label">\u79ef\u91d1\u6bd4\u4f8b (%): {{ fundRate }}</text><slider :value="fundRate" min="5" max="12" show-value @change="fundRate=Number($event.detail.value)"/></view>
      <view class="calc-btn" @click="calc"><text>\u8ba1\u7b97</text></view>
      <view class="result-card" v-if="total > 0">
        <view class="result-row"><text>\u4e2a\u4eba\u627f\u62c5:</text><text class="result-val">{{ personalTotal }} \u5143</text></view>
        <view class="result-row"><text>\u5355\u4f4d\u627f\u62c5:</text><text class="result-val">{{ companyTotal }} \u5143</text></view>
        <view class="result-row total"><text>\u5408\u8ba1:</text><text class="result-val">{{ total }} \u5143</text></view>
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
  if (s <= 0) { uni.showToast({ title: "\u8bf7\u8f93\u5165\u6708\u85aa", icon: "none" }); return }
  const f = fundRate.value / 100
  const rates = [
    {name:"\u517b\u8001\u4fdd\u9669", personal: 0.08, company: 0.16},
    {name:"\u533b\u7597\u4fdd\u9669", personal: 0.02, company: 0.08},
    {name:"\u5931\u4e1a\u4fdd\u9669", personal: 0.005, company: 0.005},
    {name:"\u5de5\u4f24\u4fdd\u9669", personal: 0, company: 0.004},
    {name:"\u751f\u80b2\u4fdd\u9669", personal: 0, company: 0.008},
    {name:"\u4f4f\u623f\u516c\u79ef\u91d1", personal: f, company: f}
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
