# -*- coding: utf-8 -*-
import os
base = "pkgTools/pages"
def w(name, content):
    with open(os.path.join(base, name, name + ".vue"), "w") as f:
        f.write(content)
    print("OK:", name)

# ===== decisionwheel =====
w("decisionwheel", """<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\\u2190</text><text class="nav-title">\\u968f\\u673a\\u51b3\\u5b9a\\u5668</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="wheel-container">
        <view class="wheel" :style="{transform: 'rotate('+rotation+'deg)', transition: spinning?'2s ease-out':'none'}">
          <view class="wheel-section" v-for="(opt, i) in options" :key="i" :style="{transform: 'rotate('+(i*360/options.length)+'deg)', background: wheelColors[i%wheelColors.length]}">
            <text class="wheel-text">{{ opt }}</text>
          </view>
        </view>
        <view class="wheel-pointer">\\u25b2</view>
      </view>
      <text class="result-text\" v-if=\"result\">{{ result }}</text>
      <view class=\"spin-btn\" @click=\"spin\"><text>{{ spinning ? '\\u8f6c\\u52a8\\u4e2d...' : '\\u5f00\\u59cb\\u8f6c\\u52a8' }}</text></view>
      <view class=\"options-edit\">
        <text class=\"section-title\">\\u9009\\u9879 (\\u6bcf\\u884c\\u4e00\\u4e2a)</text>
        <textarea class=\"opt-input\" v-model=\"optionsText\" placeholder=\"\\u8f93\\u5165\\u9009\\u9879\" auto-height></textarea>
        <text class=\"save-btn\" @click=\"saveOptions\">\\u4fdd\\u5b58</text>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const defaultOpts = ["\\u662f\",\"\\u5426\",\"\\u518d\\u60f3\\u60f3\",\"\\u5f53\\u7136\",\"\\u4e0d\\u884c\",\"\\u53ef\\u4ee5\"]
const options = ref(defaultOpts.slice())
const optionsText = ref(defaultOpts.join("\\n"))
const rotation = ref(0)
const spinning = ref(false)
const result = ref("")
const wheelColors = ["#ff6b6b","#feca57","#48dbfb","#ff9ff3","#54a0ff","#5f27cd","#00d2d3","#ff9f43"]
function spin() {
  if (spinning.value) return
  spinning.value = true
  result.value = ""
  const spins = 5 + Math.random() * 5
  const idx = Math.floor(Math.random() * options.value.length)
  rotation.value += spins * 360 + (360 - idx * (360 / options.value.length))
  setTimeout(function() {
    spinning.value = false
    result.value = "\\u2728 " + options.value[idx]
    uni.vibrateShort({})
  }, 2000)
}
function saveOptions() {
  const arr = optionsText.value.split("\\n").map(function(s){return s.trim()}).filter(function(s){return s})
  if (arr.length < 2) { uni.showToast({ title: "\\u81f3\\u5c112\\u4e2a\\u9009\\u9879", icon: "none" }); return }
  options.value = arr
  uni.showToast({ title: "\\u5df2\\u4fdd\\u5b58", icon: "success" })
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #f6d365, #fda085); }
.custom-nav { background: linear-gradient(135deg, #f39c12, #e17055); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; display: flex; flex-direction: column; align-items: center; }
.wheel-container { position: relative; width: 500rpx; height: 500rpx; margin-bottom: 32rpx; }
.wheel { width: 100%; height: 100%; border-radius: 50%; position: relative; overflow: hidden; border: 8rpx solid #fff; box-shadow: 0 8rpx 32rpx rgba(0,0,0,0.2); }
.wheel-section { position: absolute; width: 50%; height: 50%; top: 0; left: 50%; transform-origin: 0 100%; display: flex; align-items: flex-start; justify-content: center; padding-top: 40rpx; }
.wheel-text { font-size: 22rpx; color: #fff; font-weight: 700; }
.wheel-pointer { position: absolute; top: -20rpx; left: 50%; transform: translateX(-50%); font-size: 40rpx; color: #e17055; }
.result-text { font-size: 40rpx; font-weight: 700; color: #fff; margin-bottom: 24rpx; }
.spin-btn { width: 80%; background: linear-gradient(135deg, #f39c12, #e17055); border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 32rpx; }
.spin-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.options-edit { width: 100%; background: rgba(255,255,255,0.3); border-radius: 20rpx; padding: 24rpx; }
.section-title { font-size: 26rpx; color: #fff; display: block; margin-bottom: 12rpx; }
.opt-input { width: 100%; background: #fff; border-radius: 12rpx; padding: 16rpx; font-size: 26rpx; min-height: 120rpx; margin-bottom: 12rpx; }
.save-btn { display: block; background: #f39c12; color: #fff; text-align: center; border-radius: 12rpx; padding: 16rpx; font-size: 26rpx; }
</style>
""")

