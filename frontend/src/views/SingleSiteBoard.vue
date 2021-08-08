<template>
  <el-container class="page-background">
    <el-header>
      <Navbar
        v-bind="this.user"
        :default-active="'SiteBoard'"
        :getUserProfile="this.getUserProfile"
      />
    </el-header>
    <el-container>
      <el-aside
        ><SingleSiteBoardSidebar :handleSelect="this.handleSelect"
      /></el-aside>
      <el-main v-loading="this.loading">
        <SiteCard
          v-if="curActive === 'SiteInfo'"
          :siteId="this.siteId"
          :changeLoadState="this.changeLoadState"
        />
        <StatisticsCard
          v-if="curActive === 'StatisticsInfo'"
          :siteId="this.siteId"
          :changeLoadState="this.changeLoadState"
        />
        <SSIDCard
          v-if="curActive === 'SSIDInfo'"
          :siteId="this.siteId"
          :changeLoadState="this.changeLoadState"
        />
      </el-main>
    </el-container>
  </el-container>
</template>
<script lang="ts">
import mixins from "vue-typed-mixins";
import Navbar from "@/components/Navbar.vue";
import SingleSiteBoardSidebar from "@/components/SingleSiteBoardSidebar.vue";
import CsrfMixin from "@/mixins/CsrfMixin";
import UserMixin from "@/mixins/UserMixin";
import NetworkStatusMixin from "@/mixins/NetworkStatusMixin";
import SiteCard from "@/components/SiteCard.vue";
import SSIDCard from "@/components/SSIDCard.vue";
import StatisticsCard from "@/components/StatisticsCard.vue";

require("@/assets/styles/main.css");

export default mixins(CsrfMixin, UserMixin, NetworkStatusMixin).extend({
  components: {
    Navbar,
    SingleSiteBoardSidebar,
    SiteCard,
    SSIDCard,
    StatisticsCard
  },
  data() {
    return {
      curActive: "SiteInfo",
      siteId: "",
      loading: false
    };
  },
  created() {
    if (this.$route.params.id !== undefined) {
      this.siteId = this.$route.params.id;
    } else {
      this.siteId = "";
    }
  },
  name: "SingleSiteBoard",
  methods: {
    changeLoadState(isLoading: boolean): void {
      this.loading = isLoading;
    },
    handleSelect(key: string): void {
      if (key === "GoBack") {
        this.$router.push(this.$router.resolve({ name: "SiteBoard" }).href);
      } else {
        this.curActive = key;
      }
    }
  }
});
</script>
