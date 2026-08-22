<template>
  <view class="packing-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">\u2190</text>
        <text class="nav-title">行李收纳</text>
        <text class="nav-icon" @click="openCreate">+</text>
      </view>
    </view>

    <view class="content">
      <view class="list-card" v-for="(list, lIdx) in lists" :key="list.id">
        <view class="list-header">
          <text class="list-title">{{ list.title }}</text>
          <text class="list-progress">{{ getProgress(list) }}</text>
        </view>
        <text class="list-subtitle">{{ list.subtitle }}</text>

        <view class="item-row" v-for="(item, iIdx) in list.items" :key="iIdx">
          <text class="item-check" @click="toggleItem(lIdx, iIdx)" :class="{ checked: item.checked }">{{ item.checked ? "\u2713" : "" }}</text>
          <text class="item-name" :class="{ done: item.checked }">{{ item.name }}</text>
          <text class="item-cat">{{ item.category }}</text>
        </view>

        <view class="list-actions">
          <text class="action-text" @click="openAddItem(lIdx)">添加物品</text>
          <text class="action-text danger" @click="deleteList(lIdx)">删除清单</text>
        </view>
      </view>

      <view class="empty" v-if="lists.length === 0">
        <text class="empty-emoji">🧳</text>
        <text class="empty-title">还没有收纳清单</text>
        <text class="empty-desc">点击右上角 + 创建清单</text>
      </view>
    </view>

    <!-- Create List Modal -->
    <view v-if="showCreate" class="mask" @click="showCreate = false">
      <view class="create-panel" @click.stop>
        <view class="panel-head">
          <text class="panel-title">新建清单</text>
          <text class="panel-close" @click="showCreate = false">\u00d7</text>
        </view>
        <view class="panel-body">
          <view class="form-row">
            <text class="form-l">标题</text>
            <input class="form-input" v-model="newList.title" placeholder="如：日本旅行" />
          </view>
          <view class="form-row">
            <text class="form-l">说明</text>
            <input class="form-input" v-model="newList.subtitle" placeholder="如：5天4夜" />
          </view>
          <view class="form-row column">
            <text class="form-l">快速模板</text>
            <view class="tpl-list">
              <view class="tpl-item" v-for="(tpl, idx) in templates" :key="idx" @click="useTemplate(tpl)">
                <text class="tpl-name">{{ tpl.name }}</text>
                <text class="tpl-meta">{{ tpl.items.length }} 项</text>
              </view>
            </view>
          </view>
        </view>
        <view class="panel-footer">
          <button class="btn-cancel" @click="showCreate = false">取消</button>
          <button class="btn-save" @click="createList">创建</button>
        </view>
      </view>
    </view>

    <!-- Add Item Modal -->
    <view v-if="showAddItem" class="mask" @click="showAddItem = false">
      <view class="create-panel" @click.stop>
        <view class="panel-head">
          <text class="panel-title">添加物品</text>
          <text class="panel-close" @click="showAddItem = false">\u00d7</text>
        </view>
        <view class="panel-body">
          <view class="form-row">
            <text class="form-l">物品名</text>
            <input class="form-input" v-model="newItem.name" placeholder="如：T恤" />
          </view>
          <view class="form-row">
            <text class="form-l">分类</text>
            <picker class="form-picker" :value="newItemCatIdx" :range="categories" @change="onCatChange">
              <text>{{ categories[newItemCatIdx] }}</text>
            </picker>
          </view>
        </view>
        <view class="panel-footer">
          <button class="btn-cancel" @click="showAddItem = false">取消</button>
          <button class="btn-save" @click="addItem">添加</button>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from "vue"

const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const lists = ref([])
const showCreate = ref(false)
const showAddItem = ref(false)
const currentListIdx = ref(0)
const newList = ref({ title: "", subtitle: "" })
const newItem = ref({ name: "", category: "衣物" })
const newItemCatIdx = ref(0)
const categories = ["衣物", "洗漱", "电子", "证件", "药品", "其他"]

