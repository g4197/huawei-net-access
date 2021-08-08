import Vue from "vue";
export default Vue.extend({
  data() {
    return {
      kSpeedFlowUnit: 1000,
      kKB: 1,
      kMB: 1000,
      kGB: 1000000,
      kTB: 1000000000,
      kSpeedLimit: 1000
    };
  },
  methods: {
    speed2Str(speed: number): string {
      if (isNaN(speed)) return "";
      if (speed < this.kMB) {
        return String((speed / this.kKB).toFixed(2)) + "KB/s";
      } else if (speed < this.kGB) {
        return String((speed / this.kMB).toFixed(2)) + "MB/s";
      } else {
        return String((speed / this.kGB).toFixed(2)) + "GB/s";
      }
    },
    flow2Str(flow: number): string {
      if (isNaN(flow)) return "";
      if (flow < this.kMB) {
        return String((flow / this.kKB).toFixed(2)) + "KB";
      } else if (flow < this.kGB) {
        return String((flow / this.kMB).toFixed(2)) + "MB";
      } else if (flow < this.kTB) {
        return String((flow / this.kGB).toFixed(2)) + "GB";
      } else {
        return String((flow / this.kTB).toFixed(2)) + "TB";
      }
    }
  }
});
