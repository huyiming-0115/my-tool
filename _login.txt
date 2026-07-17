<template>
  <view class="login-page">
    <!-- 背景装饰 -->
    <view class="bg-decor">
      <view class="circle c1"></view>
      <view class="circle c2"></view>
      <view class="circle c3"></view>
    </view>

    <!-- 内容区 -->
    <view class="content">
      <!-- Logo 区 -->
      <view class="logo-area">
        <view class="logo-wrap">
          <text class="logo-emoji">🧭</text>
        </view>
        <text class="app-title">我的笔记工具箱</text>
        <text class="app-subtitle">记录生活，规划旅程，一处搞定</text>
      </view>

      <!-- 表单区 -->
      <view class="form-wrap">
        <view class="tab-row">
          <text
            class="tab-item"
            :class="{ active: tab === 'pwd' }"
            @click="tab = 'pwd'"
          >密码登录</text>
          <text
            class="tab-item"
            :class="{ active: tab === 'sms' }"
            @click="tab = 'sms'"
          >验证码登录</text>
        </view>

        <!-- 密码登录 -->
        <view v-if="tab === 'pwd'" class="form-content">
          <view class="input-group">
            <text class="input-icon">👤</text>
            <input
              class="input"
              type="text"
              v-model="form.username"
              placeholder="请输入手机号/账号"
              placeholder-class="ph"
              maxlength="30"
            />
          </view>
          <view class="input-group">
            <text class="input-icon">🔒</text>
            <input
              class="input"
              :password="!form.showPwd"
              v-model="form.password"
              placeholder="请输入密码"
              placeholder-class="ph"
              confirm-type="done"
              @confirm="handleLogin"
            />
            <text class="eye" @click="form.showPwd = !form.showPwd">
              {{ form.showPwd ? "🙈" : "👁️" }}
            </text>
          </view>
          <view class="form-extra">
            <label class="remember" @click="form.remember = !form.remember">
              <view class="checkbox" :class="{ checked: form.remember }">
                <text v-if="form.remember">✓</text>
              </view>
              <text class="remember-text">记住登录</text>
            </label>
            <text class="forgot" @click="handleForgot">忘记密码？</text>
          </view>
        </view>

        <!-- 验证码登录 -->
        <view v-else class="form-content">
          <view class="input-group">
            <text class="input-icon">📱</text>
            <input
              class="input"
              type="number"
              v-model="form.phone"
              placeholder="请输入手机号"
              placeholder-class="ph"
              maxlength="11"
            />
          </view>
          <view class="input-group">
            <text class="input-icon">✉️</text>
            <input
              class="input"
              type="number"
              v-model="form.code"
              placeholder="请输入验证码"
              placeholder-class="ph"
              maxlength="6"
            />
            <text class="code-btn" :class="{ disabled: codeCount > 0 }" @click="handleSendCode">
              {{ codeCount > 0 ? codeCount + "s 后重发" : "获取验证码" }}
            </text>
          </view>
        </view>

        <!-- 登录按钮 -->
        <button
          class="login-btn"
          :class="{ loading: loading }"
          :disabled="loading"
          @click="handleLogin"
        >
          <text v-if="!loading">登 录</text>
          <text v-else>登录中...</text>
        </button>

        <!-- 分割 -->
        <view class="divider">
          <view class="divider-line"></view>
          <text class="divider-text">其他方式</text>
          <view class="divider-line"></view>
        </view>

        <!-- 微信一键登录 -->
        <button class="wechat-btn" :disabled="loading" @click="handleWechat">
          <text class="wechat-text">微信一键登录</text>
        </button>

        <!-- 注册入口 -->
        <view class="register-row">
          <text>还没有账号？</text>
          <text class="register-link" @click="handleRegister">立即注册</text>
        </view>
      </view>
    </view>

    <!-- 底部协议 -->
    <view class="agreement-row">
      <text class="agreement-text">登录即同意</text>
      <text class="agreement-link" @click="handleToast">《用户协议》</text>
      <text class="agreement-text">和</text>
      <text class="agreement-link" @click="handleToast">《隐私政策》</text>
    </view>
  </view>
</template>

<script setup>
import { ref, reactive, onUnmounted } from "vue"

