<template>
    <ContantBase>
      <h1>{{ keywordTitle }}</h1>
      <div class="input-group">
        <button
          class="btn btn-outline-secondary"
          type="button"
          @click="fetchUserPortrait"
        >
          Get User Portrait
        </button>
      </div>
      <div v-if="userPortrait && userPortrait.data">
        <h3>User Portrait:</h3>
        <!-- 使用 v-html 渲染已转换的 Markdown -->
        <div v-html="renderedMarkdown"></div>
      </div>
      <div v-if="errorMessage" style="color: red">{{ errorMessage }}</div>
    </ContantBase>
  </template>
  
  <script>
  import axios from "axios";
  import ContantBase from "../components/ContantBase.vue";
  import store from "../store/index.js";
  import { mapState } from "vuex";
  import { marked } from "marked";
  
  export default {
    name: "UserPortrait",
    components: {
      ContantBase,
    },
    data() {
      return {
        errorMessage: null,
      };
    },
    computed: {
      ...mapState({
        userPortrait: (state) => state.userPortrait,
      }),
      keywordTitle() {
        return store.state.searchKeyword || "User Portrait";
      },
      // 计算属性，将 userPortrait.data 转换为 HTML
      renderedMarkdown() {
        if (this.userPortrait && this.userPortrait.data) {
          return marked(this.userPortrait.data); // 使用 marked 转换 Markdown 为 HTML
        }
        return "";
      },
    },
    methods: {
      async fetchUserPortrait() {
        this.errorMessage = null;
        try {
          const keyword = store.state.searchKeyword; // 获取 store 中的关键字
          if (!keyword) {
            this.errorMessage = "No keyword found in store.";
            return;
          }
          const response = await axios.post(
            "http://127.0.0.1:5000/api/userportrait",
            { keyword }
          );
          if (response.data.status === "success") {
            // 保存用户画像到 store
            store.commit("setUserPortrait", response.data);
            this.errorMessage = null;
          } else {
            this.errorMessage = response.data.message || "An error occurred";
          }
        } catch (error) {
          this.errorMessage = error.response
            ? error.response.data.message
            : "Server connection error";
        }
      },
    },
  };
  </script>
  
  <style scoped></style>
  