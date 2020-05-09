import Vue from 'vue'
import 'normalize.css/normalize.css'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import locale from 'element-ui/lib/locale/lang/zh-CN'
import '@/styles/index.scss'
import App from './App'
import router from './router'
import VCharts from 'v-charts'
import '@/icons'
import SvgIcon from './components/SvgIcon'
import store from './store'
import echarts from 'echarts'
import '@/permission' // permission control
import 'echarts/map/js/china'
Vue.use(VCharts);
Vue.prototype.$echarts = echarts
Vue.use(ElementUI, { locale })
Vue.config.productionTip = false
Vue.component('icon-svg', SvgIcon)

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app")
