<template>
  <view class="qr-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">←</text>
        <text class="nav-title">二维码生成</text>
        <text class="nav-icon" @click="saveQR" v-if="qrImage">💾</text>
        <text class="nav-icon empty" v-else> </text>
      </view>
    </view>

    <view class="content">
      <view class="input-card">
        <view class="input-label">输入内容</view>
        <textarea class="qr-input" v-model="qrText" placeholder="输入文本、网址、联系方式等..." auto-height maxlength="500" />
        <view class="char-count">{{ qrText.length }}/500</view>
      </view>

      <view class="type-tabs">
        <text class="type-tab" :class="{ active: qrType === 'text' }" @click="qrType = 'text'">文本</text>
        <text class="type-tab" :class="{ active: qrType === 'url' }" @click="setUrl">网址</text>
        <text class="type-tab" :class="{ active: qrType === 'phone' }" @click="setPhone">电话</text>
        <text class="type-tab" :class="{ active: qrType === 'wifi' }" @click="showWifi = true">WiFi</text>
      </view>

      <view class="size-row">
        <text class="size-label">尺寸</text>
        <view class="size-options">
          <text class="size-opt" :class="{ active: qrSize === 200 }" @click="qrSize = 200; generateQR()">200px</text>
          <text class="size-opt" :class="{ active: qrSize === 300 }" @click="qrSize = 300; generateQR()">300px</text>
          <text class="size-opt" :class="{ active: qrSize === 400 }" @click="qrSize = 400; generateQR()">400px</text>
        </view>
      </view>

      <view class="generate-btn" @click="generateQR">
        <text>{{ qrImage ? "重新生成" : "生成二维码" }}</text>
      </view>

      <view class="qr-result" v-if="qrImage">
        <image class="qr-img" :src="qrImage" mode="aspectFit" show-menu-by-longpress="true"></image>
        <view class="qr-tip">长按图片可保存或分享</view>
      </view>

      <view class="empty-state" v-else>
        <text class="empty-icon">🔳</text>
        <text class="empty-text">输入内容后点击生成</text>
      </view>
    </view>

    <!-- WiFi 弹窗 -->
    <view v-if="showWifi" class="mask" @click="showWifi = false">
      <view class="wifi-panel" @click.stop>
        <view class="panel-head"><text class="panel-title">WiFi 配置</text><text class="panel-close" @click="showWifi = false">×</text></view>
        <view class="panel-body">
          <view class="form-row"><text class="form-l">网络名称(SSID)</text><input class="form-input" v-model="wifi.ssid" placeholder="WiFi名称" /></view>
          <view class="form-row"><text class="form-l">密码</text><input class="form-input" v-model="wifi.password" placeholder="WiFi密码" password /></view>
          <view class="form-row"><text class="form-l">加密类型</text>
            <view class="enc-options">
              <text class="enc-opt" :class="{ active: wifi.enc === 'WPA' }" @click="wifi.enc = 'WPA'">WPA/WPA2</text>
              <text class="enc-opt" :class="{ active: wifi.enc === 'WEP' }" @click="wifi.enc = 'WEP'">WEP</text>
              <text class="enc-opt" :class="{ active: wifi.enc === 'nopass' }" @click="wifi.enc = 'nopass'">无密码</text>
            </view>
          </view>
        </view>
        <view class="panel-footer">
          <button class="btn-cancel" @click="showWifi = false">取消</button>
          <button class="btn-save" @click="generateWifiQR">生成</button>
        </view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20

const qrText = ref("")
const qrImage = ref("")
const qrSize = ref(300)
const qrType = ref("text")
const showWifi = ref(false)
const wifi = ref({ ssid: "", password: "", enc: "WPA" })

function generateQR() {
  if (!qrText.value.trim()) { uni.showToast({ title: "请输入内容", icon: "none" }); return }
  const encoded = encodeURIComponent(qrText.value)
  qrImage.value = "https://api.qrserver.com/v1/create-qr-code/?size=" + qrSize.value + "x" + qrSize.value + "&margin=10&data=" + encoded
}

function generateWifiQR() {
  if (!wifi.value.ssid.trim()) { uni.showToast({ title: "请输入WiFi名称", icon: "none" }); return }
  const data = "WIFI:T:" + wifi.value.enc + ";S:" + wifi.value.ssid + ";P:" + wifi.value.password + ";;"
  qrText.value = data
  qrType.value = "wifi"
  showWifi.value = false
  generateQR()
}

function setUrl() {
  qrType.value = "url"
  qrText.value = "https://"
}

function setPhone() {
  qrType.value = "phone"
  qrText.value = "tel:"
}

