<template>
  <el-card class="login-container">
    <div class="title">登陆</div>
    <el-form label-width="auto" :model="form" :rules="rules">
      <el-form-item label="用户名:" prop="username">
        <el-input v-model="form.username" />
      </el-form-item>
      <el-form-item label="密码:" prop="password">
        <el-input type="password" v-model="form.password" />
      </el-form-item>
      <div class="login-btn-container">
        <el-button type="primary" @click="onSubmit">登陆</el-button>
      </div>
    </el-form>
  </el-card>
</template>
<script setup>
import { reactive } from "vue";
import userApi from "@/api/user";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
const store = useStore();
const router = useRouter();

const form = reactive({
  username: "",
  password: "",
});

const rules = {
  username: [{ required: true, message: "请输入账号" }],
  password: [{ required: true, message: "请输入密码" }],
};

function onSubmit() {
  if (!(form.username && form.password)) {
    return;
  }

  userApi
    .login(form.username, form.password)
    .then(function ({ data, headers }) {
      let { token } = { ...data };
      store.commit("user/setToken", token);
      store.commit("user/setPermUpdateTS", headers["perm-update-ts"]);
      router.push({ name: "home" });

      userApi.getUserPersonal().then(({ data }) => {
        let { menus, user_data, permissions } = { ...data };
        store.commit("user/setMenus", menus);
        store.commit("user/setUserData", user_data);
        store.commit("user/setPermissions", permissions);
      });
    });
}
</script>

<style scoped>
.login-container {
  width: 400px;
  height: 250px;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -70%);
  border-radius: 10px;

  .el-form {
    padding: 0 50px;
    transform: translate(-10px);
  }

  .title {
    text-align: center;
    font-weight: bolder;
    font-size: 20px;
    margin-bottom: 35px;
  }

  .login-btn-container {
    text-align: center;
    margin-top: 20px;
  }
}
</style>
