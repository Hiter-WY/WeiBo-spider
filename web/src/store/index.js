import { createStore } from "vuex";

export default createStore({
  state() {
    return {
      userInfo: [],
      textInfo: [],
      keywordInfo: [],
      keywordTextInfo: [],
      retransmissionData: [], // 保存 retransmission 数据
      searchKeyword: "", // 搜索关键字
      userPortrait: {}, // 用户画像数据
      count: {
        体育: 0,
        娱乐: 0,
        家居: 0,
        房产: 0,
        教育: 0,
        时尚: 0,
        时政: 0,
        游戏: 0,
        科技: 0,
        财经: 0,
      },
    };
  },
  mutations: {
    // UserInfo related mutations
    setUserInfo(state, userInfo) {
      state.userInfo = userInfo;
    },
    setTextInfo(state, textInfo) {
      state.textInfo = textInfo;
    },
    updateTextInfo(state, { index, value }) {
      state.textInfo[index] = value;
    },
    clearUserInfo(state) {
      state.userInfo = [];
    },
    clearTextInfo(state) {
      state.textInfo = [];
    },

    // KeywordInfo related mutations
    setKeywordInfo(state, keywordInfo) {
      state.keywordInfo = keywordInfo;
    },
    setKeywordTextInfo(state, keywordTextInfo) {
      state.keywordTextInfo = keywordTextInfo;
    },
    updateKeywordTextInfo(state, { index, value }) {
      state.keywordTextInfo[index] = value;
    },
    clearKeywordInfo(state) {
      state.keywordInfo = [];
    },
    clearKeywordTextInfo(state) {
      state.keywordTextInfo = [];
    },
    setSearchKeyword(state, keyword) {
      state.searchKeyword = keyword; // 新增
    },
    setUserPortrait(state, userPortrait) {
      state.userPortrait = userPortrait; // 新增
    },
    // RetransmissionData related mutations
    setRetransmissionData(state, retransmissionData) {
      state.retransmissionData = retransmissionData; // 覆盖现有数据
    },
    updateRetransmissionData(state, retransmissionData) {
      if (!Array.isArray(state.retransmissionData)) {
        state.retransmissionData = [];
      }
      state.retransmissionData.push(...retransmissionData); // 追加新数据
    },
    clearRetransmissionData(state) {
      state.retransmissionData = [];
    },
    // Common mutations
    clear(state) {
      state.userInfo = [];
      state.textInfo = [];
      state.keywordInfo = [];
      state.keywordTextInfo = [];
      state.searchKeyword = ""; // 新增
      state.userPortrait = {};
      state.count = {
        体育: 0,
        娱乐: 0,
        家居: 0,
        房产: 0,
        教育: 0,
        时尚: 0,
        时政: 0,
        游戏: 0,
        科技: 0,
        财经: 0,
      };
    },
    increment(state, key) {
      if (state.count[key] !== undefined) {
        state.count[key]++;
      }
    },
  },
});