const templates = [
  { name: "短途旅行 (2-3天)", items: [{ name: "T恤", category: "衣物" }, { name: "裤子", category: "衣物" }, { name: "内衣裤", category: "衣物" }, { name: "袜子", category: "衣物" }, { name: "牙刷牙膏", category: "洗漱" }, { name: "充电器", category: "电子" }, { name: "身份证", category: "证件" }, { name: "手机", category: "电子" }] },
  { name: "长途旅行 (5-7天)", items: [{ name: "T恤", category: "衣物" }, { name: "外套", category: "衣物" }, { name: "裤子", category: "衣物" }, { name: "内衣裤", category: "衣物" }, { name: "袜子", category: "衣物" }, { name: "运动鞋", category: "衣物" }, { name: "牙刷牙膏", category: "洗漱" }, { name: "洗发水", category: "洗漱" }, { name: "充电器", category: "电子" }, { name: "身份证", category: "证件" }, { name: "护照", category: "证件" }, { name: "常用药", category: "药品" }] },
  { name: "出差", items: [{ name: "衬衫", category: "衣物" }, { name: "西装", category: "衣物" }, { name: "皮鞋", category: "衣物" }, { name: "领带", category: "衣物" }, { name: "洗漱用品", category: "洗漱" }, { name: "笔记本电脑", category: "电子" }, { name: "充电器", category: "电子" }, { name: "身份证", category: "证件" }, { name: "名片", category: "证件" }] },
]

function goBack() { uni.navigateBack() }

function getProgress(list) {
  if (!list.items.length) return "0/0"
  const checked = list.items.filter(i => i.checked).length
  return checked + "/" + list.items.length
}

function toggleItem(lIdx, iIdx) {
  lists.value[lIdx].items[iIdx].checked = !lists.value[lIdx].items[iIdx].checked
  saveLists()
}

function openCreate() {
  newList.value = { title: "", subtitle: "" }
  showCreate.value = true
}

function openAddItem(lIdx) {
  currentListIdx.value = lIdx
  newItem.value = { name: "", category: "衣物" }
  newItemCatIdx.value = 0
  showAddItem.value = true
}

function onCatChange(e) {
  newItemCatIdx.value = e.detail.value
  newItem.value.category = categories[e.detail.value]
}

function useTemplate(tpl) {
  newList.value.title = tpl.name
}

function createList() {
  if (!newList.value.title.trim()) {
    uni.showToast({ title: "请输入标题", icon: "none" })
    return
  }
  const tpl = templates.find(t => t.name === newList.value.title)
  const items = tpl ? tpl.items.map(i => ({ ...i, checked: false })) : []
  lists.value.push({
    id: Date.now(),
    title: newList.value.title,
    subtitle: newList.value.subtitle,
    items: items,
  })
  saveLists()
  showCreate.value = false
}

function addItem() {
  if (!newItem.value.name.trim()) {
    uni.showToast({ title: "请输入物品名", icon: "none" })
    return
  }
  lists.value[currentListIdx.value].items.push({
    name: newItem.value.name,
    category: newItem.value.category,
    checked: false,
  })
  saveLists()
  showAddItem.value = false
}

function deleteList(lIdx) {
  uni.showModal({
    title: "删除清单",
    content: "确定删除此清单？",
    success: (res) => {
      if (res.confirm) {
        lists.value.splice(lIdx, 1)
        saveLists()
      }
    },
  })
}

function saveLists() {
  uni.setStorageSync("packing_lists", JSON.stringify(lists.value))
}

onMounted(() => {
  if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }
  const saved = uni.getStorageSync("packing_lists")
  if (saved) {
    try { lists.value = JSON.parse(saved) } catch (e) { lists.value = [] }
  }
})
</script>

