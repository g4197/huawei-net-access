<template>
  <el-menu
    class="Navbar"
    default-active="ViewOrder"
    @select="this.handleSelect"
    :default-openeds="['1']"
    :background-color="bgColor"
    :text-color="textColor"
    :active-text-color="activeTextColor"
  >
    <div class="sidebar-menu">
      <el-submenu index="1">
        <template slot="title">订单管理</template>
        <el-menu-item-group>
          <el-menu-item index="CreateOrder">创建订单</el-menu-item>
          <el-menu-item index="ViewOrder">订单列表</el-menu-item>
        </el-menu-item-group>
      </el-submenu>
    </div>
  </el-menu>
</template>
<script lang="ts">
import mixins from "vue-typed-mixins";
import SidebarMixin from "@/mixins/SidebarMixin";
export default mixins(SidebarMixin).extend({
  name: "OrderBoardSidebar",
  props: {
    handleSelect: Function
  }
});
</script>
