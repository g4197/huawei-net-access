<template>
  <el-dialog
    :title="title"
    width="400px"
    :visible.sync="dialogVisible"
    :show-close="false"
    :close-on-click-modal="false"
  >
    <span>{{ text }}</span>
    <span slot="footer" class="dialog-footer">
      <el-button
        round
        id="confirm"
        type="primary"
        @click="onConfirm()"
        :disabled="confirmDisabled"
        >{{ confirmText }}</el-button
      >
      <el-button
        round
        id="cancel"
        @click="onCancel()"
        :disabled="cancelDisabled"
        >{{ cancelText }}</el-button
      >
    </span>
  </el-dialog>
</template>
<script lang="ts">
import Vue from "vue";
export default Vue.extend({
  name: "AlertDialog",
  props: {
    title: {
      type: String,
      default: "提示"
    },
    text: {
      type: String,
      default: ""
    },
    confirmText: {
      type: String,
      default: "确定"
    },
    cancelText: {
      type: String,
      default: "取消"
    },
    onConfirm: {
      type: Function,
      default: () => {
        return;
      }
    },
    onCancel: {
      type: Function,
      default: () => {
        return;
      }
    },
    dialogVisible: {
      type: Boolean,
      default: false
    },
    confirmDisabled: {
      type: Boolean,
      default: false
    },
    cancelDisabled: {
      type: Boolean,
      default: false
    }
  }
});
</script>
