<template>





  <view class="home-container">





    <view class="home-header">





      <view class="bg-grad"></view>





      <view class="header-content">





        <text class="app-name">我的工具箱</text>





        <text class="app-desc">高效工作 · 轻松生活</text>





      </view>





    </view>











    <view class="tools-grid">





      <view class="tool-card" @click="goTravel">





        <view class="tool-icon" style="background: linear-gradient(135deg, #4a6cf7, #7c3aed);">





          <text>🗺️</text>





        </view>





        <text class="tool-name">旅游计划</text>





      </view>











      <view class="tool-card" @click="goNotes">





        <view class="tool-icon" style="background: linear-gradient(135deg, #f59e0b, #ef4444);">





          <text>📝</text>





        </view>





        <text class="tool-name">笔记</text>





      </view>











      <view class="tool-card" @click="goBMI">





        <view class="tool-icon" style="background: linear-gradient(135deg, #10b981, #34d399);">





          <text>⚖️</text>





        </view>





        <text class="tool-name">BMI计算</text>





      </view>











      <view class="tool-card" @click="goCalorie">





        <view class="tool-icon" style="background: linear-gradient(135deg, #f97316, #fb923c);">





          <text>🔥</text>





        </view>





        <text class="tool-name">热量计算</text>





      </view>











      <view class="tool-card" @click="goPomodoro">





        <view class="tool-icon" style="background: linear-gradient(135deg, #ef4444, #dc2626);">





          <text>🍅</text>





        </view>





        <text class="tool-name">番茄钟</text>





      </view>











      <view class="tool-card" @click="goAltitude">





        <view class="tool-icon" style="background: linear-gradient(135deg, #06b6d4, #0ea5e9);">





          <text>⛰️</text>





        </view>





        <text class="tool-name">海拔高度</text>





      </view>











      <view class="tool-card" @click="goCurrency">





        <view class="tool-icon" style="background: linear-gradient(135deg, #8b5cf6, #a855f7);">





          <text>💱</text>





        </view>





        <text class="tool-name">汇率查询</text>





      </view>











      <view class="tool-card" @click="goWeather">





        <view class="tool-icon" style="background: linear-gradient(135deg, #f59e0b, #f97316);">





          <text>🌤️</text>





        </view>





        <text class="tool-name">实时天气</text>





      </view>











      <view class="tool-card" @click="goUnitConverter">





        <view class="tool-icon" style="background: linear-gradient(135deg, #6366f1, #8b5cf6);">





          <text>📏</text>





        </view>





        <text class="tool-name">单位转换</text>





      </view>











      <view class="tool-card" @click="goPassword">





        <view class="tool-icon" style="background: linear-gradient(135deg, #14b8a6, #06b6d4);">





          <text>🔐</text>





        </view>





        <text class="tool-name">密码生成</text>





      </view>











      <view class="tool-card" @click="goCountdown">





        <view class="tool-icon" style="background: linear-gradient(135deg, #f43f5e, #e11d48);">





          <text>⏱️</text>





        </view>





        <text class="tool-name">倒计时</text>





      </view>











      <view class="tool-card" @click="goLottery">





        <view class="tool-icon" style="background: linear-gradient(135deg, #a855f7, #7c3aed);">





          <text>🎲</text>





        </view>





        <text class="tool-name">随机决策</text>





      </view>











      <view class="tool-card" @click="goTodo">





        <view class="tool-icon" style="background: linear-gradient(135deg, #84cc16, #22c55e);">





          <text>📋</text>





        </view>





        <text class="tool-name">待办清单</text>





      </view>











      <view class="tool-card" @click="goHabit">





        <view class="tool-icon" style="background: linear-gradient(135deg, #8b5cf6, #7c3aed);">





          <text>🎯</text>





        </view>





        <text class="tool-name">习惯打卡</text>





      </view>











      <view class="tool-card" @click="goPacking">





        <view class="tool-icon" style="background: linear-gradient(135deg, #f59e0b, #d97706);">





          <text>🧳</text>





        </view>





        <text class="tool-name">行李收纳</text>





      </view>











      <view class="tool-card" @click="goWorkout">





        <view class="tool-icon" style="background: linear-gradient(135deg, #ef4444, #dc2626);">





          <text>💪</text>





        </view>





        <text class="tool-name">训练计划</text>





      </view>











      <view class="tool-card" @click="goFatLoss">





        <view class="tool-icon" style="background: linear-gradient(135deg, #10b981, #059669);">





          <text>🏃</text>





        </view>





        <text class="tool-name">减脂计划</text>





      </view>











      <view class="tool-card" @click="goWater">





        <view class="tool-icon" style="background: linear-gradient(135deg, #06b6d4, #0284c7);">





          <text>💧</text>





        </view>





        <text class="tool-name">饮水记录</text>





      </view>











      <view class="tool-card" @click="goSleep">





        <view class="tool-icon" style="background: linear-gradient(135deg, #6366f1, #4f46e5);">





          <text>😴</text>





        </view>





        <text class="tool-name">睡眠记录</text>





      </view>











      <view class="tool-card" @click="goFood">





        <view class="tool-icon" style="background: linear-gradient(135deg, #f97316, #ea580c);">





          <text>🍱</text>





        </view>





        <text class="tool-name">美食记录</text>





      </view>











      <view class="tool-card" @click="goStudy">





        <view class="tool-icon" style="background: linear-gradient(135deg, #14b8a6, #0d9488);">





          <text>📚</text>





        </view>





        <text class="tool-name">学习打卡</text>





      </view>











      <view class="tool-card" @click="goDiary">





        <view class="tool-icon" style="background: linear-gradient(135deg, #a855f7, #9333ea);">





          <text>📖</text>





        </view>





        <text class="tool-name">日记</text>





      </view>











      <view class="tool-card" @click="goShopping">





        <view class="tool-icon" style="background: linear-gradient(135deg, #ec4899, #db2777);">





          <text>🛒</text>





        </view>





        <text class="tool-name">购物清单</text>





      </view>











      <view class="tool-card" @click="goMovie">





        <view class="tool-icon" style="background: linear-gradient(135deg, #f59e0b, #b45309);">





          <text>🎬</text>





        </view>





        <text class="tool-name">电影清单</text>





      </view>











      <view class="tool-card" @click="goRunning">





        <view class="tool-icon" style="background: linear-gradient(135deg, #84cc16, #65a30d);">





          <text>🏃‍♂️</text>





        </view>





        <text class="tool-name">跑步记录</text>





      </view>











      <view class="tool-card" @click="goContact">





        <view class="tool-icon" style="background: linear-gradient(135deg, #0ea5e9, #0284c7);">





          <text>📇</text>





        </view>





        <text class="tool-name">名片夹</text>





      </view>











      <view class="tool-card" @click="goPeriod">





        <view class="tool-icon" style="background: linear-gradient(135deg, #f472b6, #ec4899);">





          <text>🌸</text>





        </view>





        <text class="tool-name">经期追踪</text>





      </view>











      <view class="tool-card" @click="goExpense">





        <view class="tool-icon" style="background: linear-gradient(135deg, #f59e0b, #d97706);">





          <text>💰</text>





        </view>





        <text class="tool-name">记账本</text>





      </view>











      <view class="tool-card" @click="goImgFilter">





        <view class="tool-icon" style="background: linear-gradient(135deg, #667eea, #764ba2);">





          <text>🎨</text>





        </view>





        <text class="tool-name">图片滤镜</text>





      </view>











            <view class="tool-card" @click="goQRCode">




        <view class="tool-icon" style="background: linear-gradient(135deg, #10b981, #059669);">




          <text>🗳</text>




        </view>




        <text class="tool-name">二维码</text>




      </view>









