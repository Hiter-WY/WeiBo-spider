<template>
  <ContantBase>
    <h1>User Info</h1>
    <div>
      <div class="input-group">
        <input
          v-model="keyword"
          type="text"
          class="form-control"
          placeholder="Enter username"
        />
        <button
          class="btn btn-outline-secondary"
          type="button"
          @click="fetchUserInfo"
        >
          Search User Info
        </button>
        <button
          class="btn btn-outline-secondary"
          @click="classifyMultiInfo"
          type="button"
        >
          PredictAll
        </button>
      </div>

      <table class="table" v-if="userInfo && userInfo.length">
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">Time</th>
            <th scope="col" style="text-align: center">Text</th>
            <th scope="col">Classify</th>
            <th scope="col">Predict</th>
            <th scope="col">Retransmission</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(info, index) in userInfo" :key="index">
            <th scope="row">{{ index + 1 }}</th>
            <td>{{ info.created_time }}</td>
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
            <td>
              <button
                style="width: 145px"
                type="button"
                @click="retransmission(index)"
                class="btn btn-secondary"
              >
                Retransmission
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
  name: "UserInfo",
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
      userInfo: (state) => state.userInfo,
      textInfo: (state) => state.textInfo,
    }),
  },
  methods: {
    async fetchUserInfo() {
      this.errorMessage = null;
      store.commit("clearUserInfo");
      store.commit("clearTextInfo");

      if (!this.keyword) {
        this.errorMessage = "Keyword is required";
        return;
      }
      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/api/userinfo",
          { keyword: this.keyword }
        );
        if (response.data.status === "success") {
          store.commit("setUserInfo", response.data.data);
          store.commit("setSearchKeyword", this.keyword);
          console.log(store.state.searchKeyword);
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
          { text: [this.userInfo[index].cleaned_text] }
        );
        if (response.data.status === "success") {
          store.commit("updateTextInfo", {
            index,
            value: response.data.data[0],
          });
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
        var textList = this.userInfo.map((info) => info.cleaned_text);
        const response = await axios.post(
          "http://127.0.0.1:5000/api/classfiy",
          { text: textList }
        );
        if (response.data.status === "success") {
          store.commit("setTextInfo", response.data.data);
          response.data.data.forEach((text) => {
            store.commit("increment", text);
          });
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
    async retransmission(index) {
      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/api/retransmission",
          { mid: [this.userInfo[index].mid] },
          console.log(this.userInfo[index].mid)
        );
        if (response.data.status === "success") {
          // 成功时，将后端返回的内容打印到控制台
          store.commit("setRetransmissionData", response.data.data);
          console.log("Retransmission data:", response.data.data);
          this.errorMessage = null;
        } else {
          // 错误信息显示
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
    if (store.state.userInfo && store.state.userInfo.length > 0) {
      store.commit("setUserInfo", store.state.userInfo);
      store.commit("setTextInfo", store.state.textInfo);
    }
  },
};
</script>

<style scoped></style>
