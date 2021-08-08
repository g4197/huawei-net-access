<template>
  <el-container class="page-background">
    <el-header>
      <Navbar v-bind="this.user" :getUserProfile="this.getUserProfile" />
    </el-header>
    <el-container>
      <el-aside
        ><UserProfileSidebar :handleSelect="this.handleSelect"
      /></el-aside>
      <el-main>
        <el-card
          v-if="this.curPage === 'Profile'"
          key="Profile"
          class="text-center w-80"
          shadow="never"
        >
          <div slot="header">用户信息</div>
          <el-form
            ref="profileForm"
            :rules="rules"
            :model="user"
            label-width="80px"
          >
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="用户名" prop="username">
                  <el-input
                    prefix-icon="el-icon-user"
                    v-model="user.username"
                    disabled
                  ></el-input>
                </el-form-item> </el-col
              ><el-col :span="12">
                <el-form-item label="用户ID">
                  <el-input v-model="user.id" disabled></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-form-item label="公司名称" prop="name">
              <el-input
                prefix-icon="el-icon-suitcase"
                v-model="user.name"
              ></el-input>
            </el-form-item>
            <el-form-item label="电子邮件" prop="email">
              <el-input
                prefix-icon="el-icon-message"
                v-model="user.email"
              ></el-input>
            </el-form-item>
            <el-form-item label="地址" prop="address">
              <el-input
                prefix-icon="el-icon-office-building"
                v-model="user.address"
              ></el-input>
            </el-form-item>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="电话" prop="telephone">
                  <el-input
                    prefix-icon="el-icon-mobile-phone"
                    v-model="user.telephone"
                  ></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="用户权限" prop="privilege">
                  <el-select
                    class="w-100"
                    v-if="isAdmin()"
                    v-model="user.privilege"
                  >
                    <el-option
                      v-for="item in privilegeArr"
                      :key="item.id"
                      :label="item.label"
                      :value="item.value"
                      :disabled="privilegeIsAdmin(item.value)"
                    ></el-option>
                  </el-select>
                  <el-select
                    class="w-100"
                    disabled
                    v-else
                    v-model="user.privilege"
                  >
                    <el-option
                      :label="privilegeArr[this.user.privilege].label"
                      :value="this.user.privilege"
                    ></el-option>
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
            <el-form-item>
              <el-button type="primary" @click="confirmModify('profileForm')"
                >修改</el-button
              >
              <el-button style="margin-right: 10%" @click="resetUserProfile()"
                >重置</el-button
              >
            </el-form-item>
          </el-form>
        </el-card>
        <el-card
          v-if="this.curPage === 'Password'"
          key="Password"
          class="text-center w-80"
          shadow="never"
        >
          <div slot="header">密码修改</div>
          <el-form
            ref="passwordForm"
            :rules="rules"
            :model="passwordFormData"
            label-width="100px"
          >
            <el-form-item label="原密码" prop="originalPassword">
              <el-input
                type="password"
                v-model="passwordFormData.originalPassword"
              ></el-input>
            </el-form-item>
            <el-form-item label="新密码" prop="password">
              <el-input
                type="password"
                v-model="passwordFormData.password"
              ></el-input>
              <el-progress
                :percentage="this.passwordStrengthPercent"
                :format="passwordFormat"
              ></el-progress>
            </el-form-item>
            <el-form-item label="确认新密码" prop="checkPassword">
              <el-input
                type="password"
                v-model="passwordFormData.checkPassword"
              ></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="confirmModify('passwordForm')"
                >修改</el-button
              >
              <el-button style="margin-right: 10%" @click="resetPassword()"
                >重置</el-button
              >
            </el-form-item>
          </el-form>
        </el-card>
      </el-main>
    </el-container>
  </el-container>
</template>
<script lang="ts">
import mixins from "vue-typed-mixins";
import Navbar from "@/components/Navbar.vue";
import UserProfileSidebar from "@/components/UserProfileSidebar.vue";
import CsrfMixin from "@/mixins/CsrfMixin";
import UserMixin from "@/mixins/UserMixin";
import NetworkStatusMixin from "@/mixins/NetworkStatusMixin";
import { UserPrivilege } from "@/enums/enums";
import { encrypt } from "@/utils/encrypt";
import ConfirmMixin from "@/mixins/ConfirmMixin";
require("@/assets/styles/main.css");

