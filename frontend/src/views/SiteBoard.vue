<template>
  <el-container class="page-background-no-pic">
    <el-header>
      <Navbar
        v-bind="this.user"
        :default-active="'SiteBoard'"
        :getUserProfile="this.getUserProfile"
      />
    </el-header>
    <el-container>
      <el-aside><SiteBoardSidebar :handleSelect="this.handleSelect"/></el-aside>
      <el-main v-loading="loading" class="dashboard-background">
        <ViewSite
          :changeLoadState="changeLoadState"
          :viewSiteInfo="viewSiteInfo"
          v-if="curPage === 'ViewSite'"
        />
        <ViewBill
          :changeLoadState="changeLoadState"
          v-if="curPage === 'ViewBill'"
        />
      </el-main>
    </el-container>
  </el-container>
</template>

<script lang="ts">
import mixins from "vue-typed-mixins";
import CsrfMixin from "@/mixins/CsrfMixin";
import UserMixin from "@/mixins/UserMixin";
import Navbar from "@/components/Navbar.vue";
import SiteBoardSidebar from "@/components/SiteBoardSidebar.vue";
import ViewSite from "@/components/ViewSite.vue";
import ViewBill from "@/components/ViewBill.vue";
require("@/assets/styles/main.css");

export default mixins(CsrfMixin, UserMixin).extend({
  components: {
    Navbar,
    SiteBoardSidebar,
    ViewSite,
    ViewBill
  },
  name: "SiteBoard",
  data() {
    return {
      curPage: "ViewSite",
      orderId: 0,
      loading: false
    };
  },
  methods: {
    viewSiteInfo(siteId: string): void {
      this.$router.push(
        this.$router.resolve({
          name: "SingleSiteBoard",
          params: { id: siteId }
        }).href
      );
    },
    changeLoadState(isLoading: boolean): void {
      this.loading = isLoading;
    },
    setCurPage(key: string): void {
      this.curPage = key;
    },
    handleSelect(key: string): void {
      if (this.curPage !== key) {
        this.changeLoadState(false);
      }
      this.setCurPage(key);
    }
  }
});
</script>
