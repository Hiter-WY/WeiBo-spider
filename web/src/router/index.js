import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import UserInfoView from "../views/UserInfo.vue";
import KeyWordsView from "../views/KeyWords.vue";
import StaisticsInfoView from "../views/StaisticsInfo.vue";
import UserPortraitsView from "../views/UserPortrait.vue";
import BlogRetransmission from "../views/BlogRetransmission.vue";
const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/userinfo",
    name: "userinfo",
    component: UserInfoView,
  },
  {
    path: "/keywords",
    name: "keywords",
    component: KeyWordsView,
  },
  {
    path: "/",
    name: "staisticsinfo",
    component: StaisticsInfoView,
  },
  {
    path: "/",
    name: "userportraits",
    component: UserPortraitsView,
  },{
    path: "/",
    name: "blogretransmission",
    component: BlogRetransmission,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
