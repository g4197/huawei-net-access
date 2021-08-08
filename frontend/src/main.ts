import Vue from "vue";
import VueCookies from "vue-cookies";
import DrVueEcharts from "dr-vue-echarts";
import router from "./router";
import App from "./App.vue";

import ElementUI from "element-ui";
import "element-ui/lib/theme-chalk/index.css";
Vue.use(ElementUI);
Vue.use(VueCookies);
Vue.use(DrVueEcharts);

Vue.config.productionTip = false;

new Vue({
  router,
  render: h => h(App)
}).$mount("#app");
