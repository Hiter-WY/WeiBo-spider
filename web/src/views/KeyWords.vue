<template>
  <ContantBase>
    <h1 class="gradient-text">Keyword Info</h1>
    <div>
      <div class="InputContainer">
        <input v-model="keyword" type="text" class="input" placeholder="Enter keyword to search"
          @keyup.enter="fetchKeywordInfo" />
          <label for="input" class="labelforsearch">
          <svg viewBox="0 0 512 512" class="searchIcon">
            <path
              d="M416 208c0 45.9-14.9 88.3-40 122.7L502.6 457.4c12.5 12.5 12.5 32.8 0 45.3s-32.8 12.5-45.3 0L330.7 376c-34.4 25.2-76.8 40-122.7 40C93.1 416 0 322.9 0 208S93.1 0 208 0S416 93.1 416 208zM208 352a144 144 0 1 0 0-288 144 144 0 1 0 0 288z">
            </path>
          </svg>
        </label>
        <button class="predictButton" type="button" @click="classifyMultiInfo" title="Predict All">
          <img src="@/assets/Predictions.png" alt="Predict" class="predictIcon" />
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
              <button style="width: 80px" type="button" @click="classifyInfo(index)" class="btn btn-secondary">
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
        let keywordnumber = parseInt(localStorage.getItem("keywordnumber"), 10);
        if (isNaN(keywordnumber)) {
          keywordnumber = 0;
          store.commit("setkeywordnumber", 0);
          localStorage.setItem("keywordnumber", 0);
        } else {
          store.commit("setkeywordnumber", keywordnumber);
        }
        const response = await axios.post(
          "http://127.0.0.1:5000/api/keywordsinfo", // 修改后的API路由
          { keyword: this.keyword }
        );
        if (response.data.status === "success") {
          store.commit("setKeywordInfo", response.data.data);
          const keywordcount = response.data.data.length;
          store.commit("updatekeywordnumber", keywordcount);
          localStorage.setItem("keywordnumber", store.state.keywordnumber);
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

<style scoped>
.gradient-text {
  font-size: 3rem;
  font-weight: bold;
  background: linear-gradient(45deg, #ff7e5f, #feb47b);
  /* 渐变色定义 */
  -webkit-background-clip: text;
  /* 让渐变色应用于文本 */
  color: transparent;
  /* 让文本颜色透明，显示渐变 */
  text-align: center;
  font-family: Arial, sans-serif;
}
.InputContainer {
  display: flex;
  align-items: center;
  background-color: rgb(255, 255, 255);
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  /* 增强外部阴影效果 */
  padding: 10px;
  /* 调整内边距 */
  width: 400px;
  /* 设置一个合适的宽度 */
  margin: 20px auto;
  /* 增加外边距并居中 */
}

.input {
  flex-grow: 1;
  height: 36px;
  /* 设置一个合适的高度 */
  border: none;
  /* 去除内部边框 */
  border-radius: 5px;
  /* 圆角边框 */
  outline: none;
  font-size: 1em;
  /* 调整字体大小 */
  padding: 0 10px;
  /* 调整内边距 */
  margin-right: 10px;
  /* 与按钮之间的间距 */
  box-shadow: none;
  /* 去除内部阴影 */
  transition: box-shadow 0.3s;
  /* 过渡效果 */
}

.input:focus {
  box-shadow: none;
  /* 聚焦时不显示阴影 */
}

.labelforsearch {
    cursor: text;
    padding: 0px 12px;
  }

  .searchIcon {
    width: 20px;
  }

  .searchIcon path {
  fill: #cccccc; /* 浅灰色 */
}

.predictButton {
  width: 40px;
  /* 根据图片大小调整宽度 */
  padding: 0;
  border: none;
  background-color: transparent;
  height: 36px;
  /* 与输入框高度一致 */
  cursor: pointer;
  transition-duration: .3s;
  overflow: hidden;
  /* 确保图片不会超出按钮边界 */
}

.predictButton:hover {
  background-color: rgb(255, 230, 230);
  transition-duration: .3s;
}

.predictIcon {
  width: 100%;
  height: auto;
  pointer-events: none;
  /* 允许点击事件传递到按钮 */
}
</style>
