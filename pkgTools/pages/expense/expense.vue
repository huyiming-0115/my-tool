<template>
  <view class="expense-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">←</text>
        <text class="nav-title">记账本</text>
        <text class="nav-icon" @click="openAdd">+</text>
      </view>
    </view>
    <view class="content">
      <view class="summary-card">
        <view class="summary-row">
          <view class="summary-item">
            <text class="s-label">月收入</text>
            <text class="s-value income">+{{ monthIncome }}</text>
          </view>
          <view class="summary-item">
            <text class="s-label">月支出</text>
            <text class="s-value expense">-{{ monthExpense }}</text>
          </view>
          <view class="summary-item">
            <text class="s-label">结余</text>
            <text class="s-value">{{ monthBalance }}</text>
          </view>
        </view>
      </view>
      <view class="filter-tabs">
        <text class="filter-tab" :class="{ active: filter === 'all' }" @click="filter = 'all'">全部</text>
        <text class="filter-tab" :class="{ active: filter === 'income' }" @click="filter = 'income'">收入</text>
        <text class="filter-tab" :class="{ active: filter === 'expense' }" @click="filter = 'expense'">支出</text>
      </view>
      <view class="record-list">
        <view class="record-item" v-for="(r, idx) in filteredRecords" :key="idx" @click="deleteRecord(r.id)">
          <view class="r-left">
            <text class="r-cat">{{ r.category }}</text>
            <text class="r-note" v-if="r.note">{{ r.note }}</text>
            <text class="r-date">{{ r.date }}</text>
          </view>
          <text class="r-amount" :class="r.type">{{ r.type === 'income' ? '+' : '-' }}{{ r.amount }}</text>
        </view>
      </view>
      <view class="empty-mini" v-if="filteredRecords.length === 0">
        <text>暂无记录</text>
      </view>
    </view>
    <view v-if="showAdd" class="mask" @click="showAdd = false">
      <view class="create-panel" @click.stop>
        <view class="panel-head">
          <text class="panel-title">添加记录</text>
          <text class="panel-close" @click="showAdd = false">×</text>
        </view>
        <view class="panel-body">
          <view class="type-toggle">
            <text class="type-btn" :class="{ active: newRecord.type === 'expense' }" @click="newRecord.type = 'expense'">支出</text>
            <text class="type-btn" :class="{ active: newRecord.type === 'income' }" @click="newRecord.type = 'income'">收入</text>
          </view>
          <view class="form-row">
            <text class="form-l">金额</text>
            <input class="form-input" v-model="newRecord.amount" type="digit" placeholder="0.00" />
          </view>
          <view class="form-row">
            <text class="form-l">分类</text>
            <picker class="form-picker" :value="newRecordCatIdx" :range="categories" @change="onCatChange">
              <text>{{ categories[newRecordCatIdx] }}</text>
            </picker>
          </view>
          <view class="form-row">
            <text class="form-l">备注</text>
            <input class="form-input" v-model="newRecord.note" placeholder="可选" />
          </view>
        </view>
        <view class="panel-footer">
          <button class="btn-cancel" @click="showAdd = false">取消</button>
          <button class="btn-save" @click="addRecord">保存</button>
        </view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, computed, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const records = ref([])
