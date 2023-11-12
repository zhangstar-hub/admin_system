<template>
  <div class="navbar">
    <div class="left-menu">
      <el-icon
        @click="store.commit('menu/updateCollapse')"
        class="icon"
        :size="30"
      >
        <Expand v-if="store.getters['menu/collapse']" />
        <Fold v-else />
      </el-icon>
    </div>
    <div class="right-menu">
      <el-dropdown class="avatar-container" trigger="click">
        <div class="avatar-wrapper">
          <img src="@/assets/avatar.jpg" class="user-avatar" />
          <el-icon class="el-icon-caret-bottom"><CaretBottom /></el-icon>
        </div>

        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="logout">退出登陆</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>
<script setup>
import { useRouter } from "vue-router";
import { useStore } from "vuex";

const store = useStore();
const router = useRouter();

function logout() {
  store.commit("user/clearAll");
  router.push({ name: "login" });
}
</script>

<style lang="scss" scoped>
.navbar {
  background: rgba(255, 255, 255, 0.3);
  height: 50px;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);

  .left-menu {
    height: 50px;
    padding-left: 10px;
    float: left;
    cursor: pointer;
    display: flex;
    align-items: center;
  }

  .right-menu {
    height: 50px;
    display: flex;
    align-items: center;
    float: right;
    height: 100%;
    line-height: 50px;
    user-select: none;
    cursor: pointer;

    .avatar-container {
      margin-right: 30px;

      .avatar-wrapper {
        .user-avatar {
          width: 40px;
          height: 40px;
          border-radius: 10px;
        }
      }
    }
  }
}
</style>
