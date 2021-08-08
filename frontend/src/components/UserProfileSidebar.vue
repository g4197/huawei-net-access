<template>
  <el-menu
    default-active="Profile"
    class="Navbar"
    @select="this.handleSelect"
    :default-openeds="['1']"
    :background-color="bgColor"
    :text-color="textColor"
    :active-text-color="activeTextColor"
  >
    <div class="sidebar-menu">
      <el-submenu index="1">
        <template slot="title">用户设置</template>
        <el-menu-item-group>
          <el-menu-item index="Profile">用户信息</el-menu-item>
          <el-menu-item index="Password">密码修改</el-menu-item>
        </el-menu-item-group>
      </el-submenu>
    </div>
  </el-menu>
</template>
<script lang="ts">
import mixins from "vue-typed-mixins";
import SidebarMixin from "@/mixins/SidebarMixin";
export default mixins(SidebarMixin).extend({
  name: "UserProfileSidebar",
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
