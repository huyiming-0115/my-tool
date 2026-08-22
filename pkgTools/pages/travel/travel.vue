<template>
  <view class="travel-page">
    <!-- 自定义导航栏 -->
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">‹</text>
        <text class="nav-title" :style="{ paddingRight: navPaddingRight + 'px' }">
          {{ view === "detail" ? (currentPlan ? currentPlan.title : "计划详情") : "旅行计划" }}
        </text>

        <text class="nav-icon add" @click="openCreate" v-if="view === 'list'">+</text>
      </view>
    </view>

    <!-- 列表视图 -->
    <view v-if="view === 'list'" class="list-view">
      <view class="page-banner">
        <text class="banner-title">我的旅程</text>
        <text class="banner-desc">{{ plans.length }} 个旅行计划</text>
      </view>
      <view class="plan-list" v-if="plans.length > 0">
        <view class="plan-card" v-for="plan in plans" :key="plan.id" @click="viewPlan(plan)">
          <view class="card-row1">
            <text class="plan-title">{{ plan.title }}</text>
            <view class="status" :class="plan.status"><text>{{ statusText(plan.status) }}</text></view>
          </view>
          <view class="card-row2">
            <text class="meta">📍 {{ plan.destination }}</text>
            <text class="meta" v-if="plan.startDate">·</text>
            <text class="meta" v-if="plan.startDate">{{ plan.startDate }}</text>
          </view>
          <view class="card-row3" v-if="plan.notes">
          <view class="countdown-badge" v-if="plan.startDate">
            <text class="cd-text">{{ getCountdown(plan.startDate) }}</text>
          </view><text class="preview">{{ plan.notes }}</text></view>
          <view class="card-row4">
            <text class="tag" v-if="plan.fromStatic">📂 本地文件</text>
            <text class="view-link">查看文档 →</text>
          </view>
        </view>
      </view>
      <view v-else class="empty">
        <text class="empty-emoji">🗺️</text>
        <text class="empty-title">还没有旅行计划</text>
        <text class="empty-desc">点击右上角 + 开始规划旅程</text>
      </view>
    </view>

    <!-- 详情视图 -->
    <view v-if="view === 'detail'" class="detail-view">
      <view class="detail-meta" v-if="currentPlan">
        <view class="meta-line" v-if="currentPlan.destination">
          <text class="meta-l">📍 目的地</text>
          <text class="meta-v">{{ currentPlan.destination }}</text>
        </view>
        <view class="meta-line" v-if="currentPlan.startDate">
          <text class="meta-l">📅 时间</text>
          <text class="meta-v">{{ currentPlan.startDate }} ~ {{ currentPlan.endDate }}</text>
        </view>
        <view class="meta-line" v-if="currentPlan.budget">
          <text class="meta-l">💰 预算</text>
          <text class="meta-v">¥{{ currentPlan.budget }}</text>
        </view>
      </view>

      <!-- 倒计时横幅 -->
      <view class="countdown-banner" v-if="currentPlan && currentPlan.startDate">
        <text class="cd-label">距离出发</text>
        <text class="cd-days">{{ getCountdown(currentPlan.startDate) }}</text>
      </view>

      <!-- 编辑模式 -->
      <view v-if="!isPreview" class="editor-wrap">
        <view class="mode-tip">Markdown 编辑模式</view>
        <textarea class="md-input" v-model="editContent" placeholder="编写 Markdown 文档..." placeholder-class="ph" auto-height maxlength="-1" @input="markDirty" />
        <view class="stat-row">
          <text class="stat">{{ editContent.length }} 字符</text>
          <text class="stat">{{ lineCount }} 行</text>
          <text class="stat dirty-mark" v-if="isDirty">未保存</text>
        </view>
      </view>

      <!-- 地图视图 -->
      <view v-else-if="showMap" class="map-wrap">
        <view class="mode-tip">📍 行程地图</view>
        <view class="map-container">
          <map class="map" :latitude="mapCenter.latitude" :longitude="mapCenter.longitude" :markers="mapMarkers.filter(m => m.latitude).map(m => ({ ...m, callout: m.name }))" :scale="mapScale" show-location @markertap="onMarkerTap"></map>
        </view>
        <view class="map-nav" v-if="hasMapLocations">
          <text class="map-nav-btn" @click="prevLocation" :class="{ disabled: focusIndex <= 0 }">‹ 上一个</text>
          <text class="map-nav-idx">{{ focusIndex + 1 }} / {{ mapMarkers.filter(m => m.latitude).length }}</text>
          <text class="map-nav-btn" @click="nextLocation" :class="{ disabled: focusIndex >= mapMarkers.filter(m => m.latitude).length - 1 }">下一个 ›</text>
        </view>
        <view class="map-loc-list" v-if="mapMarkers.length > 0">
          <view class="map-loc-item" v-for="(m, idx) in mapMarkers" :key="idx" :class="{ active: focusIndex === idx }" @click="focusIndex = idx">
            <text class="loc-name">{{ m.name }}</text>
            <text class="loc-addr" v-if="m.address">{{ m.address }}</text>
            <text class="loc-coord" v-if="m.latitude">{{ m.latitude.toFixed(4) }}, {{ m.longitude.toFixed(4) }}</text>
          </view>
        </view>
      </view>

      <!-- 预览模式 -->
      <view v-else class="preview-wrap">
        <view class="mode-tip">Markdown 预览</view>
        <view class="md-wrap">
          <mp-html :content="renderedHtml" container-style="padding:0" />
        </view>
      </view>
    </view>

    <!-- 详情页悬浮操作按钮 -->
    <view v-if="view === 'detail'" class="detail-fab-group">
      <view class="detail-fab" :class="{ on: !isPreview }" @click="setView('edit')"><text class="df-icon">✏️</text><text class="df-t">编辑</text></view>
      <view class="detail-fab" :class="{ on: isPreview && !showMap }" @click="setView('preview'); showMap = false"><text class="df-icon">👁️</text><text class="df-t">预览</text></view>
      <view class="detail-fab" :class="{ on: showMap }" @click="showMap = !showMap" v-if="isPreview && hasMapLocations"><text class="df-icon">🗺️</text><text class="df-t">地图</text></view>
      <view class="detail-fab save" @click="handleEditSave" v-if="isDirty"><text class="df-icon">💾</text><text class="df-t">保存</text></view>
    </view>

    <!-- 底部快捷工具栏 (编辑模式) -->
    <view v-if="view === 'detail' && !isPreview" class="bottom-bar safe-bottom">
      <view class="bb-btn" data-sym="# " @click="onSyntaxTap"><text class="bb-icon">H</text><text class="bb-t">标题</text></view>
      <view class="bb-btn" data-sym="**" @click="onSyntaxTap"><text class="bb-icon">B</text><text class="bb-t">加粗</text></view>
      <view class="bb-btn" data-sym="*" @click="onSyntaxTap"><text class="bb-icon">I</text><text class="bb-t">斜体</text></view>
      <view class="bb-btn" data-sym="- " @click="onSyntaxTap"><text class="bb-icon">≡</text><text class="bb-t">列表</text></view>
      <view class="bb-btn" data-sym="> " @click="onSyntaxTap"><text class="bb-icon">❝</text><text class="bb-t">引用</text></view>
      <view class="bb-btn" data-sym="---\n" @click="onSyntaxTap"><text class="bb-icon">—</text><text class="bb-t">分隔</text></view>
    </view>

    <!-- 悬浮新增按钮 -->
    <view v-if="view === 'list'" class="fab" @click="openCreate">
      <text class="fab-icon">+</text>
      <text class="fab-text">新增计划</text>
    </view>
    <!-- 新建计划弹窗 -->
    <view v-if="showCreate" class="mask" @click.self="closeCreate">
      <view class="create-panel">
        <view class="panel-head">
          <text class="panel-title">新建旅行计划</text>
          <text class="panel-close" @click="closeCreate">✕</text>
        </view>
        <scroll-view class="panel-body" scroll-y>
          <view class="form-row">
            <text class="form-l">创建方式</text>
            <view class="seg">
              <text class="seg-item" :class="{ on: createMode === 'input' }" @click="createMode = 'input'">手动输入</text>
              <text class="seg-item" :class="{ on: createMode === 'md' }" @click="createMode = 'md'">粘贴 Markdown</text>
              <text class="seg-item" :class="{ on: createMode === 'import' }" @click="createMode = 'import'">导入 .md</text>
              <text class="seg-item" :class="{ on: createMode === 'smart' }" @click="createMode = 'smart'">智能导入</text>
            </view>
          </view>
          <view class="form-row column" v-if="createMode === 'import'">
            <text class="form-l">选择文件</text>
            <view class="import-area" @click="importMdFile">
              <text class="import-icon">📂</text>
              <text class="import-text">{{ importFileName || "点击选择 .md / .txt 文件" }}</text>
            </view>
          </view>
          <view class="form-row column" v-if="createMode === 'smart'">
            <text class="form-l">粘贴内容</text>
            <view class="form-tip">粘贴小红书攻略、游记、行程文本，自动提取结构化行程</view>
            <textarea class="md-input" v-model="smartImportText" placeholder="粘贴旅行攻略..." placeholder-class="ph" auto-height maxlength="-1" />
            <button class="btn-save" @click="handleSmartImport" style="margin-top:12rpx">智能解析</button>
          </view>
          <view class="form-row"><text class="form-l">计划标题</text><input class="form-input" v-model="newPlan.title" placeholder="如：云南7日游" placeholder-class="ph" /></view>
          <view class="form-row"><text class="form-l">目的地</text><input class="form-input" v-model="newPlan.destination" placeholder="如：云南" placeholder-class="ph" /></view>
          <view class="form-row"><text class="form-l">出发日期</text><picker mode="date" :value="newPlan.startDate" @change="(e) => newPlan.startDate = e.detail.value"><text class="form-input date-pick">{{ newPlan.startDate || "选择出发日期" }}</text></picker></view>
          <view class="form-row"><text class="form-l">结束日期</text><picker mode="date" :value="newPlan.endDate" @change="(e) => newPlan.endDate = e.detail.value"><text class="form-input date-pick">{{ newPlan.endDate || "选择结束日期" }}</text></picker></view>
          <view class="form-row"><text class="form-l">预算 (¥)</text><input class="form-input" type="digit" v-model="newPlan.budget" placeholder="0" placeholder-class="ph" /></view>
          <view class="form-row"><text class="form-l">状态</text><view class="seg"><text class="seg-item" :class="{ on: newPlan.status === 'planning' }" @click="newPlan.status = 'planning'">规划中</text><text class="seg-item" :class="{ on: newPlan.status === 'ongoing' }" @click="newPlan.status = 'ongoing'">进行中</text><text class="seg-item" :class="{ on: newPlan.status === 'completed' }" @click="newPlan.status = 'completed'">已完成</text></view></view>
          <view class="form-row column"><text class="form-l">Markdown 内容</text><view class="form-tip">支持 Markdown 全语法</view><textarea class="md-input" v-model="newPlan.markdown" placeholder="粘贴或编写 Markdown..." placeholder-class="ph" auto-height maxlength="-1" /></view>
          <view class="form-row column"><text class="form-l">或加载内置模板</text><view class="tpl-list"><view class="tpl-item" @click="useTpl(0)"><text class="tpl-name">云南大理-丽江</text><text class="tpl-meta">7天</text></view><view class="tpl-item" @click="useTpl(1)"><text class="tpl-name">日本东京-京都</text><text class="tpl-meta">8天</text></view><view class="tpl-item" @click="useTpl(2)"><text class="tpl-name">成都周末美食</text><text class="tpl-meta">2天</text></view></view></view>
          <view class="form-row"><text class="form-l">简短备注</text><input class="form-input" v-model="newPlan.notes" placeholder="一句话描述" placeholder-class="ph" /></view>
        </scroll-view>
        <view class="panel-footer"><button class="btn-cancel" @click="closeCreate">取消</button><button class="btn-save" @click="handleSavePlan">保存计划</button></view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, reactive, onMounted, watch } from "vue"
