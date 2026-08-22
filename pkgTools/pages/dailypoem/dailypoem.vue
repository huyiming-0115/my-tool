<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\u2190</text><text class="nav-title">\u6bcf\u65e5\u8bd7\u8bcd</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="poem-card">
        <text class="poem-title">{{ poem.title }}</text>
        <text class="poem-author">{{ poem.author }} \u00b7 {{ poem.dynasty }}</text>
        <view class="poem-body"><text class="poem-line" v-for="(line, i) in poem.lines" :key="i">{{ line }}</text></view>
        <view class="poem-desc" v-if="showDesc"><text>{{ poem.desc }}</text></view>
        <text class="toggle-btn" @click="showDesc=!showDesc">{{ showDesc ? '\u6536\u8d77\u8bd1\u6587' : '\u67e5\u770b\u8bd1\u6587' }}</text>
      </view>
      <view class="refresh-btn" @click="refresh"><text>\u6362\u4e00\u9996</text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const poem = ref({title:"",author:"",dynasty:"",lines:[],desc:""})
const showDesc = ref(false)
const poems = [
  {title:"\u9759\u591c\u601d",author:"\u674e\u767d",dynasty:"\u5549",lines:["\u5e8a\u524d\u660e\u6708\u5149","\u7591\u662f\u5730\u4e0a\u971c","\u4e3e\u5934\u671b\u660e\u6708","\u4f4e\u5934\u601d\u6545\u4e61"],desc:"\u8fd9\u9996\u8bd7\u5199\u7684\u662f\u5728\u9759\u8b60\u7684\u591c\u665a\uff0c\u89c2\u770b\u660e\u6708\u7684\u60c5\u666f"},
  {title:"\u767b\u9e40\u697c",author:"\u738b\u4e4b\u6da3",dynasty:"\u5549",lines:["\u767d\u65e5\u4f0a\u5c71\u5c3d","\u9ec4\u6cb3\u5165\u6d77\u6d41","\u6b32\u7a77\u5343\u91cc\u76ee","\u66f4\u4e0a\u4e00\u5c42\u697c"],desc:"\u8fd9\u9996\u8bd7\u8868\u8fbe\u4e86\u8bd7\u4eba\u7684\u626c\u5fd7\u594b\u53d1\u4e4b\u60c5"},
  {title:"\u6625\u6653",author:"\u5b5f\u6d69\u7136",dynasty:"\u5549",lines:["\u6625\u7720\u4e0d\u89c9\u6653","\u5904\u5904\u95fb\u557c\u9e1f","\u591c\u6765\u98ce\u96e8\u58f0","\u82b1\u843d\u77e5\u591a\u5c11"],desc:"\u8fd9\u9996\u8bd7\u5199\u6625\u65e5\u6e05\u6668\u7684\u666f\u8c22"},
  {title:"\u5c71\u5c45\u79cb\u665f",author:"\u738b\u7ef4",dynasty:"\u5549",lines:["\u7a7a\u5c71\u65b0\u96e8\u540e","\u5929\u6c14\u6765\u66ae\u79cb","\u660e\u6708\u67f4\u95f4\u7167","\u6e05\u6cc9\u77f3\u4e0a\u6d41"],desc:"\u8fd9\u9996\u8bd7\u63cf\u5199\u7684\u662f\u5c71\u95f4\u79cb\u591c\u7684\u7f8e\u4e3d\u666f\u8272"},
  {title:"\u6708\u4e0b\u72ec\u914c",author:"\u674e\u767d",dynasty:"\u5549",lines:["\u82b1\u95f4\u4e00\u58f6\u9152","\u72ec\u914c\u65e0\u76f8\u4eb2","\u63ea\u6708\u6210\u4e09\u5f71","\u6211\u6b4c\u6708\u5f25\u8fb9"],desc:"\u8fd9\u9996\u8bd7\u8868\u8fbe\u4e86\u8bd7\u4eba\u72ec\u5c45\u5f02\u4e61\u7684\u611f\u60c5"}
]
function refresh() {
  showDesc.value = false
  poem.value = poems[Math.floor(Math.random() * poems.length)]
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }; refresh() })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #ffecd2, #fcb69f); }
.custom-nav { background: linear-gradient(135deg, #e17055, #fdcb6e); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.poem-card { background: #fff; border-radius: 24rpx; padding: 40rpx; text-align: center; margin-bottom: 32rpx; }
.poem-title { font-size: 36rpx; font-weight: 700; color: #333; display: block; margin-bottom: 8rpx; }
.poem-author { font-size: 24rpx; color: #999; display: block; margin-bottom: 24rpx; }
.poem-body { margin-bottom: 20rpx; }
.poem-line { font-size: 30rpx; color: #444; display: block; padding: 4rpx 0; line-height: 1.8; }
.poem-desc { background: #f8f8f8; border-radius: 16rpx; padding: 20rpx; font-size: 24rpx; color: #666; text-align: left; margin-top: 16rpx; }
.toggle-btn { font-size: 24rpx; color: #e17055; margin-top: 16rpx; display: inline-block; }
.refresh-btn { background: linear-gradient(135deg, #e17055, #fdcb6e); border-radius: 16rpx; padding: 24rpx; text-align: center; }
.refresh-btn text { color: #fff; font-size: 28rpx; font-weight: 600; }
</style>
