<template>
  <view class="pc-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">比价计算</text><text class="nav-icon" @click="addItem">+</text></view>
    </view>
    <view class="content">
      <view class="hint-card"><text>添加多个商品，自动计算单价对比</text></view>
      <view class="pc-list">
        <view class="pc-item" v-for="(item, idx) in items" :key="idx">
          <view class="pc-row"><input class="pc-name" v-model="item.name" placeholder="商品名称" /><text class="pc-del" @click="items.splice(idx,1)">×</text></view>
          <view class="pc-inputs"><input class="pc-val" v-model="item.price" type="digit" placeholder="价格" /><input class="pc-val" v-model="item.qty" type="digit" placeholder="数量" /><input class="pc-unit" v-model="item.unit" placeholder="单位" /></view>
          <view class="pc-unit-price" v-if="item.price && item.qqty">单价: {{ (item.price / item.qqty).toFixed(4) }} 元/{{ item.unit || '件' }}</view>
        </view>
      </view>
      <view class="pc-result" v-if="ranked.length > 1">
        <text class="pc-r-title">性价比排行</text>
        <view class="pc-rank" v-for="(r, idx) in ranked" :key="idx">
          <text class="rank-num">{{ idx + 1 }}</text>
          <text class="rank-name">{{ r.name }}</text>
          <text class="rank-price">{{ r.unitPrice.toFixed(4) }}元</text>
          <text class="rank-tag" v-if="idx === 0">★ 最划算</text>
        </view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, computed, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const items = ref([{ name: "", price: "", qty: "", unit: "" }])
const ranked = computed(() => {
  const valid = items.value.filter(i => i.price && i.qty && parseFloat(i.qty) > 0)
  return valid.map(i => ({ name: i.name || "未命名", unitPrice: parseFloat(i.price) / parseFloat(i.qty) })).sort((a, b) => a.unitPrice - b.unitPrice)
})
function addItem() { items.value.push({ name: "", price: "", qty: "", unit: "" }) }
function goBack() { uni.navigateBack() }
onMounted(() => { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.pc-page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #ff9a9e, #fad0c4); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.hint-card { background: #fff; border-radius: 16rpx; padding: 20rpx; margin-bottom: 24rpx; font-size: 26rpx; color: #666; }
.pc-item { background: #fff; border-radius: 20rpx; padding: 20rpx; margin-bottom: 16rpx; }
.pc-row { display: flex; align-items: center; margin-bottom: 12rpx; }
.pc-name { flex: 1; font-size: 28rpx; font-weight: 600; }
.pc-del { font-size: 36rpx; color: #ccc; padding: 0 8rpx; }
.pc-inputs { display: flex; gap: 12rpx; }
.pc-val { flex: 1; height: 64rpx; background: #f5f7fb; border-radius: 12rpx; padding: 0 16rpx; font-size: 26rpx; text-align: center; }
.pc-unit { width: 100rpx; height: 64rpx; background: #f5f7fb; border-radius: 12rpx; padding: 0 8rpx; font-size: 26rpx; text-align: center; }
.pc-unit-price { font-size: 24rpx; color: #999; margin-top: 8rpx; text-align: right; }
.pc-result { background: #fff; border-radius: 20rpx; padding: 24rpx; margin-top: 24rpx; }
.pc-r-title { font-size: 28rpx; font-weight: 600; color: #333; margin-bottom: 16rpx; display: block; }
.pc-rank { display: flex; align-items: center; padding: 16rpx 0; border-bottom: 2rpx solid #f8f8f8; }
.rank-num { width: 48rpx; height: 48rpx; line-height: 48rpx; text-align: center; background: #f0f0f0; border-radius: 50%; font-size: 24rpx; font-weight: 700; margin-right: 16rpx; }
.pc-rank:first-child .rank-num { background: #ff6b6b; color: #fff; }
.rank-name { flex: 1; font-size: 26rpx; }
.rank-price { font-size: 26rpx; color: #ff6b6b; font-weight: 600; margin-right: 16rpx; }
.rank-tag { font-size: 22rpx; color: #ff6b6b; }
</style>
