/** layuiAdmin.std-v1.0.0 LPPL License By http://www.layui.com/admin/ */
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
        function randomData(data) {
            var now = new Date();
            return {
                name: now.toString(),
                value: [now.getHours() + ':' + now.getMinutes() + ':' + now.getSeconds(), data]
            }
        }
        var cpu = [
            {'name': '0:00:00', 'value': ['0:00:00', '0']},
            {'name': '0:00:01', 'value': ['0:00:01', '0']},
            {'name': '0:00:02', 'value': ['0:00:02', '0']},
            {'name': '0:00:03', 'value': ['0:00:03', '0']},
            {'name': '0:00:04', 'value': ['0:00:04', '0']},
            {'name': '0:00:05', 'value': ['0:00:05', '0']},
            {'name': '0:00:06', 'value': ['0:00:06', '0']},
            {'name': '0:00:07', 'value': ['0:00:07', '0']},
            {'name': '0:00:08', 'value': ['0:00:08', '0']},
            {'name': '0:00:09', 'value': ['0:00:09', '0']},
            {'name': '0:00:10', 'value': ['0:00:10', '0']},
            {'name': '0:00:11', 'value': ['0:00:11', '0']},
            {'name': '0:00:12', 'value': ['0:00:12', '0']},
            {'name': '0:00:13', 'value': ['0:00:13', '0']},
            {'name': '0:00:14', 'value': ['0:00:14', '0']}
        ];
        var memory = [
            {'name': '0:00:00', 'value': ['0:00:00', '0']},
            {'name': '0:00:01', 'value': ['0:00:01', '0']},
            {'name': '0:00:02', 'value': ['0:00:02', '0']},
            {'name': '0:00:03', 'value': ['0:00:03', '0']},
            {'name': '0:00:04', 'value': ['0:00:04', '0']},
            {'name': '0:00:05', 'value': ['0:00:05', '0']},
            {'name': '0:00:06', 'value': ['0:00:06', '0']},
            {'name': '0:00:07', 'value': ['0:00:07', '0']},
            {'name': '0:00:08', 'value': ['0:00:08', '0']},
            {'name': '0:00:09', 'value': ['0:00:09', '0']},
            {'name': '0:00:10', 'value': ['0:00:10', '0']},
            {'name': '0:00:11', 'value': ['0:00:11', '0']},
            {'name': '0:00:12', 'value': ['0:00:12', '0']},
            {'name': '0:00:13', 'value': ['0:00:13', '0']},
            {'name': '0:00:14', 'value': ['0:00:14', '0']}
        ];
        var e = layui.$, t = layui.carousel, a = layui.echarts, i = [], l = [{
            tooltip: {
                trigger: 'axis',
                // formatter: function (params) {
                //     params = params[0];
                //     var date = new Date(params.name);
                //     return date.getHours() + ':' + date.getMinutes() + ':' + date.getSeconds() + ' -- ' + params.value[1];
                // },
                // axisPointer: {
                //     animation: false
                // }
            },
            legend: {data: ["CPU利用率", "内存利用率"]},
            xAxis: {
                type: 'category',
                splitLine: {
                    show: false
                }
            },
            yAxis: [{
                type: 'value',
                name: 'CPU利用率',
                boundaryGap: [0, '100%'],
                splitLine: {
                    show: false
                }
            }, {
                type: 'value',
                name: '内存利用率',
                boundaryGap: [0, '100%'],
                splitLine: {
                    show: false
                }
            }],
            series: [{
                name: 'CPU利用率',
                type: 'line',
                showSymbol: false,
                hoverAnimation: false,
                data: cpu
            }, {
                name: '内存利用率',
                type: 'line',
                yAxisIndex: 1,
                showSymbol: false,
                hoverAnimation: false,
                data: memory
            }]
        }], n = e("#LAY-index-dataview").children("div"), r = function (e) {
            i[e] = a.init(n[e], layui.echartsTheme);
            var timer = setInterval(function () {
                layui.$.ajax({
                    url: 'getCpuAndMemory',
                    success: function (data) {
                        for (var i = 0; i < 1; i++) {
                            cpu.shift();
                            cpu.push(randomData(data.cpu));
                            memory.shift();
                            memory.push(randomData(data.memory));
                        }
                        // console.log(data);
                    }
                });
                i[e].setOption(l[e]);
            }, 1000);
            window.onresize = i[e].resize;
            // clearInterval(timer);
        };
        n[0] && r(0);
    }), e("general", {})
});
