<template>
  <el-row type="flex">
    <el-col :span="12">
      <el-menu
        class="Navbar"
        mode="horizontal"
        @select="handleSelect"
        :default-active="this.defaultActive"
        background-color="#006fc9"
        text-color="#f1f1f1"
        active-text-color="#f1f1f1"
      >
        <template v-if="this.visible">
          <el-menu-item index="OrderBoard">订单管理</el-menu-item>
          <el-menu-item index="SiteBoard">站点管理</el-menu-item>
        </template>
        <template v-else>
          <el-menu-item index="">
            {{ this.textWhenInvisible }}
          </el-menu-item>
        </template>
      </el-menu>
    </el-col>
    <el-col style="margin: auto" :span="12"
      ><template v-if="this.username !== ''">
        <el-dropdown
          class="text-right"
          @command="handleCommand"
          trigger="click"
        >
          <el-button class="el-dropdown-link" circle>
            <i class="el-icon-user-solid"></i>
          </el-button>
          <el-dropdown-menu slot="dropdown" style="min-width: 240px">
            <el-dropdown-item style="line-height: 30px" disabled
              ><b style="color: black">{{ this.username }}</b>
              <div v-if="this.email !== ''">{{ this.email }}</div>
            </el-dropdown-item>
            <el-dropdown-item divided command="UserProfile"
              >用户设置</el-dropdown-item
            >
            <el-dropdown-item v-if="isAdmin()" command="AdminUserProfile"
              >用户管理</el-dropdown-item
            >
            <el-dropdown-item divided command="logout">注销</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown> </template
      ><template v-else>
        <el-button-group class="text-right">
          <el-button
            type="primary"
            class="radius-button"
            style="border-right-color: #409EFF;"
            @click="handleSelect('Login')"
            >登录</el-button
          >
          <el-button
            style="margin-left: 8px"
            class="radius-button"
            @click="handleSelect('Register')"
            >注册</el-button
          >
        </el-button-group>
      </template></el-col
    >
  </el-row>
</template>

<script lang="ts">
import mixins from "vue-typed-mixins";
import AxiosMixin from "@/mixins/AxiosMixin";
import { UserPrivilege } from "@/enums/enums";
require("@/assets/styles/main.css");
export default mixins(AxiosMixin).extend({
  name: "Navbar",
  props: {
    username: String,
    email: String,
    name: String,
    telephone: String,
    address: String,
    id: Number,
    privilege: Number,
    getUserProfile: Function,
    defaultActive: {
      type: String,
      default: ""
    },
    visible: {
      type: Boolean,
      default: true
    },
    textWhenInvisible: String
  },
  methods: {
    isAdmin(): boolean {
      return this.privilege === UserPrivilege.kAdmin;
    },
    handleSelect(key: string): void {
      if (key) {
        this.$router.push(this.$router.resolve({ name: key }).href);
      }
    },
    handleCommand(command: string) {
      if (command == "logout") {
        this.logout();
      } else {
        this.$router.push(this.$router.resolve({ name: command }).href);
      }
    },
    logout(): void {
      this.axiosPostNoCatch("ApiLogout", {})
        .then(() => {
          this.$message({
            message: "注销成功",
            type: "success"
          });
          // eslint-disable-next-line
          (this as any).getUserProfile();
        })
        .catch(() => {
          // eslint-disable-next-line
          (this as any).getUserProfile();
        });
    }
  }
});
</script>
<!--Only effective when put here, do not move-->
<style scoped>
.el-menu.el-menu--horizontal {
  border: none;
}
</style>
