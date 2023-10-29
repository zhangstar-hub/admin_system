<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <span>菜单管理</span>
      </div>
    </template>
    <TableTools>
      <template #toolar>
        <el-button type="primary" plain @click="createMenuModal()">
          新建
        </el-button>
      </template>
    </TableTools>
    <el-table ref="tableRef" row-key="id" :data="tableData">
      <el-table-column prop="title" label="标题" />
      <el-table-column prop="name" label="菜单ID" />
      <el-table-column fixed="right" label="操作">
        <template #default="scope">
          <el-button
            link
            type="primary"
            size="small"
            v-show="scope.row.pid == undefined"
            @click.prevent="createMenuModal(scope.row.id, scope.row)"
          >
            新建子菜单
          </el-button>
          <el-button
            link
            type="primary"
            size="small"
            @click.prevent="updateMenuModal(scope.row)"
          >
            编辑
          </el-button>
          <el-button
            link
            type="primary"
            size="small"
            @click.prevent="deleteMenu(scope.$index, scope.row)"
          >
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-card>

  <el-dialog v-model="dialogFormVisible" title="菜单编辑">
    <el-form v-model="form" label-width="auto">
      <el-form-item label="菜单标题:" prop="name">
        <el-input v-model="form.title" placeholder="显示的名字" />
      </el-form-item>
      <el-form-item label="菜单ID:" prop="name">
        <el-input v-model="form.name" placeholder="菜单ID" />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取消</el-button>
        <el-button type="primary" @click="saveMenu"> 确认 </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { onMounted, reactive, ref } from "vue";
import userApi from "@/api/user";
import TableTools from "@/components/TableTools";
import { ElMessage, ElMessageBox } from "element-plus";
const tableData = reactive([]);
const dialogFormVisible = ref(false);

onMounted(() => {
  refreshMenus();
});

// 刷新菜单
function refreshMenus() {
  userApi.getMenu().then(({ data }) => {
    tableData.splice(0);
    tableData.push(...data);
  });
}

const form = reactive({
  id: "",
  name: "",
  title: "",
  pid: "",
  children: [],
});

// 创建菜单modal
function createMenuModal(pid) {
  form.id = "";
  form.name = "";
  form.title = "";
  form.pid = pid;
  form.children = [];
  dialogFormVisible.value = true;
}

// 更新全新modal
function updateMenuModal(row) {
  form.id = row.id;
  form.name = row.name;
  form.title = row.title;
  form.pid = row.pid;
  dialogFormVisible.value = true;
}

// 删除菜单
function deleteMenu(index, row) {
  ElMessageBox.confirm("确认删除吗？", "确认", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(() => {
      userApi.deleteMenu(row.id).then(() => {
        refreshMenus();
        ElMessage.success("删除成功！");
      });
    })
    .catch(() => {});
}

// 保存菜单
function saveMenu() {
  if (form.id) {
    const { children, ...new_form } = form;
    userApi.updateMenu(form.id, new_form, children).then(() => {
      refreshMenus();
      ElMessage.success("菜单更新成功");
      dialogFormVisible.value = false;
    });
  } else {
    userApi.createMenu(form).then(() => {
      refreshMenus();
      ElMessage.success("菜单创建成功");
      dialogFormVisible.value = false;
    });
  }
}
</script>
<style lang="scss">
.el-select {
  width: 100%;
}
</style>