function saveQR() {
  if (!qrImage.value) return
  uni.showLoading({ title: "保存中..." })
  uni.downloadFile({
    url: qrImage.value,
    success: (res) => {
      if (res.statusCode === 200) {
        uni.saveImageToPhotosAlbum({
          filePath: res.tempFilePath,
          success: () => { uni.hideLoading(); uni.showToast({ title: "已保存到相册", icon: "success" }) },
          fail: () => { uni.hideLoading(); uni.showToast({ title: "保存失败", icon: "none" }) }
        })
      } else {
        uni.hideLoading()
        uni.showToast({ title: "下载失败", icon: "none" })
      }
    },
    fail: () => { uni.hideLoading(); uni.showToast({ title: "下载失败", icon: "none" }) }
  })
}

function goBack() { uni.navigateBack() }

onMounted(() => { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style lang="scss" scoped>
.qr-page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #10b981, #059669); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }

.input-card { background: #fff; border-radius: 24rpx; padding: 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); margin-bottom: 24rpx; }
.input-label { font-size: 26rpx; color: #666; margin-bottom: 12rpx; }
.qr-input { width: 100%; min-height: 160rpx; font-size: 30rpx; color: #333; line-height: 1.6; }
.char-count { text-align: right; font-size: 22rpx; color: #999; margin-top: 8rpx; }

.type-tabs { display: flex; gap: 16rpx; margin-bottom: 24rpx; }
.type-tab { flex: 1; text-align: center; padding: 16rpx; background: #fff; border-radius: 16rpx; font-size: 26rpx; color: #666; }
.type-tab.active { background: linear-gradient(135deg, #10b981, #059669); color: #fff; }

.size-row { display: flex; align-items: center; margin-bottom: 24rpx; }
.size-label { font-size: 26rpx; color: #333; width: 100rpx; }
.size-options { display: flex; gap: 16rpx; flex: 1; }
.size-opt { flex: 1; text-align: center; padding: 12rpx; background: #fff; border-radius: 12rpx; font-size: 24rpx; color: #666; }
.size-opt.active { background: #10b981; color: #fff; }

.generate-btn { background: linear-gradient(135deg, #10b981, #059669); border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 24rpx; }
.generate-btn text { font-size: 30rpx; color: #fff; font-weight: 600; }

.qr-result { background: #fff; border-radius: 24rpx; padding: 40rpx; text-align: center; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.qr-img { width: 400rpx; height: 400rpx; margin: 0 auto; }
.qr-tip { font-size: 24rpx; color: #999; margin-top: 24rpx; }

.empty-state { text-align: center; padding: 80rpx 0; }
.empty-icon { font-size: 100rpx; display: block; }
.empty-text { font-size: 26rpx; color: #999; margin-top: 16rpx; display: block; }

.mask { position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 999; display: flex; align-items: flex-end; }
.wifi-panel { width: 100%; background: #fff; border-radius: 32rpx 32rpx 0 0; display: flex; flex-direction: column; }
.panel-head { display: flex; justify-content: space-between; align-items: center; padding: 28rpx 32rpx; border-bottom: 2rpx solid #f0f0f0; }
.panel-title { font-size: 30rpx; font-weight: 600; color: #1a1a1a; }
.panel-close { font-size: 40rpx; color: #999; padding: 4rpx 8rpx; }
.panel-body { padding: 12rpx 32rpx; }
.form-row { padding: 20rpx 0; border-bottom: 2rpx solid #f8f8f8; }
.form-l { font-size: 26rpx; color: #333; margin-bottom: 12rpx; display: block; }
.form-input { width: 100%; height: 64rpx; font-size: 28rpx; border: 2rpx solid #e5e7eb; border-radius: 12rpx; padding: 0 16rpx; box-sizing: border-box; }
.enc-options { display: flex; gap: 16rpx; }
.enc-opt { padding: 8rpx 20rpx; background: #f5f5f5; border-radius: 20rpx; font-size: 24rpx; color: #666; }
.enc-opt.active { background: #10b981; color: #fff; }
.panel-footer { display: flex; gap: 24rpx; padding: 24rpx 32rpx; border-top: 2rpx solid #f0f0f0; }
.btn-cancel { flex: 1; height: 80rpx; line-height: 80rpx; border-radius: 40rpx; background: #f5f5f5; color: #666; font-size: 28rpx; border: none; }
.btn-cancel::after { border: none; }
.btn-save { flex: 1; height: 80rpx; line-height: 80rpx; border-radius: 40rpx; background: linear-gradient(135deg, #10b981, #059669); color: #fff; font-size: 28rpx; font-weight: 600; border: none; }
.btn-save::after { border: none; }
</style>
