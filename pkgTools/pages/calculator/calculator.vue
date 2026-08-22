<template>
  <view class="calc-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">计算器</text><text class="nav-icon" @click="showHistory = !showHistory">📖</text></view>
    </view>
    <view class="content">
      <view class="display"><text class="expr">{{ expression || ' ' }}</text><text class="result">{{ display }}</text></view>
      <view class="pad">
        <view class="pad-row"><button class="key fn" @click="clearAll">AC</button><button class="key fn" @click="delOne">⌫</button><button class="key fn" @click="appendOp('%')">%</button><button class="key op" @click="appendOp('÷')">÷</button></view>
        <view class="pad-row"><button class="key" @click="appendNum('7')">7</button><button class="key" @click="appendNum('8')">8</button><button class="key" @click="appendNum('9')">9</button><button class="key op" @click="appendOp('×')">×</button></view>
        <view class="pad-row"><button class="key" @click="appendNum('4')">4</button><button class="key" @click="appendNum('5')">5</button><button class="key" @click="appendNum('6')">6</button><button class="key op" @click="appendOp('-')">-</button></view>
        <view class="pad-row"><button class="key" @click="appendNum('1')">1</button><button class="key" @click="appendNum('2')">2</button><button class="key" @click="appendNum('3')">3</button><button class="key op" @click="appendOp('+')">+</button></view>
        <view class="pad-row"><button class="key zero" @click="appendNum('0')">0</button><button class="key" @click="appendNum('.')">.</button><button class="key eq" @click="calculate">=</button></view>
      </view>
    </view>
    <view v-if="showHistory" class="history-overlay" @click="showHistory = false">
      <view class="history-panel" @click.stop>
        <view class="h-head"><text class="h-title">历史记录</text><text class="h-clear" @click="history = []">清空</text><text class="h-close" @click="showHistory = false">×</text></view>
        <scroll-view class="h-list" scroll-y><view class="h-item" v-for="(h, idx) in history" :key="idx" @click="loadHistory(h)"><text class="h-expr">{{ h.expr }}</text><text class="h-res">= {{ h.res }}</text></view><view class="h-empty" v-if="!history.length"><text>无记录</text></view></scroll-view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const display = ref("0")
const expression = ref("")
const showHistory = ref(false)
const history = ref([])
function appendNum(n) { if (display.value === "0" && n !== ".") display.value = n; else display.value += n }
function appendOp(op) { expression.value = display.value + " " + op + " "; display.value = "0" }
function clearAll() { display.value = "0"; expression.value = "" }
function delOne() { display.value = display.value.length > 1 ? display.value.slice(0, -1) : "0" }
function calculate() {
  try {
    const expr = (expression.value + display.value).replace(/×/g, "*").replace(/÷/g, "/")
    const res = eval(expr)
    const result = Math.round(res * 1e10) / 1e10
    history.value.unshift({ expr: expression.value + display.value, res: result })
    if (history.value.length > 20) history.value.pop()
    expression.value = ""; display.value = String(result)
  } catch (e) { display.value = "Error"; expression.value = "" }
}
function loadHistory(h) { display.value = h.res; expression.value = ""; showHistory.value = false }
function goBack() { uni.navigateBack() }
onMounted(() => { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.calc-page { min-height: 100vh; background: #1a1a2e; display: flex; flex-direction: column; }
.custom-nav { background: linear-gradient(135deg, #16213e, #0f3460); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 44rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { flex: 1; display: flex; flex-direction: column; }
.display { padding: 32rpx; text-align: right; min-height: 200rpx; display: flex; flex-direction: column; justify-content: flex-end; }
.expr { font-size: 32rpx; color: rgba(255,255,255,0.5); display: block; }
.result { font-size: 80rpx; color: #fff; font-weight: 300; display: block; }
.pad { display: flex; flex-direction: column; gap: 16rpx; padding: 0 16rpx 32rpx; }
.pad-row { display: flex; gap: 16rpx; }
.key { flex: 1; height: 110rpx; line-height: 110rpx; text-align: center; border-radius: 50rpx; font-size: 36rpx; background: #2d2d44; color: #fff; border: none; }
.key.fn { background: #4a4a6a; color: #ffa502; }
.key.op { background: #ffa502; color: #fff; }
.key.eq { background: #2ed573; color: #fff; }
.key.zero { flex: 2; }
.key::after { border: none; }
.history-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.6); z-index: 999; display: flex; align-items: flex-end; }
.history-panel { width: 100%; max-height: 70vh; background: #fff; border-radius: 32rpx 32rpx 0 0; display: flex; flex-direction: column; }
.h-head { display: flex; align-items: center; padding: 28rpx 32rpx; border-bottom: 2rpx solid #f0f0f0; }
.h-title { flex: 1; font-size: 30rpx; font-weight: 600; }
.h-clear { font-size: 24rpx; color: #999; padding: 0 16rpx; }
.h-close { font-size: 40rpx; color: #999; }
.h-list { max-height: 60vh; padding: 0 32rpx; }
.h-item { padding: 20rpx 0; border-bottom: 2rpx solid #f8f8f8; text-align: right; }
.h-expr { font-size: 24rpx; color: #999; display: block; }
.h-res { font-size: 32rpx; color: #333; display: block; margin-top: 4rpx; }
.h-empty { text-align: center; padding: 40rpx; font-size: 24rpx; color: #999; }
</style>
