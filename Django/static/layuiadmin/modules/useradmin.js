/** layuiAdmin.std-v1.0.0 LPPL License By http://www.layui.com/admin/ */
;layui.define(["table", "form"], function (e) {
    var t = layui.$, i = layui.table;
    layui.form;
    var admin = layui.admin;
    var $ = layui.$;
    i.render({
        elem: "#LAY-user-manage",
        toolbar: "#test-table-toolbar-toolbarDemo",
        // url: layui.setter.base + "json/useradmin/webuser.js",
        url: "getUserInfo",
        cols: [[{
            type: "checkbox", fixed: "left"
        }, {
            field: "id", width: 100, title: "ID", sort: !0
        }, {
            field: "username", title: "用户名", minWidth: 100
        }, {
            field: "avatar", title: "头像", width: 100,
            templet: '<div><img style="display: inline-block; width: 50%; height: 100%;" src="{{ d.avatar }}"></div>'
        }, {
            field: "phone", title: "手机"
        }, {
            field: "email", title: "邮箱"
        }, {
            field: "sex", width: 80, title: "性别"
        }, {
            field: "jointime", title: "加入时间", sort: !0
        }, {
            title: "操作", width: 150, align: "center", fixed: "right", toolbar: "#table-useradmin-webuser"
        }]],
        page: !0,
        limit: 10,
        height: "full-220",
        text: "对不起，加载出现异常！"
    }), i.on("tool(LAY-user-manage)", function (e) {
        e.data;
        if ("del" === e.event) {
            layer.prompt({formType: 1, title: "敏感操作，请验证口令"}, function (t, i) {
                if (t === '000000') {
                    layer.close(i);
                    layer.confirm("真的删除行么", function (t) {
                        var csrfToken = $("[name='csrfmiddlewaretoken']").val();
                        admin.req({
                            url: 'del',
                            headers: {"X-CSRFToken": csrfToken},
                            data: {'id': e.data.id}
                            // type: 'post'
                        });
                        // e.del();
                        layer.close(t);
                        layui.table.reload('LAY-user-manage');
                    })
                } else {
                    layer.msg("密码错误！");
                }
            });
        } else if ("edit" === e.event) {
            t(e.tr);
            layer.open({
                type: 2,
                title: "编辑用户",
                content: "/accounts/editUserInfo?id=" + e.data.id,
                maxmin: !0,
                area: ["500px", "380px"],
                btn: ["确定", "取消"],
                yes: function (e, t) {
                    var l = window["layui-layer-iframe" + e], r = "LAY-user-front-submit",
                        n = t.find("iframe").contents().find("#" + r);
                    l.layui.form.on("submit(" + r + ")", function (t) {
                        var field = t.field;

                        admin.req({
                            url: "/accounts/updateUser",
                            data: field
                        });

                        i.reload("LAY-user-front-submit");
                        layer.close(e)
                    });
                    n.trigger("click")
                },
                success: function (e, t) {
                }
            });

        }
    }), e("useradmin", {})
});