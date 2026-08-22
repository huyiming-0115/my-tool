<template>
  <view class="shopping-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">←</text>
        <text class="nav-title">购物清单</text>
        <text class="nav-icon" @click="openAdd">+</text>
      </view>
    </view>
    <view class="content">
      <view class="stats-row">
        <view class="stat-box"><text class="s-num">{{ unboughtCount }}</text><text class="s-label">未购</text></view>
        <view class="stat-box"><text class="s-num">{{ boughtCount }}</text><text class="s-label">已购</text></view>
        <view class="stat-box"><text class="s-num">¥{{ totalEstimate }}</text><text class="s-label">预估</text></view>
      </view>
      <view class="cat-tabs">
        <text class="cat-tab" :class="{ active: filterCat === 'all' }" @click="filterCat = 'all'">全部</text>
        <text class="cat-tab" :class="{ active: filterCat === c }" v-for="c in categories" :key="c" @click="filterCat = c">{{ c }}</text>
      </view>
      <view class="item-list">
        <view class="item-row" v-for="(item, idx) in filteredItems" :key="item.id">
          <text class="item-check" @click="toggleBought(item.id)" :class="{ bought: item.bought }">{{ item.bought ? "✓" : "" }}</text>
          <view class="item-info">
            <text class="item-name" :class="{ done: item.bought }">{{ item.name }}</text>
            <text class="item-meta">{{ item.category }} · {{ item.quantity }}件</text>
          </view>
          <text class="item-price">¥{{ item.price }}</text>
          <text class="item-del" @click="deleteItem(item.id)">×</text>
        </view>
      </view>
      <view class="empty-mini" v-if="filteredItems.length === 0"><text>暂无物品</text></view>
      <view class="clear-bar" v-if="boughtCount > 0"><text class="clear-btn" @click="clearBought">清除已购物品</text></view>
    </view>
    <view v-if="showAdd" class="mask" @click="showAdd = false">
      <view class="create-panel" @click.stop>
        <view class="panel-head"><text class="panel-title">添加物品</text><text class="panel-close" @click="showAdd = false">×</text></view>
        <view class="panel-body">
          <view class="form-row"><text class="form-l">名称</text><input class="form-input" v-model="newItem.name" placeholder="如：牛奶" /></view>
          <view class="form-row"><text class="form-l">数量</text><input class="form-input" v-model="newItem.quantity" type="number" placeholder="1" /></view>
          <view class="form-row"><text class="form-l">价格</text><input class="form-input" v-model="newItem.price" type="digit" placeholder="0.00" /></view>
          <view class="form-row"><text class="form-l">分类</text><picker class="form-picker" :value="newItemCatIdx" :range="categories" @change="onCatChange"><text>{{ categories[newItemCatIdx] }}</text></picker></view>
        </view>
        <view class="panel-footer"><button class="btn-cancel" @click="showAdd = false">取消</button><button class="btn-save" @click="addItem">添加</button></view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, computed, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const items = ref([])
