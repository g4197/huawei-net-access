<template>
  <el-menu
    default-active="OrderInfo"
    class="Navbar"
    @select="this.handleSelect"
    :default-openeds="['1']"
    :background-color="bgColor"
    :text-color="textColor"
    :active-text-color="activeTextColor"
  >
    <el-menu-item
      index="GoBack"
      style="padding: 0px; display: flex; align-items: stretch"
      ><span
        style="
          width: 100%;
          height: 100%;
          background-color: #d9dee4;
          color: #546478;
        "
        ><span class="el-menu-item-inner"
          ><i class="el-icon-arrow-left"></i>返回</span
        ></span
      ></el-menu-item
    >
    <div class="sidebar-menu">
      <el-menu-item index="OrderInfo">订单详情</el-menu-item>
    </div>
  </el-menu>
</template>
<script lang="ts">
import mixins from "vue-typed-mixins";
import SidebarMixin from "@/mixins/SidebarMixin";
export default mixins(SidebarMixin).extend({
  name: "SingleOrderBoardSidebar",
  props: {
    handleSelect: Function
  }
});
</script>
