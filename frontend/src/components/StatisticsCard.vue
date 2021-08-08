<template>
  <el-card>
    <div slot="header" style="font-size: 24px">
      <span>统计信息</span>
    </div>
    <el-row class="site-row">
      <el-card shadow="none">
        <el-row class="site-row">
          <div class="statistics-subheader">在线人数</div>
          <el-button-group class="text-right">
            <el-button
              size="mini"
              v-for="item in statisticsModeArr"
              :key="item.index"
              :autofocus="item.index === 0"
              @click="getOnlineData(item.value)"
            >
              {{ item.label }}
            </el-button>
          </el-button-group>
        </el-row>
        <DataChart :data="onlineData" />
      </el-card>
    </el-row>
    <el-row class="site-row">
      <el-card shadow="none">
        <el-row class="site-row">
          <div class="statistics-subheader">网络</div>
          <el-button-group class="text-right">
            <el-button
              size="mini"
              v-for="item in statisticsModeArr"
              :key="item.index"
              :autofocus="item.index === 0"
              @click="getSpeedData(item.value)"
            >
              {{ item.label }}
            </el-button>
          </el-button-group>
        </el-row>
        <DataChart :data="speedData" />
      </el-card>
    </el-row>
    <el-row class="site-row">
      <el-card shadow="none">
        <el-row class="site-row">
          <div class="statistics-subheader">流量</div>
          <el-button-group class="text-right">
            <el-button
              size="mini"
              v-for="item in statisticsModeArr"
              :key="item.index"
              :autofocus="item.index === 0"
              @click="getFlowData(item.value)"
            >
              {{ item.label }}
            </el-button>
          </el-button-group>
        </el-row>
        <DataChart :data="flowData" />
      </el-card>
    </el-row>
  </el-card>
</template>
<script lang="ts">
import DataChart from "@/components/DataChart.vue";
import mixins from "vue-typed-mixins";
import AxiosMixin from "@/mixins/AxiosMixin";
import { StatisticsMode } from "@/enums/enums";

interface ChartData {
  name: string;
  data: Array<{
    label: string;
    value: number;
  }>;
}

interface ServerSideChartDataItem {
  time: number;
  value: number;
}

interface ServerSideChartData {
  online: Array<ServerSideChartDataItem>;
  upSpeed: Array<ServerSideChartDataItem>;
  downSpeed: Array<ServerSideChartDataItem>;
  flow: Array<ServerSideChartDataItem>;
}

export default mixins(AxiosMixin).extend({
  name: "StatisticsCard",
  components: {
    DataChart
  },
  mounted() {
    this.getStatistics();
  },
  data() {
    return {
      speedData: [] as Array<ChartData>,
      flowData: [] as Array<ChartData>,
      onlineData: [] as Array<ChartData>,
      serverSideData: {} as ServerSideChartData,
      statisticsModeArr: [
        {
          label: "1小时",
          value: StatisticsMode.kOneHour
        },
        {
          label: "1天",
          value: StatisticsMode.kOneDay
        },
        {
          label: "1周",
          value: StatisticsMode.kOneWeek
        },
        {
          label: "1月",
          value: StatisticsMode.kOneMonth
        }
      ]
    };
  },
  props: {
    siteId: String,
    changeLoadState: Function
  },
  methods: {
    getStatistics(): void {
      this.axiosGet("ApiStatisticsInfo", "获取统计信息", {
        id: this.siteId
      }).then(res => {
        if (typeof res !== "undefined") {
          const data = res.data.data as ServerSideChartData;
          this.serverSideData = data;
          this.getOnlineData(StatisticsMode.kOneHour);
          this.getSpeedData(StatisticsMode.kOneHour);
          this.getFlowData(StatisticsMode.kOneHour);
        }
      });
    },
    timestampToTime(
      timestamp: number,
      needDay: boolean,
      needMinute: boolean
    ): string {
      // assume timestamp is a number with 10 digits
      const date = new Date(timestamp * 1000);
      const arr = [] as Array<string>;
      if (needDay) arr.push([date.getMonth() + 1, date.getDate()].join("."));
      let h = String(date.getHours());
      let m = String(date.getMinutes());
      if (Number(h) < 10) h = "0" + h;
      if (Number(m) < 10) m = "0" + m;
      if (needMinute) arr.push([h, m].join(":"));
      return arr.join(" ");
    },
    serverSideChartDataToChartData(
      data: Array<ServerSideChartDataItem>,
      name: string,
      mode: StatisticsMode
    ): ChartData {
      const ret = {
        name: "",
        data: []
      } as ChartData;
      ret.name = name;
      let needDay = false,
        needMinute = false;
      if (mode === StatisticsMode.kOneHour || mode === StatisticsMode.kOneDay) {
        needDay = false;
        needMinute = true;
      } else if (
        mode === StatisticsMode.kOneWeek ||
        mode === StatisticsMode.kOneMonth
      ) {
        needDay = true;
        needMinute = false;
      }
      const curTime = new Date();
      const earliestTime = curTime;
      if (mode === StatisticsMode.kOneHour)
        earliestTime.setHours(curTime.getHours() - 1);
      else if (mode === StatisticsMode.kOneDay)
        earliestTime.setDate(curTime.getDate() - 1);
      else if (mode === StatisticsMode.kOneWeek)
        earliestTime.setDate(curTime.getDate() - 7);
      else if (mode === StatisticsMode.kOneMonth)
        earliestTime.setMonth(curTime.getMonth() - 1);
      const dataMap = new Map<
        string,
        {
          sum: number;
          count: number;
        }
      >();
      const earliestTimestamp = Math.round(earliestTime.getTime() / 1000);
      for (let i = 0; i < data.length; ++i) {
        if (data[i].time < earliestTimestamp) continue;
        const label = this.timestampToTime(data[i].time, needDay, needMinute);
        const value = data[i].value;
        const val = dataMap.get(label);
        if (typeof val !== "undefined") {
          dataMap.set(label, {
            sum: val.sum + value,
            count: val.count + 1
          });
        } else {
          dataMap.set(label, {
            sum: value,
            count: 1
          });
        }
      }
      dataMap.forEach((value, key) => {
        ret.data.push({
          label: key,
          value: Math.round(value.sum / value.count)
        });
      });
      return ret;
    },
    getOnlineData(mode: StatisticsMode) {
      this.onlineData = [];
      this.onlineData.push(
        this.serverSideChartDataToChartData(
          this.serverSideData.online,
          "在线人数(人)",
          mode
        )
      );
    },
    getFlowData(mode: StatisticsMode) {
      this.flowData = [];
      this.flowData.push(
        this.serverSideChartDataToChartData(
          this.serverSideData.flow,
          "流量 MB",
          mode
        )
      );
    },
    getSpeedData(mode: StatisticsMode) {
      this.speedData = [];
      this.speedData.push(
        this.serverSideChartDataToChartData(
          this.serverSideData.upSpeed,
          "上行 KB/s",
          mode
        )
      );
      this.speedData.push(
        this.serverSideChartDataToChartData(
          this.serverSideData.downSpeed,
          "下行 KB/s",
          mode
        )
      );
    }
  }
});
</script>
