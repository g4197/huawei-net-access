<template>
  <el-container class="page-background-no-pic">
    <el-header>
      <Navbar
        v-bind="this.user"
        :default-active="'OrderBoard'"
        :getUserProfile="this.getUserProfile"
      />
    </el-header>
    <el-container>
      <el-aside style="float: right"
        ><OrderBoardSidebar :handleSelect="this.handleSelect"
      /></el-aside>
      <el-main class="dashboard-background" v-loading="this.loading">
        <CreateOrder v-if="curPage === 'CreateOrder'" />
        <template v-if="curPage === 'ViewOrder'">
          <ViewOrder
            ref="viewOrder"
            :privilege="this.user.privilege"
            :viewOrderInfo="this.viewOrderInfo"
            :changeLoadState="this.changeLoadState"
          />
        </template>
      </el-main>
    </el-container>
  </el-container>
</template>
<script lang="ts">
import mixins from "vue-typed-mixins";
import Navbar from "@/components/Navbar.vue";
import OrderBoardSidebar from "@/components/OrderBoardSidebar.vue";
import CsrfMixin from "@/mixins/CsrfMixin";
import UserMixin from "@/mixins/UserMixin";
import NetworkStatusMixin from "@/mixins/NetworkStatusMixin";
import CreateOrder from "@/components/CreateOrder.vue";
import ViewOrder from "@/components/ViewOrder.vue";
import OrderCard from "@/components/OrderCard.vue";
require("@/assets/styles/main.css");

export default mixins(CsrfMixin, UserMixin, NetworkStatusMixin).extend({
  components: {
    Navbar,
    OrderBoardSidebar,
    CreateOrder,
    ViewOrder,
    OrderCard
  },
  data() {
    return {
      curPage: "ViewOrder",
      loading: false
    };
  },
  name: "OrderBoard",
  methods: {
    changeLoadState(isLoading: boolean): void {
      this.loading = isLoading;
    },
    viewOrderInfo(orderId: string): void {
      this.$router.push(
        this.$router.resolve({
          name: "SingleOrderBoard",
          params: { id: orderId }
        }).href
      );
    },
    setCurPage(key: string): void {
      this.curPage = key;
    },
    handleSelect(key: string): void {
      this.setCurPage(key);
    }
  }
});
</script>