const tab = ref("pwd")
const loading = ref(false)
const codeCount = ref(0)
let codeTimer = null

const form = reactive({
  username: "",
  password: "",
  showPwd: false,
  remember: true,
  phone: "",
  code: "",
})

const handleSendCode = () => {
  if (!form.phone.trim() || form.phone.length < 11) {
    uni.showToast({ title: "请输入正确的手机号", icon: "none" })
    return
  }
  if (codeCount.value > 0) return
  uni.showToast({ title: "验证码已发送", icon: "success" })
  codeCount.value = 60
  codeTimer = setInterval(() => {
    codeCount.value--
    if (codeCount.value <= 0) clearInterval(codeTimer)
  }, 1000)
}

const handleLogin = () => {
  if (tab.value === "pwd") {
    if (!form.username.trim()) { uni.showToast({ title: "请输入账号", icon: "none" }); return }
    if (!form.password.trim()) { uni.showToast({ title: "请输入密码", icon: "none" }); return }
  } else {
    if (!form.phone.trim()) { uni.showToast({ title: "请输入手机号", icon: "none" }); return }
    if (!form.code.trim()) { uni.showToast({ title: "请输入验证码", icon: "none" }); return }
  }
  loading.value = true
  setTimeout(() => {
    uni.setStorageSync("isLoggedIn", true)
    uni.setStorageSync("username", form.username || form.phone || "用户")
    loading.value = false
    uni.showToast({ title: "登录成功", icon: "success" })
    setTimeout(() => { uni.switchTab({ url: "/pages/home/home" }) }, 700)
  }, 800)
}

const handleWechat = () => {
  loading.value = true
  uni.login({
    provider: "weixin",
    success: () => {
      uni.setStorageSync("isLoggedIn", true)
      uni.setStorageSync("username", "微信用户")
      loading.value = false
      uni.showToast({ title: "登录成功", icon: "success" })
      setTimeout(() => { uni.switchTab({ url: "/pages/home/home" }) }, 700)
    },
    fail: () => {
      loading.value = false
      uni.showToast({ title: "微信登录失败", icon: "none" })
    },
  })
}

const handleForgot = () => uni.showToast({ title: "请联系管理员重置密码", icon: "none" })
const handleRegister = () => uni.showToast({ title: "注册功能开发中...", icon: "none" })
const handleToast = () => uni.showToast({ title: "开发中...", icon: "none" })

onUnmounted(() => {
  if (codeTimer) clearInterval(codeTimer)
})
</script>

