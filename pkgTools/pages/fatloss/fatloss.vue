<template>
  <view class="fatloss-page">
    <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-row">
        <text class="nav-icon" @click="goBack">←</text>
        <text class="nav-title">减脂计划</text>
        <text class="nav-icon" @click="openDietPlan">🍽</text>
      </view>
    </view>

    <view class="content">
      <view class="overview-card">
        <view class="overview-row">
          <view class="overview-item">
            <text class="ov-label">起始体重</text>
            <text class="ov-value">{{ goal.startWeight || "--" }}<text class="ov-unit">kg</text></text>
          </view>
          <view class="overview-item">
            <text class="ov-label">当前体重</text>
            <text class="ov-value">{{ currentWeight }}<text class="ov-unit">kg</text></text>
          </view>
          <view class="overview-item">
            <text class="ov-label">目标体重</text>
            <text class="ov-value">{{ goal.targetWeight || "--" }}<text class="ov-unit">kg</text></text>
          </view>
        </view>
        <view class="progress-section">
          <view class="progress-header">
            <text class="progress-label">减脂进度</text>
            <text class="progress-pct">{{ progressPct }}%</text>
          </view>
          <view class="progress-bar">
            <view class="progress-fill" :style="{ width: progressPct + '%' }"></view>
          </view>
          <text class="progress-sub">已减 {{ lostWeight }}kg / 共需减 {{ totalToLose }}kg</text>
        </view>
      </view>

      <view class="diet-today-card" v-if="activeDietPlan">
        <view class="diet-plan-header">
          <text class="diet-plan-name">{{ activeDietPlan.name }}</text>
          <text class="diet-day-tag">{{ todayDietLabel }}</text>
        </view>
        <view class="diet-target-row">
          <view class="diet-target-item">
            <text class="dt-value">{{ todayCalorieTarget }}</text>
            <text class="dt-label">千卡</text>
          </view>
          <view class="diet-target-item">
            <text class="dt-value">{{ todayProtein }}g</text>
            <text class="dt-label">蛋白质</text>
          </view>
          <view class="diet-target-item">
            <text class="dt-value">{{ todayCarbs }}g</text>
            <text class="dt-label">碳水</text>
          </view>
          <view class="diet-target-item">
            <text class="dt-value">{{ todayFat }}g</text>
            <text class="dt-label">脂肪</text>
          </view>
        </view>
        <view class="diet-timeline" v-if="todayMeals.length > 0">
          <text class="diet-timeline-title">今日餐食安排</text>
          <view class="meal-row" v-for="(meal, idx) in todayMeals" :key="idx">
            <text class="meal-time">{{ meal.time }}</text>
            <text class="meal-name">{{ meal.name }}</text>
            <text class="meal-cal">{{ meal.calories }}kcal</text>
          </view>
        </view>
      </view>

      <view class="diet-select-card" v-if="!activeDietPlan" @click="openDietPlan">
        <text class="diet-select-icon">🍽</text>
        <text class="diet-select-text">选择你的饮食方案</text>
        <text class="diet-select-sub">碳循环 · 16+8轻断食 · 低碳水 · 生酫</text>
      </view>

      <view class="input-section">
        <text class="section-title">今日数据</text>
        <view class="data-inputs">
          <view class="data-field">
            <text class="df-label">体重 (kg)</text>
            <input class="df-input" v-model="todayEntry.weight" type="digit" placeholder="0.0" />
          </view>
          <view class="data-field">
            <text class="df-label">饮食 (kcal)</text>
            <input class="df-input" v-model="todayEntry.calories" type="number" placeholder="0" />
          </view>
          <view class="data-field">
            <text class="df-label">运动 (分)</text>
            <input class="df-input" v-model="todayEntry.exercise" type="number" placeholder="0" />
          </view>
        </view>
        <view class="data-field">
          <text class="df-label">备注</text>
          <input class="df-input" v-model="todayEntry.note" placeholder="今天感觉如何？" />
        </view>
        <button class="save-btn" @click="saveTodayEntry">保存今日记录</button>
      </view>

      <view class="section-title">本周趋势</view>
      <view class="trend-card">
        <view class="trend-chart">
          <view class="chart-bar" v-for="(day, idx) in weekData" :key="idx">
            <view class="bar-fill" :style="{ height: getBarHeight(day.weight) + '%' }"></view>
            <text class="bar-label">{{ day.label }}</text>
            <text class="bar-value">{{ day.weight || "--" }}</text>
          </view>
        </view>
      </view>

      <view class="section-title">每日记录</view>
      <view class="record-list">
        <view class="day-record" v-for="(record, idx) in recordList" :key="idx">
          <view class="dr-left">
            <text class="dr-date">{{ record.date }}</text>
            <text class="dr-note" v-if="record.note">{{ record.note }}</text>
          </view>
          <view class="dr-right">
            <text class="dr-weight">{{ record.weight }}kg</text>
            <text class="dr-cal" v-if="record.calories">{{ record.calories }}kcal</text>
          </view>
          <text class="dr-del" @click="deleteRecord(idx)">×</text>
        </view>
      </view>
      <view class="empty-mini" v-if="recordList.length === 0">
        <text>还没有记录，开始记录今天吧</text>
      </view>
    </view>

    <view v-if="showDietPlan" class="mask" @click="showDietPlan = false">
      <view class="create-panel" @click.stop>
        <view class="panel-head">
          <text class="panel-title">选择饮食方案</text>
          <text class="panel-close" @click="showDietPlan = false">×</text>
        </view>
        <view class="panel-body">
          <view class="diet-desc">根据你的身体数据和目标，为你推荐合适的饮食方案</view>

          <view class="diet-form-section">
            <text class="diet-form-title">身体数据 (用于计算营养目标)</text>
            <view class="form-row">
              <text class="form-l">性别</text>
              <picker class="form-picker" :value="dietForm.genderIdx" :range="genders" @change="onGenderChange">
                <text>{{ genders[dietForm.genderIdx] }}</text>
              </picker>
            </view>
            <view class="form-row">
              <text class="form-l">年龄</text>
              <input class="form-input" v-model="dietForm.age" type="number" placeholder="如：25" />
            </view>
            <view class="form-row">
              <text class="form-l">身高 (cm)</text>
              <input class="form-input" v-model="dietForm.height" type="digit" placeholder="如：170" />
            </view>
            <view class="form-row">
              <text class="form-l">体重 (kg)</text>
              <input class="form-input" v-model="dietForm.weight" type="digit" placeholder="如：65" />
            </view>
            <view class="form-row">
              <text class="form-l">活动量</text>
              <picker class="form-picker" :value="dietForm.activityIdx" :range="activityLevels" range-key="label" @change="onActivityChange">
                <text>{{ activityLevels[dietForm.activityIdx].label }}</text>
              </picker>
            </view>
          </view>

          <view class="diet-form-section">
            <text class="diet-form-title">饮食方案</text>
            <view class="diet-method-list">
              <view class="diet-method" v-for="(method, idx) in dietMethods" :key="idx" :class="{ active: selectedMethod === idx }" @click="selectMethod(idx)">
                <view class="method-header">
                  <text class="method-name">{{ method.name }}</text>
                  <text class="method-tag">{{ method.tag }}</text>
                </view>
                <text class="method-desc">{{ method.desc }}</text>
                <view class="method-calories" v-if="getTDEE()">
                  <text>预估每日摄入: {{ getMethodCalories(idx) }} kcal</text>
                </view>
              </view>
            </view>
          </view>

          <view class="diet-form-section" v-if="selectedMethod >= 0 && getTDEE()">
            <text class="diet-form-title">营养目标预览</text>
            <view class="macro-preview">
              <view class="macro-item">
                <text class="macro-value">{{ getTDEE() }}</text>
                <text class="macro-label">TDEE (千卡)</text>
              </view>
              <view class="macro-item">
                <text class="macro-value">{{ previewProtein }}g</text>
                <text class="macro-label">蛋白质</text>
              </view>
              <view class="macro-item">
                <text class="macro-value">{{ previewCarbs }}g</text>
                <text class="macro-label">碳水</text>
              </view>
              <view class="macro-item">
                <text class="macro-value">{{ previewFat }}g</text>
                <text class="macro-label">脂肪</text>
              </view>
            </view>
          </view>
        </view>
        <view class="panel-footer">
          <button class="btn-cancel" @click="showDietPlan = false">取消</button>
          <button class="btn-save" @click="applyDietPlan">应用方案</button>
        </view>
      </view>
    </view>

    <view v-if="showSettings" class="mask" @click="showSettings = false">
      <view class="create-panel" @click.stop>
        <view class="panel-head">
          <text class="panel-title">目标设置</text>
          <text class="panel-close" @click="showSettings = false">×</text>
        </view>
        <view class="panel-body">
          <view class="form-row">
            <text class="form-l">起始体重 (kg)</text>
            <input class="form-input" v-model="goalForm.startWeight" type="digit" placeholder="如：70" />
          </view>
          <view class="form-row">
            <text class="form-l">目标体重 (kg)</text>
            <input class="form-input" v-model="goalForm.targetWeight" type="digit" placeholder="如：60" />
          </view>
          <view class="form-row">
            <text class="form-l">每日热量目标</text>
            <input class="form-input" v-model="goalForm.calorieTarget" type="number" placeholder="如：1500" />
          </view>
          <view class="form-row">
            <text class="form-l">计划周期 (天)</text>
            <input class="form-input" v-model="goalForm.duration" type="number" placeholder="如：90" />
          </view>
        </view>
        <view class="panel-footer">
          <button class="btn-cancel" @click="showSettings = false">取消</button>
          <button class="btn-save" @click="saveGoal">保存</button>
        </view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref, computed, onMounted } from "vue"

const statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 20
const records = ref([])
const goal = ref({ startWeight: 0, targetWeight: 0, calorieTarget: 1500, duration: 90 })
const goalForm = ref({ startWeight: 0, targetWeight: 0, calorieTarget: 1500, duration: 90 })
const showSettings = ref(false)
const showDietPlan = ref(false)
const todayEntry = ref({ weight: "", calories: "", exercise: "", note: "" })

// Diet plan data
const activeDietPlan = ref(null)
const selectedMethod = ref(-1)
const dietForm = ref({
  genderIdx: 0,
  age: 25,
  height: 170,
  weight: 65,
  activityIdx: 1,
})
const genders = ["男", "女"]
const activityLevels = [
  { label: "乕坐不动", value: 1.2 },
  { label: "轻度活动 (每周1-3次)", value: 1.375 },
  { label: "中度活动 (每周3-5次)", value: 1.55 },
  { label: "高强度 (每周6-7次)", value: 1.725 },
  { label: "极高强度", value: 1.9 },
]

const dietMethods = [
  {
    id: "carb_cycle",
    name: "碳循环饮食",
    tag: "经典",
    desc: "高碳日/中碳日/低碳日交替，配合训练节奏，保持代谢活跃同时燃脂",
    deficitRatio: 0.2,
    proteinPerKg: 1.8,
    highCarbRatio: 0.5,
    midCarbRatio: 0.35,
    lowCarbRatio: 0.2,
  },
  {
    id: "intermittent_16_8",
    name: "16+8 轻断食",
    tag: "热门",
    desc: "每天在8小时窗口内进食，其余16小时空腹，简单易执行",
    deficitRatio: 0.25,
    proteinPerKg: 1.6,
    carbRatio: 0.35,
    fatRatio: 0.35,
  },
  {
    id: "intermittent_5_2",
    name: "5:2 轻断食",
    tag: "灵活",
    desc: "每周5天正常吃，2天限制热量(约500-600kcal)，不影响社交",
    deficitRatio: 0.2,
    proteinPerKg: 1.6,
    carbRatio: 0.4,
    fatRatio: 0.3,
  },
  {
    id: "low_carb",
    name: "低碳水饮食",
    tag: "高效",
    desc: "降低碳水比例至20-25%，身体转向燃脂供能，适合快速减脂",
    deficitRatio: 0.25,
    proteinPerKg: 2.0,
    carbRatio: 0.2,
    fatRatio: 0.45,
  },
  {
    id: "keto",
    name: "生酫饮食",
    tag: "激进",
    desc: "极低碳水(<50g/天)，高脂肪，身体进入酫症状态高效燃脂",
    deficitRatio: 0.25,
    proteinPerKg: 1.8,
    carbRatio: 0.05,
    fatRatio: 0.6,
  },
  {
    id: "mediterranean",
    name: "地中海饮食",
    tag: "健康",
    desc: "高纤维、优质脂肪、适量蛋白质，适合长期可持续减脂",
    deficitRatio: 0.15,
    proteinPerKg: 1.4,
    carbRatio: 0.4,
    fatRatio: 0.3,
  },
]

