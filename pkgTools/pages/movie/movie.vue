<template>
  <view class="movie-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">←</text>
        <text class="nav-title">影视清单</text>
        <text class="nav-icon" @click="openAdd">+</text>
      </view>
    </view>
    <view class="content">
      <view class="stats-row">
        <view class="stat-box"><text class="s-num">{{ wantCount }}</text><text class="s-label">想看</text></view>
        <view class="stat-box"><text class="s-num">{{ watchedCount }}</text><text class="s-label">已看</text></view>
        <view class="stat-box"><text class="s-num">{{ avgRating }}</text><text class="s-label">平均分</text></view>
      </view>
      <view class="filter-tabs">
        <text class="filter-tab" :class="{ active: filter === 'want' }" @click="filter = 'want'">想看</text>
        <text class="filter-tab" :class="{ active: filter === 'watched' }" @click="filter = 'watched'">已看</text>
      </view>
      <view class="search-bar"><input class="search-input" v-model="searchQuery" placeholder="搜索影视..." /></view>
      <view class="movie-list">
        <view class="movie-item" v-for="(m, idx) in filteredMovies" :key="idx">
          <view class="m-left">
            <text class="m-name">{{ m.name }}</text>
            <text class="m-type">{{ m.type }}</text>
            <text class="m-comment" v-if="m.comment">{{ m.comment }}</text>
          </view>
          <view class="m-right">
            <text class="m-rating" v-if="m.rating">{{ m.rating }}分</text>
            <text class="m-toggle" @click="toggleStatus(m.id)">{{ m.watched ? "←想看" : "已看→" }}</text>
            <text class="m-del" @click="deleteMovie(m.id)">×</text>
          </view>
        </view>
      </view>
      <view class="empty-mini" v-if="filteredMovies.length === 0"><text>暂无记录</text></view>
    </view>
    <view v-if="showAdd" class="mask" @click="showAdd = false">
      <view class="create-panel" @click.stop>
        <view class="panel-head"><text class="panel-title">添加影视</text><text class="panel-close" @click="showAdd = false">×</text></view>
        <view class="panel-body">
          <view class="form-row"><text class="form-l">名称</text><input class="form-input" v-model="newMovie.name" placeholder="影视名称" /></view>
          <view class="form-row"><text class="form-l">类型</text><picker class="form-picker" :value="newMovieTypeIdx" :range="movieTypes" @change="onTypeChange"><text>{{ movieTypes[newMovieTypeIdx] }}</text></picker></view>
          <view class="form-row" v-if="newMovie.watched"><text class="form-l">评分</text><input class="form-input" v-model="newMovie.rating" type="number" placeholder="1-10" /></view>
          <view class="form-row" v-if="newMovie.watched"><text class="form-l">短评</text><input class="form-input" v-model="newMovie.comment" placeholder="可选" /></view>
          <view class="form-row"><text class="form-l">状态</text><switch :checked="newMovie.watched" @change="newMovie.watched = $event.detail.value" color="#7c3aed" /></view>
        </view>
        <view class="panel-footer"><button class="btn-cancel" @click="showAdd = false">取消</button><button class="btn-save" @click="addMovie">添加</button></view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, computed, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const movies = ref([])