<view class="tool-card" @click="goCalculator">



        <view class="tool-icon" style="background: linear-gradient(135deg, #16213e, #0f3460);">



          <text>🧮</text>



        </view>



        <text class="tool-name">计算器</text>



      </view>



      <view class="tool-card" @click="goPicker">



        <view class="tool-icon" style="background: linear-gradient(135deg, #f093fb, #f5576c);">



          <text>🎰</text>



        </view>



        <text class="tool-name">随机抽签</text>



      </view>



      <view class="tool-card" @click="goLoan">



        <view class="tool-icon" style="background: linear-gradient(135deg, #4facfe, #00f2fe);">



          <text>🏠</text>



        </view>



        <text class="tool-name">房贷计算</text>



      </view>



      <view class="tool-card" @click="goDatecalc">



        <view class="tool-icon" style="background: linear-gradient(135deg, #43e97b, #38f9d7);">



          <text>📅</text>



        </view>



        <text class="tool-name">日期计算</text>



      </view>



      <view class="tool-card" @click="goTextcount">



        <view class="tool-icon" style="background: linear-gradient(135deg, #f6d365, #fda085);">



          <text>📝</text>



        </view>



        <text class="tool-name">文字统计</text>



      </view>



<view class="tool-card" @click="goPriceCompare">


        <view class="tool-icon" style="background: linear-gradient(135deg, #ff9a9e, #fad0c4);">


          <text>🛷</text>


        </view>


        <text class="tool-name">比价计算</text>


      </view>


      <view class="tool-card" @click="goSplitBill">


        <view class="tool-icon" style="background: linear-gradient(135deg, #a18cd1, #fbc2eb);">


          <text>💰</text>


        </view>


        <text class="tool-name">分账计算</text>


      </view>


      <view class="tool-card" @click="goBase64">


        <view class="tool-icon" style="background: linear-gradient(135deg, #667eea, #764ba2);">


          <text>🔤</text>


        </view>


        <text class="tool-name">Base64</text>


      </view>


      <view class="tool-card" @click="goJsonFmt">


        <view class="tool-icon" style="background: linear-gradient(135deg, #2d3436, #636e72);">


          <text>📋</text>


        </view>


        <text class="tool-name">JSON</text>


      </view>


      <view class="tool-card" @click="goUrlEncode">


        <view class="tool-icon" style="background: linear-gradient(135deg, #00b894, #00cec9);">


          <text>🔗</text>


        </view>


        <text class="tool-name">URL编码</text>


      </view>


      <view class="tool-card" @click="goLuckyWheel">


        <view class="tool-icon" style="background: linear-gradient(135deg, #f5576c, #ff6b6b);">


          <text>🎡</text>


        </view>


        <text class="tool-name">幸运转盘</text>


      </view>


      <view class="tool-card" @click="goDice">


        <view class="tool-icon" style="background: linear-gradient(135deg, #e17055, #d63031);">


          <text>🎲</text>


        </view>


        <text class="tool-name">骰子</text>


      </view>


      <view class="tool-card" @click="goCompass">


        <view class="tool-icon" style="background: linear-gradient(135deg, #0984e3, #74b9ff);">


          <text>🧭</text>


        </view>


        <text class="tool-name">指南针</text>


      </view>


      <view class="tool-card" @click="goBaseConvert">


        <view class="tool-icon" style="background: linear-gradient(135deg, #6c5ce7, #a29bfe);">


          <text>🔢</text>


        </view>


        <text class="tool-name">进制转换</text>


      </view>


      <view class="tool-card" @click="goRegexTest">


        <view class="tool-icon" style="background: linear-gradient(135deg, #fd79a8, #e84393);">


          <text>🔍</text>


        </view>


        <text class="tool-name">正则测试</text>


      </view>


      <view class="tool-card" @click="goColorPicker">


        <view class="tool-icon" style="background: linear-gradient(135deg, #667eea, #764ba2);">


          <text>🎨</text>


        </view>


        <text class="tool-name">颜色拾取</text>


      </view>