const recordList = computed(() => {
  return [...records.value].sort((a, b) => b.date.localeCompare(a.date))
})

const currentWeight = computed(() => {
  if (records.value.length === 0) return "--"
  const sorted = [...records.value].sort((a, b) => b.date.localeCompare(a.date))
  return sorted[0].weight || "--"
})

const totalToLose = computed(() => {
  const start = parseFloat(goal.value.startWeight) || 0
  const target = parseFloat(goal.value.targetWeight) || 0
  if (start <= 0 || target <= 0 || start <= target) return 0
  return (start - target).toFixed(1)
})

const lostWeight = computed(() => {
  const start = parseFloat(goal.value.startWeight) || 0
  const current = parseFloat(currentWeight.value) || 0
  if (start <= 0 || current <= 0) return "0.0"
  return (start - current).toFixed(1)
})

const progressPct = computed(() => {
  const total = parseFloat(totalToLose.value) || 0
  const lost = parseFloat(lostWeight.value) || 0
  if (total <= 0) return 0
  return Math.min(100, Math.max(0, Math.round((lost / total) * 100)))
})

const weekData = computed(() => {
  const days = ["日", "一", "二", "三", "四", "五", "六"]
  const result = []
  const today = new Date()
  for (let i = 6; i >= 0; i--) {
    const d = new Date(today)
    d.setDate(d.getDate() - i)
    const dateStr = d.toISOString().slice(0, 10)
    const record = records.value.find(r => r.date === dateStr)
    result.push({
      label: days[d.getDay()],
      weight: record ? record.weight : null,
    })
  }
  return result
})

