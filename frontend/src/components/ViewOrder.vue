<template>
  <el-card class="text-center w-80" style="height: 85vh">
    <div>
      <el-row :gutter="20">
        <el-col :span="16">
          <el-tabs
            v-model="activeIndex"
            type="card"
            @tab-click="handleTabClick"
          >
            <el-tab-pane label="全部订单"></el-tab-pane>
            <el-tab-pane
              v-for="state in stateArr"
              :key="state.index"
              :label="state"
            >
            </el-tab-pane>
          </el-tabs> </el-col
        ><el-col :span="8">
          <el-input v-model="searchKeyword" placeholder="输入内容以搜索">
            <i slot="suffix" class="el-input__icon el-icon-search"></i
          ></el-input>
        </el-col>
      </el-row>
      <el-table
        height="calc(85vh - 150px)"
        :data="
          filteredOrderList().slice((this.curPage - 1) * 10, this.curPage * 10)
        "
      >
        <el-table-column prop="siteName" label="站点名称" align="center">
        </el-table-column>
        <el-table-column
          prop="siteAddress"
          label="站点地址"
          align="center"
        ></el-table-column>
        <el-table-column label="结算方式" align="center">
          <template slot-scope="scope">
            {{ flow2Str(scope.row.flowThreshold) }} |
            {{ scope.row.billingMethod }}
          </template>
        </el-table-column>
        <el-table-column label="订单状态" align="center">
          <template slot-scope="scope">
            <el-tag :type="typeOfStateNum[scope.row.stateNum]">{{
              scope.row.state
            }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center">
          <template slot-scope="scope">
            <el-button-group>
              <el-button
                type="primary"
                @click="viewOrderInfo(scope.row.id)"
                class="radius-button"
                style="margin-right: 4px"
                >详情</el-button
              >
              <el-button
                type="danger"
                class="radius-button"
                @click="confirmCancel(scope.row.id)"
                v-if="scope.row.state !== '已取消'"
                :disabled="!canCancel(scope.row)"
                >取消</el-button
              >
              <el-button
                type="info"
                class="radius-button"
                @click="confirmRestore(scope.row.id)"
                v-if="scope.row.state === '已取消'"
                :disabled="!canRestore(scope.row)"
                >恢复</el-button
              >
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <br />
    <el-pagination
      background
      layout="prev, pager, next"
      :total="filteredOrderList().length"
      @current-change="handleCurrentChange"
    >
    </el-pagination>
  </el-card>
</template>
<script lang="ts">
import mixins from "vue-typed-mixins";
import AxiosMixin from "@/mixins/AxiosMixin";
import ConfirmMixin from "@/mixins/ConfirmMixin";
import SpeedFlowMixin from "@/mixins/SpeedFlowMixin";
import NetworkStatusMixin from "@/mixins/NetworkStatusMixin";
import { UserPrivilege } from "@/enums/enums";
require("@/assets/styles/main.css");

interface ServerSideOrderItem {
  owner: string;
  site_name: string;
  site_address: string;
  billing_method: boolean;
  network_demand: Array<string>;
  flow_threshold: number;
  state: number;
  id: string;
}

interface OrderItem {
  owner: string;
  siteName: string;
  siteAddress: string;
  billingMethod: string;
  networkDemand: Array<string>;
  flowThreshold: number;
  state: string;
  stateNum: number;
  id: string;
}

require("@/assets/styles/main.css");

export default mixins(
  NetworkStatusMixin,
  AxiosMixin,
  ConfirmMixin,
  SpeedFlowMixin
).extend({
  name: "ViewOrder",
  mounted() {
    this.getOrderList();
  },
  data() {
    return {
      orderList: [] as OrderItem[],
      curPage: 1,
      searchKeyword: "",
      orderState: "全部订单",
      activeIndex: "",
      typeOfStateNum: ["", "warning", "danger", "success", "info"]
    };
  },
  props: {
    privilege: {
      type: Number,
      default: UserPrivilege.kCustomer
    },
    changeLoadState: Function,
    setCurPage: Function,
    viewOrderInfo: Function
  },
  methods: {
    isNetworkEngineer(): boolean {
      return this.privilege === UserPrivilege.kNetworkEngineer;
    },
    getOrderList(): void {
      this.axiosGet("ApiOrderInfo", "获取订单列表", {}).then(res => {
        if (typeof res !== "undefined") {
          const orders: ServerSideOrderItem[] = res.data["data"]["orders"];
          this.orderList = [];
          for (let i = orders.length - 1; i >= 0; --i) {
            this.orderList.push(this.dataToOrderItem(orders[i]));
          }
        }
      });
    },
    filteredOrderList(): OrderItem[] {
      return this.orderList.filter(
        data =>
          (!this.searchKeyword ||
            data.siteName
              .toLowerCase()
              .includes(this.searchKeyword.toLowerCase()) ||
            data.siteAddress
              .toLowerCase()
              .includes(this.searchKeyword.toLowerCase())) &&
          (this.orderState === "全部订单" || data.state === this.orderState)
      );
    },
    dataToOrderItem(data: ServerSideOrderItem): OrderItem {
      return {
        owner: data.owner,
        siteName: data.site_name,
        siteAddress: data.site_address,
        billingMethod: this.billingMethodArr[Number(data.billing_method)],
        networkDemand: data.network_demand,
        state: this.stateArr[data.state],
        stateNum: data.state,
        flowThreshold: data.flow_threshold,
        id: data.id
      };
    },
    confirmCancel(id: string): void {
      this.$prompt("请输入取消原因", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        inputPattern: /[\s\S]+/,
        inputErrorMessage: "取消原因不能为空",
        type: "warning"
      })
        .then(obj => {
          this.confirm("确定取消当前订单吗？", () => {
            this.cancelOrder(id, (obj as { value: string }).value);
          });
        })
        .catch(() => {
          return;
        });
    },
    confirmRestore(id: string): void {
      this.confirm("确定恢复当前订单吗？", () => {
        this.restoreOrder(id);
      });
    },
    restoreOrder(idToRestore: string): void {
      this.axiosPost("ApiRestoreOrder", { id: idToRestore }, "恢复").then(
        res => {
          if (typeof res !== "undefined") {
            this.$message({
              message: "恢复成功",
              type: "success"
            });
          }
          this.getOrderList();
        }
      );
    },
    cancelOrder(idToCancel: string, reason: string): void {
      this.changeLoadState(true);
      this.axiosPostNoCatch("ApiCancelOrder", {
        id: idToCancel,
        reason: reason
      })
        .then(() => {
          this.$message({
            message: "取消成功",
            type: "success"
          });
          this.getOrderList();
          this.changeLoadState(false);
        })
        .catch(err => {
          let text = err.response.data.message;
          if (text === undefined) text = "取消失败，未知错误";
          this.$message({
            message: text,
            type: "error"
          });
          this.changeLoadState(false);
        });
    },
    canCancel(order: OrderItem): boolean {
      // if it is submitted, user can cancel it, or it should be network manager.
      return (
        order.state !== "已取消" &&
        order.state !== "已完成" &&
        (order.state === "已提交" || this.isNetworkEngineer())
      );
    },
    canRestore(order: OrderItem): boolean {
      return order.state === "已取消" && this.isNetworkEngineer();
    },
    handleCurrentChange(page: number): void {
      this.curPage = page;
    },
    handleTabClick(tab: { label: string }): void {
      this.orderState = tab.label;
    }
  }
});
</script>
