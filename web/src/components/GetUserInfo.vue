<template>
  <div class="user-info">
    <el-input
      v-model="keyword"
      placeholder="Enter keyword"
      class="input"
    ></el-input>
    <el-button type="primary" @click="fetchUserInfo"
      >Search User Info</el-button
    >

    <el-table v-if="userInfo" :data="userInfo" style="width: 100%">
      <el-table-column prop="username" label="Username" width="180" />
      <el-table-column prop="data" label="User Data" />
    </el-table>

    <el-alert v-if="errorMessage" :title="errorMessage" type="error" />
  </div>
</template>

<script>
import axios from "axios";
import { ElMessage } from "element-plus";

export default {
  name: "GetUserInfo",
  data() {
    return {
      keyword: "",
      userInfo: null,
      errorMessage: null,
    };
  },
  methods: {
    async fetchUserInfo() {
      if (!this.keyword) {
        ElMessage.error("Keyword is required");
        return;
      }
      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/api/userinfo",
          { keyword: this.keyword }
        );
        if (response.data.status === "success") {
          this.userInfo = response.data.data;
          this.errorMessage = null;
        } else {
          this.errorMessage = response.data.message || "An error occurred";
          this.userInfo = null;
        }
      } catch (error) {
        this.errorMessage = error.response
          ? error.response.data.message
          : "Server connection error";
        this.userInfo = null;
      }
    },
  },
};
</script>

<style scoped>
.input {
  margin-bottom: 20px;
}
.user-info {
  padding: 20px;
}
</style>
