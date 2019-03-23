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
        url: "getDoctorInfo",
        cols: [[{
            type: "checkbox", fixed: "left"
        }, {
            field: "doctorId", width: 120, title: "ID", sort: !0, fixed: "left"
        }, {
            field: "doctorname", title: "姓名", minWidth: 130
        }, {
            field: "doctorheader", title: "头像", width: 100,
            templet: '<div><img style="display: inline-block; width: 50%; height: 100%;" src="{{ d.doctorheader }}"></div>'
        }, {
            field: "phone", title: "手机", width: 130
        }, {
            field: "doctoremail", title: "邮箱", minWidth: 150
        }, {
            field: "sex", width: 80, title: "性别"
        }, {
            field: "date", title: "出生日期", sort: !0, width: 120
        }, {
            field: "identity", title: "身份证号", sort: !0, minWidth: 150
        }, {
            field: "paper", title: "从业资格证", width: 100,
            templet: '<div><img style="display: inline-block; width: 50%; height: 100%;" src="{{ d.paper }}"></div>'
        }, {
            field: "quiz1", title: "所属医院", minWidth: 150
        }, {
            field: "quiz2", title: "所属科室", minWidth: 100
        }, {
            field: 'isPerfect', title:'信息完善状态', minWidth: 80, align: 'center', fixed: 'right',
            templet: '<div>{{# if(d.isPerfect==1){ }}<button class="layui-btn layui-btn-xs">已完善</button>' +
                '{{# }else{ }}<button class="layui-btn layui-btn-primary layui-btn-xs">待完善</button>' +
                '{{# } }}</div>'
        }, {
            field: 'isAuditing', title:'审核状态', minWidth: 80, align: 'center', fixed: 'right',
            templet: '<div>{{# if(d.isPerfect==0){ }}' +
                '<button class="layui-btn layui-btn-xs layui-btn-disabled">待审核</button>' +
                '{{# }else{ }}{{# if(d.isAuditing==1){ }}' +
                '<button class="layui-btn layui-btn-xs" lay-event="shenhe">通过</button>' +
                '{{# }else if(d.isAuditing==2){ }}' +
                '<button class="layui-btn layui-btn-primary layui-btn-xs" lay-event="shenhe">已拒绝</button>' +
                '{{# }else{ }}' +
                '<button class="layui-btn layui-btn-xs layui-btn-warm" lay-event="shenhe">待审核</button>' +
                '{{# } }}{{# } }}</div>'
        }, {
            title: "操作", width: 100, align: "center", fixed: "right", toolbar: "#table-useradmin-webuser"
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
                            url: '/doctor/del',
                            headers: {"X-CSRFToken": csrfToken},
                            data: {'doctorId': e.data.doctorId}
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
        } else if ("shenhe" === e.event) {
            layer.open({
                type: 2,
                title: '审核状态',
                content: "/doctor/shenhe?isAuditing=" + e.data.isAuditing,
                maxmin: !0,
                area: ["400px", "180px"],
                btn: ["确定", "取消"],
                yes: function (xx, t) {
                    var l = window["layui-layer-iframe" + xx], r = "LAY-user-front-submit",
                        n = t.find("iframe").contents().find("#" + r);
                    l.layui.form.on("submit(" + r + ")", function (t) {
                        var field = t.field;
                        field['doctorId'] = e.data.doctorId;

                        admin.req({
                            url: "/doctor/updateAuditing",
                            data: field
                        });

                        i.reload("LAY-user-front-submit");
                        layer.close(xx);
                        layui.table.reload('LAY-user-manage');
                    });
                    n.trigger("click")
                },
                success: function (e, t) {
                }
            });
        }
    }), e("doctoradmin", {})
});