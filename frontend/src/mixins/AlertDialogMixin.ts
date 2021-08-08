import Vue from "vue";
export default Vue.extend({
  data() {
    return {
      alertDialog: {
        dialogVisible: false,
        text: "",
        confirmText: "",
        cancelText: "",
        onConfirm: () => {
          return;
        },
        onCancel: () => {
          return;
        },
        confirmDisabled: false,
        cancelDisabled: false
      }
    };
  }
});