# ===== runningpace =====
w("runningpace", """<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\\u2190</text><text class="nav-title">\\u8dd1\\u6b65\\u914d\\u901f\\u8ba1\\u7b97</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <view class="form-card"><text class=\"form-label\">\\u8ddd\\u79bb (km)</text><input class=\"form-input\" type=\"digit\" v-model=\"distance\" placeholder=\"\\u5982: 5, 10, 21.0975\" /></view>
      <view class=\"form-card\"><text class=\"form-label\">\\u65f6\\u95f4</text><view class=\"time-row\"><input class=\"time-input\" type=\"number\" v-model=\"hours\" placeholder=\"\\u65f6\" /><text class=\"time-sep\">:</text><input class=\"time-input\" type=\"number\" v-model=\"minutes\" placeholder=\"\\u5206\" /><text class=\"time-sep\">:</text><input class=\"time-input\" type=\"number\" v-model=\"seconds\" placeholder=\"\\u79d2\" /></view></view>
      <view class=\"calc-btn\" @click=\"calc\"><text>\\u8ba1\\u7b97\\u914d\\u901f</text></view>
      <view class=\"result-card\" v-if=\"pace\">
        <view class=\"result-row\"><text>\\u914d\\u901f:</text><text class=\"result-val\">{{ pace }} /km</text></view>
        <view class=\"result-row\"><text>\\u5e73\\u5747\\u901f\\u5ea6:</text><text class=\"result-val\">{{ speed }} km/h</text></view>
        <view class=\"result-row\"><text>\\u603b\\u65f6\\u95f4:</text><text class=\"result-val\">{{ totalTime }}</text></view>
      </view>
      <view class=\"preset-row\"><text class=\"preset-title\">\\u5feb\\u901f\\u8bbe\\u7f6e:</text><text class=\"preset-btn\" v-for=\"p in presets\" :key=\"p.d\" @click=\"distance=p.d\">{{ p.label }}</text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const distance = ref("")
const hours = ref("")
const minutes = ref("")
const seconds = ref("")
const pace = ref("")
const speed = ref("")
const totalTime = ref("")
const presets = [{label:"5K",d:"5"},{label:"10K",d:"10"},{label:"\\u534a\\u9a6c",d:"21.0975"},{label:"\\u5168\\u9a6c",d:"42.195"}]
function calc() {
  const d = parseFloat(distance.value) || 0
  const h = parseInt(hours.value) || 0
  const m = parseInt(minutes.value) || 0
  const s = parseInt(seconds.value) || 0
  if (d <= 0) { uni.showToast({ title: "\\u8bf7\\u8f93\\u5165\\u8ddd\\u79bb", icon: "none" }); return }
  if (h === 0 && m === 0 && s === 0) { uni.showToast({ title: "\\u8bf7\\u8f93\\u5165\\u65f6\\u95f4", icon: "none" }); return }
  const totalSec = h * 3600 + m * 60 + s
  const paceSec = totalSec / d
  const pm = Math.floor(paceSec / 60)
  const ps = Math.round(paceSec % 60)
  pace.value = pm + "'" + (ps < 10 ? "0" : "") + ps + "\""
  speed.value = (d / (totalSec / 3600)).toFixed(2)
  totalTime.value = (h ? h + "\\u65f6" : "") + (m ? m + "\\u5206" : "") + (s ? s + "\\u79d2" : "")
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #84fab0, #8fd3f4); }
.custom-nav { background: linear-gradient(135deg, #00b894, #55efc4); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.form-card { background: #fff; border-radius: 20rpx; padding: 24rpx; margin-bottom: 20rpx; }
.form-label { font-size: 26rpx; color: #666; display: block; margin-bottom: 12rpx; }
.form-input { font-size: 32rpx; color: #333; font-weight: 600; }
.time-row { display: flex; align-items: center; gap: 8rpx; }
.time-input { flex: 1; background: #f8f8f8; border-radius: 12rpx; padding: 16rpx; font-size: 32rpx; text-align: center; }
.time-sep { font-size: 36rpx; color: #999; font-weight: 700; }
.calc-btn { background: linear-gradient(135deg, #00b894, #55efc4); border-radius: 16rpx; padding: 24rpx; text-align: center; margin: 32rpx 0; }
.calc-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.result-card { background: #fff; border-radius: 24rpx; padding: 32rpx; }
.result-row { display: flex; justify-content: space-between; padding: 12rpx 0; font-size: 28rpx; }
.result-val { color: #00b894; font-weight: 700; }
.preset-row { margin-top: 24rpx; display: flex; align-items: center; gap: 12rpx; flex-wrap: wrap; }
.preset-title { color: rgba(255,255,255,0.8); font-size: 24rpx; }
.preset-btn { padding: 12rpx 24rpx; background: rgba(255,255,255,0.3); border-radius: 12rpx; color: #fff; font-size: 24rpx; }
</style>
""")

