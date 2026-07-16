<template>
  <view class="detail-page">
    <!-- 顶部工具栏 -->
    <view class="toolbar" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="tool-row">
        <text class="tool-btn back" @click="handleBack">‹</text>
        <view class="title-wrap">
          <input
            class="title-input"
            v-model="note.title"
            placeholder="输入标题..."
            placeholder-class="ph"
            maxlength="50"
            @input="markDirty"
          />
        </view>
        <view class="tool-actions">
          <text class="tool-btn" :class="{ on: !isPreview }" @click="setView('edit')">✏️</text>
          <text class="tool-btn" :class="{ on: isPreview }" @click="setView('preview')">👁️</text>
          <text class="tool-btn pin" :class="{ on: note.pinned }" @click="togglePin">📌</text>
          <text class="tool-btn save" @click="handleSave">💾</text>
        </view>
      </view>
      <!-- 标签编辑 -->
      <view class="tags-edit">
        <view class="tag-list">
          <text v-for="(t, i) in note.tags" :key="i" class="etag">
            #{{ t }}
            <text class="etag-x" @click="removeTag(i)">✕</text>
          </text>
          <input
            class="tag-input"
            v-model="tagInput"
            placeholder="+ 标签"
            placeholder-class="ph"
            confirm-type="done"
            @confirm="addTag"
            maxlength="12"
          />
        </view>
      </view>
    </view>

    <!-- 编辑器 -->
    <view v-if="!isPreview" class="editor-wrap">
      <view class="mode-tip">Markdown 编辑模式</view>
      <textarea
        class="md-input"
        v-model="note.content"
        placeholder="# 开始编写你的 Markdown&#10;&#10;支持标题、加粗、列表、引用、代码块等..."
        placeholder-class="ph"
        auto-height
        maxlength="-1"
        @input="markDirty"
        @blur="autoSave"
      />
      <view class="stat-row">
        <text class="stat">{{ note.content.length }} 字符</text>
        <text class="stat">{{ lineCount }} 行</text>
        <text class="stat dirty-mark" v-if="isDirty">未保存</text>
      </view>
    </view>

    <!-- 预览 -->
    <view v-else class="preview-wrap">
      <view class="mode-tip">实时预览</view>
      <view class="md-wrap">
        <rich-text :nodes="renderedNodes" @itemclick="onMdTap"></rich-text>
      </view>
    </view>

    <!-- 操作面板 -->
    <view class="bottom-bar safe-bottom">
      <view class="bb-btn" data-sym="#" @click="onSyntaxTap">
        <text class="bb-icon">H</text><text class="bb-t">标题</text>
      </view>
      <view class="bb-btn" data-sym="**" @click="onSyntaxTap">
        <text class="bb-icon">B</text><text class="bb-t">加粗</text>
      </view>
      <view class="bb-btn" data-sym="*" @click="onSyntaxTap">
        <text class="bb-icon">I</text><text class="bb-t">斜体</text>
      </view>
      <view class="bb-btn" data-sym="- " @click="onSyntaxTap">
        <text class="bb-icon">≡</text><text class="bb-t">列表</text>
      </view>
      <view class="bb-btn" data-sym="> " @click="onSyntaxTap">
        <text class="bb-icon">❝</text><text class="bb-t">引用</text>
      </view>
      <view class="bb-btn" data-sym="---\n" @click="onSyntaxTap">
        <text class="bb-icon">—</text><text class="bb-t">分隔</text>
      </view>
    </view>
</view>
</template>

<script setup>
import { ref, computed, reactive, onMounted, onBeforeUnmount } from "vue"
import { parseMarkdown } from "@/utils/markdown.js"
import { loadNotes, saveNotes, upsertNote, createEmptyNote } from "@/utils/notes-store.js"

const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20

const note = reactive(createEmptyNote())
const isPreview = ref(false)
const isDirty = ref(false)
const tagInput = ref("")
const isNew = ref(true)
let editStartCursor = { selectionStart: 0, selectionEnd: 0 }

const lineCount = computed(() => note.content.split("").length)
const renderedNodes = computed(() => {
  if (!note.content) return []
  return parseMarkdown(note.content).nodes
})

function setView(v) {
  isPreview.value = v === "preview"
}

function markDirty() {
  isDirty.value = true
}