<view class="tool-card" @click="goQrScan">

        <view class="tool-icon" style="background: linear-gradient(135deg, #0984e3, #74b9ff);">

          <text>📷</text>

        </view>

        <text class="tool-name">二维码扫描</text>

      </view>

      <view class="tool-card" @click="goWorldClock">

        <view class="tool-icon" style="background: linear-gradient(135deg, #6c5ce7, #a29bfe);">

          <text>🌐</text>

        </view>

        <text class="tool-name">世界时钟</text>

      </view>

      <view class="tool-card" @click="goTimestamp">

        <view class="tool-icon" style="background: linear-gradient(135deg, #00b894, #55efc4);">

          <text>⏱️</text>

        </view>

        <text class="tool-name">时间戳</text>

      </view>

      <view class="tool-card" @click="goCalendar">

        <view class="tool-icon" style="background: linear-gradient(135deg, #e17055, #fab1a0);">

          <text>📅</text>

        </view>

        <text class="tool-name">万年历</text>

      </view>

      <view class="tool-card" @click="goZhConvert">

        <view class="tool-icon" style="background: linear-gradient(135deg, #fdcb6e, #e17055);">

          <text>🇹🇲</text>

        </view>

        <text class="tool-name">简繁转换</text>

      </view>

      <view class="tool-card" @click="goCaseConvert">

        <view class="tool-icon" style="background: linear-gradient(135deg, #a29bfe, #6c5ce7);">

          <text>🔤</text>

        </view>

        <text class="tool-name">大小写</text>

      </view>

      <view class="tool-card" @click="goMdPreview">

        <view class="tool-icon" style="background: linear-gradient(135deg, #636e72, #2d3436);">

          <text>✍️</text>

        </view>

        <text class="tool-name">Markdown</text>

      </view>

      <view class="tool-card" @click="goCoinFlip">

        <view class="tool-icon" style="background: linear-gradient(135deg, #f9ca24, #f0932b);">

          <text>🪙</text>

        </view>

        <text class="tool-name">抛硬币</text>

      </view>

      <view class="tool-card" @click="goTarot">

        <view class="tool-icon" style="background: linear-gradient(135deg, #5f27cd, #a29bfe);">

          <text>🃏</text>

        </view>

        <text class="tool-name">塔罗牌</text>

      </view>

      <view class="tool-card" @click="goMetronome">

        <view class="tool-icon" style="background: linear-gradient(135deg, #00cec9, #81ecec);">

          <text>🎵</text>

        </view>

        <text class="tool-name">节拍器</text>

      </view>

      <view class="tool-card" @click="goSciCalc">

        <view class="tool-icon" style="background: linear-gradient(135deg, #2d3436, #00b894);">

          <text>🧬</text>

        </view>

        <text class="tool-name">科学计算</text>

      </view>

<view class="tool-card" @click="goShakeCounter">
        <view class="tool-icon" style="background: linear-gradient(135deg, #636e72, #2d3436);">
          <text>\U0001f4f1</text>
        </view>
        <text class="tool-name">\u6447\u4e00\u6447</text>
      </view>
<view class="tool-card" @click="goSpiritLevel">
        <view class="tool-icon" style="background: linear-gradient(135deg, #00b894, #00cec9);">
          <text>\U0001f4d0</text>
        </view>
        <text class="tool-name">\u6c34\u5e73\u4eea</text>
      </view>
<view class="tool-card" @click="goDecibel">
        <view class="tool-icon" style="background: linear-gradient(135deg, #6c5ce7, #a29bfe);">
          <text>\U0001f4e1</text>
        </view>
        <text class="tool-name">\u5206\u8d1d\u8ba1</text>
      </view>
<view class="tool-card" @click="goHeartRate">
        <view class="tool-icon" style="background: linear-gradient(135deg, #e84393, #fd79a8);">
          <text>\u2764\ufe0f</text>
        </view>
        <text class="tool-name">\u5fc3\u7387\u4f30\u7b97</text>
      </view>
<view class="tool-card" @click="goPedometer">
        <view class="tool-icon" style="background: linear-gradient(135deg, #00b894, #55efc4);">
          <text>\U0001f463</text>
        </view>
        <text class="tool-name">\u8ba1\u6b65\u5668</text>
      </view>
<view class="tool-card" @click="goUuidGen">
        <view class="tool-icon" style="background: linear-gradient(135deg, #636e72, #b2bec3);">
          <text>\U0001f511</text>
        </view>
        <text class="tool-name">UUID\u751f\u6210</text>
      </view>
<view class="tool-card" @click="goCronParser">
        <view class="tool-icon" style="background: linear-gradient(135deg, #0984e3, #74b9ff);">
          <text>\u23f0</text>
        </view>
        <text class="tool-name">\u89e3\u6790Cron</text>
      </view>
<view class="tool-card" @click="goHashCalc">
        <view class="tool-icon" style="background: linear-gradient(135deg, #2d3436, #636e72);">
          <text>\U0001f512</text>
        </view>
        <text class="tool-name">\u54c8\u5e0c\u8ba1\u7b97</text>
      </view>
<view class="tool-card" @click="goMorseCode">
        <view class="tool-icon" style="background: linear-gradient(135deg, #e17055, #d63031);">
          <text>\u23f3</text>
        </view>
        <text class="tool-name">\u6469\u65af\u7535\u7801</text>
      </view>
<view class="tool-card" @click="goPinyin">
        <view class="tool-icon" style="background: linear-gradient(135deg, #fd79a8, #e84393);">
          <text>\U0001f524</text>
        </view>
        <text class="tool-name">\u62fc\u97f3\u8f6c\u6362</text>
      </view>
<view class="tool-card" @click="goTypingSpeed">
        <view class="tool-icon" style="background: linear-gradient(135deg, #6c5ce7, #a29bfe);">
          <text>\u2328\ufe0f</text>
        </view>
        <text class="tool-name">\u6253\u5b57\u6d4b\u901f</text>
      </view>
<view class="tool-card" @click="goReadingSpeed">
        <view class="tool-icon" style="background: linear-gradient(135deg, #00b894, #55efc4);">
          <text>\U0001f4d6</text>
        </view>
        <text class="tool-name">\u9605\u8bfb\u6d4b\u901f</text>
      </view>
<view class="tool-card" @click="goDrawingBoard">
        <view class="tool-icon" style="background: linear-gradient(135deg, #e84393, #fd79a8);">
          <text>\u270f\ufe0f</text>
        </view>
        <text class="tool-name">\u7b80\u7b14\u753b</text>
      </view>
