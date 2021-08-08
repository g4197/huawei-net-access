import Vue from "vue";
export default Vue.extend({
  methods: {
    confirm(message: string, thenFunc: Function): void {
      this.$confirm(message, "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "info"
      })
        .then(() => {
          thenFunc();
        })
        .catch(() => {
          return;
        });
    }
  }
});