export default mixins(
  CsrfMixin,
  UserMixin,
  NetworkStatusMixin,
  ConfirmMixin
).extend({
  components: {
    Navbar,
    UserProfileSidebar
  },
  name: "UserSettings",
  data() {
    const validatePass = (rule: object, value: string, callback: Function) => {
      // eslint-disable-next-line
      (this as any).passwordStrengthPercent = 0;
      if (value === "") {
        callback(new Error("请输入新密码"));
      } else if (value.length < 6 || value.length > 16) {
        callback(new Error("密码长度需在6~16位之间"));
      } else if (value.match(/[\u4E00-\u9FA5]/)) {
        callback(new Error("密码不能包含汉字"));
      } else {
        // eslint-disable-next-line
        if ((this as any).passwordFormData.password !== "") {
          // eslint-disable-next-line
          (this.$refs.passwordForm as any).validateField("checkPassword");
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
        callback(new Error("请再次输入新密码"));
      } else {
        // eslint-disable-next-line
        if (value !== (this as any).passwordFormData.password) {
          callback(new Error("两次输入密码不一致"));
        } else {
          callback();
        }
      }
    };

    const validateEmail = (rule: object, value: string, callback: Function) => {
      // eslint-disable-next-line
      if (value === "" && (this as any).user.telephone === "") {
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
      (this.$refs.profileForm as any).validateField("email");
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
      curPage: "Profile",
      passwordFormData: {
        originalPassword: "",
        password: "",
        checkPassword: ""
      },
      privilege: 0,
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
        ],
        originalPassword: [
          {
            required: true,
            message: "请输入原密码",
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
        ]
      },
      passwordStrengthPercent: 0
    };
  },
  methods: {
    privilegeIsAdmin(privilege: number): boolean {
      return privilege === UserPrivilege.kAdmin;
    },
    isAdmin(): boolean {
      return this.user.privilege === UserPrivilege.kAdmin;
    },
    handleSelect(key: string): void {
      this.curPage = key;
    },
    confirmModify(formName: string): void {
      this.confirm("确定修改吗？", () => {
        // eslint-disable-next-line
        (this.$refs[formName] as any).validate((valid: boolean): void => {
          if (valid) {
            if (formName === "profileForm") this.modifyUserProfile();
            else if (formName === "passwordForm") this.modifyPassword();
          }
        });
      });
    },
    modifyUserProfile(): void {
      this.axiosPost("ApiModifyUserProfile", this.user, "修改").then(
        response => {
          if (typeof response !== "undefined") {
            this.$message({
              message: "修改成功",
              type: "success"
            });
            this.resetUserProfile();
          }
        }
      );
    },
    modifyPassword(): void {
      const dataToPost = JSON.parse(JSON.stringify(this.passwordFormData));
      dataToPost.originalPassword = encrypt(dataToPost.originalPassword);
      dataToPost.password = encrypt(dataToPost.password);
      dataToPost.checkPassword = encrypt(dataToPost.checkPassword);
      // eslint-disable-next-line
      dataToPost.original_password = dataToPost.originalPassword;
      // eslint-disable-next-line
      dataToPost.check_password = dataToPost.checkPassword;
      dataToPost.username = this.user.username;
      delete dataToPost.originalPassword;
      delete dataToPost.checkPassword;
      this.axiosPost("ApiModifyPassword", dataToPost, "修改").then(response => {
        if (typeof response !== "undefined") {
          this.$message({
            message: "修改成功",
            type: "success"
          });
          this.resetPassword();
          this.getUserProfile();
        }
      });
    },
    resetPassword(): void {
      // eslint-disable-next-line
      (this.$refs["passwordForm"] as any).resetFields();
      this.passwordStrengthPercent = 0;
    },
    resetUserProfile(): void {
      this.getUserProfile();
      // eslint-disable-next-line
      (this.$refs["profileForm"] as any).validate(() => {
        return true;
      });
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
