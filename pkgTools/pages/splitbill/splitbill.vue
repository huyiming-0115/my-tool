<template>
  <view class="sb-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">分账计算</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="form-card">
        <view class="form-row"><text class="form-l">总金额</text><input class="form-input" v-model="total" type="digit" placeholder="200" /></view>
        <view class="form-row"><text class="form-l">人数</text><input class="form-input" v-model="people" type="number" placeholder="4" /></view>
        <view class="form-row" v-if="hasDiscount"><text class="form-l">折扣(%)</text><input class="form-input" v-model="discount" type="digit" placeholder="100 = 免单" /></view>
        <view class="toggle-row"><text class="toggle-label">添加折扣</text><switch :checked="hasDiscount" @change="hasDiscount = $event.detail.value" color="#667eea" /></view>
        <view class="calc-trigger" @click="calc"><text>计算</text></view>
      </view>
      <view class="result-card" v-if="result">
        <view class="sb-main"><text class="sb-label">每人应付</text><text class="sb-value">{{ result.perPerson }}</text><text class="sb-unit">元</text></view>
        <view class="sb-detail"><text>总额 {{ result.total }}元 × {{ result.people }}人 {{ result.discountText }}</text></view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const total = ref("")
const people = ref("4")
const discount = ref("100")
const hasDiscount = ref(false)
const result = ref(null)
function calc() {
  const t = parseFloat(total.value); const p = parseInt(people.value)
  if (!t || !p) { uni.showToast({ title: "请填写完整", icon: "none" }); return }
  const d = hasDiscount.value ? (parseFloat(discount.value) / 100) : 1
  const final = t * d
  result.value = { perPerson: (final / p).toFixed(2), total: t, people: p, discountText: hasDiscount.value ? "(" + discount.value + "%折扣)" : "" }
}
function goBack() { uni.navigateBack() }
onMounted(() => { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.sb-page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #a18cd1, #fbc2eb); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.form-card { background: #fff; border-radius: 24rpx; padding: 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); margin-bottom: 24rpx; }
.form-row { display: flex; align-items: center; padding: 20rpx 0; border-bottom: 2rpx solid #f8f8f8; }
.form-l { font-size: 28rpx; color: #333; width: 160rpx; flex-shrink: 0; font-weight: 500; }
.form-input { flex: 1; font-size: 30rpx; height: 56rpx; text-align: right; }
.toggle-row { display: flex; align-items: center; justify-content: space-between; padding: 20rpx 0; }
.toggle-label { font-size: 28rpx; color: #333; }
.calc-trigger { background: linear-gradient(135deg, #a18cd1, #fbc2eb); border-radius: 16rpx; padding: 24rpx; text-align: center; margin-top: 24rpx; }
.calc-trigger text { font-size: 30rpx; color: #fff; font-weight: 600; }
.result-card { background: linear-gradient(135deg, #a18cd1, #fbc2eb); border-radius: 24rpx; padding: 40rpx; text-align: center; }
.sb-main { margin-bottom: 16rpx; }
.sb-label { font-size: 24rpx; color: rgba(255,255,255,0.8); display: block; }
.sb-value { font-size: 72rpx; color: #fff; font-weight: 700; display: block; }
.sb-unit { font-size: 24rpx; color: rgba(255,255,255,0.8); }
.sb-detail { font-size: 24rpx; color: rgba(255,255,255,0.7); }
</style>
