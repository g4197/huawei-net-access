<template>
  <el-dialog
    :title="title"
    :visible.sync="visible"
    :close-on-click-modal="false"
    :show-close="false"
    v-on:open="passSSIDData()"
  >
    <div class="text-center relative-w-80">
      <el-tabs v-model="curActive">
        <el-tab-pane label="基本设置" name="BasicSettings">
          <el-form
            ref="basicForm"
            :model="SSIDData"
            label-width="100px"
            :disabled="disabled"
          >
            <el-form-item label="SSID名称">
              <el-input v-model="SSIDData.name"></el-input>
            </el-form-item>
            <el-form-item label="是否启用">
              <el-select v-model="SSIDData.enable" class="w-100">
                <el-option
                  v-for="item in booleanOptions"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                ></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="连接方式">
              <el-select v-model="SSIDData.connectionMode" class="w-100">
                <el-option
                  v-for="item in connectionModeOptions"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                ></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="隐藏SSID">
              <el-select v-model="SSIDData.hidEnable" class="w-100">
                <el-option
                  v-for="item in booleanOptions"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                ></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="射频类型">
              <el-select v-model="SSIDData.relativeRadios" class="w-100">
                <el-option
                  v-for="item in relativeRadiosOptions"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                ></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="最大用户数">
              <el-input-number
                class="w-100"
                :min="1"
                :max="512"
                controls-position="right"
                v-model="SSIDData.maxUserNumber"
              ></el-input-number>
            </el-form-item>
            <el-form-item label="用户隔离">
              <el-select v-model="SSIDData.userSeparation" class="w-100">
                <el-option
                  v-for="item in booleanOptions"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="安全设置" name="SecuritySettings">
          <el-form
            ref="securityForm"
            :model="SSIDData"
            label-width="100px"
            :disabled="disabled"
          >
            <el-form-item label="认证模式">
              <el-select v-model="SSIDData.authMode" class="w-100">
                <el-option
                  v-for="item in authModeOptions"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                ></el-option>
              </el-select>
            </el-form-item>
            <el-form-item v-if="isPSKOrPPSK()" label="加密模式">
              <el-select v-model="SSIDData.authPskEncryptType" class="w-100">
                <el-option
                  v-for="item in authPskEncryptTypeOptions"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                ></el-option>
              </el-select>
            </el-form-item>
            <el-form-item v-if="isDot1x()" label="加密模式">
              <el-select v-model="SSIDData.authDot1xEncryptType" class="w-100">
                <el-option
                  v-for="item in authDot1xEncryptTypeOptions"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                ></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="PSK密钥" v-if="isPSK()">
              <el-input
                v-model="SSIDData.authSecurityKey"
                show-password
              ></el-input>
            </el-form-item>
            <el-form-item label="加密方法" v-if="isWPA2()">
              <el-select v-model="SSIDData.authSecurityKeyType" class="w-100">
                <el-option
                  v-for="item in authSecurityKeyTypeOptions"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                ></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="MAC自动绑定">
              <el-select v-model="SSIDData.authMacAutoBinding" class="w-100">
                <el-option
                  v-for="item in booleanOptions"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </div>
    <el-button type="primary" @click="submitData()">完成</el-button>
    <el-button @click="onCancel()">取消</el-button>
  </el-dialog>
</template>
<script lang="ts">
import mixins from "vue-typed-mixins";
import SSIDMixin, { SSID } from "@/mixins/SSIDMixin";
require("@/assets/styles/main.css");

export default mixins(SSIDMixin).extend({
  name: "SSIDDialog",
  data() {
    return {
      curActive: "BasicSettings",
      SSIDData: {} as SSID,
      title: "SSID编辑",
      booleanOptions: [
        {
          value: 0,
          label: "否"
        },
        {
          value: 1,
          label: "是"
        }
      ],
      connectionModeOptions: [
        {
          value: "bridge",
          label: "桥接模式"
        },
        {
          value: "nat",
          label: "NAT模式"
        }
      ],
      relativeRadiosOptions: [
        {
          value: 1,
          label: "2.4G(wlan-radio 0/0/0)"
        },
        {
          value: 2,
          label: "5G(wlan-radio 0/0/1)"
        },
        {
          value: 3,
          label: "2.4G(wlan-radio 0/0/0)&5G(wlan-radio 0/0/1)"
        },
        {
          value: 4,
          label: "5G(wlan-radio 0/0/2)"
        },
        {
          value: 5,
          label: "2.4G(wlan-radio 0/0/0)&5G(wlan-radio 0/0/2)"
        },
        {
          value: 6,
          label: "5G(wlan-radio 0/0/1)&5G(wlan-radio 0/0/2)"
        },
        {
          value: 7,
          label:
            "2.4G(wlan-radio 0/0/0)&5G(wlan-radio 0/0/1)&5G(wlan-radio 0/0/2)"
        }
      ],
      authModeOptions: [
        {
          value: "open",
          label: "open"
        },
        {
          value: "psk",
          label: "PSK"
        },
        {
          value: "ppsk",
          label: "PPSK"
        },
        {
          value: "dot1x",
          label: "dot1x"
        },
        {
          value: "mac",
          label: "mac"
        }
      ],
      authPskEncryptTypeOptions: [
        {
          value: "wpa1AndWpa2",
          label: "WPA+WPA2"
        },
        {
          value: "wpa2",
          label: "WPA2"
        },
        {
          value: "wep",
          label: "WEP"
        }
      ],
      authDot1xEncryptTypeOptions: [
        {
          value: "wpa1AndWpa2",
          label: "WPA+WPA2"
        },
        {
          value: "wpa2",
          label: "WPA2"
        }
      ],
      authSecurityKeyTypeOptions: [
        {
          value: "AES",
          label: "AES"
        },
        {
          value: "AES-TKIP",
          label: "AES-TKIP"
        },
        {
          value: "TKIP",
          label: "TKIP"
        }
      ]
    };
  },
  props: {
    SSIDDataToPass: {},
    visible: Boolean,
    onComplete: Function,
    hide: Function,
    disabled: Boolean
  },
  methods: {
    isPSK(): boolean {
      return this.SSIDData.authMode === "psk";
    },
    isPSKOrPPSK(): boolean {
      return this.isPSK() || this.SSIDData.authMode === "ppsk";
    },
    isDot1x(): boolean {
      return this.SSIDData.authMode === "dot1x";
    },
    isWPA2(): boolean {
      return this.SSIDData.authPskEncryptType === "wpa2";
    },
    submitData(): void {
      // eslint-disable-next-line
      this.onComplete(this.SSIDData);
    },
    onCancel(): void {
      // eslint-disable-next-line
      this.hide();
    },
    passSSIDData(): void {
      this.SSIDData = this.SSIDDataToPass as SSID;
      this.curActive = "BasicSettings";
      this.title = this.disabled ? "SSID信息" : "SSID编辑";
    }
  },
  watch: {
    disabled: function(newVal: boolean): void {
      this.title = newVal ? "SSID信息" : "SSID编辑";
    }
  }
});
</script>
