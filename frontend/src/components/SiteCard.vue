<template>
  <el-card style="max-width: 1500px" class="text-center">
    <el-row>
      <div
        class="clearfix text-left"
        style="display: flex; align-items: center;"
      >
        <span style="margin-right: 12px;">{{ site.name }}</span>
        <template v-if="!site.flowLimitExceeded">
          <span class="card-content-sm">
            <span class="card-dot" style="background-color: green;"></span
            >运行中</span
          >
        </template>
        <template v-else>
          <span class="card-content-sm">
            <span class="card-dot" style="background-color: grey;"></span
            >待缴费</span
          >
        </template>
      </div>
    </el-row>
    <el-row class="site-row">
      <div class="site-subheader"><i class="el-icon-s-grid"></i> 站点监控</div>
    </el-row>
    <el-row :gutter="20">
      <el-col :lg="8" :md="24">
        <el-card shadow="none">
          <el-row>
            <el-col :span="16">
              <el-row style="padding-bottom: 24px">
                <div class="text-left">流量</div> </el-row
              ><el-row>
                <div class="text-left">
                  <span style="font-size: 24px">{{
                    flow2Str(site.flow).slice(0, -2)
                  }}</span>
                  <span style="font-size: 14px">
                    {{ flow2Str(site.flow).slice(-2) }} /
                  </span>
                  <span style="font-size: 24px">{{
                    flow2Str(site.flowThreshold).slice(0, -2)
                  }}</span>
                  <span style="font-size: 14px">
                    {{ flow2Str(site.flowThreshold).slice(-2) }}</span
                  >
                </div>
              </el-row>
            </el-col>
            <el-col :span="8">
              <el-progress
                class="site-progress"
                type="dashboard"
                :width="80"
                :color="flowColor()"
                :percentage="getPercent(site.flow, site.flowThreshold)"
              ></el-progress>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
      <el-col :lg="8" :md="24">
        <el-card shadow="none">
          <el-row>
            <el-col :span="16">
              <el-row style="padding-bottom: 24px">
                <div class="text-left">在线人数</div> </el-row
              ><el-row>
                <div class="text-left">
                  <span style="font-size: 24px">{{ site.onlineUserCnt }}</span>
                  <span style="font-size: 14px"> 人</span> /
                  <span style="font-size: 24px">{{
                    site.maxUserNumberCnt
                  }}</span>
                  <span style="font-size: 14px"> 人</span>
                </div>
              </el-row>
            </el-col>
            <el-col :span="8">
              <el-progress
                class="site-progress"
                type="dashboard"
                :width="80"
                :color="userColor()"
                :percentage="
                  getPercent(site.onlineUserCnt, site.maxUserNumberCnt)
                "
              ></el-progress>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
      <el-col :lg="8" :md="24">
        <el-card shadow="none">
          <el-row>
            <el-col :span="24">
              <el-row
                style="padding-bottom: 24px; display: flex; align-items: center"
              >
                <el-col :span="16">
                  <div class="text-left">
                    <span style="margin-right: 8px">上行</span>
                    <span style="font-size: 24px">{{
                      speed2Str(site.upSpeed).slice(0, -4)
                    }}</span>
                    <span style="font-size: 14px">
                      {{ speed2Str(site.upSpeed).slice(-4) }}
                    </span>
                  </div></el-col
                ><el-col :span="8">
                  <el-progress
                    :show-text="false"
                    :percentage="getPercent(site.upSpeed, kSpeedLimit)"
                  ></el-progress>
                </el-col> </el-row
              ><el-row style="display: flex; align-items: center">
                <el-col :span="16">
                  <div class="text-left">
                    <span style="margin-right: 8px">下行</span>
                    <span style="font-size: 24px">{{
                      speed2Str(site.downSpeed).slice(0, -4)
                    }}</span>
                    <span style="font-size: 14px">
                      {{ speed2Str(site.downSpeed).slice(-4) }}</span
                    >
                  </div></el-col
                ><el-col :span="8">
                  <el-progress
                    :show-text="false"
                    :percentage="getPercent(site.downSpeed, kSpeedLimit)"
                  ></el-progress>
                </el-col>
              </el-row>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>
    <el-row class="site-row">
      <div class="site-subheader"><i class="el-icon-s-grid"></i> 站点信息</div>
    </el-row>
    <el-row>
      <el-card shadow="none">
        <el-col :lg="12" :md="24">
          <el-row class="site-list-row">
            <div class="text-left">
              <span class="site-list-title">站点ID:</span>
              <span class="site-list-content">
                {{ site.id }}
              </span>
            </div> </el-row
          ><el-row class="site-list-row">
            <div class="text-left">
              <span class="site-list-title">地址:</span>
              <span class="site-list-content">
                {{ site.address }}
              </span>
            </div>
          </el-row>
          <el-row class="site-list-row">
            <div class="text-left">
              <span class="site-list-title">经度:</span>
              <span class="site-list-content">
                {{ site.latitude }}
              </span>
            </div>
          </el-row>
          <el-row class="site-list-row">
            <div class="text-left">
              <span class="site-list-title">纬度:</span>
              <span class="site-list-content">
                {{ site.longtitude }}
              </span>
            </div>
          </el-row>
        </el-col>
        <el-col :lg="12" :md="24">
          <el-row class="site-list-row">
            <div class="text-left">
              <span class="site-list-title">用户ID:</span>
              <span class="site-list-content">
                {{ site.tenantId }}
              </span>
            </div>
          </el-row>
          <el-row class="site-list-row">
            <div class="text-left">
              <span class="site-list-title">邮箱:</span>
              <span class="site-list-content">
                {{ site.email }}
              </span>
            </div>
          </el-row>
          <el-row class="site-list-row">
            <div class="text-left">
              <span class="site-list-title">电话:</span>
              <span class="site-list-content">
                {{ site.phone }}
              </span>
            </div>
          </el-row>
          <el-row class="site-list-row">
            <div class="text-left">
              <span class="site-list-title">邮编:</span>
              <span class="site-list-content">
                {{ site.postcode }}
              </span>
            </div>
          </el-row>
        </el-col>
      </el-card>
    </el-row>
    <el-row class="site-row">
      <div class="site-subheader"><i class="el-icon-s-grid"></i> 设备信息</div>
    </el-row>
    <el-card shadow="none">
      <el-table v-loading="loading" border :data="device" class="text-center">
        <el-table-column prop="id" label="设备ID" align="center">
        </el-table-column>
        <el-table-column prop="deviceModel" label="设备型号" align="center">
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间" align="center">
        </el-table-column>
      </el-table>
    </el-card>
  </el-card>
