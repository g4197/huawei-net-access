<template>
  <el-card class="text-center w-80">
    <SSIDDialog
      :SSIDDataToPass="SSIDDataToPass"
      :disabled="SSIDDialogDisabled"
      :visible="SSIDDialogVisible"
      :onComplete="onComplete"
      :hide="hideSSIDDialog"
    />
    <el-dialog
      title="添加网络"
      :visible.sync="networkDialogVisible"
      :close-on-click-modal="false"
      :show-close="false"
    >
      <div class="text-center relative-w-80">
        <el-form :model="networkToAdd" ref="surveyForm" :rules="surveyRules">
          <el-form-item label="网络名称" prop="name">
            <el-input v-model="networkToAdd.name"></el-input>
          </el-form-item>
        </el-form>
        <el-button
          type="primary"
          class="radius-button"
          @click="addNetwork()"
          style="margin-right: 4px"
          >完成</el-button
        >
        <el-button @click="hideNetworkDialog()">取消</el-button>
      </div>
    </el-dialog>
    <el-row>
      <div
        class="clearfix text-left"
        style="display: flex; align-items: center"
      >
        <span style="margin-right: 12px">{{ this.order.siteName }}</span>
        <span class="card-content-sm">
          <span
            v-if="this.order.state !== '已取消'"
            class="card-dot"
            style="background-color: green"
          ></span>
          <span v-else class="card-dot" style="background-color: grey"></span>
          {{ this.order.state }}</span
        >
      </div>
    </el-row>
    <el-row :gutter="40">
      <el-col :span="24">
        <el-row class="site-row">
          <div class="site-subheader">
            <i class="el-icon-s-grid"></i>订单基本信息
          </div>
        </el-row>
        <el-card shadow="none">
          <el-row
            ><el-col :lg="12" :md="24">
              <el-row class="site-list-row">
                <div class="text-left">
                  <span class="site-list-title">站点ID:</span>
                  <span class="site-list-content">
                    {{ this.order.id }}
                  </span>
                </div>
              </el-row>
              <el-row class="site-list-row">
                <div class="text-left">
                  <span class="site-list-title">公司名称:</span>
                  <span class="site-list-content">
                    {{ this.order.owner }}
                  </span>
                </div>
              </el-row>
              <el-row class="site-list-row">
                <div class="text-left">
                  <span class="site-list-title">站点地址:</span>
                  <span class="site-list-content">
                    {{ this.order.siteAddress }}
                  </span>
                </div>
              </el-row> </el-col
            ><el-col :lg="12" :md="24">
              <el-row class="site-list-row">
                <div class="text-left">
                  <span class="site-list-title">计费方式:</span>
                  <span class="site-list-content">
                    {{ this.order.billingMethod }}
                  </span>
                </div>
              </el-row>
              <el-row class="site-list-row">
                <div class="text-left">
                  <span class="site-list-title">套餐流量:</span>
                  <span class="site-list-content">
                    {{ flow2Str(order.flowThreshold) }}
                  </span>
                </div>
              </el-row>
              <el-row class="site-list-row">
                <div class="text-left">
                  <span class="site-list-title">基础网络需求:</span>
                  <span class="site-list-content">
                    {{ networkDemand() }}
                  </span>
                </div>
              </el-row>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>
    <el-row class="site-row">
      <div class="site-subheader"><i class="el-icon-s-grid"></i>订单状态</div>
    </el-row>
    <template v-if="!isNetworkEngineer()">
      <el-row>
        <span class="order-state-content" v-if="this.order.state === '已取消'"
          >您的订单{{ this.order.state }}，原因：{{ this.order.reason }}</span
        >
        <span
          class="order-state-content"
          v-else-if="this.order.state === '已完成'"
          >您的订单{{
            this.order.state
          }}，请到“站点管理”页面查看站点部署情况</span
        >
        <span class="order-state-content" v-else
          >您的订单{{ this.order.state }}，请您耐心等待</span
        >
      </el-row>
    </template>
    <el-row>
      <el-steps
        finish-status="success"
        simple
        :active="this.order.state === '已取消' ? -1 : this.order.stateNum + 1"
        style="margin-top: 10px; background-color: #ffffff"
      >
        <el-step
          v-for="state in stepArr"
          :key="state.index"
          :title="state"
        ></el-step>
      </el-steps>
    </el-row>
    <el-row :gutter="40"
      ><el-col :md="24" :lg="12">
        <el-row class="site-row">
          <div class="site-subheader">
            <i class="el-icon-s-grid"></i>网络信息
          </div>
          <el-button
            v-if="canSurvey()"
            class="text-right"
            size="mini"
            plain
            type="primary"
            icon="el-icon-plus"
            @click="showNetworkDialog()"
          ></el-button>
        </el-row>
        <el-row>
          <el-card shadow="never">
            <el-table :data="order.network" :height="242">
              <el-table-column prop="name" label="网络名称" align="center">
                <template slot-scope="scope">
                  {{ scope.row.name }}
                </template>
              </el-table-column>
              <el-table-column v-if="canSurvey()" label="操作" align="center">
                <template slot-scope="scope">
                  <el-button type="danger" @click="removeNetwork(scope.$index)"
                    >删除</el-button
                  >
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </el-row></el-col
      >
      <el-col :md="24" :lg="12">
        <el-row class="site-row">
          <div class="site-subheader">
            <i class="el-icon-s-grid"></i>SSID信息
          </div>
          <el-button
            v-if="canSurvey()"
            class="text-right"
            size="mini"
            plain
            type="primary"
            icon="el-icon-plus"
            @click="addSSID()"
          ></el-button>
        </el-row>
        <el-row>
          <el-card shadow="never">
            <el-table :data="order.SSID" :height="242">
              <el-table-column prop="name" label="SSID名称" align="center">
              </el-table-column>
              <el-table-column label="操作" align="center">
                <template slot-scope="scope">
                  <el-button
                    v-if="!canSurvey()"
                    type="primary"
                    class="radius-button"
                    style="margin-right: 4px"
                    @click="showSSID(scope.$index)"
                  >
                    详情
                  </el-button>
                  <el-button-group v-if="canSurvey()">
                    <el-button
                      type="primary"
                      class="radius-button"
                      style="margin-right: 4px"
                      @click="editSSID(scope.$index)"
                      >编辑</el-button
                    >
                    <el-button
                      type="danger"
                      class="radius-button"
                      @click="removeSSID(scope.$index)"
                      >删除</el-button
                    >
                  </el-button-group>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </el-row>
      </el-col></el-row
    >
    <el-row style="margin-top: 20px" v-if="canSurvey()">
      <el-button
        type="success"
        style="margin-left: 20px"
        class="radius-button"
        @click="confirmSurvey()"
        >提交工勘</el-button
      >
    </el-row>
    <el-row style="margin-top: 20px" v-if="canDeploy()">
      <el-button type="success" class="radius-button" @click="confirmDeploy()"
        >提交部署</el-button
      >
    </el-row>
    <el-row style="margin-top: 20px" v-if="canOpen()">
      <el-button type="success" class="radius-button" @click="confirmOpen()"
        >开通</el-button
      >
    </el-row>
  </el-card>