const showAdd = ref(false)
const newItem = ref({ name: "", quantity: 1, price: "", category: "生鲜" })
const newItemCatIdx = ref(0)
const filterCat = ref("all")
const categories = ["生鲜", "日用品", "零食", "服装", "电子", "其他"]
const unboughtCount = computed(() => items.value.filter(i => !i.bought).length)
const boughtCount = computed(() => items.value.filter(i => i.bought).length)
const totalEstimate = computed(() => items.value.filter(i => !i.bought).reduce((s, i) => s + (parseFloat(i.price) || 0), 0).toFixed(2))
const filteredItems = computed(() => {
  let list = [...items.value].sort((a, b) => (a.bought ? 1 : 0) - (b.bought ? 1 : 0))
  if (filterCat.value !== "all") list = list.filter(i => i.category === filterCat.value)
  return list
})
function goBack() { uni.navigateBack() }
function openAdd() { newItem.value = { name: "", quantity: 1, price: "", category: "生鲜" }; newItemCatIdx.value = 0; showAdd.value = true }
function onCatChange(e) { newItemCatIdx.value = e.detail.value; newItem.value.category = categories[e.detail.value] }
function addItem() {
  if (!newItem.value.name.trim()) { uni.showToast({ title: "请输入名称", icon: "none" }); return }
  items.value.push({ id: Date.now(), name: newItem.value.name, quantity: parseInt(newItem.value.quantity) || 1, price: parseFloat(newItem.value.price) || 0, category: newItem.value.category, bought: false })
  saveData(); showAdd.value = false
}
function toggleBought(id) { const item = items.value.find(i => i.id === id); if (item) { item.bought = !item.bought; saveData() } }
function deleteItem(id) { items.value = items.value.filter(i => i.id !== id); saveData() }
function clearBought() { items.value = items.value.filter(i => !i.bought); saveData() }
function saveData() { uni.setStorageSync("shopping_items", JSON.stringify(items.value)) }
onMounted(() => {
  if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }
  const saved = uni.getStorageSync("shopping_items"); if (saved) { try { items.value = JSON.parse(saved) } catch (e) {} }
})
</script>
<style lang="scss" scoped>
.shopping-page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #14b8a6, #0d9488); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.stats-row { display: flex; gap: 16rpx; margin-bottom: 24rpx; }
.stat-box { flex: 1; background: #fff; border-radius: 20rpx; padding: 24rpx; text-align: center; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.s-num { font-size: 28rpx; font-weight: 700; color: #14b8a6; display: block; }
.s-label { font-size: 20rpx; color: #999; margin-top: 4rpx; display: block; }
.cat-tabs { display: flex; flex-wrap: wrap; gap: 12rpx; margin-bottom: 24rpx; }
.cat-tab { padding: 10rpx 24rpx; background: #fff; border-radius: 30rpx; font-size: 24rpx; color: #666; }
.cat-tab.active { background: linear-gradient(135deg, #14b8a6, #0d9488); color: #fff; }
.item-list { background: #fff; border-radius: 24rpx; padding: 8rpx 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.item-row { display: flex; align-items: center; padding: 20rpx 0; border-bottom: 2rpx solid #f9f9f9; }
.item-check { width: 40rpx; height: 40rpx; border-radius: 50%; border: 2rpx solid #ddd; display: flex; align-items: center; justify-content: center; font-size: 22rpx; color: #fff; margin-right: 16rpx; }
.item-check.bought { background: #14b8a6; border-color: #14b8a6; }
.item-info { flex: 1; }
.item-name { font-size: 26rpx; color: #333; display: block; }
.item-name.done { text-decoration: line-through; color: #999; }
.item-meta { font-size: 20rpx; color: #999; margin-top: 4rpx; display: block; }
.item-price { font-size: 24rpx; color: #14b8a6; font-weight: 600; margin-right: 16rpx; }
.item-del { font-size: 32rpx; color: #ccc; }
.empty-mini { text-align: center; padding: 32rpx; font-size: 24rpx; color: #999; }
.clear-bar { text-align: center; margin-top: 24rpx; }
.clear-btn { font-size: 24rpx; color: #ef4444; }
.mask { position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 999; display: flex; align-items: flex-end; }
.create-panel { width: 100%; background: #fff; border-radius: 32rpx 32rpx 0 0; max-height: 70vh; display: flex; flex-direction: column; }
.panel-head { display: flex; justify-content: space-between; align-items: center; padding: 28rpx 32rpx; border-bottom: 2rpx solid #f0f0f0; }
.panel-title { font-size: 30rpx; font-weight: 600; color: #1a1a1a; }
.panel-close { font-size: 40rpx; color: #999; padding: 4rpx 8rpx; }
.panel-body { flex: 1; padding: 12rpx 32rpx; overflow-y: auto; }
.form-row { display: flex; align-items: center; padding: 20rpx 0; border-bottom: 2rpx solid #f8f8f8; }
.form-l { font-size: 26rpx; color: #333; width: 120rpx; flex-shrink: 0; font-weight: 500; }
.form-input { flex: 1; font-size: 28rpx; color: #333; height: 56rpx; }
.form-picker { flex: 1; height: 56rpx; line-height: 56rpx; font-size: 26rpx; }
.panel-footer { display: flex; gap: 24rpx; padding: 24rpx 32rpx; border-top: 2rpx solid #f0f0f0; }
.btn-cancel { flex: 1; height: 80rpx; line-height: 80rpx; border-radius: 40rpx; background: #f5f5f5; color: #666; font-size: 28rpx; border: none; }
.btn-cancel::after { border: none; }
.btn-save { flex: 1; height: 80rpx; line-height: 80rpx; border-radius: 40rpx; background: linear-gradient(135deg, #14b8a6, #0d9488); color: #fff; font-size: 28rpx; font-weight: 600; border: none; }
.btn-save::after { border: none; }
</style>
