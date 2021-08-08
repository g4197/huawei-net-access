<template>
  <el-menu
    default-active="SiteInfo"
    class="Navbar"
    @select="this.handleSelect"
    :default-openeds="['1', '1-1']"
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
      <el-menu-item index="SiteInfo">站点概览</el-menu-item>
      <el-submenu style="padding: 0px" index="1-1">
        <template slot="title">站点运维</template>
        <div class="sidebar-submenu-item">
          <el-menu-item index="StatisticsInfo">统计信息</el-menu-item>
          <el-menu-item index="SSIDInfo">SSID信息</el-menu-item>
        </div>
      </el-submenu>
    </div>
  </el-menu>
</template>
<script lang="ts">
import mixins from "vue-typed-mixins";
import SidebarMixin from "@/mixins/SidebarMixin";
export default mixins(SidebarMixin).extend({
  name: "SingleSiteBoardSidebar",
  props: {
    handleSelect: Function
  }
});
</script>
