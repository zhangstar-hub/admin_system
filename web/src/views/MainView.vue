<template>
  <el-container class="app-container">
    <el-aside
      class="asider-container"
      :width="store.getters['menu/sidebarWidth']"
    >
      <SideView></SideView>
    </el-aside>
    <el-container
      class="main-container"
      :style="{ paddingLeft: store.getters['menu/sidebarWidth'] }"
    >
      <el-header>
        <HeaderView></HeaderView>
      </el-header>
      <MenuHistory></MenuHistory>
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import SideView from "@/views/SideView";
import HeaderView from "@/views/HeaderView";
import MenuHistory from "@/components/MenuHistory";
import store from "@/store";
</script>

<style lang="scss" scoped>
.app-container {
  .el-header {
    padding: 0;
    margin: 0;
    height: 55px;
  }
  .asider-container {
    position: fixed;
  }
  .main-container {
    min-height: calc(100vh + 60px);
  }
  .el-main {
    padding-top: 8px;
  }
}
</style>
