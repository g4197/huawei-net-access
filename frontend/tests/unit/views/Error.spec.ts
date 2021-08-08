import { shallowMount } from "@vue/test-utils";
import Vue from "vue";
import ElementUI from "element-ui";
import Error from "@/views/Error.vue";

Vue.use(ElementUI);

describe("Error.vue", () => {
  it("Renders 404 page", () => {
    const wrapper = shallowMount(Error);
    expect(wrapper.find(".msg").exists()).toBe(true);
    expect(wrapper.find("#back").exists()).toBe(true);
  });
  it("Func: returnToFrontpage", () => {
    const wrapper = shallowMount(Error);
    wrapper.vm.$emit("returnFrontPage");
    // eslint-disable-next-line
    expect(wrapper.emitted().returnFrontPage as any).toBeTruthy();
  });
});
