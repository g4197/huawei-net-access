<template>
  <el-container class="page-background">
    <el-header>
      <Navbar
        :visible="false"
        textWhenInvisible="登录"
        v-bind="this.user"
        :getUserProfile="this.getUserProfile"
        defaultActive=""
      />
    </el-header>
    <el-main>
      <AlertDialog v-bind="alertDialog" />
      <LoginCard />
    </el-main>
    <el-footer class="ms-footer">
      @Copyright 2021 OneHoldsThree
    </el-footer>
  </el-container>
</template>

<script>
import mixins from "vue-typed-mixins";
import LoginCard from "@/components/LoginCard";
import Navbar from "@/components/Navbar";
import AlertDialog from "@/components/AlertDialog";
import AlertDialogMixin from "@/mixins/AlertDialogMixin";
import CsrfMixin from "@/mixins/CsrfMixin";
import UserMixin from "@/mixins/UserMixin";

require("@/assets/styles/main.css");
export default mixins(AlertDialogMixin, CsrfMixin, UserMixin).extend({
  components: {
    AlertDialog,
    Navbar,
    LoginCard
  }
});
</script>
