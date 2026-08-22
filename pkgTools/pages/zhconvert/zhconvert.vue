<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">简繁转换</text><text class="nav-icon" @click="swap">⇄</text></view>
    </view>
    <view class="content">
      <view class="mode-tabs"><text class="mode-tab" :class="{ active: mode === 's2t' }" @click="mode = 's2t'">简→繁</text><text class="mode-tab" :class="{ active: mode === 't2s' }" @click="mode = 't2s'">繁→简</text></view>
      <view class="io-card"><text class="io-label">{{ mode === 's2t' ? '简体中文' : '繁体中文' }}</text><textarea class="io-input" v-model="input" placeholder="输入要转换的文本..." auto-height maxlength="2000" /></view>
      <view class="io-card"><view class="io-head"><text class="io-label">{{ mode === 's2t' ? '繁体中文' : '简体中文' }}</text><text class="copy-btn" @click="copyResult">复制</text></view><textarea class="io-input result" :value="output" placeholder="结果..." auto-height readonly /></view>
    </view>
  </view>
</template>
<script setup>
import { ref, watch, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const mode = ref("s2t")
const input = ref("")
const output = ref("")
const s2t_map = {"简":"簡","体":"體","转":"轉","换":"換","对":"對","应":"應","时":"時","钟":"鐘","历":"歷","万":"萬","节":"節","区":"區","总":"總","从":"從","来":"來","书":"書","发":"發","见":"見","长":"長","门":"門","东":"東","义":"義","头":"頭","实":"實","学":"學","国":"國","图":"圖","声":"聲","点":"點","党":"黨","关":"關","过":"過","还":"還","这":"這","个":"個","们":"們","说":"說","为":"為","会":"會","业":"業","经":"經","进":"進","电":"電","话":"話","书":"書","业":"業","发":"發","实":"實","对":"對","应":"應","年":"年","月":"月","日":"日","时":"時","分":"分","秒":"秒"}
const t2s_map = {}
for (const k in s2t_map) t2s_map[s2t_map[k]] = k
function convert() {
  const map = mode.value === "s2t" ? s2t_map : t2s_map
  output.value = input.value.split("").map(function(c) { return map[c] || c }).join("")
}
watch(input, convert)
watch(mode, convert)
function swap() { mode.value = mode.value === "s2t" ? "t2s" : "s2t"; var t = input.value; input.value = output.value; output.value = t }
function copyResult() { if (output.value) { uni.setClipboardData({ data: output.value, success: function() { uni.showToast({ title: "已复制", icon: "success" }) } }) } }
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #fdcb6e, #e17055); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.mode-tabs { display: flex; gap: 16rpx; margin-bottom: 24rpx; }
.mode-tab { flex: 1; text-align: center; padding: 20rpx; background: #fff; border-radius: 16rpx; font-size: 28rpx; color: #666; }
.mode-tab.active { background: linear-gradient(135deg, #fdcb6e, #e17055); color: #fff; }
.io-card { background: #fff; border-radius: 24rpx; padding: 24rpx; margin-bottom: 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.io-head { display: flex; justify-content: space-between; align-items: center; }
.io-label { font-size: 26rpx; color: #999; display: block; margin-bottom: 12rpx; }
.copy-btn { font-size: 24rpx; color: #e17055; padding: 4rpx 12rpx; }
.io-input { width: 100%; min-height: 200rpx; font-size: 28rpx; line-height: 1.6; }
.io-input.result { background: #f8f9fa; border-radius: 12rpx; padding: 16rpx; }
</style>