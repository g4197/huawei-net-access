<template>
  <el-container class="page-background">
    <el-header>
      <Navbar
        :visible="false"
        textWhenInvisible="注册"
        v-bind="this.user"
        :getUserProfile="this.getUserProfile"
        defaultActive=""
      />
    </el-header>
    <el-main class="form-container">
      <el-card class="text-center fixed-w-500">
        <div slot="header" class="clearfix">
          <span>注册</span>
        </div>
        <el-form
          status-icon
          ref="registerForm"
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
            <el-progress
              :percentage="this.passwordStrengthPercent"
              :format="passwordFormat"
            ></el-progress>
          </el-form-item>
          <el-form-item label="确认密码" prop="checkPassword">
            <el-input
              type="password"
              prefix-icon="el-icon-lock"
              v-model="formData.checkPassword"
            ></el-input>
          </el-form-item>
          <el-form-item label="公司名称" prop="name">
            <el-input
              prefix-icon="el-icon-suitcase"
              v-model="formData.name"
            ></el-input>
          </el-form-item>
          <el-form-item label="电子邮件" prop="email">
            <el-input
              prefix-icon="el-icon-message"
              v-model="formData.email"
            ></el-input>
          </el-form-item>
          <el-form-item label="电话" prop="telephone">
            <el-input
              prefix-icon="el-icon-mobile-phone"
              v-model="formData.telephone"
            ></el-input>
          </el-form-item>
          <el-form-item label="地址" prop="address">
            <el-input
              prefix-icon="el-icon-office-building"
              v-model="formData.address"
            ></el-input>
          </el-form-item>
          <el-form-item>
            <el-button
              class="reg-button"
              type="primary"
              @click="submitForm('registerForm')"
              >注册</el-button
            >
            <el-button
              style="margin-right: 10%"
              class="reg-button"
              @click="resetForm('registerForm')"
              >重置</el-button
            >
          </el-form-item>
        </el-form>
      </el-card>
    </el-main>
    <el-footer class="ms-footer">
      @Copyright 2021 OneHoldsThree
    </el-footer>
  </el-container>
</template>
<script lang="ts">
import mixins from "vue-typed-mixins";
import Navbar from "@/components/Navbar.vue";
import CsrfMixin from "@/mixins/CsrfMixin";
import UserMixin from "@/mixins/UserMixin";
import { encrypt } from "@/utils/encrypt";
require("../assets/styles/main.css");
export default mixins(CsrfMixin, UserMixin).extend({
  components: {
    Navbar
  },
  data() {
    const validatePass = (rule: object, value: string, callback: Function) => {
      // eslint-disable-next-line
      (this as any).passwordStrengthPercent = 0;
      if (value === "") {
        callback(new Error("请输入密码"));
      } else if (value.length < 6 || value.length > 16) {
        callback(new Error("密码长度需在6~16位之间"));
      } else if (value.match(/[\u4E00-\u9FA5]/)) {
        callback(new Error("密码不能包含汉字"));
      } else {
        // eslint-disable-next-line
        if ((this as any).formData.password != "") {
          // eslint-disable-next-line
          (this.$refs.registerForm as any).validateField("checkPassword");
        }
        let types = 0;
        if (value.match(/[a-z]/)) types++;
        if (value.match(/[A-Z]/)) types++;
        if (value.match(/[0-9]/)) types++;
        if (value.match(/[\W]/)) types++;
        if (types > 3) types = 3;
        // eslint-disable-next-line
        (this as any).passwordStrengthPercent = Math.floor(types * 33.34);
        callback();
      }
    };

    const validatePass2 = (rule: object, value: string, callback: Function) => {
      if (value === "") {
        callback(new Error("请再次输入密码"));
      } else {
        // eslint-disable-next-line
        if (value != (this as any).formData.password) {
          callback(new Error("两次输入密码不一致"));
        } else {
          callback();
        }
      }
    };

    const validateEmail = (rule: object, value: string, callback: Function) => {
      // eslint-disable-next-line
      if (value === "" && (this as any).formData.telephone === "") {
        callback(new Error("请输入电子邮件或电话"));
      } else {
        callback();
      }
    };

    const validateTelephone = (
      rule: object,
      value: string,
      callback: Function
    ): void => {
      // eslint-disable-next-line
      (this.$refs.registerForm as any).validateField("email");
      if (
        value !== "" &&
        !RegExp("0?(13|14|15|17|18|19)[0-9]{9}|[0-9-()（）]{7,18}").test(value)
      ) {
        callback(new Error("请输入合法电话"));
      } else {
        callback();
      }
    };

    return {
      formData: {
        name: "",
        username: "",
        email: "",
        telephone: "",
        address: "",
        password: "",
        checkPassword: ""
      },
      rules: {
        username: [
          { required: true, message: "请输入用户名", trigger: "blur" }
        ],
        name: [{ required: true, message: "请输入公司名称", trigger: "blur" }],
        address: [
          {
            required: true,
            message: "请输入地址",
            trigger: ["blur", "change"]
          }
        ],
        password: [
          {
            required: true,
            validator: validatePass,
            trigger: ["blur", "change"]
          }
        ],
        checkPassword: [
          {
            required: true,
            validator: validatePass2,
            trigger: ["blur", "change"]
          }
        ],
        email: [
          { validator: validateEmail, trigger: ["blur", "change"] },
          {
            type: "email",
            message: "请输入正确的邮箱地址",
            trigger: ["blur", "change"]
          }
        ],
        telephone: [
          { validator: validateTelephone, trigger: ["blur", "change"] }
        ]
      },
      passwordStrengthPercent: 0
    };
  },
  methods: {
    submitForm(formName: string): void {
      // eslint-disable-next-line
      (this.$refs[formName] as any).validate((valid: boolean): void => {
        if (valid) {
          const dataToPost = JSON.parse(JSON.stringify(this.formData));
          dataToPost.password = encrypt(dataToPost.password);
          dataToPost.checkPassword = encrypt(dataToPost.checkPassword);
          this.axiosPost("ApiRegister", dataToPost, "注册").then(response => {
            if (typeof response !== "undefined") {
              this.$message({
                message: "注册成功，正在转到登录",
                type: "success"
              });
              setTimeout(this.toLogin, 500);
            }
          });
        }
      });
    },
    resetForm(formName: string): void {
      // eslint-disable-next-line
      (this.$refs[formName] as any).resetFields();
    },
    toLogin(): void {
      this.$router.push({ name: "Login" });
    },
    passwordFormat(percentage: number): string {
      return percentage == 33
        ? "弱"
        : percentage == 66
        ? "中"
        : percentage == 100
        ? "强"
        : "";
    }
  }
});
</script>
