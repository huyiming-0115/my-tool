<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">科学计算</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="sci-display"><text class="sci-result">{{ display }}</text></view>
      <view class="sci-pad">
        <view class="sci-row"><button class="sci-key fn" @click="appendFn('sin')">sin</button><button class="sci-key fn" @click="appendFn('cos')">cos</button><button class="sci-key fn" @click="appendFn('tan')">tan</button><button class="sci-key fn" @click="appendFn('log')">log</button></view>
        <view class="sci-row"><button class="sci-key fn" @click="appendOp('^')">x^y</button><button class="sci-key fn" @click="appendFn('ln')">ln</button><button class="sci-key fn" @click="display = Math.sqrt(display) + ''">√</button><button class="sci-key fn" @click="display = (Math.PI) + ''">π</button></view>
        <view class="sci-row"><button class="sci-key" @click="appendNum('7')">7</button><button class="sci-key" @click="appendNum('8')">8</button><button class="sci-key" @click="appendNum('9')">9</button><button class="sci-key op" @click="appendOp('/')">/</button></view>
        <view class="sci-row"><button class="sci-key" @click="appendNum('4')">4</button><button class="sci-key" @click="appendNum('5')">5</button><button class="sci-key" @click="appendNum('6')">6</button><button class="sci-key op" @click="appendOp('*')">*</button></view>
        <view class="sci-row"><button class="sci-key" @click="appendNum('1')">1</button><button class="sci-key" @click="appendNum('2')">2</button><button class="sci-key" @click="appendNum('3')">3</button><button class="sci-key op" @click="appendOp('-')">-</button></view>
        <view class="sci-row"><button class="sci-key" @click="appendNum('0')">0</button><button class="sci-key" @click="appendNum('.')">.</button><button class="sci-key fn" @click="clearAll">AC</button><button class="sci-key op" @click="appendOp('+')">+</button></view>
        <view class="sci-row"><button class="sci-key eq wide" @click="calculate">=</button></view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const display = ref("0")
var pendingOp = null; var prevVal = 0
function appendNum(n) { display.value = display.value === "0" ? n : display.value + n }
function appendOp(op) { prevVal = parseFloat(display.value); pendingOp = op; display.value = "0" }
function appendFn(fn) {
  var v = parseFloat(display.value)
  if (fn === "sin") display.value = Math.sin(v * Math.PI / 180) + ""
  else if (fn === "cos") display.value = Math.cos(v * Math.PI / 180) + ""
  else if (fn === "tan") display.value = Math.tan(v * Math.PI / 180) + ""
  else if (fn === "log") display.value = Math.log10(v) + ""
  else if (fn === "ln") display.value = Math.log(v) + ""
}
function calculate() {
  if (!pendingOp) return
  var curr = parseFloat(display.value), res = 0
  if (pendingOp === "+") res = prevVal + curr
  else if (pendingOp === "-") res = prevVal - curr
  else if (pendingOp === "*") res = prevVal * curr
  else if (pendingOp === "/") res = prevVal / curr
  else if (pendingOp === "^") res = Math.pow(prevVal, curr)
  display.value = Math.round(res * 1e10) / 1e10 + ""
  pendingOp = null
}
function clearAll() { display.value = "0"; pendingOp = null }
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: #1a1a2e; display: flex; flex-direction: column; }
.custom-nav { background: linear-gradient(135deg, #2d3436, #00b894); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 44rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { flex: 1; display: flex; flex-direction: column; }
.sci-display { padding: 32rpx; text-align: right; min-height: 160rpx; display: flex; align-items: flex-end; justify-content: flex-end; }
.sci-result { font-size: 64rpx; color: #00b894; font-weight: 300; word-break: break-all; }
.sci-pad { flex: 1; display: flex; flex-direction: column; gap: 12rpx; padding: 0 16rpx 32rpx; }
.sci-row { display: flex; gap: 12rpx; }
.sci-key { flex: 1; height: 90rpx; line-height: 90rpx; text-align: center; border-radius: 16rpx; font-size: 28rpx; background: #2d2d44; color: #fff; border: none; }
.sci-key.fn { background: #4a4a6a; color: #00cec9; }
.sci-key.op { background: #00b894; color: #fff; }
.sci-key.eq { background: #e17055; color: #fff; }
.sci-key.wide { flex: 4; }
.sci-key::after { border: none; }
</style>