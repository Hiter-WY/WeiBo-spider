<template>
  <div class="main-content">
    <div class="dashboard-grid">
      <div class="dashboard-card data-overview">
        <div class="card-header">
          <h3 class="card-title">数据概览</h3>
        </div>
        <div class="stat-grid">
          <div class="stat-item">
            <div class="stat-value">{{ $store.state.weibonumber }}</div>
            <div class="stat-label">今日收集微博</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ $store.state.usernumber }}</div>
            <div class="stat-label">关注用户</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ classifycount }}</div>
            <div class="stat-label">分类次数</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ $store.state.keywordnumber }}</div>
            <div class="stat-label">关键词匹配</div>
          </div>
        </div>
      </div>

      <div class="dashboard-card task-management">
      <div class="card-header">
        <h3 class="card-title">任务管理</h3>
      </div>
      <div class="quick-actions">
        <router-link :to="{ name: 'userinfo' }" class="quick-action-btn">
          <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/>
          </svg>
          <span>查找用户</span>
        </router-link>
        <router-link :to="{ name: 'keywords' }" class="quick-action-btn">
          <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M17 3H7c-1.1 0-2 .9-2 2v16l7-3 7 3V5c0-1.1-.9-2-2-2zm0 15l-5-2.18L7 18V5h10v13z"/>
          </svg>
          <span>查找关键词</span>
        </router-link>
        <router-link :to="{name: 'userportraits'}" class="quick-action-btn">
          <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V5h14v14zm-7-2h2V7h-4v2h2z"/>
          </svg>
          <span>用户画像</span>
        </router-link>
      </div>
    </div>

      <div class="dashboard-card data-collection-status">
        <div class="card-header">
          <h3 class="card-title">数据收集状态</h3>
        </div>
        <div class="storage-status">
          <div>本地存储空间 <span>{{ databasecount }} / 3000条 </span></div>
          <div class="progress-bar">
            <div class="progress" :style="{width: databasecount / 30 + '%'}"></div>
          </div>
        </div>
      </div>

      <div class="dashboard-card personal-stats">
        <div class="card-header">
          <h3 class="card-title">个人数据统计</h3>
        </div>
        <div class="stats">
          <div>本月收集微博 <span>{{ 1325 + $store.state.weibonumber + $store.state.keywordnumber }}</span></div>
          <div>关键词匹配率 <span>{{ (90 + databasecount / 3000).toFixed(3) + '%' }}</span></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import store from "../store";

export default {
  name: "HomeView",
  mounted() {
    // 从 localStorage 中加载 weibonumber
    const weibonumber = parseInt(localStorage.getItem("weibonumber"), 10);
    const usernumber = parseInt(localStorage.getItem("usernumber"), 10);
    const keywordnumber = parseInt(localStorage.getItem("keywordnumber"), 10);
    if (!isNaN(weibonumber)) {
      // 如果存在，初始化 Vuex
      store.commit("setNumber", weibonumber);
    } else {
      // 如果不存在，初始化为 0
      store.commit("setNumber", 0);
      localStorage.setItem("weibonumber", 0);
    }
    if(!isNaN(usernumber)){
      store.commit("setusernumber", usernumber);
    } else {
      store.commit("setusernumber", 0);
      localStorage.setItem("usernumber", 0);
    }
    if(!isNaN(keywordnumber)){
      store.commit("setkeywordnumber", keywordnumber);
    } else {
      store.commit("setkeywordnumber", 0);
      localStorage.setItem("keywordnumber", 0);
    }
  },
  data() {
    return {
      classifycount: parseInt(localStorage.getItem("classifycount")),
      databasecount: parseInt(localStorage.getItem("databasecount")),
    };
  },
};
</script>

<style scoped>
.main-content {
  padding: 20px;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.dashboard-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.stat-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.stat-item {
  text-align: center;
  padding: 10px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #feb47b;
}

.stat-label {
  font-size: 12px;
  color: #666;
}

.quick-actions {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.quick-action-btn {
  background: #f5f5f5;
  border: none;
  border-radius: 4px;
  padding: 10px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  text-decoration: none; /* 移除下划线 */
  color: black; /* 设置字体颜色为黑色 */
}

.quick-action-btn:hover {
  background: #e0e0e0;
}

.quick-action-btn svg {
  width: 20px;
  height: 20px;
  color: #feb47b;
}

.storage-status, .data-breakdown, .stats {
  margin-top: 15px;
}

.progress-bar {
  height: 10px;
  background: #eee;
  border-radius: 5px;
  margin-top: 5px;
}

.progress {
  height: 100%;
  background: #feb47b;
  border-radius: 5px;
}
</style>