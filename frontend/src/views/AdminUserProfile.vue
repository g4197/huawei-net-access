<template>
  <el-container class="page-background">
    <el-header>
      <Navbar v-bind="this.user" :getUserProfile="this.getUserProfile" />
    </el-header>
    <el-container>
      <el-main>
        <el-card class="text-center w-80" style="height: 85vh">
          <el-row :gutter="20">
            <el-col :span="16">
              <el-tabs
                v-model="activeIndex"
                type="card"
                @tab-click="handleTabClick"
              >
                <el-tab-pane
                  v-for="privilege in privilegeArr"
                  :key="privilege.value"
                  :label="privilege.label"
                >
                </el-tab-pane>
              </el-tabs> </el-col
            ><el-col :span="8">
              <el-input v-model="searchKeyword" placeholder="输入内容以搜索">
                <i slot="suffix" class="el-input__icon el-icon-search"></i
              ></el-input>
            </el-col>
          </el-row>
          <el-table
            :data="
              filteredList().slice((this.curPage - 1) * 10, this.curPage * 10)
            "
            height="calc(85vh - 150px)"
          >
            <el-table-column prop="username" label="用户名" align="center">
            </el-table-column>
            <el-table-column
              prop="name"
              label="公司名称"
              align="center"
            ></el-table-column>
            <el-table-column label="权限" align="center">
              <template slot-scope="scope">
                <el-row :gutter="10">
                  <el-col :span="16">
                    <el-select
                      v-model="scope.row.newPrivilege"
                      placeholder="请选择"
                    >
                      <el-option
                        v-for="item in privilegeArr"
                        :key="item.index"
                        :label="item.label"
                        :value="item.value"
                      >
                      </el-option>
                    </el-select> </el-col
                  ><el-col :span="8">
                    <el-button type="danger" @click="confirmModify(scope.row)"
                      >修改</el-button
                    >
                  </el-col>
                </el-row>
              </template>
            </el-table-column>
            <el-table-column label="密码" align="center">
              <template slot-scope="scope">
                <el-button
                  type="primary"
                  @click="confirmModifyPassword(scope.row.username)"
                >
                  修改
                </el-button>
              </template>
            </el-table-column>
          </el-table>
          <br />
          <el-pagination
            background
            layout="prev, pager, next"
            :total="filteredList().length"
            @current-change="handleCurrentChange"
          >
          </el-pagination>
        </el-card>
      </el-main>
    </el-container>
  </el-container>
</template>
<script lang="ts">
import mixins from "vue-typed-mixins";
import Navbar from "@/components/Navbar.vue";
import CsrfMixin from "@/mixins/CsrfMixin";
import UserMixin from "@/mixins/UserMixin";
import { User } from "@/mixins/UserMixin";
import { encrypt } from "@/utils/encrypt";
import { UserPrivilege } from "@/enums/enums";
import ConfirmMixin from "@/mixins/ConfirmMixin";
require("@/assets/styles/main.css");

interface NewPrivilegeUser extends User {
  newPrivilege: number;
}

export default mixins(CsrfMixin, UserMixin, ConfirmMixin).extend({
  components: {
    Navbar
  },
  name: "AdminUserProfile",
  data() {
    return {
      userList: [] as Array<NewPrivilegeUser>,
      searchKeyword: "",
      curPage: 1,
      activeIndex: "",
      activePrivilege: UserPrivilege.kCustomer
    };
  },
  mounted() {
    this.getUserList();
  },
  methods: {
    getUserList(): void {
      this.axiosGet("ApiUserList", "获取用户列表", {}).then(res => {
        this.userList = [];
        if (typeof res !== "undefined") {
          const lst = res.data["data"]["userprofile"] as User[];
          for (let i = 0; i < lst.length; ++i) {
            this.userList.push(
              Object.assign(lst[i], { newPrivilege: lst[i].privilege })
            );
          }
        }
      });
    },
    confirmModify(newPrivilegeUser: NewPrivilegeUser): void {
      this.confirm("确定修改吗？", () => {
        this.modifyUserProfile(newPrivilegeUser);
      });
    },
    modifyUserProfile(newPrivilegeUser: NewPrivilegeUser): void {
      const user = JSON.parse(
        JSON.stringify(newPrivilegeUser)
      ) as NewPrivilegeUser;
      user.privilege = user.newPrivilege;
      this.axiosPostNoCatch("ApiModifyUserProfile", user)
        .then(response => {
          if (response.data["code"] === 201) {
            this.$message({
              message: "修改成功",
              type: "success"
            });
            newPrivilegeUser.privilege = newPrivilegeUser.newPrivilege;
          }
        })
        .catch(error => {
          let text = error.response.data.message;
          if (text === undefined) text = "修改失败，未知错误";
          this.$message({
            message: text,
            type: "error"
          });
          newPrivilegeUser.newPrivilege = newPrivilegeUser.privilege;
        });
    },
    filteredList(): Array<User> {
      return this.userList.filter(
        data =>
          (!this.searchKeyword ||
            data.username
              .toLowerCase()
              .includes(this.searchKeyword.toLowerCase()) ||
            data.name
              .toLowerCase()
              .includes(this.searchKeyword.toLowerCase()) ||
            data.email
              .toLowerCase()
              .includes(this.searchKeyword.toLowerCase())) &&
          data.privilege === this.activePrivilege
      );
    },
    confirmModifyPassword(username: string): void {
      this.$prompt("请输入新密码", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        inputType: "password",
        inputPattern: /[\S]{6,16}/,
        inputErrorMessage: "密码不合法"
      })
        .then(obj => {
          const newPassword = (obj as { value: string }).value;
          this.confirm("确定修改密码吗？", () => {
            return this.modifyPassword(username, newPassword);
          });
        })
        .catch(() => {
          return;
        });
    },
    modifyPassword(username: string, password: string): void {
      const dataToPost = {
        // eslint-disable-next-line
        original_password: "",
        password: encrypt(password),
        // eslint-disable-next-line
        check_password: encrypt(password),
        username: username
      };
      this.axiosPost("ApiModifyPassword", dataToPost, "修改").then(response => {
        if (typeof response !== "undefined") {
          this.$message({
            message: "修改成功",
            type: "success"
          });
          this.getUserProfile();
        }
      });
    },
    handleCurrentChange(page: number): void {
      this.curPage = page;
    },
    handleTabClick(tab: { index: number }): void {
      this.activePrivilege = this.privilegeArr[tab.index].value;
    }
  }
});
</script>