// Diet plan computed
const todayDietLabel = computed(() => {
  if (!activeDietPlan.value) return ""
  const method = activeDietPlan.value.method
  if (method.id === "carb_cycle") {
    const dayOfWeek = new Date().getDay()
    const cycle = ["高碳日", "中碳日", "低碳日", "高碳日", "低碳日", "中碳日", "休息日"]
    return cycle[dayOfWeek]
  }
  if (method.id === "intermittent_16_8") return "进食窗口内"
  if (method.id === "intermittent_5_2") {
    const dayOfWeek = new Date().getDay()
    return (dayOfWeek === 2 || dayOfWeek === 5) ? "断食日 (~500kcal)" : "正常饮食日"
  }
  return "持续执行中"
})

const todayCalorieTarget = computed(() => {
  if (!activeDietPlan.value) return 0
  const base = activeDietPlan.value.tdee
  const method = activeDietPlan.value.method
  if (method.id === "carb_cycle") {
    const dayOfWeek = new Date().getDay()
    const ratios = [0.95, 0.85, 0.7, 0.95, 0.7, 0.85, 0.9]
    return Math.round(base * ratios[dayOfWeek])
  }
  if (method.id === "intermittent_5_2") {
    const dayOfWeek = new Date().getDay()
    return (dayOfWeek === 2 || dayOfWeek === 5) ? 550 : Math.round(base * (1 - method.deficitRatio))
  }
  return Math.round(base * (1 - method.deficitRatio))
})

const todayProtein = computed(() => {
  if (!activeDietPlan.value) return 0
  return Math.round(dietForm.value.weight * activeDietPlan.value.method.proteinPerKg)
})

const todayCarbs = computed(() => {
  if (!activeDietPlan.value) return 0
  const method = activeDietPlan.value.method
  const cal = todayCalorieTarget.value
  let carbRatio = 0.35
  if (method.id === "carb_cycle") {
    const dayOfWeek = new Date().getDay()
    const ratios = [method.highCarbRatio, method.midCarbRatio, method.lowCarbRatio, method.highCarbRatio, method.lowCarbRatio, method.midCarbRatio, method.midCarbRatio]
    carbRatio = ratios[dayOfWeek]
  } else if (method.id === "intermittent_5_2") {
    const dayOfWeek = new Date().getDay()
    if (dayOfWeek === 2 || dayOfWeek === 5) return 30
    carbRatio = method.carbRatio
  } else {
    carbRatio = method.carbRatio
  }
  return Math.round((cal * carbRatio) / 4)
})

const todayFat = computed(() => {
  if (!activeDietPlan.value) return 0
  const method = activeDietPlan.value.method
  const cal = todayCalorieTarget.value
  let fatRatio = 0.3
  if (method.id === "carb_cycle") {
    const dayOfWeek = new Date().getDay()
    const ratios = [0.2, 0.3, 0.4, 0.2, 0.4, 0.3, 0.3]
    fatRatio = ratios[dayOfWeek]
  } else if (method.id === "intermittent_5_2") {
    const dayOfWeek = new Date().getDay()
    if (dayOfWeek === 2 || dayOfWeek === 5) return 25
    fatRatio = method.fatRatio
  } else {
    fatRatio = method.fatRatio
  }
  return Math.round((cal * fatRatio) / 9)
})

