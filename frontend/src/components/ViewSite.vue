<template>
  <el-card class="text-center w-80" style="min-height: 80vh">
    <el-dialog :visible.sync="dialogVisible">
      <el-table :data="device">
        <el-table-column prop="id" label="设备ID" align="center">
        </el-table-column>
        <el-table-column prop="deviceModel" label="设备型号" align="center">
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间" align="center">
        </el-table-column>
      </el-table>
    </el-dialog>
    <div slot="header" style="font-size: 24px">
      <span>站点信息</span>
    </div>
    <el-row
      :gutter="20"
      style="
        min-height: calc(80vh - 100px);
        display: flex;
        flex-wrap: wrap;
        align-content: flex-start;
      "
    >
      <el-col
        :md="12"
        :xl="8"
        v-for="site in sites.slice((this.curPage - 1) * 12, this.curPage * 12)"
        :key="site.index"
      >
        <el-card
          shadow="none"
          style="
            border: 1px solid #dcdfe6;
            margin-top: 20px;
            margin-bottom: 20px;
          "
        >
          <el-row>
            <span class="card-title">{{ site.name }}</span>
          </el-row>
          <el-divider style="margin: 16px 0"></el-divider>
          <el-row>
            <span class="card-content">站点地址：{{ site.address }}</span>
          </el-row>
          <el-row>
            <span class="card-content">站点ID：{{ site.id }}</span>
          </el-row>
          <el-row type="flex" style="margin-top: 36px; align-items: stretch">
            <el-col :span="12" style="display: flex; align-items: center">
              <template v-if="!site.flowLimitExceeded">
                <span class="card-content">
                  <span class="card-dot" style="background-color: green"></span
                  >运行中</span
                >
              </template>
              <template v-else>
                <span class="card-content">
                  <span class="card-dot" style="background-color: grey"></span
                  >待缴费</span
                >
              </template>
            </el-col>
            <el-col :span="12">
              <div class="text-right">
                <el-tooltip
                  class="item"
                  effect="dark"
                  content="查看详情"
                  placement="bottom"
                >
                  <el-button
                    icon="el-icon-more-outline"
                    @click="viewSiteInfo(site.id)"
                    circle
                  >
                  </el-button
                ></el-tooltip>
                <el-tooltip
                  class="item"
                  effect="dark"
                  content="设备信息"
                  placement="bottom"
                >
                  <el-button
                    icon="el-icon-cpu"
                    @click="viewDeviceInfo(site)"
                    circle
                  >
                  </el-button
                ></el-tooltip>
              </div>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>
    <el-pagination
      background
      layout="prev, pager, next"
      :total="sites.length"
      :page-size="12"
      @current-change="handleCurrentChange"
    >
    </el-pagination>
  </el-card>
</template>

<script lang="ts">
interface Site {
  id: string;
  tenantId: string;
  name: string;
  description: string;
  type: Array<string>;
  latitude: string;
  longtitude: string;
  contact: string;
  tag: Array<string>;
  isolated: boolean | null;
  email: string;
  phone: string;
  postcode: string;
  address: string;
  flowLimitExceeded: boolean;
}

interface Device {
  createTime: string;
  deviceModel: string;
  deviceType: string;
  id: string;
  ip: string | null;
  mac: string | null;
  neType: string;
}

import mixins from "vue-typed-mixins";
import AxiosMixin from "@/mixins/AxiosMixin";
export default mixins(AxiosMixin).extend({
  name: "ViewSite",
  data() {
    return {
      loading: true,
      dialogVisible: false,
      device: [] as Array<Device>,
      sites: [] as Array<Site>,
      curPage: 1
    };
  },
  props: {
    changeLoadState: Function,
    viewSiteInfo: Function
  },
  mounted() {
    this.getSiteInfo();
  },
  methods: {
    getSiteInfo(): void {
      this.changeLoadState(true);
      this.axiosGetNoCatch("ApiSiteInfo", {})
        .then(res => {
          if (typeof res !== "undefined") {
            const sites = res.data.data.sites;
            this.sites = sites;
            this.changeLoadState(false);
          }
        })
        .catch(err => {
          let text = err.response.data.message;
          if (text === undefined) text = "获取站点信息失败，未知错误";
          this.$message({
            message: text,
            type: "error"
          });
          this.changeLoadState(false);
        });
    },
    viewDeviceInfo(site: Site) {
      this.changeLoadState(true);
      // eslint-disable-next-line
      this.axiosGetNoCatch("ApiDeviceInfo", { id: site.id })
        .then(res => {
          this.device = res.data.data.devices;
          this.dialogVisible = true;
          this.changeLoadState(false);
        })
        .catch(err => {
          let text = err.response.data.message;
          if (text === undefined) text = "获取设备信息失败，未知错误";
          this.$message({
            message: text,
            type: "error"
          });
          this.changeLoadState(false);
        });
    },
    handleCurrentChange(page: number): void {
      this.curPage = page;
    }
  }
});
</script>
