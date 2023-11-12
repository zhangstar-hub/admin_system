<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <span>权限管理</span>
      </div>
    </template>
    <TableTools>
      <template #toolar>
        <el-button
          type="primary"
          plain
          @click="createPermissionModal"
          v-permControl="'permission_post'"
        >
          新建
        </el-button>
      </template>
    </TableTools>
    <el-table ref="tableRef" row-key="id" :data="tableData">
      <el-table-column prop="name" label="路由" />
      <el-table-column prop="method" label="操作权限">
        <template #default="scope">
          {{ utils.method_alias(scope.row.method) }}
        </template>
      </el-table-column>
      <el-table-column prop="menus" label="菜单ID">
        <template #default="scope">
          {{ menus_formatter(scope.row.menus) }}
        </template>
      </el-table-column>
      <el-table-column prop="desc" label="描述" />
      <el-table-column fixed="right" label="操作">
        <template #default="scope">
          <el-button
            link
            type="primary"
            size="small"
            @click.prevent="updatePermissionModal(scope.row)"
            v-permControl="'permission_put'"
          >
            编辑
          </el-button>
          <el-button
            link
            type="primary"
            size="small"
            @click.prevent="deletePermission(scope.$index, scope.row)"
            v-permControl="'permission_delete'"
          >
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-card>

  <el-dialog v-model="dialogFormVisible" title="权限编辑">
    <el-form v-model="form" label-width="auto">
      <el-form-item label="路由:" prop="name">
        <el-select v-model="form.name" filterable>
          <el-option
            v-for="item in routerNames"
            :key="item.router_name"
            :label="item.router_name"
            :value="item.router_name"
          >
            <span style="float: left">{{ item.router_name }}</span>
            <span
              style="
                float: right;
                color: var(--el-text-color-secondary);
                font-size: 13px;
              "
              >{{ item.router_desc }}</span
            >
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="操作权限:" prop="method">
        <el-select v-model="form.methods" placeholder="必选项" multiple>
          <el-option value="GET" label="查看(GET)">查看(GET)</el-option>
          <el-option value="POST" label="新增(POST)">新增(POST)</el-option>
          <el-option value="PUT" label="修改(PUT)">修改(PUT)</el-option>
          <el-option value="DELETE" label="删除(DELETE)">
            删除(DELETE)
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="菜单ID:" prop="menus">
        <el-select
          v-model="form.menus"
          placeholder="可选项"
          multiple
          filterable
        >
          <el-option-group
            v-for="group in allMenus"
            :key="group.id"
            :label="group.title"
          >
            <el-option
              v-for="item in group.children"
              :key="item.id"
              :label="item.title"
              :value="item.id"
            >
              <span style="float: left">{{ item.title }}</span>
              <span
                style="
                  float: right;
                  color: var(--el-text-color-secondary);
                  font-size: 13px;
                "
                >{{ item.name }}</span
              >
            </el-option>
          </el-option-group>
        </el-select>
      </el-form-item>
      <el-form-item label="描述:" prop="desc">
        <el-input v-model="form.desc" placeholder="描述..." />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取消</el-button>
        <el-button type="primary" @click="savePermission"> 确认 </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { onMounted, reactive, ref } from "vue";
import userApi from "@/api/user";
import TableTools from "@/components/TableTools";
import { ElMessage, ElMessageBox } from "element-plus";
import utils from "@/utils";
const tableData = reactive([]);
const allMenus = reactive([]);
const routerNames = reactive([]);

onMounted(() => {
  userApi.getComboPermissions().then(({ data }) => {
    let { permissions, menus, router_names } = { ...data };
    tableData.splice(0);
    tableData.push(...permissions);
    allMenus.splice(0);
    allMenus.push(...menus);
    routerNames.splice(0);
    routerNames.push(...router_names);
  });
});
const dialogFormVisible = ref(false);

const form = reactive({
  id: "",
  name: "",
  methods: [],
  menus: [],
  desc: "",
});

// 创建权限modal
function createPermissionModal() {
  form.id = "";
  form.name = "";
  form.methods = ["GET"];
  form.menus = [];
  form.desc = "";
  dialogFormVisible.value = true;
}

// 更新全新modal
function updatePermissionModal(row) {
  form.id = row.id;
  form.name = row.name;
  form.methods = [row.method];
  form.menus = row.menus;
  form.desc = row.desc;
  dialogFormVisible.value = true;
}

// 刷新权限数据
function refreshPermission() {
  userApi.getPermission().then(({ data }) => {
    tableData.splice(0);
    tableData.push(...data);
  });
}

// 删除权限
function deletePermission(index, row) {
  ElMessageBox.confirm("确认删除吗？", "确认", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(() => {
      userApi.deletePermission(row.id).then(() => {
        tableData.splice(index, 1);
        ElMessage.success("删除成功！");
      });
    })
    .catch(() => {});
}

// 保存权限
function savePermission() {
  if (form.methods.length <= 0) {
    ElMessage.error("操作权限至少选中一个！");
    return;
  }
  if (form.id) {
    if (form.methods.length !== 1) {
      ElMessage.error("只能选择一个操作权限进行更新！");
      return;
    }
    let t_form = { ...form, method: form.methods[0] };
    userApi.updatePermission(t_form.id, t_form).then(() => {
      refreshPermission();
      ElMessage.success("权限更新成功");
      dialogFormVisible.value = false;
    });
  } else {
    userApi.createPermission(form).then(({ data }) => {
      tableData.push(...data);
      ElMessage.success("权限创建成功");
      dialogFormVisible.value = false;
    });
  }
}

function menus_formatter(menus) {
  return menus
    .map((item) => {
      for (const menu of allMenus) {
        for (const c_menu of menu.children) {
          if (c_menu.id == item) {
            return c_menu.title;
          }
        }
      }
      return item;
    })
    .join("|");
}
</script>
<style lang="scss">
.el-select {
  width: 100%;
}
</style>
