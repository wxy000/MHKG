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
    }), layui.use(["layer", "carousel", "echarts", "echartsWordcloud"], function () {
        var layer = layui.layer;
        var e = layui.$, a = (layui.carousel, layui.echarts, layui.echartsWordcloud), l = [], t = [{
            // title: {
            //     text: 'echarts3云图展示'
            // },
            tooltip: {},
            series: [{
                type: 'wordCloud',  //类型为字符云
                shape: 'smooth',  //平滑
                gridSize: 2, //网格尺寸
                size: ['80%', '80%'],
                //sizeRange: [ 50, 100 ],
                rotationRange: [-45, 90], //旋转范围
                textStyle: {
                    normal: {
                        fontFamily: 'sans-serif',
                        color: function () {
                            return 'rgb('
                                + [Math.round(Math.random() * 160),
                                    Math.round(Math.random() * 160),
                                    Math.round(Math.random() * 160)]
                                    .join(',') + ')';
                        }
                    },
                    emphasis: {
                        shadowBlur: 5,  //阴影距离
                        shadowColor: '#333'  //阴影颜色
                    }
                },
                data: data
            }]
        }], i = e("#LAY-index-wordCloud").children("div"), n = function (e) {
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
    }), e("baike", {})
});