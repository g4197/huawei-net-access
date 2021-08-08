<template>
  <el-container class="login-wrap">
    <el-header>
      <Navbar />
    </el-header>
    <el-main>
      <div class="ms-login">
        <div class="ms-title">企业网络接入服务系统</div>
        <el-button
          type="primary"
          @click="jumpToLogin()"
          style="margin-right: 2%"
          >登录</el-button
        >
        <el-button type="primary" @click="jumpToRegister()">注册</el-button>
      </div>
    </el-main>
    <el-footer class="ms-footer"> @Copyright 2021 OneHoldsThree </el-footer>
  </el-container>
</template>

<script lang="ts">
import mixins from "vue-typed-mixins";
import CsrfMixin from "@/mixins/CsrfMixin";
import UserMixin from "@/mixins/UserMixin";
import Navbar from "@/components/Navbar.vue";

export default mixins(CsrfMixin, UserMixin).extend({
  name: "Home",
  components: {
    Navbar
  },
  mounted() {
    this.jumpToLogin();
  },
  methods: {
    jumpToRegister(): void {
      this.$router.push("/register");
    },
    jumpToLogin(): void {
      this.$router.push("/login");
    }
  }
});
</script>

<style scoped>
.login-wrap {
  height: 100vh;
  background-size: 100% 100%;
}
.ms-title {
  width: 100%;
  line-height: 50px;
  text-align: center;
  font-size: 20px;
  color: #fff;
  border-bottom: 1px solid #ddd;
}
.ms-login {
  position: absolute;
  left: 30%;
  top: 30%;
  width: 40%;
  margin: auto;
  border-radius: 5px;
  background: rgba(255, 255, 255, 0.3);
  overflow: hidden;
}
.ms-footer {
  background: rgba(255, 255, 255, 0.3);
  margin: auto;
  padding-top: 2%;
}
</style>
