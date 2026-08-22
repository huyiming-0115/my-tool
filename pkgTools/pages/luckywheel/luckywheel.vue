<template>
  <view class="lw-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">幸运转盘</text><text class="nav-icon" @click="showEdit = !showEdit">⚙</text></view>
    </view>
    <view class="content">
      <view class="wheel-container">
        <view class="wheel" :style="{ transform: 'rotate(' + angle + 'deg)', transition: spinning ? 'transform 3s cubic-bezier(0.17, 0.67, 0.12, 0.99)' : 'none' }">
          <view class="wheel-section" v-for="(item, idx) in items" :key="idx" :style="{ transform: 'rotate(' + (360 / items.length * idx) + 'deg)', background: colors[idx % colors.length] }">
            <text class="wheel-text">{{ item }}</text>
          </view>
        </view>
        <view class="wheel-pointer"><text>▼</text></view>
      </view>
      <view class="spin-btn" :class="{ disabled: spinning || items.length < 2 }" @click="spin"><text>{{ spinning ? '旋转中...' : '开始转动' }}</text></view>
      <view class="result-area" v-if="result"><text class="result-label">结果</text><text class="result-value">{{ result }}</text></view>
    </view>
    <view v-if="showEdit" class="mask" @click="showEdit = false">
      <view class="edit-panel" @click.stop>
        <view class="panel-head"><text class="panel-title">编辑选项</text><text class="panel-close" @click="showEdit = false">×</text></view>
        <scroll-view class="panel-body" scroll-y>
          <view class="edit-item" v-for="(item, idx) in items" :key="idx">
            <input class="edit-input" v-model="items[idx]" />
            <text class="edit-del" @click="items.splice(idx, 1)">×</text>
          </view>
        </scroll-view>
        <view class="panel-footer"><button class="btn-add" @click="items.push('新选项')">添加</button><button class="btn-done" @click="showEdit = false">完成</button></view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const items = ref(["头奖", "二等奖", "三等奖", "感谢参与", "再来一次"])
const colors = ["#ff6b6b", "#feca57", "#48dbfb", "#ff9ff3", "#54a0ff", "#5f27cd"]
const angle = ref(0)
const spinning = ref(false)
const result = ref("")
const showEdit = ref(false)
function spin() {
  if (spinning.value || items.value.length < 2) return
  spinning.value = true; result.value = ""
  const idx = Math.floor(Math.random() * items.value.length)
  const secAngle = 360 / items.value.length
  angle.value += 360 * 5 + (360 - idx * secAngle - secAngle / 2)
  setTimeout(() => { spinning.value = false; result.value = items.value[idx]; uni.vibrateShort({}) }, 3200)
}
function goBack() { uni.navigateBack() }
onMounted(() => { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.lw-page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #f5576c, #ff6b6b); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 44rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 32rpx; display: flex; flex-direction: column; align-items: center; }
.wheel-container { position: relative; width: 500rpx; height: 500rpx; margin-bottom: 32rpx; }
.wheel { width: 100%; height: 100%; border-radius: 50%; overflow: hidden; position: relative; border: 8rpx solid #fff; box-shadow: 0 8rpx 32rpx rgba(0,0,0,0.15); }
.wheel-section { position: absolute; width: 50%; height: 50%; top: 0; left: 50%; transform-origin: 0 100%; display: flex; align-items: flex-start; justify-content: center; padding-top: 40rpx; }
.wheel-text { font-size: 24rpx; color: #fff; font-weight: 700; }
.wheel-pointer { position: absolute; top: -20rpx; left: 50%; transform: translateX(-50%); font-size: 48rpx; color: #d63031; z-index: 10; }
.spin-btn { width: 80%; background: linear-gradient(135deg, #f5576c, #ff6b6b); border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 24rpx; }
.spin-btn text { font-size: 32rpx; color: #fff; font-weight: 600; }
.spin-btn.disabled { opacity: 0.4; }
.result-area { text-align: center; background: #fff; border-radius: 24rpx; padding: 40rpx 60rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.result-label { font-size: 24rpx; color: #999; display: block; }
.result-value { font-size: 48rpx; color: #f5576c; font-weight: 700; display: block; margin-top: 8rpx; }
.mask { position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 999; display: flex; align-items: flex-end; }
.edit-panel { width: 100%; max-height: 70vh; background: #fff; border-radius: 32rpx 32rpx 0 0; display: flex; flex-direction: column; }
.panel-head { display: flex; justify-content: space-between; align-items: center; padding: 28rpx 32rpx; border-bottom: 2rpx solid #f0f0f0; }
.panel-title { font-size: 30rpx; font-weight: 600; }
.panel-close { font-size: 40rpx; color: #999; }
.panel-body { flex: 1; padding: 16rpx 32rpx; max-height: 50vh; }
.edit-item { display: flex; align-items: center; padding: 12rpx 0; }
.edit-input { flex: 1; height: 64rpx; background: #f5f5f5; border-radius: 12rpx; padding: 0 16rpx; font-size: 26rpx; }
.edit-del { font-size: 36rpx; color: #ccc; padding: 0 8rpx; }
.panel-footer { display: flex; gap: 24rpx; padding: 24rpx 32rpx; }
.btn-add { flex: 1; height: 80rpx; line-height: 80rpx; border-radius: 40rpx; background: #f5f5f5; color: #666; font-size: 28rpx; border: none; }
.btn-add::after { border: none; }
.btn-done { flex: 1; height: 80rpx; line-height: 80rpx; border-radius: 40rpx; background: linear-gradient(135deg, #f5576c, #ff6b6b); color: #fff; font-size: 28rpx; font-weight: 600; border: none; }
.btn-done::after { border: none; }
</style>
