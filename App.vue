<script>
export default {
  onLaunch: function() {
    console.log('App Launch')
    // 小程序启动时检查登录态
    const isLoggedIn = uni.getStorageSync('isLoggedIn')
    // 如果未登录且当前不在 login 页，则跳转到 login
    const pages = getCurrentPages()
    if (pages.length > 0) {
      const currentRoute = pages[pages.length - 1].route
      if (!isLoggedIn && currentRoute !== 'pages/login/login') {
        uni.reLaunch({ url: '/pages/login/login' })
      }
    }
  },
  onShow: function() {
    console.log('App Show')
  },
  onHide: function() {
    console.log('App Hide')
  }
}
</script>

<style>
/* 全局公共样式 */
view, text, input, button {
  box-sizing: border-box;
}

/* 安全区域 */
.safe-bottom {
  padding-bottom: env(safe-area-inset-bottom);
}

/* 通用按钮反馈 */
.btn-active {
  opacity: 0.7;
  transform: scale(0.97);
}
</style>
