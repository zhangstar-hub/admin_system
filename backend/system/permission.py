
# 所有的路由名称，一个路由名称对应GET，POST，PUT，DELETE中一个或者多个请求方式
# 路由名称会在判定路由权限时使用
ROUTER_NAMES = []


class RouterNameMeta(type):
    """自定义路由名称处理"""
    def __new__(cls, name, bases, attr):
        if 'router_name' in attr:
            assert attr['router_name'] not in ROUTER_NAMES, f"路由名称{attr['router_name']}已经存在了"
            ROUTER_NAMES.append({
                "router_name": attr['router_name'],
                "router_desc": attr.get("router_desc", "")
            })
        return super().__new__(cls, name, bases, attr)
