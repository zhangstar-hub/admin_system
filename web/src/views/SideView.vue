<template>
  <el-menu
    class="sidebar"
    :default-active="router.name"
    active-text-color="#ffd04b"
    background-color="#333333"
    text-color="#fff"
    :router="true"
    :collapse-transition="false"
    :collapse="store.getters['menu/collapse']"
  >
    <el-menu-item class="sider-title">
      <h2 v-if="store.getters['menu/collapse']">后台</h2>
      <h2 v-else>后台管理系统</h2>
    </el-menu-item>
    <el-sub-menu
      :index="index.toString()"
      v-for="(item, index) of menuList"
      :key="index"
    >
      <template #title>
        <el-icon><component :is="item.icon"></component></el-icon>
        <span>{{ item.meta.title }}</span>
      </template>
      <el-menu-item
        v-for="i of item.children"
        :key="i.name"
        v-text="i.meta.title"
        :index="i.name"
      ></el-menu-item>
    </el-sub-menu>
  </el-menu>
</template>

<script setup>
import { onMounted, computed } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

const store = useStore();
const router = useRouter();
onMounted(() => {
  console.log(store.state.user.menus);
  let routers = initRouters(store.state.user.menus);
  console.log(routers);
  store.commit("menu/updateRouters", routers);
});

function initRouters(menus) {
  let controllableRouters = router
    .getRoutes()
    .find((route) => route.name === "main").children;
  const routers = [];
  for (const router of controllableRouters) {
    if (router.meta && router.meta.isShow === false) {
      continue;
    }
    let menu = menus.find((x) => x.name == router.name);
    if (!menu) {
      continue;
    }
    routers.push(router);
    router.meta = router.meta || {};
    router.meta.title = menu.title;
    router.meta.permissions = menu.permissions;
    let children = [];
    for (const c_router of router.children) {
      let c_menu = menu.children.find((x) => x.name == c_router.name);
      if (!c_menu) {
        continue;
      }
      c_router.meta = c_router.meta || {};
      c_router.meta.title = c_menu.title;
      c_router.meta.permission = c_menu.permission;
      children.push(c_router);
    }
    router.children = children;
  }
  return routers;
}

const menuList = computed(() => {
  return store.state.menu.routers.filter((item) => {
    return item.children && item.children.length > 0;
  });
});
</script>

<style lang="scss" scoped>
.sidebar {
  height: 100%;
  min-height: 100vh;
  .sider-title {
    display: flex;
    justify-content: space-around;
    height: 50px;
    line-height: 50px;
    margin: auto;
  }
}
</style>
