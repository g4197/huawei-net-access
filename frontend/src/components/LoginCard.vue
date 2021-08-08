<template>
  <el-card class="text-center fixed-w-500">
    <div slot="header" class="clearfix">
      <span>登录</span>
    </div>
    <el-form
      status-icon
      ref="loginForm"
      :rules="rules"
      :model="formData"
      label-width="80px"
    >
      <el-form-item label="用户名" prop="username">
        <el-input
          prefix-icon="el-icon-user"
          v-model="formData.username"
        ></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input
          type="password"
          prefix-icon="el-icon-lock"
          v-model="formData.password"
        ></el-input>
      </el-form-item>
    </el-form>
    <el-button
      class="login-button"
      type="primary"
      @click="submitForm('loginForm')"
      >登录</el-button
    >
    <el-button class="login-button" @click="resetForm('loginForm')"
      >重置</el-button
    >
  </el-card>
</template>

<script lang="ts">
import mixins from "vue-typed-mixins";
import CsrfMixin from "@/mixins/CsrfMixin";
import UserMixin from "@/mixins/UserMixin";
import AxiosMixin from "@/mixins/AxiosMixin";
import { encrypt } from "@/utils/encrypt";

export default mixins(CsrfMixin, UserMixin, AxiosMixin).extend({
  data() {
    return {
      type: "LoginCard",
      formData: {
        username: "",
        password: ""
      },
      rules: {
        username: [
          {
            required: true,
            message: "请输入用户名",
            trigger: ["blur", "change"]
          }
        ],
        password: [
          { required: true, message: "请输入密码", trigger: ["blur", "change"] }
        ]
      }
    };
  },
  methods: {
    submitForm(formName: string): void {
      // eslint-disable-next-line
      (this.$refs[formName] as any).validate((valid: boolean) => {
        if (!valid) {
          return false;
        } else {
          const dataToPost = JSON.parse(JSON.stringify(this.formData));
          dataToPost.password = encrypt(dataToPost.password);
          this.axiosPost("ApiLogin", dataToPost, "登录").then(response => {
            if (typeof response !== "undefined") {
              this.$message({
                message: "登录成功",
                type: "success"
              });
              setTimeout(() => {
                this.$router.push({ name: "OrderBoard" });
              }, 500);
            }
          });
        }
      });
    },
    resetForm(formName: string): void {
      // eslint-disable-next-line
      (this.$refs[formName] as any).resetFields();
    }
  }
});
</script>
