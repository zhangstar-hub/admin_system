<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <span>账号管理</span>
      </div>
    </template>
    <div>
      <TableTools>
        <template #toolar>
          <el-button
            type="primary"
            plain
            @click="createUserModal()"
            v-permControl="'user_post'"
          >
            新建
          </el-button>
        </template>
      </TableTools>
      <el-table ref="tableRef" row-key="id" :data="tableData">
        <el-table-column prop="username" label="账号" column-key="username" />
        <el-table-column prop="name" label="拥有者" column-key="name" />
        <el-table-column prop="is_active" label="开通">
          <template #default="scope">
            <el-tag v-if="scope.row.is_active">已激活 </el-tag>
            <el-tag v-else type="danger">未激活 </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_superuser" label="角色">
          <template #default="scope">
            <el-tag v-for="role in scope.row.roles" :key="role">
              {{ roleName(role) }}
            </el-tag>
            <el-text
              v-if="scope.row.roles.length <= 0"
              type="info"
              size="small"
            >
              无角色
            </el-text>
          </template>
        </el-table-column>
        <el-table-column fixed="right" label="操作">
          <template #default="scope">
            <el-button
              link
              type="primary"
              size="small"
              @click.prevent="updateUserModal(scope.row)"
              v-permControl="'user_put'"
            >
              编辑
            </el-button>
            <el-button
              link
              type="primary"
              size="small"
              @click.prevent="deleteUser(scope.$index, scope.row)"
              v-permControl="'user_delete'"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </el-card>

  <el-dialog v-model="dialogFormVisible" title="账号编辑">
    <el-form v-model="form" label-width="auto">
      <el-form-item label="账号:" prop="username" placeholder="账号">
        <el-input v-model="form.username" />
      </el-form-item>
      <el-form-item label="密码:" prop="password">
        <template #label>
          <div>
            密码:
            <el-tooltip
              content="密码只能被重置, 默认锁定密码"
              placement="bottom-start"
            >
              <el-icon><QuestionFilled /></el-icon>
            </el-tooltip>
          </div>
        </template>
        <div class="password-input">
          <el-input
            v-model="form.password"
            placeholder="新密码"
            :disabled="lockPassword"
          />
          <el-switch
            v-model="lockPassword"
            inline-prompt
            active-text="重置"
            inactive-text="锁定"
          />
        </div>
      </el-form-item>
      <el-form-item label="拥有者:" prop="name">
        <el-input v-model="form.name" placeholder="张三" />
      </el-form-item>
      <el-form-item label="开通:" prop="is_active">
        <el-switch v-model="form.is_active" />
      </el-form-item>
      <el-form-item label="角色:" prop="roles">
        <el-select
          v-model="form.roles"
          multiple
          collapse-tags
          collapse-tags-tooltip
          :max-collapse-tags="3"
          placeholder="Select"
          style="width: 100%"
          @change="inheritPermssions"
        >
          <el-option
            v-for="item in allRoles"
            :key="item.name"
            :label="item.name"
            :value="item.id"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="拥有权限：">
        <PermissionsTree
          :defaultPermissions="defaultPermissions"
          :validPermissions="form.permissions"
          @synPer="synPermissions"
        ></PermissionsTree>
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取消</el-button>
        <el-button type="primary" @click="saveUser"> 确认 </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { reactive, ref, onMounted, computed } from "vue";
import userApi from "@/api/user";
import TableTools from "@/components/TableTools";
import PermissionsTree from "@/components/PermissionsTree";
import { ElMessage, ElMessageBox } from "element-plus";
const tableData = reactive([]);
const dialogFormVisible = ref(false);
const allRoles = reactive([]);
const lockPassword = ref(true);

onMounted(() => {
  userApi.getComboUsers().then(({ data }) => {
    let { users, roles } = { ...data };
    tableData.splice(0);
    tableData.push(...users);
    allRoles.splice(0);
    allRoles.push(...roles);
  });
});

const defaultPermissions = computed(() => {
  return form.permissions.filter((item) => {
    return !form.disabled_permission.find((i) => i == item);
  });
});

const roleName = function (roleId) {
  let role = allRoles.find((x) => {
    return x.id == roleId;
  });
  if (role) {
    return role.name;
  }
  return "未知角色";
};

const form = reactive({
  id: undefined,
  username: "",
  password: "",
  is_active: false,
  roles: [],
  permissions: [],
  new_permissions: [],
  disabled_permission: [],
});

// 创建角色modal
function createUserModal() {
  form.id = "";
  form.username = "";
  form.name = "";
  form.password = "";
  form.is_active = false;
  form.roles = [];
  form.permissions = [];
  form.new_permissions = [];
  form.disabled_permission = [];
  lockPassword.value = false;
  dialogFormVisible.value = true;
}

// 更新全新modal
function updateUserModal(row) {
  form.id = row.id;
  form.username = row.username;
  form.name = row.name;
  form.password = "";
  form.is_active = row.is_active;
  form.roles = row.roles;
  form.permissions = row.permissions;
  form.new_permissions = JSON.parse(JSON.stringify(row.permissions));
  form.disabled_permission = row.disabled_permission;
  lockPassword.value = true;
  dialogFormVisible.value = true;
}

// 删除角色
function deleteUser(index, row) {
  ElMessageBox.confirm("确认删除吗？", "确认", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(() => {
      userApi.deleteUser(row.id).then(() => {
        tableData.splice(index, 1);
        ElMessage.success("删除成功！");
      });
    })
    .catch(() => {});
}

// 保存角色
function saveUser() {
  form.disabled_permission = form.permissions.filter((item) => {
    return !form.new_permissions.find((i) => item == i);
  });
  if (lockPassword.value) {
    form.password = undefined;
  }
  if (form.id) {
    userApi.updateUser(form.id, form).then(({ data }) => {
      for (let index = 0; index < tableData.length; index++) {
        if (tableData[index].id == data.id) {
          tableData[index] = data;
          break;
        }
      }
      ElMessage.success("角色更新成功");
      dialogFormVisible.value = false;
    });
  } else {
    userApi.createUser(form).then(({ data }) => {
      tableData.push(data);
      ElMessage.success("角色创建成功");
      dialogFormVisible.value = false;
    });
  }
}

// 继承角色权限
function inheritPermssions() {
  let permissions = new Set();
  for (const role_id of form.roles) {
    for (const role_data of allRoles) {
      if (role_id !== role_data.id) {
        continue;
      }
      console.log(role_data);
      for (const p of role_data.permissions) {
        permissions.add(p);
      }
      break;
    }
  }
  form.permissions.splice(0);
  form.permissions.push(...permissions);
  form.disabled_permission = [];
}

// 同步子组件的权限数据
const synPermissions = (data) => {
  form.new_permissions = data;
};
</script>
<style lang="scss" scoped>
.password-input {
  display: flex;
  justify-content: space-around;
  flex-wrap: nowrap;
  width: 100%;
  .el-switch {
    padding-left: 20px;
  }
}
</style>
