import { createStore } from "vuex";

export default createStore({
  state() {
    return {
      userInfo: [],
      textInfo: [],
      usernumber: 0,
      keywordnumber: 0,
      keywordInfo: [],
      keywordTextInfo: [],
      weibonumber: 0, // 今日微博数量
      retransmissionData: [], // 保存 retransmission 数据
      classifycount: 0, // 分类数量
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
    setNumber(state, weibonumber) {
      state.weibonumber = weibonumber
    },
    updateNubmer(state, weibonumber) {
      state.weibonumber += weibonumber
    },
    setkeywordnumber(state, keywordnumber) {
      state.keywordnumber = keywordnumber
    },
    updatekeywordnumber(state, keywordnumber) {
      state.keywordnumber += keywordnumber
    },
    setusernumber(state, usernumber) {
      state.usernumber = usernumber
    },
    updateusernumber(state, usernumber) {
      state.usernumber += usernumber
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
    clearNumber(state) {
      state.weibonumber = 0;
    },


    //classify相关
    setClassifyCount(state, number) {
      state.classifycount = number;
    },
    addClassifyCount(state) {
      state.classifycount += 1;
    },
    upadateclassifycount(state, number) {
      state.classifycount += number;
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
    // Retransmission相关
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
