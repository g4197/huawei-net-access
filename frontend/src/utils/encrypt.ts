import md5 from "js-md5";

export function encrypt(password: string): string {
  return md5(password);
}
