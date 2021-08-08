import Vue from "vue";
import axios from "axios";

export default Vue.extend({
  created(): void {
    this.getCsrfToken();
  },
  methods: {
    getCsrfToken(): void {
      axios.get(this.$router.resolve({ name: "ApiCsrf" }).href);
    }
  }
});
