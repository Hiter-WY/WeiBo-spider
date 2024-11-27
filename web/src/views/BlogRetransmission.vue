<template>
    <ContantBase>
      <div>
        <h2>转发详情</h2>
        <table class="table">
          <thead>
            <tr>
              <th>#</th>
              <th>Screen Name</th>
              <th>Description</th>
              <th width="120px">Profile URL</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in retransmissions" :key="index">
              <td>{{ index + 1 }}</td>
              <td>{{ item.userinfo.screen_name }}</td>
              <td>{{ item.userinfo.description }}</td>
              <td>
                <button
                position="center"
                width="120px"
                class="btn btn-outline-secondary"
                @click="performAction(index)"
                type="button"
              >
                主页
              </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </ContantBase>
  </template>
  
  <script>
  import ContantBase from "../components/ContantBase";
  import { mapState } from "vuex";
  
  export default {
    name: "BlogRetransmission",
    components: {
      ContantBase,
    },
    computed: {
      ...mapState({
        retransmissions: (state) => state.retransmissionData,
      }),
    },
    mounted() {
      if (!this.retransmissions || this.retransmissions.length === 0) {
        console.log("No retransmission data available.");
      }
    },
  };
  </script>
  
  <style scoped>
  table {
    margin-top: 20px;
  }
  </style>
  