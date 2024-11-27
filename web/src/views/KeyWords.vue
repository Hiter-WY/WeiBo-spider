<template>
  <ContantBase>
    <h1>Keyword Info</h1>
    <div>
      <div class="input-group">
        <input
          v-model="keyword"
          type="text"
          class="form-control"
          placeholder="Enter keyword"
        />
        <button
          class="btn btn-outline-secondary"
          type="button"
          @click="fetchKeywordInfo"
        >
          Search Keyword Info
        </button>
        <button
          class="btn btn-outline-secondary"
          @click="classifyMultiInfo"
          type="button"
        >
          PredictAll
        </button>
      </div>

      <table class="table" v-if="keywordInfo && keywordInfo.length">
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">Username</th>
            <th scope="col" style="text-align: center">Text</th>
            <th scope="col">Classify</th>
            <th scope="col">Predict</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(info, index) in keywordInfo" :key="index">
            <th scope="row">{{ index + 1 }}</th>
            <td>{{ info.screen_name }}</td>
            <td>{{ info.cleaned_text }}</td>
            <td>{{ textInfo[index] }}</td>
            <td>
              <button
                style="width: 80px"
                type="button"
                @click="classifyInfo(index)"
                class="btn btn-secondary"
              >
                Predict
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="errorMessage" style="color: red">{{ errorMessage }}</div>
    </div>
  </ContantBase>
</template>

<script>
import axios from "axios";
import ContantBase from "../components/ContantBase.vue";
import store from "../store/index.js";
import { mapState } from "vuex";

export default {
  name: "KeywordInfo",
  components: {
    ContantBase,
  },
  data() {
    return {
      keyword: "",
      errorMessage: null,
    };
  },
  computed: {
    ...mapState({
      keywordInfo: (state) => state.keywordInfo,
      textInfo: (state) => state.keywordTextInfo,
    }),
  },
  methods: {
    async fetchKeywordInfo() {
      this.errorMessage = null;
      store.commit("clearKeywordInfo");
      store.commit("clearKeywordTextInfo");

      if (!this.keyword) {
        this.errorMessage = "Keyword is required";
        return;
      }
      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/api/keywordsinfo", // 修改后的API路由
          { keyword: this.keyword }
        );
        if (response.data.status === "success") {
          store.commit("setKeywordInfo", response.data.data);
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
    async classifyInfo(index) {
      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/api/classfiy",
          { text: [this.keywordInfo[index].cleaned_text] }
        );
        if (response.data.status === "success") {
          store.commit("updateKeywordTextInfo", {
            index,
            value: response.data.data[0],
          });
          console.log(
            "Updated textInfo at index:",
            index,
            "with value:",
            response.data.data[0]
          );
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
    async classifyMultiInfo() {
      try {
        var textList = this.keywordInfo.map((info) => info.cleaned_text);
        const response = await axios.post(
          "http://127.0.0.1:5000/api/classfiy",
          { text: textList }
        );
        if (response.data.status === "success") {
          store.commit("setKeywordTextInfo", response.data.data);
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
  mounted() {
    if (store.state.keywordInfo && store.state.keywordInfo.length > 0) {
      store.commit("setKeywordInfo", store.state.keywordInfo);
      store.commit("setKeywordTextInfo", store.state.keywordTextInfo);
    }
  },
};
</script>

<style scoped></style>