const todayMeals = computed(() => {
  if (!activeDietPlan.value) return []
  const method = activeDietPlan.value.method
  const cal = todayCalorieTarget.value
  if (method.id === "intermittent_16_8") {
    return [
      { time: "12:00", name: "午餐 (第一餐)", calories: Math.round(cal * 0.4) },
      { time: "15:00", name: "加餐", calories: Math.round(cal * 0.15) },
      { time: "18:30", name: "晚餐", calories: Math.round(cal * 0.35) },
      { time: "20:00", name: "宵食 (可选)", calories: Math.round(cal * 0.1) },
    ]
  }
  if (method.id === "intermittent_5_2") {
    const dayOfWeek = new Date().getDay()
    if (dayOfWeek === 2 || dayOfWeek === 5) {
      return [
        { time: "任意", name: "断食日 (~500kcal)", calories: 550 },
        { time: "", name: "建议: 少量高蛋白食物", calories: 0 },
      ]
    }
  }
  if (method.id === "keto") {
    return [
      { time: "早餐", name: "防弹咖啡/鸡蛋", calories: Math.round(cal * 0.25) },
      { time: "午餐", name: "肉类+蔬菜+橁榄油", calories: Math.round(cal * 0.4) },
      { time: "晚餐", name: "鱼类+牛油果", calories: Math.round(cal * 0.3) },
      { time: "加餐", name: "坚果/芝士", calories: Math.round(cal * 0.05) },
    ]
  }
  if (method.id === "carb_cycle") {
    const dayOfWeek = new Date().getDay()
    const dayLabels = ["高碳日", "中碳日", "低碳日", "高碳日", "低碳日", "中碳日", "休息"]
    return [
      { time: "早餐", name: "碳水: " + dayLabels[dayOfWeek], calories: Math.round(cal * 0.25) },
      { time: "午餐", name: "蛋白质为主", calories: Math.round(cal * 0.35) },
      { time: "训练后", name: (dayOfWeek === 0 || dayOfWeek === 3) ? "高碳补充" : "适量蛋白", calories: Math.round(cal * 0.15) },
      { time: "晚餐", name: (dayOfWeek === 2 || dayOfWeek === 4) ? "低碳蔬菜为主" : "均衡搭配", calories: Math.round(cal * 0.25) },
    ]
  }
  return [
    { time: "早餐 (7-7点)", name: "碳水+蛋白质", calories: Math.round(cal * 0.25) },
    { time: "午餐 (12点)", name: "碳水+蛋白+蔬菜", calories: Math.round(cal * 0.35) },
    { time: "加餐 (15点)", name: "蛋白质/水果", calories: Math.round(cal * 0.1) },
    { time: "晚餐 (18-19点)", name: "蛋白质+蔬菜", calories: Math.round(cal * 0.3) },
  ]
})

const previewProtein = computed(() => {
  if (selectedMethod.value < 0) return 0
  const method = dietMethods[selectedMethod.value]
  return Math.round(dietForm.value.weight * method.proteinPerKg)
})

const previewCarbs = computed(() => {
  if (selectedMethod.value < 0) return 0
  const method = dietMethods[selectedMethod.value]
  const tdee = getTDEE()
  if (!tdee) return 0
  const targetCal = Math.round(tdee * (1 - method.deficitRatio))
  return Math.round((targetCal * method.carbRatio) / 4)
})

const previewFat = computed(() => {
  if (selectedMethod.value < 0) return 0
  const method = dietMethods[selectedMethod.value]
  const tdee = getTDEE()
  if (!tdee) return 0
  const targetCal = Math.round(tdee * (1 - method.deficitRatio))
  return Math.round((targetCal * method.fatRatio) / 9)
})

function getBarHeight(weight) {
  if (!weight) return 5
  const weights = weekData.value.filter(d => d.weight).map(d => d.weight)
  if (weights.length === 0) return 5
  const min = Math.min(...weights)
  const max = Math.max(...weights)
  const range = max - min || 1
  return 10 + ((weight - min) / range) * 80
}

function goBack() { uni.navigateBack() }

function openSettings() {
  goalForm.value = {
    startWeight: goal.value.startWeight || "",
    targetWeight: goal.value.targetWeight || "",
    calorieTarget: goal.value.calorieTarget || "",
    duration: goal.value.duration || "",
  }
  showSettings.value = true
}

function saveGoal() {
  goal.value = {
    startWeight: parseFloat(goalForm.value.startWeight) || 0,
    targetWeight: parseFloat(goalForm.value.targetWeight) || 0,
    calorieTarget: parseInt(goalForm.value.calorieTarget) || 0,
    duration: parseInt(goalForm.value.duration) || 0,
  }
  saveData()
  showSettings.value = false
  uni.showToast({ title: "已保存", icon: "success" })
}

