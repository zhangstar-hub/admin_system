<template>
  <div class="menu-tag">
    <el-tag
      class="tag"
      closable
      v-for="(item, index) in store.state.menu.menuHistroy"
      :key="index"
      @close="handleClose(item)"
      @click="handleClick(item)"
      :type="router.currentRoute.value.name == item.name ? '' : 'info'"
    >
      {{ item.title }}
    </el-tag>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";
import { useStore } from "vuex";
const store = useStore();
const router = useRouter();

function handleClick(item) {
  if (item.name === router.currentRoute.value.name) {
    return;
  }
  router.push({ name: item.name });
}

function handleClose(item) {
  console.log(item);
  store.commit("menu/deleteMenuHistory", item);
}
</script>

<style scoped lang="scss">
.menu-tag {
  position: sticky;
  display: flex;
  top: 0px;
  justify-content: left;
  flex-wrap: wrap;
  user-select: none;
  z-index: 99;
  background-color: white;
  .tag {
    margin-top: 2px;
    margin-left: 15px;
    cursor: pointer;
    box-shadow: 1px 3px 3px #ddd;
  }
}
</style>