const showAdd = ref(false)
const filter = ref("want")
const searchQuery = ref("")
const newMovie = ref({ name: "", type: "电影", watched: false, rating: "", comment: "" })
const newMovieTypeIdx = ref(0)
const movieTypes = ["电影", "电视剧", "动漫", "纪录片", "综艺"]
const wantCount = computed(() => movies.value.filter(m => !m.watched).length)
const watchedCount = computed(() => movies.value.filter(m => m.watched).length)
const avgRating = computed(() => {
  const rated = movies.value.filter(m => m.watched && m.rating)
  if (!rated.length) return "-"
  return (rated.reduce((s, m) => s + parseFloat(m.rating), 0) / rated.length).toFixed(1)
})
const filteredMovies = computed(() => {
  let list = movies.value.filter(m => filter.value === "want" ? !m.watched : m.watched)
  if (searchQuery.value) list = list.filter(m => m.name.includes(searchQuery.value))
  return list
})
function goBack() { uni.navigateBack() }
function openAdd() { newMovie.value = { name: "", type: "电影", watched: false, rating: "", comment: "" }; newMovieTypeIdx.value = 0; showAdd.value = true }
function onTypeChange(e) { newMovieTypeIdx.value = e.detail.value; newMovie.value.type = movieTypes[e.detail.value] }
function addMovie() {
  if (!newMovie.value.name.trim()) { uni.showToast({ title: "请输入名称", icon: "none" }); return }
  movies.value.push({ id: Date.now(), name: newMovie.value.name, type: newMovie.value.type, watched: newMovie.value.watched, rating: parseFloat(newMovie.value.rating) || 0, comment: newMovie.value.comment })
  saveData(); showAdd.value = false
}
function toggleStatus(id) { const m = movies.value.find(m => m.id === id); if (m) { m.watched = !m.watched; saveData() } }
function deleteMovie(id) {
  uni.showModal({ title: "删除", content: "确定删除？", success: (r) => { if (r.confirm) { movies.value = movies.value.filter(m => m.id !== id); saveData() } } })
}
function saveData() { uni.setStorageSync("movie_list", JSON.stringify(movies.value)) }
onMounted(() => {
  if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }
  const saved = uni.getStorageSync("movie_list"); if (saved) { try { movies.value = JSON.parse(saved) } catch (e) {} }
})
</script>
<style lang="scss" scoped>
.movie-page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #7c3aed, #6d28d9); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.stats-row { display: flex; gap: 16rpx; margin-bottom: 24rpx; }
.stat-box { flex: 1; background: #fff; border-radius: 20rpx; padding: 24rpx; text-align: center; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.s-num { font-size: 28rpx; font-weight: 700; color: #7c3aed; display: block; }
.s-label { font-size: 20rpx; color: #999; margin-top: 4rpx; display: block; }
.filter-tabs { display: flex; gap: 12rpx; margin-bottom: 24rpx; }
.filter-tab { padding: 12rpx 28rpx; background: #fff; border-radius: 30rpx; font-size: 24rpx; color: #666; }
.filter-tab.active { background: linear-gradient(135deg, #7c3aed, #6d28d9); color: #fff; }
.search-bar { margin-bottom: 24rpx; }
.search-input { width: 100%; height: 72rpx; background: #fff; border-radius: 36rpx; padding: 0 28rpx; font-size: 26rpx; box-sizing: border-box; }
.movie-list { background: #fff; border-radius: 24rpx; padding: 8rpx 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.movie-item { display: flex; justify-content: space-between; align-items: flex-start; padding: 20rpx 0; border-bottom: 2rpx solid #f9f9f9; }
.movie-item:last-child { border-bottom: none; }
.m-left { flex: 1; }
.m-name { font-size: 26rpx; color: #333; font-weight: 600; display: block; }
.m-type { font-size: 20rpx; color: #999; margin-top: 4rpx; display: block; }
.m-comment { font-size: 20rpx; color: #666; margin-top: 8rpx; display: block; }
.m-right { display: flex; align-items: center; gap: 16rpx; }
.m-rating { font-size: 22rpx; color: #f59e0b; font-weight: 600; }
.m-toggle { font-size: 20rpx; color: #7c3aed; }
.m-del { font-size: 32rpx; color: #ccc; }
.empty-mini { text-align: center; padding: 32rpx; font-size: 24rpx; color: #999; }
.mask { position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 999; display: flex; align-items: flex-end; }
.create-panel { width: 100%; background: #fff; border-radius: 32rpx 32rpx 0 0; max-height: 80vh; display: flex; flex-direction: column; }
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
.btn-save { flex: 1; height: 80rpx; line-height: 80rpx; border-radius: 40rpx; background: linear-gradient(135deg, #7c3aed, #6d28d9); color: #fff; font-size: 28rpx; font-weight: 600; border: none; }
.btn-save::after { border: none; }
</style>