function saveTodayEntry() {
  const w = parseFloat(todayEntry.value.weight)
  if (!w || w <= 0) {
    uni.showToast({ title: "请输入体重", icon: "none" })
    return
  }
  const today = new Date().toISOString().slice(0, 10)
  const existing = records.value.findIndex(r => r.date === today)
  const entry = {
    date: today,
    weight: w,
    calories: parseInt(todayEntry.value.calories) || 0,
    exercise: parseInt(todayEntry.value.exercise) || 0,
    note: todayEntry.value.note || "",
  }
  if (existing >= 0) {
    records.value[existing] = entry
  } else {
    records.value.push(entry)
  }
  saveData()
  todayEntry.value = { weight: "", calories: "", exercise: "", note: "" }
  uni.showToast({ title: "记录已保存", icon: "success" })
}

function deleteRecord(idx) {
  uni.showModal({
    title: "删除记录",
    content: "确定删除此记录？",
    success: (res) => {
      if (res.confirm) {
        const sorted = recordList.value
        const target = sorted[idx]
        records.value = records.value.filter(r => r.date !== target.date)
        saveData()
      }
    },
  })
}

// Diet plan functions
function openDietPlan() {
  selectedMethod.value = activeDietPlan.value
    ? dietMethods.findIndex(m => m.id === activeDietPlan.value.method.id)
    : -1
  showDietPlan.value = true
}

function onGenderChange(e) {
  dietForm.value.genderIdx = e.detail.value
}

function onActivityChange(e) {
  dietForm.value.activityIdx = e.detail.value
}

function selectMethod(idx) {
  selectedMethod.value = idx
}

function getTDEE() {
  const w = parseFloat(dietForm.value.weight) || 0
  const h = parseFloat(dietForm.value.height) || 0
  const a = parseInt(dietForm.value.age) || 25
  if (w <= 0 || h <= 0) return 0
  let bmr
  if (dietForm.value.genderIdx === 0) {
    bmr = 10 * w + 6.25 * h - 5 * a + 5
  } else {
    bmr = 10 * w + 6.25 * h - 5 * a - 161
  }
  const activity = activityLevels[dietForm.value.activityIdx].value
  return Math.round(bmr * activity)
}

function getMethodCalories(methodIdx) {
  const tdee = getTDEE()
  if (!tdee) return "--"
  const method = dietMethods[methodIdx]
  return Math.round(tdee * (1 - method.deficitRatio))
}

function applyDietPlan() {
  if (selectedMethod.value < 0) {
    uni.showToast({ title: "请选择一种饮食方案", icon: "none" })
    return
  }
  const method = dietMethods[selectedMethod.value]
  const tdee = getTDEE()
  activeDietPlan.value = {
    name: method.name,
    method: method,
    tdee: tdee,
    createdAt: new Date().toISOString(),
  }
  saveData()
  showDietPlan.value = false
  uni.showToast({ title: "饮食方案已启用", icon: "success" })
}

function saveData() {
  uni.setStorageSync("fatloss_records", JSON.stringify(records.value))
  uni.setStorageSync("fatloss_goal", JSON.stringify(goal.value))
  uni.setStorageSync("fatloss_diet_plan", JSON.stringify(activeDietPlan.value))
  uni.setStorageSync("fatloss_diet_form", JSON.stringify(dietForm.value))
}

