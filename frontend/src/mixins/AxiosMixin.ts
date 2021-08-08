import Vue from "vue";
import axios from "axios";

export default Vue.extend({
  name: "AxiosMixin",
  methods: {
    // Get params have no "data" shell, needing to pass.
    axiosGet(linkName: string, operationName: string, getParams: {}) {
      return axios
        .get(this.$router.resolve({ name: linkName }).href, {
          params: getParams
        })
        .catch(err => {
          let text = err.response.data.message;
          if (text === undefined) text = operationName + "失败，未知错误";
          this.$message({
            message: text,
            type: "error"
          });
        });
    },
    axiosGetNoCatch(linkName: string, getParams: {}) {
      return axios.get(this.$router.resolve({ name: linkName }).href, {
        params: getParams
      });
    },
    // post params have "data" shell, therefore only pass real data.
    axiosPost(linkName: string, dataToPost: {}, operationName: string) {
      return axios
        .post(
          this.$router.resolve({ name: linkName }).href,
          { data: dataToPost },
          {
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": this.$cookies.get("csrftoken")
            }
          }
        )
        .catch(err => {
          let text = err.response.data.message;
          if (text === undefined) text = operationName + "失败，未知错误";
          this.$message({
            message: text,
            type: "error"
          });
        });
    },
    axiosPostNoCatch(linkName: string, dataToPost: {}) {
      return axios.post(
        this.$router.resolve({ name: linkName }).href,
        { data: dataToPost },
        {
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": this.$cookies.get("csrftoken")
          }
        }
      );
    }
  }
});
