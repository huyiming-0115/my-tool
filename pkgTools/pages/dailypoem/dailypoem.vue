
<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">←</text><text class="nav-title">每日诗词</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="dp-date"><text>{{dateStr}}</text></view>
      <view class="dp-card">
        <view class="dp-decoration">❝</view>
        <text class="dp-title">{{poem.title}}</text>
        <text class="dp-author">{{poem.author}} · {{poem.dynasty}}</text>
        <view class="dp-lines">
          <text class="dp-line" v-for="(line, i) in poem.lines" :key="i">{{line}}</text>
        </view>
        <view class="dp-decoration bottom">❞</view>
      </view>
      <view class="dp-notes" v-if="poem.notes">
        <text class="dp-notes-title">注释</text>
        <text class="dp-notes-text">{{poem.notes}}</text>
      </view>
      <view class="dp-appreciation" v-if="poem.appreciation">
        <text class="dp-notes-title">赏析</text>
        <text class="dp-notes-text">{{poem.appreciation}}</text>
      </view>
      <view class="dp-refresh" @click="refresh"><text>换一首</text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const dateStr = ref("")
const poem = ref({title:"", author:"", dynasty:"", lines:[], notes:"", appreciation:""})
const poems = [
  {title:"静夜思",author:"李白",dynasty:"唐",lines:["床前明月光，","疑是地上霜。","举头望明月，","低头思故乡。"],notes:"床：井栏。 疑：怀疑。 举头：抬头。",appreciation:"这首诗写的是在寂静的月夜思念家乡的感受。诗人用比喻的手法，把月光比作霜，表达了他对家乡的深深思念。"},
  {title:"春晓",author:"孟浩然",dynasty:"唐",lines:["春眠不觉晓，","处处闻啼鸟。","夜来风雨声，","花落知多少。"],notes:"晓：天亮。 闻：听到。",appreciation:"全诗语言平易浅近，自然天成，言浅意浓，景真情真，是唐代五绝的典型代表作品。"},
  {title:"登鹳雀楼",author:"王之涣",dynasty:"唐",lines:["白日依山尽，","黄河入海流。","欲穷千里目，","更上一层楼。"],notes:"鹳雀楼：古名鹳鹊楼。 依：靠着。 穷：尽。",appreciation:"这首诗写诗人登楼望远的感受。前两句写景，气势磅礴；后两句议论，寓含深刻的人生哲理。"},
  {title:"相思",author:"王维",dynasty:"唐",lines:["红豆生南国，","春来发几枝。","愿君多采撷，","此物最相思。"],notes:"红豆：又名相思子。 采撷：采摘。",appreciation:"这首诗是借咏物而寄怀的名作。一题为《江上赠李龟年》，可见是眷怀友人无疑。"},
  {title:"江雪",author:"柳宗元",dynasty:"唐",lines:["千山鸟飞绝，","万径人踪灭。","孤舟蓑笠翁，","独钓寒江雪。"],notes:"绝：绝迹。 蓑笠：蓑衣和斗笠。",appreciation:"这首诗描绘了一幅渔翁寒江独钓图，表达了诗人虽处境孤独，但傲岸不屈的性格。"},
  {title:"水调歌头",author:"苏轼",dynasty:"宋",lines:["明月几时有？","把酒问青天。","不知天上宫阙，","今夕是何年。"],notes:"把酒：端起酒杯。 宫阙：宫殿。",appreciation:"这首词是中秋望月怀人之作，表达了对胞弟苏辙的无限思念。"}
]
function refresh() {
  var idx = Math.floor(Math.random() * poems.length)
  poem.value = poems[idx]
}
function goBack() { uni.navigateBack() }
onMounted(function() {
  if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }
  var d = new Date()
  dateStr.value = d.getFullYear() + "年" + (d.getMonth()+1) + "月" + d.getDate() + "日"
  refresh()
})
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #f5f7fa, #c3cfe2); }
.custom-nav { background: linear-gradient(135deg, #f5f7fa, #c3cfe2); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #555; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #555; font-weight: 600; }
.content { padding: 32rpx; }
.dp-date { text-align: center; margin-bottom: 24rpx; }
.dp-date text { color: #999; font-size: 26rpx; }
.dp-card { background: #fff; border-radius: 24rpx; padding: 48rpx 32rpx; margin-bottom: 24rpx; box-shadow: 0 8rpx 32rpx rgba(0,0,0,0.08); text-align: center; }
.dp-decoration { color: #c3cfe2; font-size: 48rpx; }
.dp-decoration.bottom { transform: rotate(180deg); }
.dp-title { color: #333; font-size: 40rpx; font-weight: 700; display: block; margin: 16rpx 0 8rpx; }
.dp-author { color: #999; font-size: 24rpx; display: block; margin-bottom: 32rpx; }
.dp-lines { margin-bottom: 16rpx; }
.dp-line { color: #555; font-size: 32rpx; line-height: 2; display: block; }
.dp-notes, .dp-appreciation { background: #fff; border-radius: 20rpx; padding: 24rpx; margin-bottom: 20rpx; }
.dp-notes-title { color: #764ba2; font-size: 26rpx; font-weight: 600; display: block; margin-bottom: 12rpx; }
.dp-notes-text { color: #666; font-size: 26rpx; line-height: 1.8; }
.dp-refresh { text-align: center; margin-top: 24rpx; }
.dp-refresh text { color: #764ba2; font-size: 28rpx; background: rgba(118,75,162,0.1); padding: 16rpx 40rpx; border-radius: 30rpx; }
</style>