<style lang="scss" scoped>
.packing-page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #f59e0b, #d97706); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.list-card { background: #fff; border-radius: 24rpx; padding: 28rpx; margin-bottom: 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.list-header { display: flex; justify-content: space-between; align-items: center; }
.list-title { font-size: 30rpx; font-weight: 600; color: #333; }
.list-progress { font-size: 24rpx; color: #f59e0b; font-weight: 600; }
.list-subtitle { font-size: 22rpx; color: #999; margin-top: 4rpx; display: block; margin-bottom: 16rpx; }
.item-row { display: flex; align-items: center; padding: 14rpx 0; border-bottom: 2rpx solid #f9f9f9; }
.item-check { width: 40rpx; height: 40rpx; border-radius: 50%; border: 2rpx solid #ddd; display: flex; align-items: center; justify-content: center; margin-right: 16rpx; font-size: 22rpx; color: #fff; flex-shrink: 0; }
.item-check.checked { background: #f59e0b; border-color: #f59e0b; }
.item-name { flex: 1; font-size: 26rpx; color: #333; }
.item-name.done { text-decoration: line-through; color: #999; }
.item-cat { font-size: 20rpx; color: #999; background: #f5f5f5; padding: 4rpx 12rpx; border-radius: 8rpx; }
.list-actions { display: flex; gap: 24rpx; margin-top: 16rpx; }
.action-text { font-size: 24rpx; color: #f59e0b; }
.action-text.danger { color: #ef4444; }
.empty { text-align: center; padding: 120rpx 40rpx; }
.empty-emoji { font-size: 80rpx; display: block; }
.empty-title { font-size: 28rpx; color: #333; margin-top: 24rpx; display: block; }
.empty-desc { font-size: 24rpx; color: #999; margin-top: 12rpx; display: block; }
.mask { position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 999; display: flex; align-items: flex-end; }
.create-panel { width: 100%; background: #fff; border-radius: 32rpx 32rpx 0 0; max-height: 80vh; display: flex; flex-direction: column; }
.panel-head { display: flex; justify-content: space-between; align-items: center; padding: 28rpx 32rpx; border-bottom: 2rpx solid #f0f0f0; }
.panel-title { font-size: 30rpx; font-weight: 600; color: #1a1a1a; }
.panel-close { font-size: 40rpx; color: #999; padding: 4rpx 8rpx; }
.panel-body { flex: 1; padding: 12rpx 32rpx; overflow-y: auto; }
.form-row { display: flex; align-items: center; padding: 20rpx 0; border-bottom: 2rpx solid #f8f8f8; }
.form-row.column { flex-direction: column; align-items: flex-start; gap: 12rpx; }
.form-l { font-size: 26rpx; color: #333; width: 140rpx; flex-shrink: 0; font-weight: 500; }
.form-input { flex: 1; font-size: 28rpx; color: #333; height: 56rpx; }
.form-picker { flex: 1; height: 56rpx; line-height: 56rpx; font-size: 26rpx; }
.tpl-list { display: flex; flex-direction: column; gap: 12rpx; width: 100%; }
.tpl-item { padding: 16rpx 20rpx; background: #f8f9ff; border-radius: 12rpx; display: flex; justify-content: space-between; align-items: center; }
.tpl-name { font-size: 26rpx; color: #333; font-weight: 500; }
.tpl-meta { font-size: 22rpx; color: #999; }
.panel-footer { display: flex; gap: 24rpx; padding: 24rpx 32rpx; border-top: 2rpx solid #f0f0f0; }
.btn-cancel { flex: 1; height: 80rpx; line-height: 80rpx; border-radius: 40rpx; background: #f5f5f5; color: #666; font-size: 28rpx; border: none; }
.btn-cancel::after { border: none; }
.btn-save { flex: 1; height: 80rpx; line-height: 80rpx; border-radius: 40rpx; background: linear-gradient(135deg, #f59e0b, #d97706); color: #fff; font-size: 28rpx; font-weight: 600; border: none; }
.btn-save::after { border: none; }
</style>
