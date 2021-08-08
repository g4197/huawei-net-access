<template>
  <el-card class="text-center w-80" style="min-height: 80vh">
    <div slot="header" style="font-size: 24px">
      <span>账单信息</span>
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
        v-for="bill in bills.slice((this.curPage - 1) * 12, this.curPage * 12)"
        :key="bill.index"
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
            <span class="card-title">{{ bill.siteName }}</span>
          </el-row>
          <el-divider style="margin: 16px 0"></el-divider>
          <el-row>
            <span class="card-content">站点ID：{{ bill.siteId }}</span>
          </el-row>
          <el-row>
            <span class="card-content"
              >计费方式：{{ billingArr[Number(bill.billingMethod)] }}</span
            >
          </el-row>
          <el-row>
            <span class="card-content"
              >超额流量：{{ flow2Str(bill.flowOverused) }}</span
            >
          </el-row>
          <el-row>
            <span class="card-content"
              >应缴费用：{{ bill.fee.toFixed(2) }}CNY</span
            >
          </el-row>
          <el-row type="flex" style="margin-top: 36px; align-items: stretch">
            <el-col :span="12" style="display: flex; align-items: center">
              <span class="card-content">
                <span class="card-dot" style="background-color: grey"></span
                >待缴费</span
              >
            </el-col>
            <el-col :span="12">
              <div class="text-right">
                <el-tooltip
                  class="item"
                  effect="dark"
                  content="缴费"
                  placement="bottom"
                >
                  <el-button
                    icon="el-icon-coin"
                    @click="payBill(bill.siteId)"
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
      :total="bills.length"
      :page-size="12"
      @current-change="handleCurrentChange"
    >
    </el-pagination>
  </el-card>
</template>

<script lang="ts">
interface Bill {
  siteName: string;
  siteId: string;
  billingMethod: boolean;
  fee: number;
  flowOverused: number;
}
import mixins from "vue-typed-mixins";
import AxiosMixin from "@/mixins/AxiosMixin";
import SpeedFlowMixin from "@/mixins/SpeedFlowMixin";
import ConfirmMixin from "@/mixins/ConfirmMixin";
export default mixins(AxiosMixin, SpeedFlowMixin, ConfirmMixin).extend({
  name: "ViewBill",
  data() {
    return {
      loading: true,
      bills: [] as Array<Bill>,
      billingArr: ["包年", "包月"],
      curPage: 1
    };
  },
  props: {
    changeLoadState: Function,
    viewSiteInfo: Function
  },
  mounted() {
    this.getBill();
  },
  methods: {
    payBill(id: string) {
      this.confirm("确认缴费吗？", () => {
        this.axiosPost("ApiPayBill", { id: id }, "缴费").then(res => {
          if (typeof res !== "undefined") {
            this.$message({
              message: "缴费成功",
              type: "success"
            });
            this.getBill();
          }
        });
      });
    },
    getBill(): void {
      this.axiosGet("ApiBillInfo", "获取账单信息", {}).then(res => {
        if (typeof res !== "undefined") {
          this.bills = res.data.data.Bill;
        }
      });
    },
    handleCurrentChange(page: number): void {
      this.curPage = page;
    }
  }
});
</script>
