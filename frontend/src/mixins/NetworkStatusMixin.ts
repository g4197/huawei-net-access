import Vue from "vue";

export default Vue.extend({
  data() {
    return {
      networkDemandArr: ["Guest", "Management", "Test"],
      billingMethodArr: ["包年", "包月"],
      stateArr: ["已提交", "已工勘", "已部署", "已完成", "已取消"],
      stepArr: ["提交", "工勘", "部署", "完成"]
    };
  }
});
