<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <span>角色管理</span>
      </div>
    </template>
    <TableTools>
      <template #toolar>
        <el-button type="primary" plain @click="createRoleModal()">
          新建
        </el-button>
      </template>
    </TableTools>
    <el-table ref="tableRef" row-key="id" :data="tableData">
      <el-table-column prop="name" label="角色" column-key="角色" />
      <el-table-column prop="desc" label="描述" column-key="描述" />
      <el-table-column
        prop="permissions.length"
        label="权限数量"
        column-key="权限数量"
      />
      <el-table-column fixed="right" label="操作">
        <template #default="scope">
          <el-button
            link
            type="primary"
            size="small"
            @click.prevent="updateRoleModal(scope.row)"
          >
            编辑
          </el-button>
          <el-button
            link
            type="primary"
            size="small"
            @click.prevent="deleteRole(scope.$index, scope.row)"
          >
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
  <el-dialog v-model="dialogFormVisible" title="角色编辑">
    <el-form v-model="form" label-width="auto">
      <el-form-item label="角色:" prop="name">
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item label="描述:" prop="desc">
        <el-input v-model="form.desc" />
      </el-form-item>
      <el-form-item label="权限:" prop="permission">
        <div class="premission-tree">
          <div class="tree-tools">
            <el-select
              v-model="roleCandidates"
              multiple
              placeholder="Select"
              :max-collapse-tags="3"
            >
              <el-option
                v-for="item in allRoles"
                :key="item"
                :value="item"
              ></el-option>
            </el-select>
            <el-button type="primary" @click="inheritPermssions">
              继承权限
            </el-button>
          </div>

          <PermissionsTree
            ref="permTreeRef"
            :defaultPermissions="form.permissions"
            @synPer="synPermissions"
          ></PermissionsTree>
        </div>
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取消</el-button>
        <el-button type="primary" @click="saveRole"> 确认 </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from "vue";
import userApi from "@/api/user";
import TableTools from "@/components/TableTools";
import PermissionsTree from "@/components/PermissionsTree";
import { ElMessage, ElMessageBox } from "element-plus";

const permTreeRef = PermissionsTree;
const dialogFormVisible = ref(false);
const tableData = reactive([]);
const roleCandidates = ref([]);
onMounted(() => {
  userApi.getRole().then(({ data }) => {
    tableData.splice(0);
    tableData.push(...data);
  });
});

const allRoles = computed(() => {
  return tableData.map((item) => {
    return item.name;
  });
});

const form = reactive({
  id: "",
  name: "",
  desc: "",
  permissions: [],
  new_permissions: [],
});

// 创建角色modal
function createRoleModal() {
  form.id = "";
  form.name = "";
  form.desc = "";
  form.permissions = [];
  form.new_permissions = [];
  roleCandidates.value = [];
  dialogFormVisible.value = true;
}

// 更新全新modal
function updateRoleModal(row) {
  form.id = row.id;
  form.name = row.name;
  form.desc = row.desc;
  form.permissions = row.permissions;
  form.new_permissions = row.permissions;
  roleCandidates.value = [];
  dialogFormVisible.value = true;
}

// 删除角色
function deleteRole(index, row) {
  ElMessageBox.confirm("确认删除吗？", "确认", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(() => {
      userApi.deleteRole(row.id).then(() => {
        tableData.splice(index, 1);
        ElMessage.success("删除成功！");
      });
    })
    .catch(() => {});
}

// 保存角色
function saveRole() {
  if (form.id) {
    form.permissions = form.new_permissions;
    const { children, ...new_form } = form;
    userApi.updateRole(form.id, new_form, children).then(({ data }) => {
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
    userApi.createRole(form).then(({ data }) => {
      tableData.push(data);
      ElMessage.success("角色创建成功");
      dialogFormVisible.value = false;
    });
  }
}

// 继承角色权限
function inheritPermssions() {
  if (roleCandidates.value.length === 0) {
    return;
  }
  let permissions = new Set();
  for (const candidate of roleCandidates.value) {
    for (const role_data of tableData) {
      if (candidate !== role_data.name) {
        continue;
      }
      for (const p of role_data.permissions) {
        permissions.add(p);
      }
    }
  }
  form.permissions = [...permissions].sort();
}

// 同步子组件的权限数据
const synPermissions = (data) => {
  form.new_permissions = data;
};
</script>

<style lang="scss" scoped>
.premission-tree {
  width: 100%;

  .tree-tools {
    display: flex;
    justify-content: space-between; /* 或其他适当的对齐方式 */
    .el-select {
      flex: 1;
    }
  }
}
</style>
