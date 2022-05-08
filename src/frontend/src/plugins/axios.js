import Vue from "vue";

import axios from "axios";
import env from "../../env";

axios.defaults.baseURL = env.API_URL ? `${env.API_URL}` : "/api/v1";
Vue.use(axios);
