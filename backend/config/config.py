import time

# 权限更新时间标记，权限更新时需要更新前端展示
PERM_UPDATE_TS = int(time.time())


# 所有的路由名称，一个路由名称对应GET，POST，PUT，DELETE中一个或者多个请求方式
# 路由名称会在判定路由权限时使用
ROUTER_NAMES = [
    {'router_name': 'visitor_1', 'router_desc': '游客访问通用_1'},
    {'router_name': 'visitor_2', 'router_desc': '游客访问通用_2'}
]