import { marked } from "marked"
import { tianjinPlanMarkdown } from "../../../utils/tianjin-plan.js"
import { smartImport } from "../../utils/travel-import.js"
import { extractLocations, matchLocationsWithCoords } from "../../utils/travel-map.js"
import mpHtml from "../../../components/mp-html/mp-html.vue"

const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const navPaddingRight = ref(32)
try {
  // #ifdef MP-WEIXIN
  const menu = wx.getMenuButtonBoundingClientRect()
  if (menu && menu.left) {
    navPaddingRight.value = (uni.getSystemInfoSync().windowWidth - menu.left) + 12
  }
  // #endif
} catch (e) { /* 非微信环境使用默认值 */ }
const view = ref("list")
const plans = ref([])
const currentPlan = ref(null)
const showCreate = ref(false)
const createMode = ref("input")
const isPreview = ref(true)
const editContent = ref("")
const isDirty = ref(false)
const showMap = ref(false)
const focusIndex = ref(0)
const mapScale = ref(12)
const importFileName = ref("")
const smartImportText = ref("")

const newPlan = reactive({ title: "", destination: "", startDate: "", endDate: "", budget: "", status: "planning", markdown: "", notes: "" })

const defaultMarkdown = (title = "我的旅行计划") => "# " + title + "\n\n> 一段美好的旅程即将开始\n\n---\n\n## Day 1\n\n- 上午抵达目的地\n- 下午游览市区\n- 晚享当地美食\n\n> 💡 享受旅途的每一刻\n\n*一路顺风*"

