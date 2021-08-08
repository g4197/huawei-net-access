<template>
  <el-card class="text-center fixed-w-500">
    <div slot="header" class="clearfix">
      <span>创建订单</span>
    </div>
    <el-form
      status-icon
      ref="orderForm"
      :rules="rules"
      :model="formData"
      label-width="120px"
    >
      <el-form-item label="站点名称" prop="siteName">
        <el-input v-model="formData.siteName"></el-input>
      </el-form-item>
      <el-form-item label="站点地址" prop="siteAddress">
        <el-input v-model="formData.siteAddress"></el-input>
      </el-form-item>
      <el-form-item label="计费方式" prop="billingMethod">
        <el-select
          v-model="formData.billingMethod"
          placeholder="请选择"
          class="w-100"
        >
          <el-option
            v-for="item in billingOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="套餐总量" prop="flowThreshold">
        <el-row>
          <el-col :span="16">
            <el-input-number
              v-model="formData.flowThreshold"
              class="w-100"
              :min="1"
              :max="999"
              controls-position="right"
            ></el-input-number> </el-col
          ><el-col :span="7" :offset="1">
            <el-select
              v-model="formData.flowThresholdMul"
              placeholder="请选择"
              default-first-option=""
            >
              <el-option
                v-for="item in flowThresholdMulOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              >
              </el-option>
            </el-select>
          </el-col>
        </el-row>
      </el-form-item>
      <el-form-item label="基础网络需求" prop="networkDemand">
        <el-checkbox-group class="w-100" v-model="formData.networkDemand">
          <el-checkbox
            :key="item.value"
            v-for="item in networkDemandOptions"
            :label="item.label"
          ></el-checkbox>
        </el-checkbox-group>
      </el-form-item>
      <el-form-item class="text-left">
        <el-button type="primary" @click="confirmCreate()">提交</el-button>
        <el-button @click="resetForm('orderForm')">重置</el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script lang="ts">
import mixins from "vue-typed-mixins";
import AxiosMixin from "@/mixins/AxiosMixin";
import ConfirmMixin from "@/mixins/ConfirmMixin";
import SpeedFlowMixin from "@/mixins/SpeedFlowMixin";
require("@/assets/styles/main.css");
export default mixins(AxiosMixin, SpeedFlowMixin, ConfirmMixin).extend({
  name: "CreateOrder",
  data() {
    return {
      formData: {
        siteName: "",
        siteAddress: "",
        billingMethod: 1,
        networkDemand: [],
        flowThreshold: 0,
        flowThresholdMul: 0
      },
      rules: {
        siteName: [
          {
            required: true,
            message: "请输入站点名称",
            trigger: ["blur", "change"]
          }
        ],
        siteAddress: [
          {
            required: true,
            message: "请输入站点地址",
            trigger: ["blur", "change"]
          }
        ],
        billingMethod: [
          {
            required: true,
            message: "请选择结算方式",
            trigger: ["blur", "change"]
          }
        ],
        networkDemand: [
          {
            required: true,
            message: "请选择基础网络需求",
            trigger: ["blur", "change"]
          }
        ],
        flowThreshold: [
          {
            required: true,
            message: "请输入套餐总量",
            trigger: ["blur", "change"]
          }
        ]
      },
      billingOptions: [
        {
          value: 1,
          label: "包月"
        },
        {
          value: 0,
          label: "包年"
        }
      ],
      networkDemandOptions: [
        {
          value: 0,
          label: "Guest"
        },
        {
          value: 1,
          label: "Management"
        },
        {
          value: 2,
          label: "Test"
        }
      ],
      flowThresholdMulOptions: [
        {
          value: 0,
          label: "MB"
        },
        {
          value: 1,
          label: "GB"
        },
        {
          value: 2,
          label: "TB"
        }
      ]
    };
  },
  methods: {
    confirmCreate(): void {
      this.confirm("确定创建吗？", () => {
        return this.submitForm("orderForm");
      });
    },
    submitForm(formName: string): void {
      // eslint-disable-next-line
      (this.$refs[formName] as any).validate((valid: boolean): void => {
        if (valid) {
          /* eslint-disable */
          let realFlowThresholdMul = 1;
          if (this.formData.flowThresholdMul == 0) {
            realFlowThresholdMul = this.kMB;
          } else if (this.formData.flowThresholdMul == 1) {
            realFlowThresholdMul = this.kGB;
          } else {
            realFlowThresholdMul = this.kTB;
          }
          const dataToPost = {
            site_name: this.formData.siteName,
            site_address: this.formData.siteAddress,
            billing_method: this.formData.billingMethod,
            network_demand: this.formData.networkDemand,
            flow_threshold: this.formData.flowThreshold * realFlowThresholdMul
          };
          this.axiosPost("ApiSubmitOrder", dataToPost, "创建").then(
            response => {
              if (typeof response !== "undefined") {
                this.$message({
                  message: "创建成功",
                  type: "success"
                });
                this.resetForm(formName);
              }
            }
          );
        }
      });
    },
    resetForm(formName: string): void {
      // eslint-disable-next-line
      (this.$refs[formName] as any).resetFields();
    }
  }
});
</script>
