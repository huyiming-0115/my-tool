<template>
  <view class="contact-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">←</text>
        <text class="nav-title">名片夹</text>
        <text class="nav-icon" @click="openAdd">+</text>
      </view>
    </view>
    <view class="content">
      <view class="search-bar"><input class="search-input" v-model="searchQuery" placeholder="搜索联系人..." /></view>
      <view class="contact-list">
        <view class="contact-item" v-for="(c, idx) in filteredContacts" :key="idx">
          <view class="c-avatar">{{ c.name.charAt(0) }}</view>
          <view class="c-info">
            <text class="c-name">{{ c.name }}</text>
            <text class="c-phone">{{ c.phone }}</text>
          </view>
          <view class="c-actions">
            <text class="c-call" @click="callPhone(c.phone)">☎</text>
            <text class="c-del" @click="deleteContact(c.id)">×</text>
          </view>
        </view>
      </view>
      <view class="empty-mini" v-if="filteredContacts.length === 0"><text>暂无联系人</text></view>
    </view>
    <view v-if="showAdd" class="mask" @click="showAdd = false">
      <view class="create-panel" @click.stop>
        <view class="panel-head"><text class="panel-title">添加联系人</text><text class="panel-close" @click="showAdd = false">×</text></view>
        <view class="panel-body">
          <view class="form-row"><text class="form-l">姓名</text><input class="form-input" v-model="newContact.name" placeholder="姓名" /></view>
          <view class="form-row"><text class="form-l">电话</text><input class="form-input" v-model="newContact.phone" type="number" placeholder="电话号码" /></view>
          <view class="form-row"><text class="form-l">公司</text><input class="form-input" v-model="newContact.company" placeholder="可选" /></view>
          <view class="form-row"><text class="form-l">备注</text><input class="form-input" v-model="newContact.note" placeholder="可选" /></view>
        </view>
        <view class="panel-footer"><button class="btn-cancel" @click="showAdd = false">取消</button><button class="btn-save" @click="addContact">保存</button></view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, computed, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const contacts = ref([])
const showAdd = ref(false)
const searchQuery = ref("")
const newContact = ref({ name: "", phone: "", company: "", note: "" })
const filteredContacts = computed(() => {
  let list = [...contacts.value].sort((a, b) => a.name.localeCompare(b.name))
  if (searchQuery.value) list = list.filter(c => c.name.includes(searchQuery.value) || c.phone.includes(searchQuery.value))
  return list
})
function goBack() { uni.navigateBack() }
function openAdd() { newContact.value = { name: "", phone: "", company: "", note: "" }; showAdd.value = true }
function addContact() {
  if (!newContact.value.name.trim() || !newContact.value.phone.trim()) { uni.showToast({ title: "请输入姓名和电话", icon: "none" }); return }
  contacts.value.push({ id: Date.now(), ...newContact.value }); saveData(); showAdd.value = false
}
function deleteContact(id) {
  uni.showModal({ title: "删除", content: "确定删除？", success: (r) => { if (r.confirm) { contacts.value = contacts.value.filter(c => c.id !== id); saveData() } } })
}
function callPhone(phone) { uni.makePhoneCall({ phoneNumber: phone }) }
function saveData() { uni.setStorageSync("contact_list", JSON.stringify(contacts.value)) }
onMounted(() => {
  if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }
  const saved = uni.getStorageSync("contact_list"); if (saved) { try { contacts.value = JSON.parse(saved) } catch (e) {} }
})
</script>
<style lang="scss" scoped>
.contact-page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #0ea5e9, #0284c7); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.search-bar { margin-bottom: 24rpx; }
.search-input { width: 100%; height: 72rpx; background: #fff; border-radius: 36rpx; padding: 0 28rpx; font-size: 26rpx; box-sizing: border-box; }
.contact-list { background: #fff; border-radius: 24rpx; padding: 8rpx 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.contact-item { display: flex; align-items: center; padding: 20rpx 0; border-bottom: 2rpx solid #f9f9f9; }
.contact-item:last-child { border-bottom: none; }
.c-avatar { width: 72rpx; height: 72rpx; border-radius: 50%; background: linear-gradient(135deg, #0ea5e9, #0284c7); display: flex; align-items: center; justify-content: center; color: #fff; font-size: 28rpx; font-weight: 600; margin-right: 16rpx; }
.c-info { flex: 1; }
.c-name { font-size: 26rpx; color: #333; font-weight: 600; display: block; }
.c-phone { font-size: 22rpx; color: #999; margin-top: 4rpx; display: block; }
.c-actions { display: flex; gap: 24rpx; }
.c-call { font-size: 32rpx; color: #0ea5e9; }
.c-del { font-size: 32rpx; color: #ccc; }
.empty-mini { text-align: center; padding: 32rpx; font-size: 24rpx; color: #999; }
.mask { position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 999; display: flex; align-items: flex-end; }
.create-panel { width: 100%; background: #fff; border-radius: 32rpx 32rpx 0 0; max-height: 70vh; display: flex; flex-direction: column; }
.panel-head { display: flex; justify-content: space-between; align-items: center; padding: 28rpx 32rpx; border-bottom: 2rpx solid #f0f0f0; }
.panel-title { font-size: 30rpx; font-weight: 600; color: #1a1a1a; }
.panel-close { font-size: 40rpx; color: #999; padding: 4rpx 8rpx; }
.panel-body { flex: 1; padding: 12rpx 32rpx; overflow-y: auto; }
.form-row { display: flex; align-items: center; padding: 20rpx 0; border-bottom: 2rpx solid #f8f8f8; }
.form-l { font-size: 26rpx; color: #333; width: 120rpx; flex-shrink: 0; font-weight: 500; }
.form-input { flex: 1; font-size: 28rpx; color: #333; height: 56rpx; }
.panel-footer { display: flex; gap: 24rpx; padding: 24rpx 32rpx; border-top: 2rpx solid #f0f0f0; }
.btn-cancel { flex: 1; height: 80rpx; line-height: 80rpx; border-radius: 40rpx; background: #f5f5f5; color: #666; font-size: 28rpx; border: none; }
.btn-cancel::after { border: none; }
.btn-save { flex: 1; height: 80rpx; line-height: 80rpx; border-radius: 40rpx; background: linear-gradient(135deg, #0ea5e9, #0284c7); color: #fff; font-size: 28rpx; font-weight: 600; border: none; }
.btn-save::after { border: none; }
</style>