onMounted(() => {
  if (!uni.getStorageSync("isLoggedIn")) { uni.reLaunch({ url: "/pages/login/login" }); return }
  const savedRecords = uni.getStorageSync("fatloss_records")
  if (savedRecords) { try { records.value = JSON.parse(savedRecords) } catch (e) {} }
  const savedGoal = uni.getStorageSync("fatloss_goal")
  if (savedGoal) { try { goal.value = JSON.parse(savedGoal) } catch (e) {} }
  const savedDiet = uni.getStorageSync("fatloss_diet_plan")
  if (savedDiet) { try { activeDietPlan.value = JSON.parse(savedDiet) } catch (e) {} }
  const savedDietForm = uni.getStorageSync("fatloss_diet_form")
  if (savedDietForm) { try { dietForm.value = JSON.parse(savedDietForm) } catch (e) {} }
  const today = new Date().toISOString().slice(0, 10)
  const todayRecord = records.value.find(r => r.date === today)
  if (todayRecord) {
    todayEntry.value = {
      weight: todayRecord.weight || "",
      calories: todayRecord.calories || "",
      exercise: todayRecord.exercise || "",
      note: todayRecord.note || "",
    }
  }
})
</script>
<style lang="scss" scoped>
.fatloss-page { min-height: 100vh; background: #f5f7fb; }
.custom-nav { background: linear-gradient(135deg, #10b981, #059669); width: 100%; }
.nav-row { height: 88rpx; display: flex; align-items: center; padding: 0 24rpx; }
.nav-icon { width: 72rpx; text-align: center; font-size: 40rpx; color: #fff; font-weight: 700; flex-shrink: 0; }
.nav-icon.empty { visibility: hidden; }
.nav-title { flex: 1; text-align: center; font-size: 32rpx; color: #fff; font-weight: 600; }
.content { padding: 24rpx; }
.overview-card { background: linear-gradient(135deg, #10b981, #059669); border-radius: 24rpx; padding: 32rpx; margin-bottom: 24rpx; }
.overview-row { display: flex; justify-content: space-between; }
.overview-item { text-align: center; flex: 1; }
.ov-label { font-size: 22rpx; color: rgba(255,255,255,0.7); display: block; }
.ov-value { font-size: 36rpx; color: #fff; font-weight: 700; display: block; margin-top: 8rpx; }
.ov-unit { font-size: 20rpx; font-weight: 400; }
.progress-section { margin-top: 32rpx; }
.progress-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12rpx; }
.progress-label { font-size: 24rpx; color: rgba(255,255,255,0.8); }
.progress-pct { font-size: 28rpx; color: #fff; font-weight: 700; }
.progress-bar { height: 16rpx; background: rgba(255,255,255,0.2); border-radius: 8rpx; overflow: hidden; }
.progress-fill { height: 100%; background: #fff; border-radius: 8rpx; transition: width 0.5s; }
.progress-sub { font-size: 20rpx; color: rgba(255,255,255,0.7); margin-top: 8rpx; display: block; }

.diet-today-card { background: #fff; border-radius: 24rpx; padding: 28rpx; margin-bottom: 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.diet-plan-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20rpx; }
.diet-plan-name { font-size: 28rpx; font-weight: 600; color: #333; }
.diet-day-tag { font-size: 22rpx; color: #10b981; background: #ecfdf5; padding: 4rpx 16rpx; border-radius: 20rpx; font-weight: 600; }
.diet-target-row { display: flex; justify-content: space-around; padding: 20rpx 0; border-bottom: 2rpx solid #f0f0f0; }
.diet-target-item { text-align: center; }
.dt-value { font-size: 28rpx; font-weight: 700; color: #10b981; display: block; }
.dt-label { font-size: 20rpx; color: #999; margin-top: 4rpx; display: block; }
.diet-timeline { margin-top: 20rpx; }
.diet-timeline-title { font-size: 24rpx; color: #666; margin-bottom: 12rpx; }
.meal-row { display: flex; align-items: center; padding: 12rpx 0; border-bottom: 2rpx solid #f9f9f9; }
.meal-row:last-child { border-bottom: none; }
.meal-time { width: 140rpx; font-size: 22rpx; color: #999; }
.meal-name { flex: 1; font-size: 24rpx; color: #333; }
.meal-cal { font-size: 22rpx; color: #10b981; font-weight: 600; }

.diet-select-card { background: #fff; border-radius: 24rpx; padding: 40rpx; margin-bottom: 24rpx; text-align: center; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); border: 2rpx dashed #d1d5db; }
.diet-select-icon { font-size: 60rpx; display: block; }
.diet-select-text { font-size: 28rpx; font-weight: 600; color: #333; margin-top: 16rpx; display: block; }
.diet-select-sub { font-size: 22rpx; color: #999; margin-top: 8rpx; display: block; }

.section-title { font-size: 28rpx; font-weight: 600; color: #333; margin: 24rpx 0 16rpx; }
.input-section { background: #fff; border-radius: 24rpx; padding: 28rpx; margin-bottom: 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.data-inputs { display: flex; gap: 16rpx; margin-bottom: 16rpx; }
.data-field { flex: 1; }
.data-field:not(:last-child) { margin-bottom: 16rpx; }
.df-label { font-size: 24rpx; color: #666; margin-bottom: 8rpx; display: block; }
.df-input { width: 100%; height: 72rpx; border: 2rpx solid #e5e7eb; border-radius: 12rpx; padding: 0 16rpx; font-size: 26rpx; box-sizing: border-box; }
.data-field:not(.data-inputs .data-field) { flex: none; }
.save-btn { background: linear-gradient(135deg, #10b981, #059669); color: #fff; border-radius: 50rpx; font-size: 28rpx; margin-top: 16rpx; }
.trend-card { background: #fff; border-radius: 24rpx; padding: 28rpx; margin-bottom: 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.trend-chart { display: flex; align-items: flex-end; justify-content: space-between; height: 240rpx; }
.chart-bar { flex: 1; display: flex; flex-direction: column; align-items: center; height: 100%; justify-content: flex-end; }
.bar-fill { width: 32rpx; background: linear-gradient(to top, #10b981, #6ee7b7); border-radius: 8rpx 8rpx 0 0; min-height: 10rpx; transition: height 0.5s; }
.bar-label { font-size: 20rpx; color: #999; margin-top: 8rpx; }
.bar-value { font-size: 18rpx; color: #666; margin-top: 2rpx; }
.record-list { background: #fff; border-radius: 24rpx; padding: 8rpx 24rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); }
.day-record { display: flex; align-items: center; padding: 20rpx 0; border-bottom: 2rpx solid #f9f9f9; }
.day-record:last-child { border-bottom: none; }
.dr-left { flex: 1; }
.dr-date { font-size: 24rpx; color: #333; font-weight: 600; display: block; }
.dr-note { font-size: 20rpx; color: #999; margin-top: 4rpx; display: block; }
.dr-right { text-align: right; }
.dr-weight { font-size: 26rpx; color: #10b981; font-weight: 600; display: block; }
.dr-cal { font-size: 20rpx; color: #999; margin-top: 4rpx; display: block; }
.dr-del { width: 48rpx; height: 48rpx; display: flex; align-items: center; justify-content: center; font-size: 32rpx; color: #ccc; margin-left: 16rpx; }
.empty-mini { text-align: center; padding: 32rpx; font-size: 24rpx; color: #999; }
.mask { position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 999; display: flex; align-items: flex-end; }
.create-panel { width: 100%; background: #fff; border-radius: 32rpx 32rpx 0 0; max-height: 80vh; display: flex; flex-direction: column; }
.panel-head { display: flex; justify-content: space-between; align-items: center; padding: 28rpx 32rpx; border-bottom: 2rpx solid #f0f0f0; }
.panel-title { font-size: 30rpx; font-weight: 600; color: #1a1a1a; }
.panel-close { font-size: 40rpx; color: #999; padding: 4rpx 8rpx; }
.panel-body { flex: 1; padding: 12rpx 32rpx; overflow-y: auto; }
.form-row { display: flex; align-items: center; padding: 20rpx 0; border-bottom: 2rpx solid #f8f8f8; }
.form-l { font-size: 26rpx; color: #333; width: 200rpx; flex-shrink: 0; font-weight: 500; }
.form-input { flex: 1; font-size: 28rpx; color: #333; height: 56rpx; }
.form-picker { flex: 1; height: 56rpx; line-height: 56rpx; font-size: 26rpx; }
.panel-footer { display: flex; gap: 24rpx; padding: 24rpx 32rpx; border-top: 2rpx solid #f0f0f0; }
.btn-cancel { flex: 1; height: 80rpx; line-height: 80rpx; border-radius: 40rpx; background: #f5f5f5; color: #666; font-size: 28rpx; border: none; }
.btn-cancel::after { border: none; }
.btn-save { flex: 1; height: 80rpx; line-height: 80rpx; border-radius: 40rpx; background: linear-gradient(135deg, #10b981, #059669); color: #fff; font-size: 28rpx; font-weight: 600; border: none; }
.btn-save::after { border: none; }

.diet-desc { font-size: 24rpx; color: #666; padding: 16rpx 0; text-align: center; }
.diet-form-section { margin-bottom: 20rpx; }
.diet-form-title { font-size: 24rpx; font-weight: 600; color: #333; padding: 16rpx 0 8rpx; display: block; }
.diet-method-list { display: flex; flex-direction: column; gap: 12rpx; }
.diet-method { padding: 20rpx; background: #f9fafb; border-radius: 16rpx; border: 2rpx solid transparent; transition: all 0.2s; }
.diet-method.active { border-color: #10b981; background: #ecfdf5; }
.method-header { display: flex; align-items: center; gap: 12rpx; margin-bottom: 8rpx; }
.method-name { font-size: 26rpx; font-weight: 600; color: #333; }
.method-tag { font-size: 18rpx; color: #10b981; background: #d1fae5; padding: 2rpx 12rpx; border-radius: 8rpx; }
.diet-method.active .method-name { color: #10b981; }
.method-desc { font-size: 22rpx; color: #666; line-height: 1.5; }
.method-calories { font-size: 22rpx; color: #10b981; font-weight: 600; margin-top: 8rpx; }
.macro-preview { display: flex; justify-content: space-around; padding: 20rpx 0; background: #f9fafb; border-radius: 16rpx; }
.macro-item { text-align: center; }
.macro-value { font-size: 28rpx; font-weight: 700; color: #10b981; display: block; }
.macro-label { font-size: 20rpx; color: #999; margin-top: 4rpx; display: block; }
</style>
