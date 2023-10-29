<template>
  <el-container class="app-container">
    <el-aside
      class="asider-container"
      :width="store.getters['menu/sidebarWidth']"
    >
      <SideView></SideView>
    </el-aside>
    <el-container class="main-container">
      <el-header>
        <HeaderView></HeaderView>
      </el-header>
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import SideView from "@/views/SideView";
import HeaderView from "@/views/HeaderView";
import store from "@/store";
</script>

<style lang="scss" scoped>
.app-container {
  .el-header {
    padding: 0;
    margin: 0;
    overflow-x: hidden;
  }
}
</style>
