;layui.define(function (e) {
    layui.use(["admin", "carousel"], function () {
        var e = layui.$, t = (layui.admin, layui.carousel), a = layui.element, i = layui.device();
        e(".layadmin-carousel").each(function () {
            var a = e(this);
            t.render({
                elem: this,
                width: "100%",
                arrow: "none",
                interval: a.data("interval"),
                autoplay: a.data("autoplay") === !0,
                trigger: i.ios || i.android ? "click" : "hover",
                anim: a.data("anim")
            })
        }), a.render("progress")
    }), layui.use(["carousel", "echarts", "form"], function () {
        var form = layui.form;
        var $ = layui.$;
        var layer = layui.layer;
        $.ajax({
            url: "relation",
			type: "GET",
			dataType: "json",
            success: function (data) {
                var result = data['relation'];
                console.log(result);
                var root = document.getElementById("selectRelation");
                for (var i = 0; i < result.length; i++) {
                    var option = document.createElement("option");
                    option.setAttribute("value", (i + 1));
                    option.innerText = result[i];
                    root.appendChild(option);
                    form.render("select");
                }
            }
        });
        // category只能是这个顺序，因为后台写死了
        var categories = [{'name': '疾病'}, {'name': '症状'}, {'name': '检查'}, {'name': '药品'}];
        var node = [];
        var relation = [];
        var e = layui.$, a = (layui.carousel, layui.echarts), l = [], t = [{
            // title: { text: '疾病关系图谱' },
            tooltip: {
                formatter: function (x) {
                    return x.data.des;
                }
            },
            legend: [{
                // selectedMode: 'single',
                x: 'left',
                data: categories.map(function (a) {
                    return a.name;
                })
            }],
            series: [
                {
                    type: 'graph',
                    layout: 'force',
                    symbolSize: 80,
                    roam: true,
                    edgeSymbol: ['circle', 'arrow'],
                    edgeSymbolSize: [4, 10],
                    force: {
                        repulsion: 2500,
                        edgeLength: [10, 50]
                    },
                    draggable: true,
                    lineStyle: {
                        normal: {
                            width: 2,
                            color: '#4b565b'

                        }
                    },
                    edgeLabel: {
                        normal: {
                            show: true,
                            formatter: function (x) {
                                return x.data.name;
                            }
                        }
                    },
                    label: {
                        normal: {
                            show: true,
                            textStyle: {
                            }
                        }
                    },
                    data: node,
                    links: relation,
                    categories: categories
                }
            ]
        }], i = e("#LAY-index-pageone").children("div"), n = function (e) {
            l[e] = a.init(i[e], layui.echartsTheme), l[e].setOption(t[e]), window.onresize = l[e].resize;
            l[e].on('click', function (param) {
                var index = layer.load(2);
                var data = param.data;
                //判断节点的相关数据是否正确
                if (data != null && data != undefined) {
                    if (data.url != null && data.url != undefined) {
                        //根据节点的扩展属性url打开新页面
                        window.location.href = data.url;
                        // layer.close(index);
                    } else {
                        layer.close(index);
                    }
                } else {
                    layer.close(index);
                }
            })
        };
        i[0] && n(0);
        function getNR(n1, n2, r){
            l[0].showLoading();
            $.ajax({
                url: "nodeRelation?entity1=" + n1 + "&entity2=" + n2 + "&relation=" + r,
                type: "GET",
                dataType: "json",
                success: function (data) {
                    node = data.data;
                    relation = data.links;
                    l[0].setOption({
                        series: [{
                            data: node,
                            links: relation,
                            categories: categories
                        }]
                    });
                    l[0].hideLoading();
                }
            });
            i[0] && n(0);
        }
        $("#searchBtn").on('click', function(){
            var text = $("#selectRelation option:selected").text();
            var id = $("#selectRelation option:selected").val();
            var name = '';
            if (id === '*' || id === '0') {
                name = id;
            } else {
                name = text;
            }
            var nodeid1 = $("#entity1").attr("nodeid1");
            var nodeid2 = $("#entity2").attr("nodeid2");
            if (nodeid1 === undefined && nodeid2 === undefined) {
                layer.msg('请至少填写一项实体名');
            } else if ((nodeid1 !== undefined && nodeid2 === undefined) || nodeid1 === undefined && nodeid2 !== undefined) {
                if (name === '*' || name === '0') {
                    layer.tips('关系选择错误', '#select', {
                        tips: [3, '#FF5722'],
                        tipsMore: true
                    });
                } else {
                    getNR(nodeid1, nodeid2, name);
                }
            } else if (nodeid1 !== undefined && nodeid2 !== undefined) {
                if (nodeid1 === nodeid2) {
                    layer.msg('请选择不同的实体');
                } else {
                    if (name !== '*' && name !== '0') {
                        layer.tips('关系选择错误', '#select', {
                            tips: [3, '#FF5722'],
                            tipsMore: true
                        });
                    } else {
                        getNR(nodeid1, nodeid2, name);
                    }
                }
            }
        });
        // console.log(data);
    }), e("relationQuery", {})
});