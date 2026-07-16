<template>
  <view class="notes-page">
    <!-- 自定义导航 -->
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">‹</text>
        <text class="nav-title">📝 我的笔记</text>
      </view>
    </view>

    <!-- 搜索栏 -->
    <view class="search-bar">
      <view class="search-wrap">
        <text class="search-icon">🔍</text>
        <input
          class="search-input"
          v-model="searchText"
          placeholder="搜索笔记标题或内容..."
          placeholder-class="ph"
          confirm-type="search"
        />
        <text v-if="searchText" class="clear-btn" @click="searchText = ''">✕</text>
      </view>
    </view>

    <!-- 标签筛选 -->
    <scroll-view class="tags-scroll" scroll-x v-if="allTags.length > 0">
      <view class="tags-row">
        <text
          class="tag-chip"
          :class="{ on: activeTag === '' }"
          @click="activeTag = ''"
        >全部</text>
        <text
          v-for="tag in allTags"
          :key="tag"
          class="tag-chip"
          :class="{ on: activeTag === tag }"
          @click="activeTag = (activeTag === tag ? '' : tag)"
        ># {{ tag }}</text>
      </view>
    </scroll-view>

    <!-- 笔记列表 -->
    <view class="note-list" v-if="filteredNotes.length > 0">
      <view
        class="note-card"
        v-for="note in filteredNotes"
        :key="note.id"
        @click="openNote(note.id)"
        @longpress="showNoteMenu(note)"
      >
        <view class="card-head">
          <text class="note-title">{{ note.title || '无标题' }}</text>
          <view v-if="note.pinned" class="pin-badge">📌</view>
        </view>
        <text class="note-excerpt">{{ note.excerpt }}</text>
        <view class="card-foot">
          <view class="tags-inline">
            <text v-for="t in note.tags.slice(0, 3)" :key="t" class="mini-tag">#{{ t }}</text>
          </view>
          <text class="note-date">{{ formatDate(note.updatedAt) }}</text>
        </view>
      </view>
    </view>

    <!-- 空状态 -->
    <view v-else class="empty-state">
      <view class="empty-emoji">{{ searchText ? '🔍' : (activeTag ? '🏷️' : '📝') }}</view>
      <text class="empty-title">
        {{ searchText ? '没找到相关笔记' : (activeTag ? '这个标签下没内容' : '还没有笔记') }}
      </text>
      <text class="empty-desc">点击右上角 + 开始记录灵感</text>
      <view v-if="!searchText && !activeTag" class="empty-btn" @click="createNote">+ 新建笔记</view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from "vue"
import { loadNotes, saveNotes, makeExcerpt, formatDate, getTags } from "@/utils/notes-store.js"

const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20

const goBack = () => { uni.navigateBack() }
const notes = ref([])
const searchText = ref("")
const activeTag = ref("")
const sortDesc = ref(true)

const allTags = computed(() => getTags(notes.value))

const filteredNotes = computed(() => {
  let list = notes.value.slice()
  // 筛选标签
  if (activeTag.value) {
    list = list.filter((n) => n.tags.includes(activeTag.value))
  }
  // 搜索
  const q = searchText.value.trim().toLowerCase()
  if (q) {
    list = list.filter((n) =>
      (n.title || "").toLowerCase().includes(q) ||
      (n.content || "").toLowerCase().includes(q)
    )
  }
  // 置顶 + 时间排序
  list.sort((a, b) => {
    if (a.pinned !== b.pinned) return a.pinned ? -1 : 1
    const ta = new Date(a.updatedAt).getTime()
    const tb = new Date(b.updatedAt).getTime()
    return sortDesc.value ? tb - ta : ta - tb
  })
  return list
})

function toggleSort() {
  sortDesc.value = !sortDesc.value
  uni.showToast({ title: sortDesc.value ? "最新优先" : "最早优先", icon: "none" })
}

function createNote() {
  uni.navigateTo({ url: "/pkgTools/pages/notes/detail" })
}

function openNote(id) {
  uni.navigateTo({ url: `/pkgTools/pages/notes/detail?id=${id}` })
}

