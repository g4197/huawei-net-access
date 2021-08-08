import Vue from "vue";
import VueRouter from "vue-router";
import Home from "@/views/Home.vue";
import Register from "@/views/Register.vue";
import Login from "@/views/Login.vue";
import OrderBoard from "@/views/OrderBoard.vue";
import SingleOrderBoard from "@/views/SingleOrderBoard.vue";
import SiteBoard from "@/views/SiteBoard.vue";
import SingleSiteBoard from "@/views/SingleSiteBoard.vue";
import Error from "@/views/Error.vue";
import UserProfile from "@/views/UserProfile.vue";
import AdminUserProfile from "@/views/AdminUserProfile.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
    meta: {
      title: "主页"
    }
  },
  {
    path: "/register",
    name: "Register",
    component: Register,
    meta: {
      title: "注册"
    }
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
    meta: {
      title: "登录"
    }
  },
  {
    path: "/order/:id",
    name: "SingleOrderBoard",
    component: SingleOrderBoard,
    meta: {
      title: "订单管理"
    }
  },
  {
    path: "/order",
    name: "OrderBoard",
    component: OrderBoard,
    meta: {
      title: "订单管理"
    }
  },
  {
    path: "/site/:id",
    name: "SingleSiteBoard",
    component: SingleSiteBoard,
    meta: {
      title: "站点管理"
    }
  },
  {
    path: "/site",
    name: "SiteBoard",
    component: SiteBoard,
    meta: {
      title: "站点管理"
    }
  },
  {
    path: "/profile",
    name: "UserProfile",
    component: UserProfile,
    meta: {
      title: "用户设置"
    }
  },
  {
    path: "/admin/profile",
    name: "AdminUserProfile",
    component: AdminUserProfile,
    meta: {
      title: "用户管理"
    }
  },
  {
    path: "/api",
    name: "Api"
  },
  {
    path: "/api/login",
    name: "ApiLogin"
  },
  {
    path: "/api/register",
    name: "ApiRegister"
  },
  {
    path: "/api/logout",
    name: "ApiLogout"
  },
  {
    path: "/api/get_csrf_token",
    name: "ApiCsrf"
  },
  {
    path: "/api/get_userprofile",
    name: "ApiUserProfile"
  },
  {
    path: "/api/get_user_list",
    name: "ApiUserList"
  },
  {
    path: "/api/modify_userprofile",
    name: "ApiModifyUserProfile"
  },
  {
    path: "/api/modify_password",
    name: "ApiModifyPassword"
  },
  {
    path: "/api/get_order_information",
    name: "ApiOrderInfo"
  },
  {
    path: "/api/get_single_order_information",
    name: "ApiGetSingleOrder"
  },
  {
    path: "/api/submit_order",
    name: "ApiSubmitOrder"
  },
  {
    path: "/api/cancel_order",
    name: "ApiCancelOrder"
  },
  {
    path: "/api/restore_order",
    name: "ApiRestoreOrder"
  },
  {
    path: "/api/survey_order",
    name: "ApiSurveyOrder"
  },
  {
    path: "/api/deploy_order",
    name: "ApiDeployOrder"
  },
  {
    path: "/api/close_order",
    name: "ApiOpenOrder"
  },
  {
    path: "/api/get_sites",
    name: "ApiSiteInfo"
  },
  {
    path: "/api/get_single_site_information",
    name: "ApiGetSingleSite"
  },
  {
    path: "/api/get_devices",
    name: "ApiDeviceInfo"
  },
  {
    path: "/api/get_ssid",
    name: "ApiSSIDInfo"
  },
  {
    path: "/api/get_statistics",
    name: "ApiStatisticsInfo"
  },
  {
    path: "/api/get_bill",
    name: "ApiBillInfo"
  },
  {
    path: "/api/pay",
    name: "ApiPayBill"
  },
  {
    path: "*",
    name: "Error",
    component: Error,
    meta: {
      title: "404"
    }
  }
];

const router = new VueRouter({
  mode: "history",
  routes
});

router.beforeEach((to, from, next) => {
  if (to.meta.title) {
    document.title = to.meta.title;
  }
  next();
});

export default router;
