<template>
  <el-tree
    ref="permTreeRef"
    :data="showedPermissions"
    disabled
    show-checkbox
    node-key="id"
    default-expand-all
    highlight-current
    :default-checked-keys="permissions"
    :props="{ children: 'children', label: 'label' }"
    @change="synPermissions"
    empty-text="无任何权限"
  />
</template>

<script setup>
import {
  onMounted,
  ref,
  reactive,
  defineProps,
  nextTick,
  computed,
  defineEmits,
} from "vue";
import userApi from "@/api/user";
import utils from "@/utils";

const permTreeRef = ref();
const routerNames = reactive([]);
const allPermissions = [];
const showedPermissions = ref([]);
const props = defineProps({
  defaultPermissions: Array, // 默认权限
  validPermissions: Array, // 可以展示的权限，如果没有就全部展示
});
const emits = defineEmits(["synPer"]);

// 监听权限变化，自动刷新树
const permissions = computed(() => {
  nextTick(() => {
    permTreeRef.value.setCheckedKeys(props.defaultPermissions);
    synPermissions();
  });
  filterPermission();
  return props.defaultPermissions;
});

onMounted(() => {
  userApi.getComboPermissions().then(({ data }) => {
    let { permissions, router_names } = { ...data };
    routerNames.splice(0);
    routerNames.push(...router_names);
    let p = [];
    for (const d of permissions) {
      let per = p.find((item) => {
        return item.name == d.name;
      });
      if (per === undefined) {
        per = {
          name: d.name,
          label: menu_alias(d.name),
          children: [],
        };
        p.push(per);
      }
      per.children.push({
        id: d.id,
        label: utils.method_alias(d.method),
      });
    }
    allPermissions.splice(0);
    allPermissions.push(...p);
    showedPermissions.value = p;

    filterPermission();
  });
});

// 菜单别名
function menu_alias(menu) {
  for (const m of routerNames) {
    if (m.router_name == menu) {
      return `${menu} (${m.router_desc})`;
    }
  }
  return `${menu} (此路由不存在！)`;
}

// 过滤可展示权限
function filterPermission() {
  if (props.validPermissions !== undefined) {
    let permissions = JSON.parse(JSON.stringify(allPermissions));
    for (const p of permissions) {
      p.children = p.children.filter((item) => {
        return props.validPermissions.find((i) => i == item.id);
      });
    }
    showedPermissions.value = permissions.filter((item) => {
      return item.children.length > 0;
    });
  }
}

// 同步树权限数据到store
function synPermissions() {
  console.log(synPermissions);
  let permissions = permTreeRef.value.getCheckedKeys().filter((item) => {
    return item;
  });
  emits("synPer", permissions);
}
</script>

<style scoped lang="scss">
::v-deep .el-tree-node.is-expanded .el-tree-node__children {
  display: flex;
  flex-wrap: wrap;
  flex-direction: row;
}

.el-tree {
  user-select: none;
  margin-top: 10px;
  ::v-deep .el-tree__empty-text {
    position: static;
    padding: 0;
    margin: 0;
  }
}
</style>
