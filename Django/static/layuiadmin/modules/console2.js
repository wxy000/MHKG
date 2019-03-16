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
    }), layui.use(["carousel", "echarts"], function () {
        // category只能是这个顺序，因为后台写死了
        var categories = [{'name': '疾病'}, {'name': '症状'}, {'name': '检查'}, {'name': '药品'}];
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
                    data: data.data,
                    links: data.links,
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
                    }
                }
            })
        };
        i[0] && n(0);
        // console.log(data);
    }), e("console2", {})
});