# ===== tts =====
w("tts", """<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\\u2190</text><text class="nav-title">\\u6587\\u5b57\\u8f6c\\u8bed\\u97f3</text><text class="nav-icon empty"> </text></view>
    </view>
    <view class="content">
      <textarea class=\"tts-input\" v-model=\"text\" placeholder=\"\\u8f93\\u5165\\u8981\\u8f6c\\u5316\\u4e3a\\u8bed\\u97f3\\u7684\\u6587\\u5b57\" auto-height></textarea>
      <view class=\"tts-controls\">
        <view class=\"ctrl-row\"><text class=\"ctrl-label\">\\u8bed\\u8a00:</text><picker class=\"ctrl-picker\" :range=\"langs\" @change=\"lang=$event.detail.value\"><text>{{ langs[lang] }} \\u25bc</text></picker></view>
        <view class=\"ctrl-row\"><text class=\"ctrl-label\">\\u901f\\u5ea6: {{ speed }}</text><slider class=\"ctrl-slider\" :value=\"speed\" min=\"0.5\" max=\"2\" step=\"0.1\" show-value @change=\"speed=Number($event.detail.value)\"/></view>
        <view class=\"ctrl-row\"><text class=\"ctrl-label\">\\u97f3\\u8c03: {{ pitch }}</text><slider class=\"ctrl-slider\" :value=\"pitch\" min=\"0\" max=\"2\" step=\"0.1\" show-value @change=\"pitch=Number($event.detail.value)\"/></view>
      </view>
      <view class=\"tts-btn\" @click=\"speak\"><text>{{ speaking ? '\\u64ad\\u653e\\u4e2d...' : '\\u25b6 \\u64ad\\u653e' }}</text></view>
      <view class=\"tts-btn stop\" v-if=\"speaking\" @click=\"stop\"><text>\\u25a0 \\u505c\\u6b62</text></view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from "vue"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const text = ref("")
const lang = ref(0)
const speed = ref(1)
const pitch = ref(1)
const speaking = ref(false)
const langs = ["\\u4e2d\\u6587", "\\u82f1\\u6587", "\\u65e5\\u6587"]
function speak() {
  if (!text.value.trim()) { uni.showToast({ title: "\\u8bf7\\u8f93\\u5165\\u6587\\u5b57", icon: "none" }); return }
  speaking.value = true
  const ctx = uni.createInnerAudioContext()
  ctx.src = "https://tts.baidu.com/text2audio?tex=" + encodeURIComponent(text.value) + "&cuid=baike&ctp=1&lan=zh&spd=" + Math.round(speed.value * 5) + "&pit=" + Math.round(pitch.value * 5) &vol=9&per=0"
  ctx.onEnded(function() { speaking.value = false; ctx.destroy() })
  ctx.onError(function() { speaking.value = false; uni.showToast({ title: "\\u64ad\\u653e\\u5931\\u8d25", icon: "none" }); ctx.destroy() })
  ctx.play()
}
function stop() {
  speaking.value = false
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #a1c4fd, #c2e9fb); }
.custom-nav { background: linear-gradient(135deg, #6c5ce7, #a29bfe); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.tts-input { background: #fff; border-radius: 20rpx; padding: 24rpx; font-size: 28rpx; min-height: 160rpx; margin-bottom: 24rpx; }
.tts-controls { background: #fff; border-radius: 20rpx; padding: 24rpx; margin-bottom: 24rpx; }
.ctrl-row { display: flex; align-items: center; gap: 16rpx; margin-bottom: 16rpx; }
.ctrl-label { font-size: 26rpx; color: #666; min-width: 100rpx; }
.ctrl-picker { flex: 1; background: #f8f8f8; border-radius: 12rpx; padding: 12rpx 16rpx; font-size: 26rpx; }
.ctrl-slider { flex: 1; }
.tts-btn { background: linear-gradient(135deg, #6c5ce7, #a29bfe); border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 16rpx; }
.tts-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.tts-btn.stop { background: #e17055; }
</style>
""")