const lineCount = computed(() => editContent.value ? editContent.value.split("\n").length : 0)
const renderedHtml = computed(() => editContent.value ? marked.parse(editContent.value) : "")
const mapMarkers = computed(() => { const md = currentPlan.value?.contentMarkdown || ""; return md ? matchLocationsWithCoords(extractLocations(md)) : [] })
const hasMapLocations = computed(() => mapMarkers.value.some(m => m.latitude))
const mapCenter = computed(() => { const v = mapMarkers.value.filter(m => m.latitude); if (!v.length) return { latitude: 39.9042, longitude: 116.4074 }; const idx = focusIndex.value >= v.length ? 0 : focusIndex.value; return { latitude: v[idx].latitude, longitude: v[idx].longitude } })
const statusText = (s) => ({ planning: "规划中", ongoing: "进行中", completed: "已完成" }[s] || s)

const STORAGE_KEY = "travelPlans"
const tianjinPlan = { id: "static-tianjin", title: "天津+北京+滨海新区", destination: "天津/北京", startDate: "2026-07-16", endDate: "2026-07-20", budget: "", status: "planning", notes: "真实出行计划 · 5天4晚", contentMarkdown: tianjinPlanMarkdown, fromStatic: true }

function loadPlans() { let s = []; try { const r = uni.getStorageSync(STORAGE_KEY); if (r) s = JSON.parse(r) } catch(e) {}; if (!s.find(p => p.id === "static-tianjin")) s.unshift(tianjinPlan); plans.value = s; uni.setStorageSync(STORAGE_KEY, JSON.stringify(s)) }
function savePlans() { uni.setStorageSync(STORAGE_KEY, JSON.stringify(plans.value)) }
function viewPlan(plan) { currentPlan.value = plan; editContent.value = plan.contentMarkdown || ""; isDirty.value = false; isPreview.value = true; showMap.value = false; focusIndex.value = 0; view.value = "detail" }
function goBack() { if (view.value === "detail") { if (isDirty.value) uni.showModal({ title: "提示", content: "有未保存的修改？", success: r => { if (r.confirm) { view.value = "list"; currentPlan.value = null } } }); else { view.value = "list"; currentPlan.value = null } } else uni.navigateBack() }
function openCreate() { Object.assign(newPlan, { title: "", destination: "", startDate: "", endDate: "", budget: "", status: "planning", markdown: defaultMarkdown(), notes: "" }); importFileName.value = ""; smartImportText.value = ""; createMode.value = "input"; showCreate.value = true }
function closeCreate() { showCreate.value = false }
function handleSavePlan() { if (!newPlan.title.trim()) { uni.showToast({ title: "请填写标题", icon: "none" }); return } if (!newPlan.markdown.trim()) { uni.showToast({ title: "请填写内容", icon: "none" }); return } plans.value.unshift({ id: "user-" + Date.now(), title: newPlan.title, destination: newPlan.destination || "未填写", startDate: newPlan.startDate || "", endDate: newPlan.endDate || "", budget: newPlan.budget || "", status: newPlan.status, notes: newPlan.notes || "", contentMarkdown: newPlan.markdown, fromStatic: false }); savePlans(); showCreate.value = false; uni.showToast({ title: "保存成功", icon: "success" }) }
function setView(v) { isPreview.value = v === "preview" }
function markDirty() { isDirty.value = true }
function handleEditSave() { if (!currentPlan.value || !editContent.value.trim()) return; currentPlan.value.contentMarkdown = editContent.value; const i = plans.value.findIndex(p => p.id === currentPlan.value.id); if (i >= 0) plans.value[i] = { ...currentPlan.value }; savePlans(); isDirty.value = false; uni.showToast({ title: "保存成功", icon: "success" }) }
function onSyntaxTap(e) { editContent.value += (editContent.value.endsWith("\n") || !editContent.value ? "" : "\n") + e.currentTarget.dataset.sym; markDirty() }
function onMarkerTap(e) { const idx = mapMarkers.value.findIndex((m, i) => i === e.markerId); if (idx >= 0) focusIndex.value = idx }
function focusLocation(m) { if (m.latitude) uni.openLocation({ latitude: m.latitude, longitude: m.longitude, name: m.name, address: m.address || "", scale: 15 }) }
watch(showMap, (v) => { if (v) focusIndex.value = 0 })
function prevLocation() { if (focusIndex.value > 0) focusIndex.value-- }
function nextLocation() { const max = mapMarkers.value.filter(m => m.latitude).length - 1; if (focusIndex.value < max) focusIndex.value++ }

