<template>
  <view class="food-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">←</text>
        <text class="nav-title">食物热量</text>
        <text class="nav-icon empty"> </text>
      </view>
    </view>
    <view class="content">
      <view class="search-bar">
        <input class="search-input" v-model="searchQuery" placeholder="搜索食物..." @input="filterFoods" />
      </view>
      <view class="cat-tabs">
        <text class="cat-tab" :class="{ active: currentCat === 'all' }" @click="currentCat = 'all'; filterFoods()">全部</text>
        <text class="cat-tab" :class="{ active: currentCat === cat }" v-for="cat in categories" :key="cat" @click="currentCat = cat; filterFoods()">{{ cat }}</text>
      </view>
      <view class="food-list">
        <view class="food-item" v-for="(f, idx) in filteredFoods" :key="idx">
          <view class="f-left">
            <text class="f-name">{{ f.name }}</text>
            <text class="f-cat">{{ f.category }}</text>
          </view>
          <view class="f-right">
            <text class="f-cal">{{ f.cal }}kcal</text>
            <text class="f-unit">/100g</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, computed, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const searchQuery = ref("")
const currentCat = ref("all")
const categories = ["主食", "肉类", "蔬菜", "水果", "零食", "饮料"]
const foods = [
  { name: "白米饭", category: "主食", cal: 130 }, { name: "土豆", category: "主食", cal: 77 },
  { name: "面条", category: "主食", cal: 138 }, { name: "单白饭", category: "主食", cal: 116 },
  { name: "印度香米", category: "主食", cal: 130 }, { name: "黄豆", category: "主食", cal: 147 },
  { name: "小麦米", category: "主食", cal: 113 }, { name: "紫菜米", category: "主食", cal: 158 },
  { name: "香菜", category: "主食", cal: 154 }, { name: "红薯", category: "主食", cal: 90 },
  { name: "肉食用大米", category: "主食", cal: 111 }, { name: "包子", category: "主食", cal: 122 },
  { name: "麻辣红豆", category: "主食", cal: 147 }, { name: "花生米", category: "主食", cal: 167 },
  { name: "麻辣豆腐干", category: "主食", cal: 152 }, { name: "牛肉", category: "肉类", cal: 125 },
  { name: "猪肉", category: "肉类", cal: 143 }, { name: "鸡胸肉", category: "肉类", cal: 106 },
  { name: "鸡腿肉", category: "肉类", cal: 181 }, { name: "鲜肉", category: "肉类", cal: 124 },
  { name: "牛排", category: "肉类", cal: 155 }, { name: "黄鲜", category: "肉类", cal: 101 },
  { name: "腰果", category: "肉类", cal: 137 }, { name: "香肠", category: "肉类", cal: 207 },
  { name: "白菜", category: "蔬菜", cal: 15 }, { name: "菠菜", category: "蔬菜", cal: 26 },
  { name: "黄瓜", category: "蔬菜", cal: 16 }, { name: "西红柿", category: "蔬菜", cal: 22 },
  { name: "菜菜", category: "蔬菜", cal: 18 }, { name: "南瓜", category: "蔬菜", cal: 22 },
  { name: "萝卜", category: "蔬菜", cal: 17 }, { name: "空心菜", category: "蔬菜", cal: 16 },
  { name: "花果菜", category: "蔬菜", cal: 20 }, { name: "菜菜", category: "蔬菜", cal: 19 },
  { name: "苹果", category: "水果", cal: 52 }, { name: "香蕉", category: "水果", cal: 89 },
  { name: "橙子", category: "水果", cal: 47 }, { name: "葡萄", category: "水果", cal: 69 },
  { name: "西瓜", category: "水果", cal: 30 }, { name: "菠萝", category: "水果", cal: 41 },
  { name: "草莓", category: "水果", cal: 33 }, { name: "柠檬", category: "水果", cal: 29 },
  { name: "番茄", category: "水果", cal: 18 }, { name: "枣", category: "水果", cal: 79 },
  { name: "牛奶", category: "饮料", cal: 60 }, { name: "豆奶", category: "饮料", cal: 45 },
  { name: "奶酸", category: "饮料", cal: 73 }, { name: "奶酸酸", category: "饮料", cal: 61 },
  { name: "腰果奶", category: "饮料", cal: 60 }, { name: "咖啡(黑)", category: "饮料", cal: 2 },
  { name: "红茶", category: "饮料", cal: 1 }, { name: "果汁", category: "饮料", cal: 54 },
  { name: "可乐", category: "饮料", cal: 42 }, { name: "奶茶", category: "饮料", cal: 58 },
  { name: "腰果", category: "零食", cal: 556 }, { name: "巧克力", category: "零食", cal: 546 },
  { name: "果仁", category: "零食", cal: 631 }, { name: "玉米片", category: "零食", cal: 365 },
  { name: "面包", category: "零食", cal: 264 }, { name: "蚓糖", category: "零食", cal: 405 },
]
const filteredFoods = ref([...foods])
function goBack() { uni.navigateBack() }
function filterFoods() {
  let list = foods
  if (currentCat.value !== "all") list = list.filter(f => f.category === currentCat.value)
  if (searchQuery.value) list = list.filter(f => f.name.includes(searchQuery.value))
  filteredFoods.value = list
}
onMounted(() => {
  if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }
  filteredFoods.value = [...foods]
})
</script>
<style lang="scss" scoped>
.food-page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #10b981, #059669); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.search-bar { margin-bottom: 16rpx; }
.search-input { width: 100%; height: 72rpx; background: #fff; border-radius: 36rpx; padding: 0 28rpx; font-size: 26rpx; box-sizing: border-box; }
.cat-tabs { display: flex; flex-wrap: wrap; gap: 12rpx; margin-bottom: 24rpx; }
.cat-tab { padding: 10rpx 24rpx; background: #fff; border-radius: 30rpx; font-size: 24rpx; color: #666; }
.cat-tab.active { background: linear-gradient(135deg, #10b981, #059669); color: #fff; }
.food-list { background: #fff; border-radius: 24rpx; padding: 8rpx 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.food-item { display: flex; justify-content: space-between; align-items: center; padding: 20rpx 0; border-bottom: 2rpx solid #f9f9f9; }
.food-item:last-child { border-bottom: none; }
.f-left { flex: 1; }
.f-name { font-size: 26rpx; color: #333; font-weight: 600; display: block; }
.f-cat { font-size: 20rpx; color: #999; margin-top: 4rpx; display: block; }
.f-right { text-align: right; }
.f-cal { font-size: 26rpx; color: #10b981; font-weight: 600; display: block; }
.f-unit { font-size: 18rpx; color: #999; margin-top: 2rpx; display: block; }
</style>
