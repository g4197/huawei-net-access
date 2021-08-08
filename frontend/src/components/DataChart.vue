<template>
  <div class="text-center chart">
    <line-chart :data="data" area />
  </div>
</template>

<script lang="ts">
import mixins from "vue-typed-mixins";
import AxiosMixin from "@/mixins/AxiosMixin";
import SpeedFlowMixin from "@/mixins/SpeedFlowMixin";

require("@/assets/styles/main.css");

export default mixins(AxiosMixin, SpeedFlowMixin).extend({
  name: "DataChart",
  props: {
    data: {}
  }
});
</script>