const TEMPLATES = [
  {
    title: "云南大理-丽江",
    destination: "云南",
    markdown: `# 云南大理-丽江 7日游

> 风花雪月，彩云之南

---

## Day 1 抵达大理

- 抵达大理凤仪机场
- 入住大理古城附近
- 晚上逛大理古城

## Day 2 洱海环线

- 洱海
- 双廊古镇
- 小普陀

## Day 3 苍山

- 苍山
- 洗马潭大索道

## Day 4 喜洲古镇

- 喜洲古镇
- 白族民居建筑

## Day 5 前往丽江

- 大理→丽江（高铁2小时）
- 丽江古城

## Day 6 玉龙雪山

- 玉龙雪山
- 蓝月谷

## Day 7 返程

- 丽江三义机场返程`
  },
  {
    title: "日本东京-京都",
    destination: "日本",
    markdown: `# 日本东京-京都 8日游

> 霓虹国的古今交错

---

## Day 1 抵达东京

- 抵达成田/羽田机场
- 入住新宿/涩谷
- 歌舞伎町夜游

## Day 2 东京经典

- 浅草寺
- 东京塔
- 银座

## Day 3 东京迪士尼

- 东京迪士尼乐园

## Day 4 前往京都

- 东京→京都（新干线2.5小时）
- 伏见稻荷大社

## Day 5 京都古韵

- 金阁寺
- 清水寺
- 祇园

## Day 6 岚山

- 岚山
- 竹林小径

## Day 7 大阪一日游

- 京都→大阪
- 环球影城

## Day 8 返程

- 关西机场返程`
  },
  {
    title: "成都周末美食",
    destination: "成都",
    markdown: `# 成都周末美食 2日游

> 巴适得板，安逸得喊

---

## Day 1 市区经典

- 宽窄巷子
- 春熙路
- 锦里
- 火锅晚餐

## Day 2 熊猫+文化

- 大熊猫基地
- 杜甫草堂
- 九眼桥
- 串串香`
  }
]