<view class="tool-card" @click="goMirror">
        <view class="tool-icon" style="background: linear-gradient(135deg, #636e72, #b2bec3);">
          <text>\U0001f503</text>
        </view>
        <text class="tool-name">\u955c\u5b50</text>
      </view>
<view class="tool-card" @click="goFlashlight">
        <view class="tool-icon" style="background: linear-gradient(135deg, #f9ca24, #f0932b);">
          <text>\U0001f4a1</text>
        </view>
        <text class="tool-name">\u624b\u7535\u7b52</text>
      </view>
<view class="tool-card" @click="goIpQuery">
        <view class="tool-icon" style="background: linear-gradient(135deg, #0984e3, #74b9ff);">
          <text>\U0001f5a5\ufe0f</text>
        </view>
        <text class="tool-name">IP\u67e5\u8be2</text>
      </view>
<view class="tool-card" @click="goImgCompress">
        <view class="tool-icon" style="background: linear-gradient(135deg, #636e72, #2d3436);">
          <text>\U000\uddbc\ufe0f</text>
        </view>
        <text class="tool-name">\u56fe\u7247\u538b\u7f29</text>
      </view>
<view class="tool-card" @click="goArMeasure">
        <view class="tool-icon" style="background: linear-gradient(135deg, #00b894, #00cec9);">
          <text>\U0001f4cf</text>
        </view>
        <text class="tool-name">\u6d4b\u8ddd</text>
      </view>
<view class="tool-card" @click="goBloodType">
        <view class="tool-icon" style="background: linear-gradient(135deg, #e84393, #fd79a8);">
          <text>\U0001fa78</text>
        </view>
        <text class="tool-name">\u8840\u578b\u9077\u4f20</text>
      </view>
<view class="tool-card" @click="goDeveloping">





        <view class="tool-icon" style="background: linear-gradient(135deg, #64748b, #475569);">





          <text>🔧</text>





        </view>





        <text class="tool-name">更多工具</text>





      </view>





    </view>











    <view v-if="username" class="user-bar">





      <text class="user-text">当前用户：{{ username }}</text>





      <text class="logout-text" @click="handleLogout">退出</text>





    </view>





  </view>





</template>











<script setup>





import { ref, onMounted } from "vue"











const username = ref("")











const goImgFilter = () => { uni.navigateTo({ url: "/pkgTools/pages/imgfilter/imgfilter" }) }





const goQRCode = () => { uni.navigateTo({ url: "/pkgTools/pages/qrcode/qrcode" }) }




const goCalculator = () => { uni.navigateTo({ url: "/pkgTools/pages/calculator/calculator" }) }



const goPicker = () => { uni.navigateTo({ url: "/pkgTools/pages/picker/picker" }) }



const goLoan = () => { uni.navigateTo({ url: "/pkgTools/pages/loan/loan" }) }



const goDatecalc = () => { uni.navigateTo({ url: "/pkgTools/pages/datecalc/datecalc" }) }



const goTextcount = () => { uni.navigateTo({ url: "/pkgTools/pages/textcount/textcount" }) }



const goPriceCompare = () => { uni.navigateTo({ url: "/pkgTools/pages/pricecompare/pricecompare" }) }


const goSplitBill = () => { uni.navigateTo({ url: "/pkgTools/pages/splitbill/splitbill" }) }


const goBase64 = () => { uni.navigateTo({ url: "/pkgTools/pages/base64/base64" }) }


const goJsonFmt = () => { uni.navigateTo({ url: "/pkgTools/pages/jsonfmt/jsonfmt" }) }


const goUrlEncode = () => { uni.navigateTo({ url: "/pkgTools/pages/urlencode/urlencode" }) }


const goLuckyWheel = () => { uni.navigateTo({ url: "/pkgTools/pages/luckywheel/luckywheel" }) }


const goDice = () => { uni.navigateTo({ url: "/pkgTools/pages/dice/dice" }) }


const goCompass = () => { uni.navigateTo({ url: "/pkgTools/pages/compass/compass" }) }


const goBaseConvert = () => { uni.navigateTo({ url: "/pkgTools/pages/baseconvert/baseconvert" }) }


const goRegexTest = () => { uni.navigateTo({ url: "/pkgTools/pages/regextest/regextest" }) }


const goColorPicker = () => { uni.navigateTo({ url: "/pkgTools/pages/colorpicker/colorpicker" }) }


const goQrScan = () => { uni.navigateTo({ url: "/pkgTools/pages/qrscan/qrscan" }) }

const goWorldClock = () => { uni.navigateTo({ url: "/pkgTools/pages/worldclock/worldclock" }) }

const goTimestamp = () => { uni.navigateTo({ url: "/pkgTools/pages/timestamp/timestamp" }) }

const goCalendar = () => { uni.navigateTo({ url: "/pkgTools/pages/calendar/calendar" }) }

const goZhConvert = () => { uni.navigateTo({ url: "/pkgTools/pages/zhconvert/zhconvert" }) }

const goCaseConvert = () => { uni.navigateTo({ url: "/pkgTools/pages/caseconvert/caseconvert" }) }

const goMdPreview = () => { uni.navigateTo({ url: "/pkgTools/pages/mdpreview/mdpreview" }) }

const goCoinFlip = () => { uni.navigateTo({ url: "/pkgTools/pages/coinflip/coinflip" }) }

const goTarot = () => { uni.navigateTo({ url: "/pkgTools/pages/tarot/tarot" }) }

const goMetronome = () => { uni.navigateTo({ url: "/pkgTools/pages/metronome/metronome" }) }

const goSciCalc = () => { uni.navigateTo({ url: "/pkgTools/pages/scicalc/scicalc" }) }

