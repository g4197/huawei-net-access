<template>
  <el-card style="max-width: 1500px; min-height: 85vh" class="text-center">
    <SSIDDialog
      :SSIDDataToPass="DialogSSIDData"
      :disabled="true"
      :visible.sync="SSIDDialogVisible"
      :hide="hide"
      :onComplete="hide"
    />
    <div slot="header" style="font-size: 24px">
      <span>SSID信息</span>
    </div>
    <el-row
      :gutter="20"
      style="
        min-height: calc(85vh - 100px);
        display: flex;
        flex-wrap: wrap;
        align-content: flex-start;
      "
    >
      <el-col :md="24" :lg="12" :xl="8" v-for="item in SSID" :key="item.index">
        <el-card
          shadow="none"
          style="
            border: 1px solid #dcdfe6;
            margin-top: 20px;
            margin-bottom: 20px;
          "
        >
          <el-row>
            <span class="card-title">{{ item.name }}</span>
          </el-row>
          <el-divider style="margin: 16px 0"></el-divider>
          <el-row>
            <span class="card-content"
              >最大用户数：{{ item.maxUserNumber }}</span
            >
          </el-row>
          <el-row>
            <span class="card-content"
              >隐藏SSID：{{ item.hidEnable ? "是" : "否" }}</span
            >
          </el-row>
          <el-row>
            <span class="card-content">加密方式：{{ item.authMode }}</span>
          </el-row>
          <el-row type="flex" style="margin-top: 36px; align-items: stretch">
            <el-col :span="12" style="display: flex; align-items: center">
              <template v-if="item.enable">
                <span class="card-content">
                  <span class="card-dot" style="background-color: green"></span
                  >运行中</span
                >
              </template>
              <template v-else>
                <span class="card-content">
                  <span class="card-dot" style="background-color: grey"></span
                  >已停用</span
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
                    @click="viewSSIDInfo(item)"
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
  </el-card>
</template>
<script lang="ts">
import mixins from "vue-typed-mixins";
import AxiosMixin from "@/mixins/AxiosMixin";
import SSIDMixin, { SSID } from "@/mixins/SSIDMixin";
import SSIDDialog from "@/components/SSIDDialog.vue";
export default mixins(AxiosMixin, SSIDMixin).extend({
  name: "SSIDCard",
  components: {
    SSIDDialog
  },
  props: {
    siteId: String,
    changeLoadState: Function
  },
  data() {
    return {
      DialogSSIDData: {} as SSID,
      SSID: [] as Array<SSID>,
      SSIDDialogVisible: false
    };
  },
  mounted() {
    this.getSSIDInfo();
  },
  methods: {
    hide(): void {
      this.SSIDDialogVisible = false;
    },
    viewSSIDInfo(ssid: SSID): void {
      this.DialogSSIDData = ssid;
      this.SSIDDialogVisible = true;
    },
    getSSIDInfo(): void {
      this.changeLoadState(true);
      this.axiosGetNoCatch("ApiSSIDInfo", { id: this.siteId })
        .then(res => {
          // eslint-disable-next-line
          this.SSID = this.serverSideSSIDToSSID(res.data.data.ssid_list);
          this.changeLoadState(false);
        })
        .catch(err => {
          let text = err.response.data.message;
          if (text === undefined) text = "获取SSID信息失败，未知错误";
          this.$message({
            message: text,
            type: "error"
          });
          this.changeLoadState(false);
        });
    }
  }
});
</script>