</template>
<script lang="ts">
import mixins from "vue-typed-mixins";
import { UserPrivilege } from "@/enums/enums";
import SSIDDialog from "@/components/SSIDDialog.vue";
import SSIDMixin, { SSID, ServerSideSSID } from "@/mixins/SSIDMixin";
import ConfirmMixin from "@/mixins/ConfirmMixin";
import NetworkStatusMixin from "@/mixins/NetworkStatusMixin";
import AxiosMixin from "@/mixins/AxiosMixin";
import SpeedFlowMixin from "@/mixins/SpeedFlowMixin";
import SiteCard from "./SiteCard.vue";
require("@/assets/styles/main.css");

interface Network {
  name: string;
}

interface ServerSideOrderItem {
  owner: string;
  site_name: string;
  site_address: string;
  billing_method: boolean;
  network_demand: Array<string>;
  flow_threshold: number;
  state: number;
  reason: string;
  id: string;
  network_list: Array<Network>;
  ssid_list: Array<ServerSideSSID>;
}

interface OrderItem {
  owner: string;
  siteName: string;
  siteAddress: string;
  billingMethod: string;
  networkDemand: Array<string>;
  flowThreshold: number;
  state: string;
  reason: string;
  stateNum: number;
  id: string;
  network: Array<Network>;
  SSID: Array<SSID>;
}