const goShakeCounter = () => { uni.navigateTo({ url: "/pkgTools/pages/shakecounter/shakecounter" }) }
const goSpiritLevel = () => { uni.navigateTo({ url: "/pkgTools/pages/spiritlevel/spiritlevel" }) }
const goDecibel = () => { uni.navigateTo({ url: "/pkgTools/pages/decibel/decibel" }) }
const goHeartRate = () => { uni.navigateTo({ url: "/pkgTools/pages/heartrate/heartrate" }) }
const goPedometer = () => { uni.navigateTo({ url: "/pkgTools/pages/pedometer/pedometer" }) }
const goUuidGen = () => { uni.navigateTo({ url: "/pkgTools/pages/uuidgen/uuidgen" }) }
const goCronParser = () => { uni.navigateTo({ url: "/pkgTools/pages/cronparser/cronparser" }) }
const goHashCalc = () => { uni.navigateTo({ url: "/pkgTools/pages/hashcalc/hashcalc" }) }
const goMorseCode = () => { uni.navigateTo({ url: "/pkgTools/pages/morsecode/morsecode" }) }
const goPinyin = () => { uni.navigateTo({ url: "/pkgTools/pages/pinyin/pinyin" }) }
const goTypingSpeed = () => { uni.navigateTo({ url: "/pkgTools/pages/typingspeed/typingspeed" }) }
const goReadingSpeed = () => { uni.navigateTo({ url: "/pkgTools/pages/readingspeed/readingspeed" }) }
const goDrawingBoard = () => { uni.navigateTo({ url: "/pkgTools/pages/drawingboard/drawingboard" }) }
const goMirror = () => { uni.navigateTo({ url: "/pkgTools/pages/mirror/mirror" }) }
const goFlashlight = () => { uni.navigateTo({ url: "/pkgTools/pages/flashlight/flashlight" }) }
const goIpQuery = () => { uni.navigateTo({ url: "/pkgTools/pages/ipquery/ipquery" }) }
const goImgCompress = () => { uni.navigateTo({ url: "/pkgTools/pages/imgcompress/imgcompress" }) }
const goArMeasure = () => { uni.navigateTo({ url: "/pkgTools/pages/armeasure/armeasure" }) }
const goBloodType = () => { uni.navigateTo({ url: "/pkgTools/pages/bloodtype/bloodtype" }) }
const goTravel = () => {





  uni.navigateTo({ url: "/pkgTools/pages/travel/travel" })





}











const goDeveloping = () => {





  uni.showToast({ title: '功能开发中...', icon: 'none' })





}











const goAltitude = () => { uni.navigateTo({ url: "/pkgTools/pages/altitude/altitude" }) }





const goCurrency = () => { uni.navigateTo({ url: "/pkgTools/pages/currency/currency" }) }





const goBMI = () => { uni.navigateTo({ url: "/pkgTools/pages/bmi/bmi" }) }





const goCalorie = () => { uni.navigateTo({ url: "/pkgTools/pages/calorie/calorie" }) }





const goWeather = () => { uni.navigateTo({ url: "/pkgTools/pages/weather/weather" }) }





const goUnitConverter = () => { uni.navigateTo({ url: "/pkgTools/pages/unit/unit" }) }





const goPassword = () => { uni.navigateTo({ url: "/pkgTools/pages/password/password" }) }





const goCountdown = () => { uni.navigateTo({ url: "/pkgTools/pages/countdown/countdown" }) }





const goLottery = () => { uni.navigateTo({ url: "/pkgTools/pages/lottery/lottery" }) }





const goTodo = () => { uni.navigateTo({ url: "/pkgTools/pages/todo/todo" }) }





const goNotes = () => { uni.navigateTo({ url: "/pkgTools/pages/notes/home" }) }





const goPacking = () => { uni.navigateTo({ url: "/pkgTools/pages/packing/packing" }) }





const goWorkout = () => { uni.navigateTo({ url: "/pkgTools/pages/workout/workout" }) }





const goFatLoss = () => { uni.navigateTo({ url: "/pkgTools/pages/fatloss/fatloss" }) }





const goPomodoro = () => { uni.navigateTo({ url: "/pkgTools/pages/pomodoro/pomodoro" }) }





const goHabit = () => { uni.navigateTo({ url: "/pkgTools/pages/habit/habit" }) }





const goSleep = () => { uni.navigateTo({ url: "/pkgTools/pages/sleep/sleep" }) }





const goWater = () => { uni.navigateTo({ url: "/pkgTools/pages/water/water" }) }





const goFood = () => { uni.navigateTo({ url: "/pkgTools/pages/food/food" }) }





const goStudy = () => { uni.navigateTo({ url: "/pkgTools/pages/study/study" }) }





const goDiary = () => { uni.navigateTo({ url: "/pkgTools/pages/diary/diary" }) }





const goShopping = () => { uni.navigateTo({ url: "/pkgTools/pages/shopping/shopping" }) }





const goContact = () => { uni.navigateTo({ url: "/pkgTools/pages/contact/contact" }) }





const goMovie = () => { uni.navigateTo({ url: "/pkgTools/pages/movie/movie" }) }





const goRunning = () => { uni.navigateTo({ url: "/pkgTools/pages/running/running" }) }





const goPeriod = () => { uni.navigateTo({ url: "/pkgTools/pages/period/period" }) }





const goExpense = () => { uni.navigateTo({ url: "/pkgTools/pages/expense/expense" }) }











const handleLogout = () => {





  uni.showModal({





    title: "退出登录",





    content: "确定退出？",





    success: (res) => {





      if (res.confirm) {





        uni.removeStorageSync("isLoggedIn")





        uni.reLaunch({ url: "/pages/login/login" })





      }





    },





  })





}












