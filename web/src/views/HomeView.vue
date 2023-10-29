<template>
  <div>
    <el-button @click="userApi.test">test</el-button>
    <el-button @click="userApi.routerName">routerName</el-button>
    <el-button @click="userApi.getUserPersonal(store.state.user.userData.id)"
      >getUserPersonal</el-button
    >
  </div>
</template>

<script setup>
import userApi from "@/api/user";
import { useStore } from "vuex";
const store = useStore();
</script>

<style lang="scss" scoped></style>
