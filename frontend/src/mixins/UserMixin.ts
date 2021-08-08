import mixins from "vue-typed-mixins";
import AxiosMixin from "@/mixins/AxiosMixin";
import { UserPrivilege } from "@/enums/enums";

export interface User {
  username: string;
  email: string;
  name: string;
  telephone: string;
  address: string;
  id: number;
  privilege: UserPrivilege;
}

export default mixins(AxiosMixin).extend({
  data() {
    return {
      user: {
        username: "",
        email: "",
        name: "",
        telephone: "",
        address: "",
        id: 0,
        privilege: UserPrivilege.kCustomer
      },
      privilegeArr: [
        {
          value: UserPrivilege.kCustomer,
          label: "用户"
        },
        {
          value: UserPrivilege.kNetworkEngineer,
          label: "网络工程师"
        },
        {
          value: UserPrivilege.kOperationEngineer,
          label: "运营工程师"
        },
        {
          value: UserPrivilege.kAdmin,
          label: "管理员"
        }
      ],
      pathNotNeedAuth: [
        this.$router.resolve({ name: "Register" }).href,
        this.$router.resolve({ name: "Login" }).href,
        this.$router.resolve({ name: "Home" }).href
      ]
    };
  },
  created(): void {
    setTimeout(this.getUserProfile, 200);
  },
  methods: {
    getUserProfile(): void {
      this.axiosGetNoCatch("ApiUserProfile", {})
        .then(res => {
          this.user = res.data.data.userprofile;
          if (
            this.$router.currentRoute.path ===
              this.$router.resolve({ name: "Login" }).href ||
            this.$router.currentRoute.path ===
              this.$router.resolve({ name: "Register" }).href
          ) {
            this.$router.push({ name: "OrderBoard" });
          }
        })
        .catch(() => {
          this.user = {
            username: "",
            email: "",
            name: "",
            telephone: "",
            address: "",
            id: 0,
            privilege: UserPrivilege.kCustomer
          };
          if (!this.pathNotNeedAuth.includes(this.$router.currentRoute.path)) {
            this.$router.push({ name: "Login" });
          }
        });
    }
  }
});