export default mixins(
  NetworkStatusMixin,
  AxiosMixin,
  SpeedFlowMixin,
  SSIDMixin,
  ConfirmMixin
).extend({
  name: "OrderCard",
  components: {
    SSIDDialog,
    SiteCard
  },
  data() {
    return {
      order: {} as OrderItem,
      networkToAdd: {} as Network,
      SSIDDataToPass: {} as SSID,
      curSSIDIndex: 0,
      SSIDDialogVisible: false,
      networkDialogVisible: false,
      SSIDDialogDisabled: false,
      surveyRules: {
        name: [{ required: true, message: "请输入网络名称", trigger: "blur" }]
      }
    };
  },
  mounted() {
    this.getSingleOrder(this.orderId);
  },
  props: {
    privilege: {
      type: Number,
      default: UserPrivilege.kCustomer
    },
    orderId: {
      type: String,
      default: ""
    },
    changeLoadState: Function
  },
  methods: {
    networkDemand(): string {
      if (typeof this.order.network === "undefined") return "";
      return this.order.networkDemand.join(", ");
    },
    isNetworkEngineer(): boolean {
      return this.privilege === UserPrivilege.kNetworkEngineer;
    },
    isOperationEngineer(): boolean {
      return this.privilege === UserPrivilege.kOperationEngineer;
    },
    hideNetworkDialog(): void {
      this.networkDialogVisible = false;
    },
    showNetworkDialog(): void {
      this.networkDialogVisible = true;
    },
    hideSSIDDialog(): void {
      this.SSIDDialogVisible = false;
    },
    showSSID(index: number): void {
      this.curSSIDIndex = index;
      this.SSIDDataToPass = JSON.parse(JSON.stringify(this.order.SSID[index]));
      this.SSIDDialogDisabled = true;
      this.SSIDDialogVisible = true;
    },
    editSSID(index: number): void {
      this.curSSIDIndex = index;
      this.SSIDDataToPass = JSON.parse(JSON.stringify(this.order.SSID[index]));
      this.SSIDDialogDisabled = false;
      this.SSIDDialogVisible = true;
    },
    removeSSID(index: number): void {
      this.order.SSID.splice(index, 1);
    },
    addSSID(): void {
      this.curSSIDIndex = this.order.SSID.length;
      this.SSIDDataToPass = {} as SSID;
      this.SSIDDialogDisabled = false;
      this.SSIDDialogVisible = true;
    },
    onComplete(SSIDDataToAdd: SSID): void {
      if (this.curSSIDIndex === this.order.SSID.length) {
        this.order.SSID.push(JSON.parse(JSON.stringify(SSIDDataToAdd)));
      } else {
        this.$set(this.order.SSID, this.curSSIDIndex, SSIDDataToAdd);
      }
      this.SSIDDialogVisible = false;
    },
    canSurvey(): boolean {
      return this.isNetworkEngineer() && this.order.state === "已提交";
    },
    canDeploy(): boolean {
      return this.isNetworkEngineer() && this.order.state === "已工勘";
    },
    canOpen(): boolean {
      return this.isNetworkEngineer() && this.order.state === "已部署";
    },
    removeNetwork(index: number): void {
      this.order.network.splice(index, 1);
    },
    addNetwork(): void {
      // eslint-disable-next-line
      let surveyForm = this.$refs["surveyForm"] as any;
      surveyForm.validate((valid: boolean): boolean => {
        if (valid) {
          this.order.network.push(
            JSON.parse(JSON.stringify(this.networkToAdd))
          );
          surveyForm.resetFields();
          this.hideNetworkDialog();
          return true;
        } else {
          return false;
        }
      });
    },
    getSingleOrder(orderId: string): void {
      this.axiosGet("ApiGetSingleOrder", "获取订单信息", {
        id: orderId
      }).then(res => {
        if (typeof res !== "undefined") {
          const order = res.data["data"] as ServerSideOrderItem;
          this.order = this.dataToOrderItem(order);
        }
      });
    },
    dataToOrderItem(data: ServerSideOrderItem): OrderItem {
      return {
        owner: data.owner,
        siteName: data.site_name,
        siteAddress: data.site_address,
        billingMethod: this.billingMethodArr[Number(data.billing_method)],
        networkDemand: data.network_demand,
        state: this.stateArr[data.state],
        reason: data.reason,
        stateNum: data.state,
        flowThreshold: data.flow_threshold,
        id: data.id, // eslint-disable-next-line
        network: data.network_list, // eslint-disable-next-line
        SSID: this.serverSideSSIDToSSID(data.ssid_list)
      };
    },
    confirmSurvey(): void {
      this.confirm("确定提交工勘信息吗？", this.surveyOrder);
    },
    surveyOrder(): void {
      this.axiosPost(
        "ApiSurveyOrder",
        {
          id: this.orderId, // eslint-disable-next-line
          network_list: this.order.network, // eslint-disable-next-line
          ssid_list: this.getSSIDList()
        },
        "工勘"
      ).then(res => {
        if (typeof res !== "undefined") {
          this.$message({
            message: "工勘成功",
            type: "success"
          });
          this.getSingleOrder(this.orderId);
        }
      });
    },
    confirmDeploy(): void {
      this.confirm("确定部署吗？", this.deployOrder);
    },
    getSSIDList(): Array<ServerSideSSID> {
      const SSIDList = [] as Array<ServerSideSSID>;
      /* eslint-disable */
      for (let i = 0; i < this.order.SSID.length; ++i) {
        let item = {} as ServerSideSSID;
        let data = this.order.SSID[i];
        item.name = data.name;
        item.enable = data.enable;
        item.connection_mode = data.connectionMode;
        item.hid_enable = data.hidEnable;
        item.relative_radios = data.relativeRadios;
        item.max_user_number = data.maxUserNumber;
        item.user_separation = data.userSeparation;
        item.auth_mode = data.authMode;
        item.auth_psk_encrypt_type = data.authPskEncryptType;
        item.auth_security_key = data.authSecurityKey;
        item.auth_security_key_type = data.authSecurityKeyType;
        item.auth_dot1x_encrypt_type = data.authDot1xEncryptType;
        item.auth_mac_auto_binding = data.authMacAutoBinding;
        SSIDList.push(JSON.parse(JSON.stringify(item)));
      }
      return SSIDList;
    },
    deployOrder(): void {
      this.changeLoadState(true);
      this.axiosPostNoCatch("ApiDeployOrder", { id: this.orderId })
        .then(() => {
          this.$message({
            message: "部署成功",
            type: "success"
          });
          this.changeLoadState(false);
          this.getSingleOrder(this.orderId);
        })
        .catch(err => {
          let text = err.response.data.message;
          if (text === undefined) text = "部署失败，未知错误";
          this.$message({
            message: text,
            type: "error"
          });
          this.changeLoadState(false);
        });
    },
    confirmOpen(): void {
      this.confirm("确定开通吗？", this.openOrder);
    },
    openOrder(): void {
      this.axiosPost("ApiOpenOrder", { id: this.orderId }, "开通").then(res => {
        if (typeof res !== "undefined") {
          this.$message({
            message: "开通成功",
            type: "success"
          });
        }
        this.getSingleOrder(this.orderId);
      });
    }
  }
});
</script>
<style>
.order-state-content {
  color: #606266;
  font-size: 12px;
  padding-left: 2%;
  float: left;
}
</style>
<style scoped>
.site-subheader {
  font-size: 16px;
}
</style>