const go2048 = () => { uni.navigateTo({ url: "/pkgTools/pages/2048/2048" }) }
const goTicTacToe = () => { uni.navigateTo({ url: "/pkgTools/pages/tictactoe/tictactoe" }) }
const goGuessNum = () => { uni.navigateTo({ url: "/pkgTools/pages/guessnum/guessnum" }) }
const goBlackjack = () => { uni.navigateTo({ url: "/pkgTools/pages/blackjack/blackjack" }) }
const goImgFormat = () => { uni.navigateTo({ url: "/pkgTools/pages/imgformat/imgformat" }) }
const goImgCrop = () => { uni.navigateTo({ url: "/pkgTools/pages/imgcrop/imgcrop" }) }
const goWatermark = () => { uni.navigateTo({ url: "/pkgTools/pages/watermark/watermark" }) }
const goImgStyle = () => { uni.navigateTo({ url: "/pkgTools/pages/imgstyle/imgstyle" }) }
const goImgMerge = () => { uni.navigateTo({ url: "/pkgTools/pages/imgmerge/imgmerge" }) }
const goColorPalette = () => { uni.navigateTo({ url: "/pkgTools/pages/colorpalette/colorpalette" }) }
const goTempConvert = () => { uni.navigateTo({ url: "/pkgTools/pages/tempconvert/tempconvert" }) }
const goSlopeCalc = () => { uni.navigateTo({ url: "/pkgTools/pages/slopecalc/slopecalc" }) }
const goAngleCalc = () => { uni.navigateTo({ url: "/pkgTools/pages/anglecalc/anglecalc" }) }


const goPdfMerge = () => { uni.navigateTo({ url: "/pkgTools/pages/pdfmerge/pdfmerge" }) }
const goOCR = () => { uni.navigateTo({ url: "/pkgTools/pages/ocr/ocr" }) }
const goFileEncrypt = () => { uni.navigateTo({ url: "/pkgTools/pages/fileencrypt/fileencrypt" }) }
const goTextEncrypt = () => { uni.navigateTo({ url: "/pkgTools/pages/textencrypt/textencrypt" }) }
const goPasswordManager = () => { uni.navigateTo({ url: "/pkgTools/pages/passwordmanager/passwordmanager" }) }
const goSpeedTest = () => { uni.navigateTo({ url: "/pkgTools/pages/speedtest/speedtest" }) }
const goDnsLookup = () => { uni.navigateTo({ url: "/pkgTools/pages/dnslookup/dnslookup" }) }
const goUrlShortener = () => { uni.navigateTo({ url: "/pkgTools/pages/urlshortener/urlshortener" }) }
const goTaxCalc = () => { uni.navigateTo({ url: "/pkgTools/pages/taxcalc/taxcalc" }) }
const goCompoundInterest = () => { uni.navigateTo({ url: "/pkgTools/pages/compoundinterest/compoundinterest" }) }
const goMortgageCalc = () => { uni.navigateTo({ url: "/pkgTools/pages/mortgagecalc/mortgagecalc" }) }
const goMatrixCalc = () => { uni.navigateTo({ url: "/pkgTools/pages/matrixcalc/matrixcalc" }) }
const goEquationSolver = () => { uni.navigateTo({ url: "/pkgTools/pages/equationsolver/equationsolver" }) }
const goStatistics = () => { uni.navigateTo({ url: "/pkgTools/pages/statistics/statistics" }) }
const goAudioConvert = () => { uni.navigateTo({ url: "/pkgTools/pages/audioconvert/audioconvert" }) }
const goRecorder = () => { uni.navigateTo({ url: "/pkgTools/pages/recorder/recorder" }) }
const goSnake = () => { uni.navigateTo({ url: "/pkgTools/pages/snake/snake" }) }
const goTetris = () => { uni.navigateTo({ url: "/pkgTools/pages/tetris/tetris" }) }
const goSudoku = () => { uni.navigateTo({ url: "/pkgTools/pages/sudoku/sudoku" }) }
const goMemory = () => { uni.navigateTo({ url: "/pkgTools/pages/memory/memory" }) }
const goJsonDiff = () => { uni.navigateTo({ url: "/pkgTools/pages/jsondiff/jsondiff" }) }
const goColorConvert = () => { uni.navigateTo({ url: "/pkgTools/pages/colorconvert/colorconvert" }) }
const goQRStyle = () => { uni.navigateTo({ url: "/pkgTools/pages/qrstyle/qrstyle" }) }
const goVideoToGif = () => { uni.navigateTo({ url: "/pkgTools/pages/videotogif/videotogif" }) }
const goNameGenerator = () => { uni.navigateTo({ url: "/pkgTools/pages/namegenerator/namegenerator" }) }
const goBarcode = () => { uni.navigateTo({ url: "/pkgTools/pages/barcode/barcode" }) }

onMounted(() => {





  username.value = uni.getStorageSync("username") || ""





})





</script>











<style lang="scss" scoped>





.home-container {





  min-height: 100vh;





  background: #f5f7fb;





  padding-bottom: 40rpx;





}











.home-header {





  position: relative;





  padding: 100rpx 40rpx 60rpx;





  overflow: hidden;





}











.bg-grad {





  position: absolute;





  inset: 0;





  background: linear-gradient(135deg, #4a6cf7 0%, #7c3aed 100%);





  z-index: 0;





}











.header-content {





  position: relative;





  z-index: 1;





}











.app-name {





  font-size: 40rpx;





  color: #fff;





  font-weight: 700;





  display: block;





}











.app-desc {





  font-size: 26rpx;





  color: rgba(255, 255, 255, 0.75);





  margin-top: 12rpx;





  display: block;





}











.tools-grid {





  display: grid;





  grid-template-columns: 1fr 1fr 1fr;





  gap: 16rpx;





  padding: 24rpx 20rpx;





}











.tool-card {





  background: #fff;





  border-radius: 16rpx;





  padding: 24rpx 12rpx;





  display: flex;





  flex-direction: column;





  align-items: center;





  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.04);





  transition: transform 0.15s;





}











.tool-card:active {





  transform: scale(0.95);





}











.tool-icon {





  width: 64rpx;





  height: 64rpx;





  border-radius: 16rpx;





  display: flex;





  align-items: center;





  justify-content: center;





  margin-bottom: 16rpx;





}











.tool-icon text {





  font-size: 32rpx;





}











.tool-name {





  font-size: 24rpx;





  font-weight: 600;





  color: #333;





  margin-bottom: 8rpx;





}











.tool-desc {





  font-size: 20rpx;





  color: #999;





}











.user-bar {





  margin-top: 40rpx;





  padding: 0 32rpx;





  display: flex;





  justify-content: space-between;





  align-items: center;





}











.user-text {





  font-size: 24rpx;





  color: #999;





}











.logout-text {





  font-size: 24rpx;





  color: #ef4444;





  padding: 4rpx 16rpx;





}





