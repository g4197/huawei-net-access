<template>
  <el-container class="page-background">
    <el-header>
      <Navbar
        v-bind="this.user"
        :default-active="'OrderBoard'"
        :getUserProfile="this.getUserProfile"
      />
    </el-header>
    <el-container>
      <el-aside
        ><SingleOrderBoardSidebar :handleSelect="this.handleSelect"
      /></el-aside>
      <el-main v-loading="this.loading">
        <OrderCard
          :changeLoadState="this.changeLoadState"
          :orderId="this.orderId"
          :privilege="this.user.privilege"
        />
      </el-main>
    </el-container>
  </el-container>
</template>
<script lang="ts">
import mixins from "vue-typed-mixins";
import Navbar from "@/components/Navbar.vue";
import SingleOrderBoardSidebar from "@/components/SingleOrderBoardSidebar.vue";
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
    SingleOrderBoardSidebar,
    CreateOrder,
    ViewOrder,
    OrderCard
  },
  data() {
    return {
      orderId: "",
      loading: false
    };
  },
  created() {
    if (this.$route.params.id !== undefined) {
      this.orderId = this.$route.params.id;
    } else {
      this.orderId = "";
    }
  },
  name: "OrderBoard",
  methods: {
    changeLoadState(isLoading: boolean): void {
      this.loading = isLoading;
    },
    handleSelect(key: string): void {
      if (key === "GoBack") {
        this.$router.push(this.$router.resolve({ name: "OrderBoard" }).href);
      }
    }
  }
});
</script>