function showNoteMenu(note) {
  const items = []
  items.push(note.pinned ? "取消置顶" : "📌 置顶")
  items.push("🗑️ 删除")
  uni.showActionSheet({
    itemList: items,
    success: (res) => {
      if (res.tapIndex === 0) {
        const n = notes.value.find((x) => x.id === note.id)
        if (n) { n.pinned = !n.pinned; n.updatedAt = new Date().toISOString(); saveNotes(notes.value) }
      } else if (res.tapIndex === 1) {
        uni.showModal({
          title: "删除笔记",
          content: `确认删除「${note.title || '无标题'}」？`,
          success: (r) => {
            if (r.confirm) {
              notes.value = notes.value.filter((x) => x.id !== note.id)
              saveNotes(notes.value)
              uni.showToast({ title: "已删除", icon: "success" })
            }
          },
        })
      }
    },
  })
}

onMounted(() => {
  if (!uni.getStorageSync("isLoggedIn")) {
    uni.reLaunch({ url: "/pages/login/login" })
    return
  }
  notes.value = loadNotes()
})
</script>

<style lang="scss" scoped>
.notes-page {
  min-height: 100vh;
  background: #f5f7fb;
}

/* 自定义导航 */
.custom-nav {
  background: linear-gradient(135deg, #4a6cf7 0%, #7c3aed 100%);
  width: 100%;
}
.nav-row {
  height: 88rpx;
  display: flex;
  align-items: center;
  padding: 0 32rpx;
}
.nav-title {
  font-size: 34rpx;
  color: #fff;
  font-weight: 600;
}
.nav-icon {
  width: 64rpx;
  height: 64rpx;
  line-height: 64rpx;
  text-align: center;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  color: #fff;
  font-size: 32rpx;
  font-weight: 700;
}
.nav-icon.add { font-size: 40rpx; }


/* 搜索 */
.search-bar {
  padding: 24rpx 32rpx 16rpx;
}
.search-wrap {
  display: flex;
  align-items: center;
  background: #fff;
  border-radius: 40rpx;
  padding: 0 28rpx;
  height: 72rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.04);
}
.search-icon {
  font-size: 28rpx;
  margin-right: 12rpx;
}
.search-input {
  flex: 1;
  font-size: 28rpx;
  color: #333;
  height: 56rpx;
}
.ph { color: #ccc; }
.clear-btn {
  font-size: 24rpx;
  color: #999;
  padding: 8rpx;
}

/* 标签 */
.tags-scroll {
  white-space: nowrap;
  padding: 0 32rpx;
  margin-bottom: 20rpx;
}
.tags-row {
  display: inline-flex;
  gap: 16rpx;
}
.tag-chip {
  display: inline-block;
  padding: 10rpx 24rpx;
  border-radius: 28rpx;
  font-size: 24rpx;
  background: #fff;
  color: #666;
  border: 2rpx solid #e8e8e8;
  transition: all 0.2s;
}
.tag-chip.on {
  background: #4a6cf7;
  color: #fff;
  border-color: #4a6cf7;
}

/* 笔记列表 */
.note-list {
  padding: 0 24rpx 40rpx;
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}
.note-card {
  background: #fff;
  border-radius: 24rpx;
  padding: 28rpx 28rpx 20rpx;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.04);
  transition: transform 0.15s;
}
.note-card:active { transform: scale(0.98); }

.card-head {
  display: flex;
  align-items: center;
  margin-bottom: 12rpx;
}
.note-title {
  font-size: 30rpx;
  font-weight: 600;
  color: #1a1a1a;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.pin-badge { font-size: 24rpx; margin-left: 12rpx; }

.note-excerpt {
  font-size: 26rpx;
  color: #666;
  line-height: 1.7;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: 16rpx;
}

.card-foot {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-top: 2rpx solid #f5f5f5;
  padding-top: 12rpx;
}
.tags-inline {
  display: flex;
  gap: 8rpx;
  flex: 1;
  overflow: hidden;
}
.mini-tag {
  font-size: 20rpx;
  color: #7c3aed;
  background: #f3f0ff;
  padding: 2rpx 12rpx;
  border-radius: 12rpx;
}
.note-date {
  font-size: 22rpx;
  color: #bbb;
  flex-shrink: 0;
  margin-left: 16rpx;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 160rpx 40rpx;
}
.empty-emoji { font-size: 100rpx; display: block; }
.empty-title { font-size: 30rpx; font-weight: 600; color: #333; display: block; margin-top: 24rpx; }
.empty-desc { font-size: 24rpx; color: #999; display: block; margin-top: 12rpx; }
.empty-btn {
  display: inline-block;
  margin-top: 32rpx;
  padding: 16rpx 40rpx;
  background: linear-gradient(135deg, #4a6cf7, #7c3aed);
  color: #fff;
  font-size: 26rpx;
  border-radius: 32rpx;
}
</style>