function addTag() {
  const t = tagInput.value.trim().replace(/[#\s]/g, "")
  if (t && !note.tags.includes(t) && note.tags.length < 5) {
    note.tags.push(t)
    markDirty()
  }
  tagInput.value = ""
}

function removeTag(i) {
  note.tags.splice(i, 1)
  markDirty()
}

function togglePin() {
  note.pinned = !note.pinned
  markDirty()
  uni.showToast({ title: note.pinned ? "已置顶" : "取消置顶", icon: "none" })
}

function onSyntaxTap(e) {
  const sym = e.currentTarget.dataset.sym;
  note.content = (note.content || "") + "" + sym + (sym === "**" || sym === "*" ? sym : "");
  isPreview.value = false;
  markDirty();
}

function onMdTap(e) {
  // rich-text 点击，目前仅支持展示
}

function handleSave() {
  const notes = loadNotes()
  upsertNote(notes, {
    ...note,
    title: note.title.trim() || "无标题",
  })
  saveNotes(notes)
  isDirty.value = false
  uni.showToast({ title: "已保存", icon: "success" })
  // 返回列表
  setTimeout(() => { uni.navigateBack() }, 600)
}

function handleBack() {
  if (isDirty.value) {
    uni.showModal({
      title: "返回",
      content: "有未保存的修改，确定离开？",
      success: (r) => {
        if (r.confirm) uni.navigateBack()
        else handleSave()
      },
    })
  } else {
    uni.navigateBack()
  }
}

function autoSave() {
  if (!isDirty.value) return
  const notes = loadNotes()
  upsertNote(notes, {
    ...note,
    title: note.title.trim() || "无标题",
  })
  saveNotes(notes)
  isDirty.value = false
}

onMounted(() => {
  if (!uni.getStorageSync("isLoggedIn")) {
    uni.reLaunch({ url: "/pages/login/login" })
    return
  }
  const pages = getCurrentPages()
  const cur = pages[pages.length - 1]
  const query = cur.options || {}
  if (query.id) {
    const notes = loadNotes()
    const found = notes.find((n) => n.id === query.id)
    if (found) {
      Object.assign(note, found)
      isNew.value = false
      isDirty.value = false
    }
  }
})

onBeforeUnmount(() => {
  // 离开前自动保存
  if (isDirty.value && note.content) {
    const notes = loadNotes()
    upsertNote(notes, {
      ...note,
      title: note.title.trim() || "无标题",
    })
    saveNotes(notes)
  }
})
</script>

<style lang="scss" scoped>
.detail-page {
  min-height: 100vh;
  background: #f5f7fb;
  padding-bottom: 140rpx;
}

/* 工具栏 */
.toolbar {
  background: linear-gradient(135deg, #4a6cf7 0%, #7c3aed 100%);
  padding-bottom: 20rpx;
  box-shadow: 0 4rpx 16rpx rgba(74, 108, 247, 0.15);
}
.tool-row {
  height: 88rpx;
  display: flex;
  align-items: center;
  padding: 0 20rpx;
}
.tool-btn {
  width: 64rpx;
  height: 64rpx;
  line-height: 64rpx;
  text-align: center;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  color: #fff;
  font-size: 32rpx;
  font-weight: 700;
  flex-shrink: 0;
}
.tool-btn.back { font-size: 44rpx; margin-right: 16rpx; }
.tool-btn.on { background: rgba(255, 255, 255, 0.4); }
.tool-actions {
  margin-left: auto;
  display: flex;
  gap: 12rpx;
}
.title-wrap {
  flex: 1;
  margin: 0 16rpx;
  overflow: hidden;
}
.title-input {
  font-size: 30rpx;
  color: #fff;
  height: 64rpx;
  width: 100%;
  font-weight: 600;
}
.title-input.ph, .ph { color: rgba(255, 255, 255, 0.6); }

/* 标签 */
.tags-edit {
  padding: 0 24rpx 8rpx;
}
.tag-list {
  display: flex;
  gap: 12rpx;
  overflow-x: auto;
  white-space: nowrap;
  flex-wrap: wrap;
}
.etag {
  font-size: 22rpx;
  color: #fff;
  background: rgba(255, 255, 255, 0.25);
  padding: 4rpx 16rpx;
  border-radius: 20rpx;
  display: inline-flex;
  align-items: center;
}
.etag-x {
  margin-left: 6rpx;
  font-size: 20rpx;
  opacity: 0.7;
}
.tag-input {
  font-size: 22rpx;
  color: #fff;
  background: rgba(255, 255, 255, 0.15);
  padding: 4rpx 16rpx;
  border-radius: 20rpx;
  min-width: 120rpx;
  max-width: 180rpx;
}
.tag-input.ph { color: rgba(255, 255, 255, 0.5); font-size: 22rpx; }

/* 编辑器 */
.editor-wrap {
  padding: 16rpx 24rpx 24rpx;
}
.mode-tip {
  font-size: 22rpx;
  color: #999;
  text-align: center;
  padding: 12rpx 0 16rpx;
  letter-spacing: 2rpx;
}
.md-input {
  width: 100%;
  min-height: 60vh;
  padding: 28rpx;
  font-size: 28rpx;
  background: #fff;
  border-radius: 20rpx;
  line-height: 1.8;
  color: #333;
  box-sizing: border-box;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.04);
}
.md-input.ph { color: #bbb; }
.stat-row {
  display: flex;
  gap: 24rpx;
  padding: 16rpx 4rpx 0;
  justify-content: flex-end;
}
.stat {
  font-size: 22rpx;
  color: #999;
}
.dirty-mark { color: #f59e0b; font-weight: 600; }

/* 预览 */
.preview-wrap {
  padding: 16rpx 24rpx 24rpx;
}
.md-wrap {
  background: #fff;
  border-radius: 20rpx;
  padding: 32rpx;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.04);
}

/* 底部快捷工具栏 */
.safe-bottom {
  padding-bottom: calc(16rpx + env(safe-area-inset-bottom));
}
.bottom-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 108rpx;
  background: #fff;
  border-top: 2rpx solid #f0f0f0;
  display: flex;
  justify-content: space-around;
  align-items: center;
  box-shadow: 0 -4rpx 20rpx rgba(0, 0, 0, 0.06);
  z-index: 99;
}
.bb-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rpx;
  padding: 4rpx 16rpx;
}
.bb-icon {
  font-size: 32rpx;
  color: #4a6cf7;
  font-weight: 700;
}
.bb-t {
  font-size: 18rpx;
  color: #999;
}
</style>