</style
      <view class="tool-card" @click="go2048">
        <view class="tool-icon" style="background: linear-gradient(135deg, #f59e0b, #f97316);">
          <text>&#x1F3AE;</text>
        
      <view class="tool-card" @click="goPdfMerge">
        <view class="tool-icon" style="background: linear-gradient(135deg, #ef4444, #dc2626);">
          <text>&#x1F4C4;</text>
        </view>
        <text class="tool-name">PDF&#x5408;&#x5E76;</text>
      </view>

      <view class="tool-card" @click="goOCR">
        <view class="tool-icon" style="background: linear-gradient(135deg, #8b5cf6, #7c3aed);">
          <text>&#x1F4F7;</text>
        </view>
        <text class="tool-name">&#x6587;&#x5B57;&#x8BC6;&#x522B;</text>
      </view>

      <view class="tool-card" @click="goFileEncrypt">
        <view class="tool-icon" style="background: linear-gradient(135deg, #10b981, #059669);">
          <text>&#x1F512;</text>
        </view>
        <text class="tool-name">&#x6587;&#x4EF6;&#x52A0;&#x5BC6;</text>
      </view>

      <view class="tool-card" @click="goTextEncrypt">
        <view class="tool-icon" style="background: linear-gradient(135deg, #f59e0b, #d97706);">
          <text>&#x1F510;</text>
        </view>
        <text class="tool-name">&#x6587;&#x672C;&#x52A0;&#x5BC6;</text>
      </view>

      <view class="tool-card" @click="goPasswordManager">
        <view class="tool-icon" style="background: linear-gradient(135deg, #06b6d4, #0891b2);">
          <text>&#x1F511;</text>
        </view>
        <text class="tool-name">&#x5BC6;&#x7801;&#x7BA1;&#x7406;</text>
      </view>

      <view class="tool-card" @click="goSpeedTest">
        <view class="tool-icon" style="background: linear-gradient(135deg, #3b82f6, #2563eb);">
          <text>&#x26A1;</text>
        </view>
        <text class="tool-name">&#x7F51;&#x901F;&#x6D4B;&#x8BD5;</text>
      </view>

      <view class="tool-card" @click="goDnsLookup">
        <view class="tool-icon" style="background: linear-gradient(135deg, #14b8a6, #0d9488);">
          <text>&#x1F310;</text>
        </view>
        <text class="tool-name">DNS&#x67E5;&#x8BE2;</text>
      </view>

      <view class="tool-card" @click="goUrlShortener">
        <view class="tool-icon" style="background: linear-gradient(135deg, #a855f7, #9333ea);">
          <text>&#x1F517;</text>
        </view>
        <text class="tool-name">URL&#x7FED;&#x77ED;</text>
      </view>

      <view class="tool-card" @click="goTaxCalc">
        <view class="tool-icon" style="background: linear-gradient(135deg, #f43f5e, #e11d48);">
          <text>&#x1F4B0;</text>
        </view>
        <text class="tool-name">&#x7A0E;&#x8D39;&#x8BA1;&#x7B97;</text>
      </view>

      <view class="tool-card" @click="goCompoundInterest">
        <view class="tool-icon" style="background: linear-gradient(135deg, #10b981, #059669);">
          <text>&#x1F4C8;</text>
        </view>
        <text class="tool-name">&#x590D;&#x5229;&#x8BA1;&#x7B97;</text>
      </view>

      <view class="tool-card" @click="goMortgageCalc">
        <view class="tool-icon" style="background: linear-gradient(135deg, #f59e0b, #d97706);">
          <text>&#x1F3E0;</text>
        </view>
        <text class="tool-name">&#u623F\u8D37\u8BA1\u7B97;</text>
      </view>

      <view class="tool-card" @click="goMatrixCalc">
        <view class="tool-icon" style="background: linear-gradient(135deg, #6366f1, #4f46e5);">
          <text>&#x1F9EE;</text>
        </view>
        <text class="tool-name">&#u77E9\u9635\u8BA1\u7B97;</text>
      </view>

      <view class="tool-card" @click="goEquationSolver">
        <view class="tool-icon" style="background: linear-gradient(135deg, #0891b2, #0e7490);">
          <text>&#u221B;</text>
        </view>
        <text class="tool-name">\u65B9\u7A0B\u6C42\u89E3;</text>
      </view>

      <view class="tool-card" @click="goStatistics">
        <view class="tool-icon" style="background: linear-gradient(135deg, #7c3aed, #6d28d9);">
          <text>\u{1F4CA};</text>
        </view>
        <text class="tool-name">\u7EDF\u8BA1\u5206\u6790;</text>
      </view>

      <view class="tool-card" @click="goAudioConvert">
        <view class="tool-icon" style="background: linear-gradient(135deg, #059669, #047857);">
          <text>\u{1F3B5};</text>
        </view>
        <text class="tool-name">\u97F3\u9891\u8F6C\u6362;</text>
      </view>

      <view class="tool-card" @click="goRecorder">
        <view class="tool-icon" style="background: linear-gradient(135deg, #e11d48, #be123c);">
          <text>\u{1F3A4};</text>
        </view>
        <text class="tool-name">\u5F55\u97F3\u673A;</text>
      </view>

      <view class="tool-card" @click="goSnake">
        <view class="tool-icon" style="background: linear-gradient(135deg, #22c55e, #16a34a);">
          <text>\u{1F40D};</text>
        </view>
        <text class="tool-name">\u8D2A\u5403\u86C7;</text>
      </view>

      <view class="tool-card" @click="goTetris">
        <view class="tool-icon" style="background: linear-gradient(135deg, #3b82f6, #2563eb);">
          <text>\u{1F3AE};</text>
        </view>
        <text class="tool-name">\u4FC4\u7F57\u65AF\u65B9\u5757;</text>
      </view>

      <view class="tool-card" @click="goSudoku">
        <view class="tool-icon" style="background: linear-gradient(135deg, #8b5cf6, #7c3aed);">
          <text>\u{1F9E9};</text>
        </view>
        <text class="tool-name">\u6570\u72EC;</text>
      </view>

      <view class="tool-card" @click="goMemory">
        <view class="tool-icon" style="background: linear-gradient(135deg, #f43f5e, #e11d48);">
          <text>\u{1F0CF};</text>
        </view>
        <text class="tool-name">\u8BB0\u5FC6\u7FFB\u724C;</text>
      </view>

      <view class="tool-card" @click="goJsonDiff">
        <view class="tool-icon" style="background: linear-gradient(135deg, #0891b2, #0e7490);">
          <text>\u{1F4D1};</text>
        </view>
        <text class="tool-name">JSON\u5BF9\u6BD4;</text>
      </view>

      <view class="tool-card" @click="goColorConvert">
        <view class="tool-icon" style="background: linear-gradient(135deg, #ec4899, #db2777);">
          <text>\u{1F308};</text>
        </view>
        <text class="tool-name">\u989C\u8272\u8F6C\u6362;</text>
      </view>

      <view class="tool-card" @click="goQRStyle">
        <view class="tool-icon" style="background: linear-gradient(135deg, #10b981, #059669);">
          <text>\u{25A3};</text>
        </view>
        <text class="tool-name">\u4E8C\u7EF4\u7801\u7F8E\u5316;</text>
      </view>

      <view class="tool-card" @click="goVideoToGif">
        <view class="tool-icon" style="background: linear-gradient(135deg, #f59e0b, #d97706);">
          <text>\u{1F3AC};</text>
        </view>
        <text class="tool-name">\u89C6\u9891\u8F6CGIF;</text>
      </view>

      <view class="tool-card" @click="goNameGenerator">
        <view class="tool-icon" style="background: linear-gradient(135deg, #6366f1, #4f46e5);">
          <text>\u{1F464};</text>
        </view>
        <text class="tool-name">\u968F\u673A\u59D3\u540D;</text>
      </view>

      <view class="tool-card" @click="goBarcode">
        <view class="tool-icon" style="background: linear-gradient(135deg, #1e293b, #334155);">
          <text>\u{1F4DB};</text>
        </view>
        <text class="tool-name">\u6761\u5F62\u7801;</text>
      </view>

    </view>
        <text class="tool-name">2048</text>
      </view>

      <view class="tool-card" @click="goTicTacToe">
        <view class="tool-icon" style="background: linear-gradient(135deg, #4a6cf7, #7c3aed);">
          <text>&#x274C;</text>
        </view>
        <text class="tool-name">&#x4E95;&#x5B57;&#x68CB;</text>
      </view>

      <view class="tool-card" @click="goGuessNum">
        <view class="tool-icon" style="background: linear-gradient(135deg, #10b981, #34d399);">
          <text>&#x1F522;</text>
        </view>
        <text class="tool-name">&#x731C;&#x6570;&#x5B57;</text>
      </view>

      <view class="tool-card" @click="goBlackjack">
        <view class="tool-icon" style="background: linear-gradient(135deg, #ef4444, #dc2626);">
          <text>&#x1F0CF;</text>
        </view>
        <text class="tool-name">21&#x70B9;</text>
      </view>

      <view class="tool-card" @click="goImgFormat">
        <view class="tool-icon" style="background: linear-gradient(135deg, #06b6d4, #0ea5e9);">
          <text>&#x1F5BC;&#xFE0F;</text>
        </view>
        <text class="tool-name">&#x56FE;&#x7247;&#x683C;&#x5F0F;</text>
      </view>

      <view class="tool-card" @click="goImgCrop">
        <view class="tool-icon" style="background: linear-gradient(135deg, #8b5cf6, #a855f7);">
          <text>&#x2702;&#xFE0F;</text>
        </view>
        <text class="tool-name">&#x56FE;&#x7247;&#x88C1;&#x526A;</text>
      </view>

      <view class="tool-card" @click="goWatermark">
        <view class="tool-icon" style="background: linear-gradient(135deg, #f59e0b, #ef4444);">
          <text>&#x1F4F7;</text>
        </view>
        <text class="tool-name">&#x56FE;&#x7247;&#x6C34;&#x5370;</text>
      </view>

      <view class="tool-card" @click="goImgStyle">
        <view class="tool-icon" style="background: linear-gradient(135deg, #a855f7, #ec4899);">
          <text>&#x1F3A8;</text>
        </view>
        <text class="tool-name">&#x98CE;&#x683C;&#x8F6C;&#x6362;</text>
      </view>

      <view class="tool-card" @click="goImgMerge">
        <view class="tool-icon" style="background: linear-gradient(135deg, #10b981, #06b6d4);">
          <text>&#x1F5BC;&#xFE0F;</text>
        </view>
        <text class="tool-name">&#x56FE;&#x7247;&#x62FC;&#x63A5;</text>
      </view>

      <view class="tool-card" @click="goColorPalette">
        <view class="tool-icon" style="background: linear-gradient(135deg, #f43f5e, #f97316);">
          <text>&#x1F308;</text>
        </view>
        <text class="tool-name">&#x914D;&#x8272;&#x65B9;&#x6848;</text>
      </view>

      <view class="tool-card" @click="goTempConvert">
        <view class="tool-icon" style="background: linear-gradient(135deg, #06b6d4, #0ea5e9);">
          <text>&#x1F321;&#xFE0F;</text>
        </view>
        <text class="tool-name">&#x6E29;&#x5EA6;&#x8F6C;&#x6362;</text>
      </view>

      <view class="tool-card" @click="goSlopeCalc">
        <view class="tool-icon" style="background: linear-gradient(135deg, #8b5cf6, #7c3aed);">
          <text>&#x1F4D0;</text>
        </view>
        <text class="tool-name">&#x5761;&#x5EA6;&#x8BA1;&#x7B97;</text>
      </view>

      <view class="tool-card" @click="goAngleCalc">
        <view class="tool-icon" style="background: linear-gradient(135deg, #14b8a6, #06b6d4);">
          <text>&#x2220;</text>
        </view>
        <text class="tool-name">&#x89D2;&#x5EA6;&#x8BA1;&#x7B97;</text>
      </view>

    >