<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">API\u8bf7\u6c42\u6d4b\u8bd5</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="req-row">
        <picker class="method-picker" :range="methods" @change="method=$event.detail.value"><text>{{ methods[method] }} \u25bc</text></picker>
        <input class="url-input" v-model="url" placeholder="https://api.example.com/data" />
      </view>
      <view class="form-card"><text class="form-label">Headers (JSON)</text><textarea class="header-input" v-model="headers" placeholder=\'{"Content-Type":"application/json"}\'></textarea></view>
      <view class="form-card" v-if="method > 1"><text class="form-label">Body</text><textarea class="body-input" v-model="body" placeholder="\u8bf7\u6c42\u4f53"></textarea></view>
      <view class="calc-btn" @click="sendRequest"><text>\u53d1\u9001\u8bf7\u6c42</text></view>
      <view class="result-card" v-if="response">
        <view class="status-row"><text>\u72b6\u6001: </text><text :style="{color: statusColor}">{{ statusCode }}</text><text class="time-text">{{ elapsed }}ms</text></view>
        <textarea class="resp-area" :value="response" disabled></textarea>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const methods = ["GET","POST","PUT","DELETE"]
const method = ref(0)
const url = ref("https://httpbin.org/get")
const headers = ref('{"Content-Type":"application/json"}')
const body = ref("")
const response = ref("")
const statusCode = ref("")
const elapsed = ref(0)
const statusColor = ref("#333")
function sendRequest() {
  if (!url.value) { uni.showToast({ title: "\u8bf7\u8f93\u5165URL", icon: "none" }); return }
  const start = Date.now()
  let opts = { url: url.value, method: methods[method.value], success: handleResp, fail: handleFail }
  if (body.value && method.value > 1) { try { opts.data = JSON.parse(body.value) } catch(e) { opts.data = body.value } }
  uni.request(opts)
  function handleResp(res) { statusCode.value = res.statusCode; response.value = JSON.stringify(res.data, null, 2); elapsed.value = Date.now() - start; statusColor.value = res.statusCode < 400 ? "#00b894" : "#e17055" }
  function handleFail(err) { response.value = "\u9519\u8bef: " + JSON.stringify(err); statusCode.value = "ERR"; elapsed.value = Date.now() - start }
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #2d3436, #636e72); }
.custom-nav { background: linear-gradient(135deg, #2d3436, #636e72); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.req-row { display: flex; gap: 12rpx; margin-bottom: 20rpx; }
.method-picker { background: #00b894; border-radius: 12rpx; padding: 20rpx; color: #fff; font-size: 24rpx; font-weight: 600; display: flex; align-items: center; min-width: 140rpx; justify-content: center; }
.url-input { flex: 1; background: rgba(255,255,255,0.1); border-radius: 12rpx; padding: 20rpx; font-size: 24rpx; color: #fff; }
.form-card { background: rgba(255,255,255,0.1); border-radius: 20rpx; padding: 24rpx; margin-bottom: 20rpx; }
.form-label { font-size: 26rpx; color: rgba(255,255,255,0.7); display: block; margin-bottom: 12rpx; }
.header-input, .body-input { background: rgba(255,255,255,0.1); border-radius: 12rpx; padding: 16rpx; font-size: 24rpx; color: #fff; min-height: 100rpx; font-family: monospace; }
.calc-btn { background: linear-gradient(135deg, #00b894, #00cec9); border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 32rpx; }
.calc-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.result-card { background: rgba(255,255,255,0.1); border-radius: 20rpx; padding: 24rpx; }
.status-row { display: flex; align-items: center; gap: 16rpx; margin-bottom: 16rpx; color: #fff; font-size: 26rpx; }
.time-text { margin-left: auto; color: rgba(255,255,255,0.6); }
.resp-area { width: 100%; min-height: 200rpx; background: rgba(0,0,0,0.3); border-radius: 12rpx; padding: 16rpx; font-size: 22rpx; color: #fff; font-family: monospace; }
</style>
