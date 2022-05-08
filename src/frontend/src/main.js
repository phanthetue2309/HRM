import Vue from "vue";
import Vuelidate from "vuelidate";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import ElementUI from "element-ui";
import locale from "element-ui/lib/locale/lang/en";
import "./assets/css/index.css";
import "./mixin";
import "./plugins/axios";

import VueCroppie from "vue-croppie";

import {library} from "@fortawesome/fontawesome-svg-core";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import {fas} from "@fortawesome/free-solid-svg-icons";
import env from "../env";

import Toast from "vue-toastification";
import VueTextareaAutosize from "vue-textarea-autosize";
import JsonExcel from "vue-json-excel";
import VueApexCharts from "vue-apexcharts";
import VueDragscroll from "vue-dragscroll";
import ConfirmHeaderProbation from "./pages/probationDetail/importExcel/confirmHeaderProbation"
import ConfirmTemplateProbation from "./pages/probationDetail/importExcel/confirmTemplateProbation"
import ConfirmAssessor from "./pages/probationDetail/importExcel/confirmAssessor";

import GAuth from "vue-google-oauth2";

const scope = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
].join(" ");
Vue.component("apexchart", VueApexCharts);
Vue.component("downloadExcel", JsonExcel);
Vue.component("font-awesome-icon", FontAwesomeIcon);
Vue.component("ConfirmHeaderProbation", ConfirmHeaderProbation);
Vue.component("ConfirmTemplateProbation", ConfirmTemplateProbation);
Vue.component("ConfirmAssessor", ConfirmAssessor);

Vue.use(Toast);
Vue.use(VueApexCharts);
Vue.use(VueDragscroll);

Vue.use(Vuelidate);
Vue.use(VueTextareaAutosize);

Vue.use(VueCroppie);

library.add(fas);

Vue.config.productionTip = false;
Vue.use(ElementUI, {locale});

const gauthOption = {
    clientId: env.VUE_APP_GOOGLE_CLIENT_ID,
    scope,
    prompt: "select_account",
    access_type: "offline",
    fetch_basic_profile: true,
};
Vue.use(GAuth, gauthOption);
new Vue({
    router,
    store,
    render: (h) => h(App),
}).$mount("#app");