</template>
<script lang="ts">
import mixins from "vue-typed-mixins";
import NetworkStatusMixin from "@/mixins/NetworkStatusMixin";
import AxiosMixin from "@/mixins/AxiosMixin";
import SpeedFlowMixin from "@/mixins/SpeedFlowMixin";
require("@/assets/styles/main.css");

interface SingleSite {
  id: string;
  tenantId: string;
  name: string;
  description: string;
  type: Array<string>;
  latitude: string;
  longtitude: string;
  contact: string;
  tag: Array<string>;
  isolated: boolean;
  email: string;
  phone: string;
  postcode: string;
  address: string;
  upSpeed: number;
  downSpeed: number;
  flow: number;
  flowThreshold: number;
  onlineUserCnt: number;
  maxUserNumberCnt: number;
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

export default mixins(NetworkStatusMixin, AxiosMixin, SpeedFlowMixin).extend({
  name: "SiteCard",
  data() {
    return {
      site: {} as SingleSite,
      device: [] as Array<Device>,
      loading: false
    };
  },
  props: {
    siteId: String,
    changeLoadState: Function
  },
  mounted() {
    this.getSiteInfo();
    this.getDeviceInfo();
  },
  methods: {
    getSiteInfo() {
      this.changeLoadState(true);
      this.axiosGetNoCatch("ApiGetSingleSite", { id: this.siteId })
        .then(res => {
          this.site = res.data.data;
          this.changeLoadState(false);
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
    getDeviceInfo() {
      this.loading = true;
      // eslint-disable-next-line
      this.axiosGetNoCatch("ApiDeviceInfo", { id: this.siteId })
        .then(res => {
          this.device = res.data.data.devices;
          this.loading = false;
        })
        .catch(err => {
          let text = err.response.data.message;
          if (text === undefined) text = "获取设备信息失败，未知错误";
          this.$message({
            message: text,
            type: "error"
          });
          this.loading = false;
        });
    },
    flowColor(): string {
      const percent =
        this.site.flowThreshold === 0
          ? 100
          : Math.round((100 * this.site.flow) / this.site.flowThreshold);
      if (percent < 75) {
        return "#409eff";
      } else if (percent < 90) {
        return "#e6a23c";
      } else {
        return "#f56c6c";
      }
    },
    userColor(): string {
      const percent =
        this.site.maxUserNumberCnt === 0
          ? 100
          : Math.round(
              (100 * this.site.onlineUserCnt) / this.site.maxUserNumberCnt
            );
      if (percent < 75) {
        return "#409eff";
      } else if (percent < 90) {
        return "#e6a23c";
      } else {
        return "#f56c6c";
      }
    },
    getPercent(cur: number, max: number): number {
      if (isNaN(cur) || isNaN(max)) return 0;
      if (max == 0) return 0;
      return Math.min(Math.round((100 * cur) / max), 100);
    }
  }
});
</script>

<style>
.site-subheader {
  color: #606266;
  float: left;
}

.site-row {
  font-size: 14px;
  padding-top: 12px;
  padding-bottom: 12px;
}

.site-progress > .el-progress__text {
  font-size: 14px !important;
}

.site-list-title {
  margin-right: 12px;
  font-size: 14px;
}

.site-list-content {
  font-size: 12px;
}

.site-list-row {
  margin-bottom: 8px;
}
</style>
