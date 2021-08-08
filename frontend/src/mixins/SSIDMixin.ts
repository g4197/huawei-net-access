import Vue from "vue";

export interface SSID {
  name: string;
  enable: number;
  connectionMode: string;
  hidEnable: number;
  relativeRadios: number;
  maxUserNumber: number;
  userSeparation: number;
  authMode: string;
  authPskEncryptType: string;
  authSecurityKey: string;
  authSecurityKeyType: string;
  authDot1xEncryptType: string;
  authMacAutoBinding: number;
  id: string | undefined;
}

export interface ServerSideSSID {
  name: string;
  enable: number;
  connection_mode: string;
  hid_enable: number;
  relative_radios: number;
  max_user_number: number;
  user_separation: number;
  auth_mode: string;
  auth_psk_encrypt_type: string;
  auth_security_key: string;
  auth_security_key_type: string;
  auth_dot1x_encrypt_type: string;
  auth_mac_auto_binding: number;
  id: string | undefined;
}

export default Vue.extend({
  methods: {
    serverSideSSIDToSSID(data: Array<ServerSideSSID>): Array<SSID> {
      const ret = [] as Array<SSID>;
      if (data === undefined) return ret;
      for (let i = 0; i < data.length; ++i) {
        ret.push({
          name: data[i].name,
          enable: Number(data[i].enable),
          connectionMode: data[i].connection_mode,
          hidEnable: Number(data[i].hid_enable),
          relativeRadios: Number(data[i].relative_radios),
          maxUserNumber: Number(data[i].max_user_number),
          userSeparation: Number(data[i].user_separation),
          authMode: data[i].auth_mode,
          authPskEncryptType: data[i].auth_psk_encrypt_type,
          authSecurityKey: data[i].auth_security_key,
          authSecurityKeyType: data[i].auth_security_key_type,
          authDot1xEncryptType: data[i].auth_dot1x_encrypt_type,
          authMacAutoBinding: Number(data[i].auth_mac_auto_binding),
          id: data[i].id
        });
      }
      return ret;
    }
  }
});
