<template>
  <el-menu
    class="Navbar"
    default-active="ViewSite"
    @select="this.handleSelect"
    :default-openeds="['1']"
    :background-color="bgColor"
    :text-color="textColor"
    :active-text-color="activeTextColor"
  >
    <div class="sidebar-menu">
      <el-submenu index="1">
        <template slot="title">站点管理</template>
        <el-menu-item-group>
          <el-menu-item index="ViewSite">站点列表</el-menu-item>
          <el-menu-item index="ViewBill">账单列表</el-menu-item>
        </el-menu-item-group>
      </el-submenu>
    </div>
  </el-menu>
</template>
<script lang="ts">
import mixins from "vue-typed-mixins";
import SidebarMixin from "@/mixins/SidebarMixin";
export default mixins(SidebarMixin).extend({
  name: "SiteBoardSidebar",
  props: {
    handleSelect: Function
  }
});
</script>

<!--Only effective when put here, do not move-->
<style scoped>
.el-menu {
  border: none;
}
</style>
