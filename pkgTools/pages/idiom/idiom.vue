
<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">成语词典</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="id-search"><input class="id-search-input" v-model="query" placeholder="输入成语或关键字" @input="search" /></view>
      <view class="id-list" v-if="results.length">
        <view class="id-item" v-for="item in results" :key="item.word" @click="selectItem(item)">
          <text class="id-word">{{item.word}}</text>
          <text class="id-spell">{{item.spell}}</text>
        </view>
      </view>
      <view class="id-detail" v-if="selected">
        <text class="id-d-word">{{selected.word}}</text>
        <text class="id-d-spell">{{selected.spell}}</text>
        <view class="id-d-section"><text class="id-d-label">释义</text><text class="id-d-text">{{selected.meaning}}</text></view>
        <view class="id-d-section"><text class="id-d-label">出处</text><text class="id-d-text">{{selected.source}}</text></view>
        <view class="id-d-section"><text class="id-d-label">例句</text><text class="id-d-text">{{selected.example}}</text></view>
      </view>
      <view class="id-empty" v-if="!results.length && !selected">
        <text>输入关键字搜索成语</text>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const query = ref("")
const results = ref([])
const selected = ref(null)
const idioms = [
  {word:"画蛇添足",spell:"huà shé tiān zú",meaning:"做多余的事，反而不恰当。",source:"《战国策·齐策二》",example:"这篇文章已有结论，再加一段就是画蛇添足了。"},
  {word:"守株待兔",spell:"sh\u016u zhš dài tù",spell:"sh\u016u zhš dài tù",meaning:"比喻不主动努力，存侥幸心理。",source:"《韩非子·五蠹》",example:"不能守株待兔，要主动出击。"},
  {word:"掩耳盗铃",spell:"yěn ěr dào líng",meaning:"比喻自欺欺人。",source:"《吕氏春秋·自知》",example:"不解决问题只掩盖事实，无异于掩耳盗铃。"},
  {word:"亡羊补牢",spell:"wáng yáng bū láo",meaning:"出了问题后及时补救。",source:"《战国策·楚策四》",example:"虽然失败了，但亡羊补牢，为时不晚。"},
  {word:"刻舟求剑",spell:"kè zhōú qiú jiàn",meaning:"比喻拘泥成例，不知变通。",source:"《吕氏春秋·察今》",example:"时代在变，不能刻舟求剑。"},
  {word:"井底之蛙",spell:"jǐng dǐ zhī wā",meaning:"比喻见识短浅的人。",source:"《庄子·秋水》",example:"不要做井底之蛙，要多出去看看。"},
  {word:"对牛弹琴",spell:"duì niú tán qín",meaning:"比喻对不懂的人讲道理。",source:"《弘明集》",example:"跟他讲这些，简直是对牛弹琴。"},
  {word:"杯弓蛇影",spell:"bēi gōng shé yǐng",meaning:"比喻疑神疑鬼，自相惊扰。",source:"《晋书·乐广传》",example:"别杯弓蛇影，事情没你想的那么糟。"}
]
function search() {
  if (!query.value) { results.value = []; selected.value = null; return }
  var q = query.value
  results.value = idioms.filter(function(item) {
    return item.word.indexOf(q) >= 0 || item.spell.toLowerCase().indexOf(q.toLowerCase()) >= 0
  }).slice(0, 10)
  selected.value = null
}
function selectItem(item) { selected.value = item }
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #ffecd2, #fcb69f); }
.custom-nav { background: linear-gradient(135deg, #ff9a9e, #fecfef); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 32rpx; }
.id-search { margin-bottom: 24rpx; }
.id-search-input { background: rgba(255,255,255,0.5); border-radius: 16rpx; padding: 16rpx 24rpx; font-size: 30rpx; color: #333; }
.id-list { display: flex; flex-direction: column; gap: 12rpx; margin-bottom: 24rpx; }
.id-item { background: rgba(255,255,255,0.5); border-radius: 16rpx; padding: 20rpx 24rpx; }
.id-word { color: #333; font-size: 32rpx; font-weight: 700; display: block; }
.id-spell { color: #888; font-size: 24rpx; display: block; margin-top: 4rpx; }
.id-detail { background: rgba(255,255,255,0.5); border-radius: 20rpx; padding: 28rpx; }
.id-d-word { color: #333; font-size: 40rpx; font-weight: 700; display: block; }
.id-d-spell { color: #888; font-size: 26rpx; display: block; margin-top: 8rpx; margin-bottom: 20rpx; }
.id-d-section { margin-bottom: 16rpx; }
.id-d-label { color: #ff6b6b; font-size: 24rpx; font-weight: 600; display: block; margin-bottom: 4rpx; }
.id-d-text { color: #555; font-size: 28rpx; line-height: 1.6; }
.id-empty { text-align: center; padding: 80rpx 0; }
.id-empty text { color: rgba(0,0,0,0.3); font-size: 28rpx; }
</style>
