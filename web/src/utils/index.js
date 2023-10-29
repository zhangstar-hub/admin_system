
export default {
    method_alias: function (method) {
        const alias = {
            GET: "GET(获取)",
            POST: "POST(新增)",
            PUT: "PUT(修改)",
            DELETE: "DELETE(删除)",
        };
        return alias[method] || method;
    },
}