function useTpl(idx) {
  const t = TEMPLATES[idx]
  if (!t) return
  newPlan.title = t.title
  newPlan.destination = t.destination
  newPlan.markdown = t.markdown
  createMode.value = "md"

}
function handleSmartImport() { if (!smartImportText.value.trim()) { uni.showToast({ title: "请先粘贴内容", icon: "none" }); return } newPlan.markdown = smartImport(smartImportText.value, newPlan.title || "我的旅行计划"); createMode.value = "md"; uni.showToast({ title: "解析完成", icon: "success" }) }
function importMdFile() {
  // #ifdef H5
  var input = document.createElement("input")
  input.type = "file"
  input.accept = ".md,.txt,.markdown,text/plain,text/markdown"
  input.style.cssText = "position:fixed;top:-9999px;left:-9999px;opacity:0"
  document.body.appendChild(input)
  input.onchange = function (e) {
    var f = e.target.files[0]
    if (!f) return
    importFileName.value = f.name
    var r = new FileReader()
    r.onload = function (ev) {
      newPlan.markdown = ev.target.result
      if (!newPlan.title) newPlan.title = f.name.replace(/\.(md|txt|markdown)$/i, "")
      uni.showToast({ title: "导入成功", icon: "success" })
    }
    r.onerror = function () {
      uni.showToast({ title: "读取失败", icon: "none" })
    }
    r.readAsText(f, "utf-8")
    input.remove()
  }
  input.oncancel = function () { input.remove() }
  input.click()
  // #endif

  // #ifdef MP-WEIXIN
  uni.chooseMessageFile({
    count: 1,
    type: "file",
    extension: [".md", ".txt", ".markdown"],
    success: function (res) { readImportedFile(res.tempFiles[0]) },
    fail: function (err) {
      if (err && err.errMsg && err.errMsg.indexOf("cancel") >= 0) return
      uni.showToast({ title: "选择文件失败", icon: "none" })
    }
  })
  // #endif

  // #ifdef APP-PLUS
  if (uni.chooseFile) {
    uni.chooseFile({
      count: 1,
      type: "file",
      success: function (res) { readImportedFile(res.tempFiles[0]) },
      fail: function (err) {
        if (err && err.errMsg && err.errMsg.indexOf("cancel") >= 0) return
        uni.showToast({ title: "选择文件失败", icon: "none" })
      }
    })
  } else {
    uni.showToast({ title: "当前环境不支持文件选择", icon: "none" })
  }
  // #endif
}

