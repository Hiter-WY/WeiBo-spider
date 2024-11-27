import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/js/bootstrap";
import VNetworkGraph from "v-network-graph";
import "v-network-graph/lib/style.css";
createApp(App).use(store).use(router).mount("#app").use(VNetworkGraph);
