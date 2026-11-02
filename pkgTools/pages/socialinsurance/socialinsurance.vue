
<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">五险一金计算器</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="si-card">
        <text class="si-label">月薪（元）</text>
        <input class="si-input" type="digit" v-model="salary" placeholder="请输入月薪" />
      </view>
      <view class="si-card">
        <text class="si-label">社保缴费基数（元）</text>
        <input class="si-input" type="digit" v-model="base" placeholder="默认为月薪" />
      </view>
      <view class="si-card">
        <text class="si-label">公积金比例</text>
        <view class="ratio-row">
          <view class="ratio-item" v-for="r in ratios" :key="r" :class="{active: fundRatio===r}" @click="fundRatio=r"><text>{{r}}%</text></view>
        </view>
      </view>
      <view class="si-btn" @click="calculate"><text>计算</text></view>
      <view class="result-card" v-if="showResult">
        <text class="result-title">缴费明细</text>
        <view class="result-section">
          <text class="section-title">个人承担</text>
          <view class="result-row"><text>养老保险 (8%)</text><text>{{personal.pension}}</text></view>
          <view class="result-row"><text>医疗保险 (2%)</text><text>{{personal.medical}}</text></view>
          <view class="result-row"><text>失业保险 (0.5%)</text><text>{{personal.unemployment}}</text></view>
          <view class="result-row"><text>公积金 ({{fundRatio}}%)</text><text>{{personal.fund}}</text></view>
          <view class="result-row total"><text>个人合计</text><text>{{personal.total}}</text></view>
        </view>
        <view class="result-section">
          <text class="section-title">公司承担</text>
          <view class="result-row"><text>养老保险 (16%)</text><text>{{company.pension}}</text></view>
          <view class="result-row"><text>医疗保险 (9%)</text><text>{{company.medical}}</text></view>
          <view class="result-row"><text>失业保险 (0.5%)</text><text>{{company.unemployment}}</text></view>
          <view class="result-row"><text>工伤保险 (0.4%)</text><text>{{company.injury}}</text></view>
          <view class="result-row"><text>生育保险 (0.8%)</text><text>{{company.birth}}</text></view>
          <view class="result-row"><text>公积金 ({{fundRatio}}%)</text><text>{{company.fund}}</text></view>
          <view class="result-row total"><text>公司合计</text><text>{{company.total}}</text></view>
        </view>
        <view class="result-section">
          <view class="result-row total"><text>税前工资</text><text>{{salary}}元</text></view>
          <view class="result-row total"><text>税后工资(估)</text><text>{{netSalary}}元</text></view>
        </view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, reactive, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const salary = ref("")
const base = ref("")
const fundRatio = ref(12)
const ratios = [5, 8, 10, 12]
const showResult = ref(false)
const personal = reactive({})
const company = reactive({})
const netSalary = ref("0")
function calculate() {
  var s = parseFloat(salary.value) || 0
  var b = parseFloat(base.value) || s
  if (s <= 0) return
  var f = fundRatio.value / 100
  personal.pension = (b * 0.08).toFixed(2)
  personal.medical = (b * 0.02).toFixed(2)
  personal.unemployment = (b * 0.005).toFixed(2)
  personal.fund = (b * f).toFixed(2)
  personal.total = (b * (0.08 + 0.02 + 0.005 + f)).toFixed(2)
  company.pension = (b * 0.16).toFixed(2)
  company.medical = (b * 0.09).toFixed(2)
  company.unemployment = (b * 0.005).toFixed(2)
  company.injury = (b * 0.004).toFixed(2)
  company.birth = (b * 0.008).toFixed(2)
  company.fund = (b * f).toFixed(2)
  company.total = (b * (0.16 + 0.09 + 0.005 + 0.004 + 0.008 + f)).toFixed(2)
  var taxable = s - parseFloat(personal.total) - 5000
  var tax = 0
  if (taxable > 0) {
    if (taxable <= 3000) tax = taxable * 0.03
    else if (taxable <= 12000) tax = taxable * 0.1 - 210
    else if (taxable <= 25000) tax = taxable * 0.2 - 1410
    else tax = taxable * 0.25 - 2660
  }
  netSalary.value = (s - parseFloat(personal.total) - tax).toFixed(2)
  showResult.value = true
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #667eea, #764ba2); }
.custom-nav { background: linear-gradient(135deg, #667eea, #764ba2); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 32rpx; }
.si-card { background: rgba(255,255,255,0.15); border-radius: 20rpx; padding: 24rpx; margin-bottom: 20rpx; backdrop-filter: blur(10px); }
.si-label { color: rgba(255,255,255,0.8); font-size: 26rpx; display: block; margin-bottom: 12rpx; }
.si-input { background: rgba(255,255,255,0.2); border-radius: 12rpx; padding: 16rpx 20rpx; font-size: 32rpx; color: #fff; font-weight: 600; }
.ratio-row { display: flex; gap: 16rpx; }
.ratio-item { flex: 1; text-align: center; padding: 12rpx; background: rgba(255,255,255,0.1); border-radius: 12rpx; }
.ratio-item text { color: rgba(255,255,255,0.7); font-size: 28rpx; }
.ratio-item.active { background: #fff; }
.ratio-item.active text { color: #764ba2; font-weight: 600; }
.si-btn { background: #fff; border-radius: 16rpx; padding: 24rpx; text-align: center; margin: 32rpx 0; }
.si-btn text { color: #764ba2; font-size: 32rpx; font-weight: 700; }
.result-card { background: rgba(255,255,255,0.15); border-radius: 20rpx; padding: 28rpx; backdrop-filter: blur(10px); }
.result-title { color: #fff; font-size: 32rpx; font-weight: 700; display: block; margin-bottom: 20rpx; }
.result-section { margin-bottom: 20rpx; }
.section-title { color: rgba(255,255,255,0.7); font-size: 24rpx; display: block; margin-bottom: 12rpx; }
.result-row { display: flex; justify-content: space-between; padding: 8rpx 0; }
.result-row text { color: #fff; font-size: 26rpx; }
.result-row.total { border-top: 1rpx solid rgba(255,255,255,0.2); padding-top: 12rpx; margin-top: 8rpx; font-weight: 600; }
</style>