function tryChooseMessageFile() {
  uni.chooseMessageFile({
    count: 1,
    type: "file",
    success: function (res) { readImportedFile(res.tempFiles[0]) },
    fail: function () { uni.showToast({ title: "请选择文件", icon: "none" }) }
  })
}

function readImportedFile(file) {
  importFileName.value = file.name
  var fs = uni.getFileSystemManager()
  fs.readFile({
    filePath: file.path,
    encoding: "utf-8",
    success: function (r) {
      newPlan.markdown = r.data
      if (!newPlan.title) newPlan.title = file.name.replace(/\.(md|txt|markdown)$/i, "")
      uni.showToast({ title: "导入成功", icon: "success" })
    },
    fail: function () { uni.showToast({ title: "读取失败", icon: "none" }) }
  })
}
onMounted(() => { if (!uni.getStorageSync("isLoggedIn")) { setTimeout(() => { uni.reLaunch({ url: "/pages/login/login" }) }, 100); return } loadPlans() })
</script>

<style lang="scss" scoped>
.travel-page { min-height: 100vh; background: #f5f7fb; padding-bottom: 140rpx; }
.custom-nav { background: linear-gradient(135deg, #4a6cf7 0%, #7c3aed 100%); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.add { font-size: 44rpx; width: 64rpx; height: 64rpx; line-height: 64rpx; border-radius: 50%; background: rgba(255,255,255,0.2); }
.nav-icon.empty { visibility: hidden; }
.fab { position: fixed; bottom: 200rpx; right: 40rpx; display: flex; align-items: center; gap: 8rpx; padding: 20rpx 32rpx; border-radius: 50rpx; background: linear-gradient(135deg, #4a6cf7, #7c3aed); box-shadow: 0 8rpx 24rpx rgba(74,108,247,0.4); z-index: 99; }
.fab-icon { font-size: 32rpx; color: #fff; font-weight: 700; }
.fab-text { font-size: 26rpx; color: #fff; font-weight: 600; }
.detail-fab-group { position: fixed; bottom: 200rpx; right: 24rpx; display: flex; flex-direction: column; gap: 16rpx; z-index: 99; }
.detail-fab { display: flex; align-items: center; gap: 8rpx; padding: 16rpx 24rpx; border-radius: 50rpx; background: linear-gradient(135deg, #4a6cf7, #7c3aed); box-shadow: 0 8rpx 24rpx rgba(74,108,247,0.4); }
.detail-fab.on { background: linear-gradient(135deg, #7c3aed, #db2777); }
.detail-fab.save { background: linear-gradient(135deg, #4caf50, #2e7d32); }
.df-icon { font-size: 28rpx; color: #fff; }
.df-t { font-size: 22rpx; color: #fff; font-weight: 600; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; box-sizing: border-box; }
.nav-actions { display: flex; gap: 8rpx; flex-shrink: 0; }
.nav-action-btn { width: 64rpx; height: 64rpx; line-height: 64rpx; text-align: center; border-radius: 50%; background: rgba(255,255,255,0.2); color: #fff; font-size: 28rpx; }
.nav-action-btn.on { background: rgba(255,255,255,0.9); color: #4a6cf7; }
.nav-action-btn.save { background: rgba(76,175,80,0.9); }
.list-view { padding: 24rpx; }
.page-banner { padding: 40rpx 32rpx; margin-bottom: 24rpx; }
.banner-title { font-size: 40rpx; font-weight: 700; color: #1a1a1a; display: block; }
.banner-desc { font-size: 24rpx; color: #999; margin-top: 8rpx; display: block; }
.plan-list { display: flex; flex-direction: column; gap: 20rpx; }
.plan-card { background: #fff; border-radius: 24rpx; padding: 28rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); transition: transform 0.15s; }
.plan-card:active { transform: scale(0.98); }
.card-row1 { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12rpx; }
.plan-title { font-size: 30rpx; font-weight: 600; color: #1a1a1a; flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.status { font-size: 22rpx; padding: 4rpx 16rpx; border-radius: 20rpx; margin-left: 16rpx; flex-shrink: 0; }
.status.planning { background: #fff3e0; color: #f57c00; }
.status.ongoing { background: #e3f2fd; color: #1976d2; }
.status.completed { background: #e8f5e9; color: #388e3c; }
.card-row2 { display: flex; align-items: center; gap: 8rpx; margin-bottom: 12rpx; flex-wrap: wrap; }
.meta { font-size: 24rpx; color: #888; }
.card-row3 { margin-bottom: 16rpx; }
.preview { font-size: 24rpx; color: #aaa; overflow: hidden; text-overflow: ellipsis; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; }
.card-row4 { display: flex; justify-content: space-between; align-items: center; border-top: 2rpx solid #f5f5f5; padding-top: 12rpx; }
.tag { font-size: 22rpx; color: #4a6cf7; }
.view-link { font-size: 24rpx; color: #4a6cf7; }
.empty { text-align: center; padding: 160rpx 40rpx; }
.empty-emoji { font-size: 100rpx; display: block; }
.empty-title { font-size: 30rpx; font-weight: 600; color: #333; display: block; margin-top: 24rpx; }
.empty-desc { font-size: 24rpx; color: #999; display: block; margin-top: 8rpx; }
.detail-view { padding: 24rpx; }
.detail-meta { background: #fff; border-radius: 24rpx; padding: 24rpx 28rpx; margin-bottom: 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.meta-line { display: flex; align-items: center; padding: 12rpx 0; border-bottom: 2rpx solid #f8f8f8; }
.meta-line:last-child { border-bottom: none; }
.meta-l { font-size: 26rpx; color: #999; width: 160rpx; flex-shrink: 0; }
.meta-v { font-size: 26rpx; color: #333; flex: 1; }
.editor-wrap { padding: 16rpx 0; }
.mode-tip { font-size: 22rpx; color: #999; text-align: center; padding: 12rpx 0 16rpx; letter-spacing: 2rpx; }
.md-input { width: 100%; min-height: 60vh; padding: 28rpx; font-size: 28rpx; background: #fff; border-radius: 20rpx; line-height: 1.8; color: #333; box-sizing: border-box; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.stat-row { display: flex; gap: 24rpx; padding: 16rpx 4rpx 0; justify-content: flex-end; }
.stat { font-size: 22rpx; color: #999; }
.dirty-mark { color: #f59e0b; font-weight: 600; }
.preview-wrap { padding: 16rpx 0; }
.md-wrap { background: #fff; border-radius: 24rpx; padding: 32rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.map-wrap { padding: 16rpx 0; }
.map-container { border-radius: 20rpx; overflow: hidden; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); margin-bottom: 16rpx; }
.map { width: 100%; height: 600rpx; }
.map-loc-list { background: #fff; border-radius: 20rpx; padding: 16rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.map-loc-item { display: flex; flex-direction: column; padding: 16rpx; border-bottom: 2rpx solid #f5f5f5; }
.map-loc-item:last-child { border-bottom: none; }
.loc-name { font-size: 28rpx; font-weight: 600; color: #333; }
.loc-addr { font-size: 22rpx; color: #999; margin-top: 4rpx; }
.loc-coord { font-size: 20rpx; color: #4a6cf7; margin-top: 4rpx; }
.map-nav { display: flex; align-items: center; justify-content: space-between; padding: 12rpx 0; }
.map-nav-btn { font-size: 26rpx; color: #4a6cf7; font-weight: 600; padding: 8rpx 20rpx; border-radius: 30rpx; background: #f0f4ff; }
.map-nav-btn.disabled { color: #ccc; background: #f5f5f5; }
.map-nav-idx { font-size: 24rpx; color: #888; font-weight: 600; }
.map-loc-item.active { background: #f0f4ff; border-radius: 16rpx; }
.map-loc-item.active .loc-name { color: #4a6cf7; }
.safe-bottom { padding-bottom: calc(16rpx + env(safe-area-inset-bottom)); }
.bottom-bar { position: fixed; bottom: 0; left: 0; right: 0; height: 108rpx; background: #fff; border-top: 2rpx solid #f0f0f0; display: flex; justify-content: space-around; align-items: center; box-shadow: 0 -4rpx 20rpx rgba(0,0,0,0.06); z-index: 99; }
.bb-btn { display: flex; flex-direction: column; align-items: center; gap: 2rpx; padding: 4rpx 16rpx; }
.bb-icon { font-size: 32rpx; color: #4a6cf7; font-weight: 700; }
.bb-t { font-size: 18rpx; color: #999; }
.mask { position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 999; display: flex; align-items: flex-end; justify-content: center; animation: fadein 0.2s; }
@keyframes fadein { from { opacity: 0; } to { opacity: 1; } }
.create-panel { width: 100%; background: #fff; border-radius: 32rpx 32rpx 0 0; max-height: 88vh; display: flex; flex-direction: column; animation: slideup 0.25s; }
@keyframes slideup { from { transform: translateY(100%); } to { transform: translateY(0); } }
.panel-head { display: flex; justify-content: space-between; align-items: center; padding: 28rpx 32rpx; border-bottom: 2rpx solid #f0f0f0; }
.panel-title { font-size: 30rpx; font-weight: 600; color: #1a1a1a; }
.panel-close { font-size: 32rpx; color: #999; padding: 4rpx 8rpx; }
.panel-body { flex: 1; padding: 12rpx 32rpx; overflow-y: auto; }
.form-row { display: flex; align-items: center; padding: 20rpx 0; border-bottom: 2rpx solid #f8f8f8; }
.form-row.column { flex-direction: column; align-items: flex-start; gap: 12rpx; }
.form-l { font-size: 26rpx; color: #333; width: 170rpx; flex-shrink: 0; font-weight: 500; }
.form-tip { font-size: 22rpx; color: #999; margin-top: -4rpx; }
.form-input { flex: 1; font-size: 28rpx; color: #333; height: 56rpx; }
.ph { color: #ccc; }
.date-pick { display: flex; align-items: center; height: 56rpx; color: #333; }
.seg { display: flex; gap: 16rpx; flex: 1; flex-wrap: wrap; }
.seg-item { font-size: 24rpx; padding: 10rpx 24rpx; border-radius: 28rpx; background: #f5f5f5; color: #666; flex-shrink: 0; }
.seg-item.on { background: #4a6cf7; color: #fff; }
.tpl-list { display: flex; flex-direction: column; gap: 12rpx; width: 100%; }
.tpl-item { padding: 16rpx 20rpx; background: #f8f9ff; border-radius: 12rpx; display: flex; justify-content: space-between; align-items: center; }
.tpl-name { font-size: 26rpx; color: #333; font-weight: 500; }
.tpl-meta { font-size: 22rpx; color: #999; }
.import-area { width: 100%; padding: 40rpx; background: #f8f9ff; border-radius: 12rpx; border: 2rpx dashed #c0c4cc; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 12rpx; box-sizing: border-box; }
.import-icon { font-size: 48rpx; }
.import-text { font-size: 26rpx; color: #666; }
.panel-footer { display: flex; gap: 24rpx; padding: 24rpx 32rpx; border-top: 2rpx solid #f0f0f0; padding-bottom: calc(24rpx + env(safe-area-inset-bottom)); }
.btn-cancel { flex: 1; height: 80rpx; line-height: 80rpx; border-radius: 40rpx; background: #f5f5f5; color: #666; font-size: 28rpx; border: none; }
.btn-cancel::after { border: none; }
.btn-save { flex: 1; height: 80rpx; line-height: 80rpx; border-radius: 40rpx; background: linear-gradient(135deg, #4a6cf7, #7c3aed); color: #fff; font-size: 28rpx; font-weight: 600; letter-spacing: 2rpx; border: none; }
.btn-save::after { border: none; }
</style>


























