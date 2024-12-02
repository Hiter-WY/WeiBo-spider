<template>
  <div class="dashboard-layout">
    <aside class="sidebar" :class="{ 'sidebar-collapsed': isSidebarCollapsed }">
      <div class="sidebar-header">
        <router-link :to="{ name: 'home' }" class="logo">Weibo</router-link>
        <button @click="toggleSidebar" class="toggle-btn">
          <span class="toggle-icon"></span>
        </button>
      </div>
      <nav class="sidebar-nav">
        <router-link :to="{ name: 'home' }" class="nav-item">
          <span class="nav-icon">🏠</span>
          <span class="nav-text">Home</span>
        </router-link>
        <router-link :to="{ name: 'userinfo' }" class="nav-item">
          <span class="nav-icon">👤</span>
          <span class="nav-text">UserInfo</span>
        </router-link>
        <router-link :to="{ name: 'keywords' }" class="nav-item">
          <span class="nav-icon">🔑</span>
          <span class="nav-text">Keywords</span>
        </router-link>
        <router-link :to="{ name: 'staisticsinfo' }" class="nav-item">
          <span class="nav-icon">📊</span>
          <span class="nav-text">Statistics</span>
        </router-link>
        <router-link :to="{ name: 'userportraits' }" class="nav-item">
          <span class="nav-icon">🖼️</span>
          <span class="nav-text">UserPortraits</span>
        </router-link>
        <router-link :to="{ name: 'blogretransmission' }" class="nav-item">
          <span class="nav-icon">🔄</span>
          <span class="nav-text">BlogreTransmission</span>
        </router-link>
      </nav>
    </aside>
    <main class="main-content">
      <header class="main-header">
        <button @click="toggleSidebar" class="mobile-toggle-btn">
          <span class="toggle-icon"></span>
        </button>
        <h1 class="page-title"></h1>
      </header>
      <div class="content">
        <!-- 路由视图将在这里渲染 -->
        <router-view></router-view>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const isSidebarCollapsed = ref(false)

const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
}
</script>

<style scoped>
.dashboard-layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 250px;
  background-color: #f8f9fa;
  border-right: 1px solid #e9ecef;
  transition: all 0.3s ease;
}

.sidebar-collapsed {
  width: 60px;
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #e9ecef;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
  text-decoration: none;
}

.toggle-btn {
  background: none;
  border: none;
  cursor: pointer;
}

.toggle-icon {
  display: block;
  width: 20px;
  height: 2px;
  background-color: #333;
  position: relative;
}

.toggle-icon::before,
.toggle-icon::after {
  content: '';
  position: absolute;
  width: 100%;
  height: 2px;
  background-color: #333;
}

.toggle-icon::before {
  top: -6px;
}

.toggle-icon::after {
  bottom: -6px;
}

.sidebar-nav {
  padding: 1rem 0;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  color: #333;
  text-decoration: none;
  transition: background-color 0.2s ease;
}

.nav-item:hover {
  background-color: #e9ecef;
}

.nav-icon {
  margin-right: 0.75rem;
  font-size: 1.2rem;
}

.sidebar-collapsed .nav-text {
  display: none;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.main-header {
  display: flex;
  align-items: center;
  padding: 1rem;
  background-color: #fff;
  border-bottom: 1px solid #e9ecef;
}

.mobile-toggle-btn {
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  margin-right: 1rem;
}

.page-title {
  font-size: 1.5rem;
  margin: 0;
}

.content {
  flex: 1;
  padding: 2rem;
}

@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    left: -250px;
    top: 0;
    bottom: 0;
    z-index: 1000;
  }

  .sidebar-collapsed {
    left: 0;
  }

  .mobile-toggle-btn {
    display: block;
  }
}
</style>