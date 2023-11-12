<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <span>短信发送</span>
      </div>
    </template>
    <TableTools>
      <template #toolar>
        <el-button
          type="primary"
          plain
          @click="createSmsModal()"
          v-permControl="'sms_post'"
        >
          新建
        </el-button>
      </template>
    </TableTools>
    <el-table ref="tableRef" row-key="id" :data="tableData">
      <el-table-column prop="id" label="编号" />
      <el-table-column prop="total_num" label="发送总数" />
      <el-table-column prop="failed_num" label="失败数量" />
      <el-table-column label="进度">
        <template #default="scope">
          <div>
            <el-progress
              type="line"
              :percentage="
                parseInt((scope.row.progress_num / scope.row.total_num) * 100.0)
              "
              color="#57DCDD"
              :text-inside="false"
              :stroke-width="12"
            />
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="desc" label="描述" />
      <el-table-column fixed="right" label="操作">
        <template #default="scope">
          <el-button
            link
            type="primary"
            size="small"
            @click.prevent="updateSmsModal(scope.row)"
            v-permControl="'sms_put'"
          >
            编辑
          </el-button>
          <el-button
            link
            type="primary"
            size="small"
            @click.prevent="deleteSms(scope.$index, scope.row)"
            v-permControl="'sms_delete'"
          >
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
  <el-dialog v-model="dialogFormVisible" title="角色编辑">
    <el-form v-model="form" label-width="auto">
      <el-form-item label="发送数量:" prop="total_num">
        <el-input v-model="form.total_num" />
      </el-form-item>
      <el-form-item label="描述:" prop="desc">
        <el-input v-model="form.desc" />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取消</el-button>
        <el-button type="primary" @click="saveSms"> 确认 </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { onMounted, onUnmounted, reactive, ref } from "vue";
import monitorApi from "@/api/monitor";
import TableTools from "@/components/TableTools";
import { ElMessage, ElMessageBox } from "element-plus";
const dialogFormVisible = ref(false);
const tableData = reactive([]);
onMounted(() => {
  monitorApi.getSms().then(({ data }) => {
    tableData.splice(0);
    tableData.push(...data);
  });
});
onUnmounted(() => {
  clearInterval(keepalive);
});
const keepalive = setInterval(() => {
  let id_list = [];
  for (const t of tableData) {
    if (t.total_num > t.progress_num) {
      id_list.push(t.id);
    }
  }
  if (id_list.length <= 0) {
    return;
  }
  monitorApi.liveShowSms(id_list).then(({ data }) => {
    for (const t of tableData) {
      for (const d of data) {
        if (t.id == d.id) {
          t.progress_num = d.progress_num;
          t.failed_num = d.failed_num;
        }
      }
    }
  });
}, 1000);

const form = reactive({
  id: "",
  desc: "",
  total_num: "",
});

// 创建角色modal
function createSmsModal() {
  form.id = "";
  form.desc = "";
  form.total_num = "";
  dialogFormVisible.value = true;
}

// 更新全新modal
function updateSmsModal(row) {
  form.id = row.id;
  form.desc = row.desc;
  form.total_num = row.total_num;
  dialogFormVisible.value = true;
}

// 删除角色
function deleteSms(index, row) {
  ElMessageBox.confirm("确认删除吗？", "确认", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(() => {
      monitorApi.deleteSms(row.id).then(() => {
        tableData.splice(index, 1);
        ElMessage.success("删除成功！");
      });
    })
    .catch(() => {});
}

// 保存角色
function saveSms() {
  if (form.id) {
    form.permissions = form.new_permissions;
    const { children, ...new_form } = form;
    monitorApi.updateSms(form.id, new_form, children).then(({ data }) => {
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
    monitorApi.createSms(form).then(({ data }) => {
      tableData.push(data);
      ElMessage.success("角色创建成功");
      dialogFormVisible.value = false;
    });
  }
}
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