<style lang="scss" scoped>
.login-page {
  min-height: 100vh;
  background: #ffffff;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

/* ====== 背景装饰 ====== */
.bg-decor {
  position: absolute;
  inset: 0;
  z-index: 0;
  overflow: hidden;
  pointer-events: none;
}
.circle {
  position: absolute;
  border-radius: 50%;
  opacity: 0.12;
}
.c1 {
  width: 400rpx;
  height: 400rpx;
  background: #4a6cf7;
  top: -100rpx;
  right: -100rpx;
}
.c2 {
  width: 300rpx;
  height: 300rpx;
  background: #7c3aed;
  top: 200rpx;
  left: -150rpx;
}
.c3 {
  width: 200rpx;
  height: 200rpx;
  background: #4a6cf7;
  bottom: 300rpx;
  right: -60rpx;
  opacity: 0.06;
}

/* ====== 内容区 ====== */
.content {
  position: relative;
  z-index: 1;
  flex: 1;
  padding: 160rpx 56rpx 32rpx;
  display: flex;
  flex-direction: column;
}

/* Logo 区 */
.logo-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 60rpx;
}
.logo-wrap {
  width: 140rpx;
  height: 140rpx;
  border-radius: 36rpx;
  background: linear-gradient(135deg, #4a6cf7, #7c3aed);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 12rpx 48rpx rgba(74, 108, 247, 0.25);
}
.logo-emoji {
  font-size: 64rpx;
}
.app-title {
  font-size: 38rpx;
  font-weight: 700;
  color: #1a1a1a;
  margin-top: 28rpx;
  letter-spacing: 1rpx;
}
.app-subtitle {
  font-size: 24rpx;
  color: #999;
  margin-top: 12rpx;
  letter-spacing: 2rpx;
}

/* 表单 */
.form-wrap {
  width: 100%;
}
.tab-row {
  display: flex;
  gap: 48rpx;
  margin-bottom: 40rpx;
  border-bottom: 2rpx solid #f0f0f0;
  padding-bottom: 8rpx;
}
.tab-item {
  font-size: 30rpx;
  color: #999;
  padding: 0 4rpx 16rpx;
  position: relative;
  font-weight: 500;
  transition: color 0.2s;
}
.tab-item.active {
  color: #4a6cf7;
  font-weight: 600;
}
.tab-item.active::after {
  content: "";
  position: absolute;
  bottom: -10rpx;
  left: 50%;
  transform: translateX(-50%);
  width: 40rpx;
  height: 6rpx;
  background: #4a6cf7;
  border-radius: 3rpx;
}

/* 输入组 */
.input-group {
  display: flex;
  align-items: center;
  border-bottom: 2rpx solid #f0f0f0;
  padding: 28rpx 8rpx 20rpx;
  margin-bottom: 8rpx;
}
.input-icon {
  font-size: 32rpx;
  margin-right: 20rpx;
  flex-shrink: 0;
}
.input {
  flex: 1;
  font-size: 30rpx;
  height: 56rpx;
  color: #333;
}
.ph {
  color: #ccc;
  font-size: 28rpx;
}
.eye {
  font-size: 32rpx;
  padding: 8rpx 8rpx 8rpx 24rpx;
}

/* 记住我 / 忘记密码 */
.form-extra {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 28rpx 8rpx 8rpx;
}
.remember {
  display: flex;
  align-items: center;
  gap: 10rpx;
}
.checkbox {
  width: 32rpx;
  height: 32rpx;
  border: 2rpx solid #ddd;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20rpx;
  color: #fff;
  transition: all 0.2s;
}
.checkbox.checked {
  background: #4a6cf7;
  border-color: #4a6cf7;
}
.remember-text, .forgot {
  font-size: 24rpx;
}
.remember-text { color: #666; }
.forgot { color: #4a6cf7; }

/* 验证码按钮 */
.code-btn {
  font-size: 24rpx;
  color: #4a6cf7;
  padding: 8rpx 16rpx;
  flex-shrink: 0;
}
.code-btn.disabled {
  color: #ccc;
}

/* 登录按钮 */
.login-btn {
  margin-top: 48rpx;
  height: 96rpx;
  line-height: 96rpx;
  border-radius: 48rpx;
  background: linear-gradient(135deg, #4a6cf7, #7c3aed);
  color: #fff;
  font-size: 32rpx;
  font-weight: 600;
  letter-spacing: 4rpx;
  border: none;
  box-shadow: 0 12rpx 32rpx rgba(74, 108, 247, 0.25);
  transition: opacity 0.2s, transform 0.1s;
}
.login-btn::after { border: none; }
.login-btn:active { transform: scale(0.98); }
.login-btn.loading { opacity: 0.7; }

/* 分割线 */
.divider {
  display: flex;
  align-items: center;
  margin: 48rpx 0 32rpx;
  gap: 24rpx;
}
.divider-line {
  flex: 1;
  height: 2rpx;
  background: #f0f0f0;
}
.divider-text {
  font-size: 22rpx;
  color: #ccc;
}

/* 微信登录 */
.wechat-btn {
  height: 88rpx;
  line-height: 88rpx;
  border-radius: 44rpx;
  background: #fff;
  color: #333;
  font-size: 28rpx;
  border: 2rpx solid #e8e8e8;
  font-weight: 500;
  letter-spacing: 1rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}
.wechat-btn::after { border: none; }
.wechat-text::before {
  content: "💬  ";
  font-size: 30rpx;
}

/* 注册入口 */
.register-row {
  text-align: center;
  margin-top: 40rpx;
  font-size: 24rpx;
  color: #bbb;
}
.register-link {
  color: #4a6cf7;
  margin-left: 4rpx;
}

/* 底部协议 */
.agreement-row {
  position: relative;
  z-index: 1;
  text-align: center;
  padding: 24rpx 40rpx 36rpx;
  font-size: 22rpx;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 4rpx;
  flex-wrap: wrap;
}
.agreement-text { color: #ccc; }
.agreement-link { color: #4a6cf7; }
</style>