# ===== vibration =====
w("vibration", """<template>
  <view class="page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row"><text class="nav-icon" @click="goBack">\\u2190</text><text class="nav-title\">\\u9707\\u52a8\\u9a6c\\u8fbe</text><text class=\"nav-icon empty\"> </text></view>
    </view>
    <view class=\"content\">
      <text class=\"section-title\">\\u9009\\u62e9\\u6a21\\u5f0f</text>
      <view class=\"vib-grid\">
        <view class=\"vib-card\" v-for=\"(p, i) in patterns\" :key=\"i\" :class=\"{ active: selected === i }\" @click=\"selected = i\">
          <text class=\"vib-emoji\">{{ p.emoji }}</text>
          <text class=\"vib-name\">{{ p.name }}</text>
        </view>
      </view>
      <view class=\"vib-btn\" @click=\"startVib\" v-if=\"selected >= 0\">
        <text>{{ vibing ? '\\u9707\\u52a8\\u4e2d...' : '\\u5f00\\u59cb\\u9707\\u52a8' }}</text>
      </view>
      <view class=\"custom-section\">
        <text class=\"section-title\">\\u81ea\\u5b9a\\u4e49\\u6a21\\u5f0f (\\u6bcf\\u884c\\u4e00\\u4e2a\\uff0c\\u5355\\u4f4dms)</text>
        <textarea class=\"vib-input\" v-model=\"customPattern\" placeholder=\"\\u5982:\\n500\\n200\\n500\\n200\\n1000\" auto-height></textarea>
        <view class=\"vib-btn custom\" @click=\"startCustom\"><text>\\u64ad\\u653e\\u81ea\\u5b9a\\u4e49</text></view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, onMounted } from \"vue\"
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const selected = ref(-1)
const vibing = ref(false)
const customPattern = ref(\"\")
const patterns = [
  { emoji: \"\\u26a1\", name: \"\\u77ed\\u4fc3\", pattern: [100] },
  { emoji: \"\\U0001f50b\", name: \"\\u8fde\\u7eed\", pattern: [200, 100, 200] },
  { emoji: \"\\u2764\\ufe0f\", name: \"\\u5fc3\\u8df3\", pattern: [300, 150, 300, 150, 600] },
  { emoji: \"\\U0001f514\", name: \"\\u94c3\\u58f0\", pattern: [500, 200, 500] },
  { emoji: \"\\U0001f680\", name: \"\\u52a0\\u901f\", pattern: [100, 50, 100, 50, 100, 50, 300] },
  { emoji: \"\\u23f0\", name: \"\\u50ac\\u4fc3\", pattern: [100, 100, 100, 100, 100, 100, 500] }
]
function startVib() {
  if (selected.value < 0) return
  vibing.value = true
  const pat = patterns[selected.value].pattern
  let i = 0
  function next() {
    if (i >= pat.length) { vibing.value = false; return }
    if (i % 2 === 0) uni.vibrateLong({})
    else uni.vibrateShort({})
    i++
    setTimeout(next, pat[i-1])
  }
  next()
}
function startCustom() {
  const arr = customPattern.value.split(\"\\n\").map(function(s){return parseInt(s.trim())}).filter(function(n){return n > 0})
  if (arr.length === 0) { uni.showToast({ title: \"\\u8bf7\\u8f93\\u5165\\u6709\\u6548\\u6a21\\u5f0f\", icon: \"none\" }); return }
  vibing.value = true
  let i = 0
  function next() {
    if (i >= arr.length) { vibing.value = false; return }
    if (i % 2 === 0) uni.vibrateLong({})
    else uni.vibrateShort({})
    i++
    setTimeout(next, arr[i-1])
  }
  next()
}
function goBack() { uni.navigateBack() }
onMounted(function() { if (!uni.getStorageSync(\"isLoggedIn\")) { uni.reLaunch({ url: \"/pages/login/login\" }); return } })
</script>
<style scoped>
.page { min-height: 100vh; background: linear-gradient(135deg, #f093fb, #f5576c); }
.custom-nav { background: linear-gradient(135deg, #e84393, #fd79a8); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 48rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 40rpx; }
.section-title { font-size: 28rpx; color: rgba(255,255,255,0.9); display: block; margin-bottom: 16rpx; }
.vib-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16rpx; margin-bottom: 32rpx; }
.vib-card { background: rgba(255,255,255,0.2); border-radius: 20rpx; padding: 24rpx; text-align: center; }
.vib-card.active { background: #fff; }
.vib-emoji { font-size: 48rpx; display: block; margin-bottom: 8rpx; }
.vib-name { font-size: 24rpx; color: #fff; }
.vib-card.active .vib-name { color: #e84393; }
.vib-btn { background: linear-gradient(135deg, #e84393, #fd79a8); border-radius: 16rpx; padding: 24rpx; text-align: center; margin-bottom: 24rpx; }
.vib-btn text { color: #fff; font-size: 30rpx; font-weight: 600; }
.vib-btn.custom { background: rgba(255,255,255,0.3); }
.custom-section { background: rgba(255,255,255,0.2); border-radius: 20rpx; padding: 24rpx; }
.vib-input { width: 100%; background: #fff; border-radius: 12rpx; padding: 16rpx; font-size: 26rpx; min-height: 120rpx; margin-bottom: 16rpx; }
</style>
""")

print("batch6 done")