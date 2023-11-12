import store from "@/store";

export default {
    permControl: {
        mounted(el, binding) {
            let [perm_name, method] = binding.value.split("_");
            for (const permission of store.state.user.permissions) {
                if (perm_name === permission.name && method.toUpperCase() === permission.method) {
                    el.style.display = 'show';
                    return
                }
            }
            el.style.display = 'none';
        }
    }
}