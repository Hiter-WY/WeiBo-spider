<template>
  <ContantBase>
    <h1 class="gradient-text">User Info</h1>
    <div>
      <div class="InputContainer">
        <input v-model="keyword" type="text" class="input" placeholder="Enter username to search"
          @keyup.enter="fetchUserInfo" />
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
              <button style="width: 80px" type="button" @click="classifyInfo(index)" class="btn btn-secondary">
                Predict
              </button>
            </td>
            <td>
              <button style="width: 145px" type="button" @click="retransmission(index)" class="btn btn-secondary">
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
// import { json } from "d3";

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
        let weibonumber = parseInt(localStorage.getItem("weibonumber"), 10);
        let usernumber = parseInt(localStorage.getItem("usernumber"), 10);
          // 如果 number 不存在，初始化为 0 并存储到 localStorage
        if (isNaN(weibonumber)) {
          weibonumber = 0;
          store.commit("setNumber", 0);
          localStorage.setItem("weibonumber", 0);
        } else {
          // 如果存在，初始化到 Vuex 中
          store.commit("setNumber", weibonumber);
        }
        if (isNaN(usernumber)) {
          usernumber = 0;
          store.commit("setusernumber", 0);
          localStorage.setItem("usernumber", 0);
        } else {
          store.commit("setusernumber", usernumber);
        }
        const response = await axios.post(
          "http://127.0.0.1:5000/api/userinfo",
          { keyword: this.keyword }
        );
        if (response.data.status === "success") {
          store.commit("setUserInfo", response.data.data);
          store.commit("setSearchKeyword", this.keyword);
          store.commit("updateNubmer", response.data.data.length);
          store.commit("updateusernumber", 1);
          // 获取更新后的 number
          const updatedWeibonumber = store.state.weibonumber;
          const updatedusernumber = store.state.usernumber;
          // 保存到 localStorage
          localStorage.setItem("weibonumber", updatedWeibonumber);
          localStorage.setItem("usernumber", updatedusernumber);
          console.log("Updated weibonumber:", updatedWeibonumber);
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
      try{
        const response = await axios.post("http://127.0.0.1:5000/api/databasenumber")
        if(response.data.status === "success"){
          console.log(response.data.data);
          localStorage.setItem("databasecount", response.data.data);
        } else {
          this.errorMessage = response.data.message || "An error occurred";
        }
      }catch (error) {
        this.errorMessage = error.response
          ? error.response.data.message
          : "Server connection error";
      }
    },
    async classifyInfo(index) {
      try {
        let classifycount = parseInt(localStorage.getItem("classifycount"), 10);
        if(isNaN(classifycount)){
          classifycount = 0;
        }
        const response = await axios.post(
          "http://127.0.0.1:5000/api/classfiy",
          { text: [this.userInfo[index].cleaned_text] }
        );
        if (response.data.status === "success") {
          localStorage.setItem("classifycount", classifycount+1);
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
        let classifycount = parseInt(localStorage.getItem("classifycount"), 10);
        if(isNaN(classifycount)){
          classifycount = 0;
        }
        var textList = this.userInfo.map((info) => info.cleaned_text);
        const response = await axios.post(
          "http://127.0.0.1:5000/api/classfiy",
          { text: textList }
        );
        if (response.data.status === "success") {
          store.commit("setTextInfo", response.data.data);
          const updatedclassifycount = store.state.classifycount;
          localStorage.setItem("classifycount", updatedclassifycount + response.data.data.length);
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

<style scoped>
.gradient-text {
  font-size: 3rem;
  font-weight: bold;
  background: linear-gradient(45deg, #ff7e5f, #feb47b);
  /* 渐变色定义 */
  background-clip: text;
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