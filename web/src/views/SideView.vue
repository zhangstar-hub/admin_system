<template>
  <el-menu
    class="sidebar"
    :default-active="router.currentRoute.value.name"
    :unique-opened="true"
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
      :index="item.name"
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
import { onMounted, computed, watch, ref } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

const store = useStore();
const router = useRouter();

onMounted(() => {
  let routers = initRouters();
  store.commit("menu/updateRouters", routers);
});

watch(
  () => store.state.user.permissions,
  () => {
    let routers = initRouters();
    store.commit("menu/updateRouters", routers);
  }
);

function initRouters() {
  let controllableRouters = JSON.parse(
    JSON.stringify(
      router.getRoutes().find((route) => route.name === "main").children
    )
  );
  const routers = [];
  for (const route of controllableRouters) {
    if (route.meta && route.meta.isShow === false) {
      continue;
    }
    let menu = store.state.user.menus.find((x) => x.name == route.name);
    if (!menu) {
      continue;
    }
    routers.push(route);
    route.meta = route.meta || {};
    route.meta.title = menu.title;
    route.meta.permissions = menu.permissions;
    let children = [];
    for (const c_route of route.children) {
      let c_menu = menu.children.find((x) => x.name == c_route.name);
      if (!c_menu) {
        continue;
      }
      c_route.meta = c_route.meta || {};
      c_route.meta.title = c_menu.title;
      c_route.meta.permission = c_menu.permission;
      children.push(c_route);
    }
    route.children = children;
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