const filter = ref("all")
const showAdd = ref(false)
const newRecord = ref({ type: "expense", amount: "", category: "餐饮", note: "" })
const newRecordCatIdx = ref(0)
const categories = ["餐饮", "交通", "购物", "娱乐", "居住", "医疗", "工资", "奖金", "其他"]
const currentMonth = new Date().toISOString().slice(0, 7)
const monthIncome = computed(() => records.value.filter(r => r.date.slice(0, 7) === currentMonth && r.type === "income").reduce((s, r) => s + parseFloat(r.amount), 0).toFixed(2))
const monthExpense = computed(() => records.value.filter(r => r.date.slice(0, 7) === currentMonth && r.type === "expense").reduce((s, r) => s + parseFloat(r.amount), 0).toFixed(2))
const monthBalance = computed(() => (parseFloat(monthIncome.value) - parseFloat(monthExpense.value)).toFixed(2))
const filteredRecords = computed(() => {
  let list = [...records.value].sort((a, b) => b.date.localeCompare(a.date))
  if (filter.value !== "all") list = list.filter(r => r.type === filter.value)
  return list
})
function goBack() { uni.navigateBack() }
function openAdd() { newRecord.value = { type: "expense", amount: "", category: "餐饮", note: "" }; newRecordCatIdx.value = 0; showAdd.value = true }
function onCatChange(e) { newRecordCatIdx.value = e.detail.value; newRecord.value.category = categories[e.detail.value] }
function addRecord() {
  if (!newRecord.value.amount) { uni.showToast({ title: "请输入金额", icon: "none" }); return }
  records.value.push({ id: Date.now(), date: new Date().toISOString().slice(0, 10), type: newRecord.value.type, amount: parseFloat(newRecord.value.amount), category: newRecord.value.category, note: newRecord.value.note })
  saveData(); showAdd.value = false
}
function deleteRecord(id) {
  uni.showModal({ title: "删除", content: "确定删除？", success: (res) => { if (res.confirm) { records.value = records.value.filter(r => r.id !== id); saveData() } } })
}
function saveData() { uni.setStorageSync("expense_records", JSON.stringify(records.value)) }
onMounted(() => {
  if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }
  const saved = uni.getStorageSync("expense_records")
  if (saved) { try { records.value = JSON.parse(saved) } catch (e) {} }
})
</script>
<style lang="scss" scoped>
.expense-page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #f59e0b, #d97706); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.summary-card { background: linear-gradient(135deg, #f59e0b, #d97706); border-radius: 24rpx; padding: 32rpx; margin-bottom: 24rpx; }
.summary-row { display: flex; justify-content: space-between; }
.summary-item { text-align: center; flex: 1; }
.s-label { font-size: 22rpx; color: rgba(255,255,255,0.7); display: block; }
.s-value { font-size: 32rpx; color: #fff; font-weight: 700; display: block; margin-top: 8rpx; }
.s-value.income { color: #bbf7d0; }
.s-value.expense { color: #fecaca; }
.filter-tabs { display: flex; gap: 12rpx; margin-bottom: 24rpx; }
.filter-tab { padding: 12rpx 28rpx; background: #fff; border-radius: 30rpx; font-size: 24rpx; color: #666; }
.filter-tab.active { background: linear-gradient(135deg, #f59e0b, #d97706); color: #fff; }
.record-list { background: #fff; border-radius: 24rpx; padding: 8rpx 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.record-item { display: flex; justify-content: space-between; align-items: center; padding: 20rpx 0; border-bottom: 2rpx solid #f9f9f9; }
.r-left { flex: 1; }
.r-cat { font-size: 26rpx; color: #333; font-weight: 600; display: block; }
.r-note { font-size: 22rpx; color: #999; margin-top: 4rpx; display: block; }
.r-date { font-size: 20rpx; color: #ccc; margin-top: 4rpx; display: block; }
.r-amount { font-size: 28rpx; font-weight: 600; }
.r-amount.income { color: #22c55e; }
.r-amount.expense { color: #ef4444; }
.empty-mini { text-align: center; padding: 32rpx; font-size: 24rpx; color: #999; }
.mask { position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 999; display: flex; align-items: flex-end; }
.create-panel { width: 100%; background: #fff; border-radius: 32rpx 32rpx 0 0; max-height: 70vh; display: flex; flex-direction: column; }
.panel-head { display: flex; justify-content: space-between; align-items: center; padding: 28rpx 32rpx; border-bottom: 2rpx solid #f0f0f0; }
.panel-title { font-size: 30rpx; font-weight: 600; color: #1a1a1a; }
.panel-close { font-size: 40rpx; color: #999; padding: 4rpx 8rpx; }
.panel-body { flex: 1; padding: 12rpx 32rpx; overflow-y: auto; }
.type-toggle { display: flex; gap: 16rpx; margin: 20rpx 0; }
.type-btn { flex: 1; text-align: center; padding: 16rpx; background: #f5f5f5; border-radius: 16rpx; font-size: 26rpx; color: #666; }
.type-btn.active { background: linear-gradient(135deg, #f59e0b, #d97706); color: #fff; }
.form-row { display: flex; align-items: center; padding: 20rpx 0; border-bottom: 2rpx solid #f8f8f8; }
.form-l { font-size: 26rpx; color: #333; width: 120rpx; flex-shrink: 0; font-weight: 500; }
.form-input { flex: 1; font-size: 28rpx; color: #333; height: 56rpx; }
.form-picker { flex: 1; height: 56rpx; line-height: 56rpx; font-size: 26rpx; }
.panel-footer { display: flex; gap: 24rpx; padding: 24rpx 32rpx; border-top: 2rpx solid #f0f0f0; }
.btn-cancel { flex: 1; height: 80rpx; line-height: 80rpx; border-radius: 40rpx; background: #f5f5f5; color: #666; font-size: 28rpx; border: none; }
.btn-cancel::after { border: none; }
.btn-save { flex: 1; height: 80rpx; line-height: 80rpx; border-radius: 40rpx; background: linear-gradient(135deg, #f59e0b, #d97706); color: #fff; font-size: 28rpx; font-weight: 600; border: none; }
.btn-save::after { border: none; }
</style>
