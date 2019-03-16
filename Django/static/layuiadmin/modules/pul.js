layui.define(function(exports){

    /*
      下面通过 layui.use 分段加载不同的模块，实现不同区域的同时渲染，从而保证视图的快速呈现
    */


    //区块轮播切换
    layui.use(['admin', 'carousel'], function(){
        var $ = layui.$
            ,admin = layui.admin
            ,carousel = layui.carousel
            ,element = layui.element
            ,device = layui.device();

        //轮播切换
        $('.layadmin-carousel').each(function(){
            var othis = $(this);
            carousel.render({
                elem: this
                ,width: '100%'
                ,arrow: 'none'
                ,interval: othis.data('interval')
                ,autoplay: othis.data('autoplay') === true
                ,trigger: (device.ios || device.android) ? 'click' : 'hover'
                ,anim: othis.data('anim')
            });
        });

        element.render('progress');

    });

    //数据概览
    layui.use(['carousel', 'echarts'], function(){
        var $ = layui.$
            ,carousel = layui.carousel
            ,echarts = layui.echarts;

        function cg(id) {
            var datas = '';
            var options = $("#" + id + " option:selected");  //获取选中的项
            // alert(id);
            // alert(options.val());   //拿到选中项的值
            // alert(options.text());   //拿到选中项的文本
            $.ajax({
                url: 'getPulData?id=' + id + '&day=' + options.val(),
                async: false,
                success: function (data) {
                    datas = data;
                }
            });
            return datas;
        }

        var pvuvdata = cg("pvuv");
        var liuliang = cg("flux");

        var time_day = pvuvdata.time_day;
        var pv = pvuvdata.pv;
        var uv = pvuvdata.uv;
        var outflux = liuliang.outflux;
        var influx = liuliang.influx;


        $("#pvuv").change(function(){
            var pvuvdata = cg("pvuv");
            // 重新渲染
            // echnormline[0].setOption(normline[0]);
            $('#LAY-index-normline').children('div').removeAttr('_echarts_instance_');
            // window.onresize = echnormline[0].resize;
            normline[0].xAxis[0].data = pvuvdata.time_day;
            normline[0].series[0].data = pvuvdata.pv;
            normline[0].series[1].data = pvuvdata.uv;
            rendernormline(0);

        });
        $("#flux").change(function(){
            var fluxdata = cg("flux");
            $('#LAY-index-area').children('div').removeAttr('_echarts_instance_');
            area[0].xAxis[0].data = fluxdata.time_day;
            area[0].series[0].data = fluxdata.outflux;
            area[0].series[1].data = fluxdata.influx;
            renderarea(0);
        });

        //标准折线图
        var echnormline = [], normline = [{
            tooltip : {
                trigger: 'axis'
            },
            legend: {
                data:['PV','UV']
            },
            xAxis : [{
                type : 'category',
                boundaryGap : false,
                data: time_day
            }],
            yAxis : [{
                type : 'value'
            }],
            series : [{
                name:'PV',
                type:'line',
                smooth:true,
                itemStyle: {normal: {areaStyle: {type: 'default'}}},
                data: pv
            },{
                name:'UV',
                type:'line',
                smooth:true,
                itemStyle: {normal: {areaStyle: {type: 'default'}}},
                data: uv
            }]
        }]
        ,elemnormline = $('#LAY-index-normline').children('div')
        ,rendernormline = function(index){
            echnormline[index] = echarts.init(elemnormline[index], layui.echartsTheme);
            echnormline[index].setOption(normline[index]);
            window.onresize = echnormline[index].resize;
        };
        if(!elemnormline[0]) return;
        rendernormline(0);

        var echarea = [], area = [{
            // title : {
            //     text: '雨量流量关系图',
            //     x: 'center'
            // },
            tooltip : {
                trigger: 'axis',
                // formatter: function(params) {
                //     return params[0].name + '<br/>' + params[0].seriesName + ' : ' + params[0].value + ' MB<br/>'
                //         + params[1].seriesName + ' : ' + params[1].value + ' MB';
                // }
                axisPointer: {
                    type: 'cross',
                    animation: false,
                    label: {
                        backgroundColor: '#505765'
                    }
                }
            },
            legend: {
                data:['流出流量','流入流量']
            },
            // dataZoom : {
            //     show : true,
            //     realtime : true,
            //     start : 0,
            //     end : 100
            // },
            xAxis : [{
                type : 'category',
                boundaryGap : false,
                axisLine: {onZero: false},
                data : time_day
            }],
            yAxis : [{
                name : '流出流量(MB)',
                type : 'value',
                // max : 500
            }, {
                name : '流入流量(MB)',
                type : 'value',
                nameLocation: 'start',
                inverse: true,
                // axisLabel : {
                //     formatter: function(v){
                //         return - v;
                //     }
                // }
            }],
            series : [{
                name:'流出流量',
                type:'line',
                itemStyle: {normal: {areaStyle: {type: 'default'}}},
                data: outflux
            }, {
                name:'流入流量',
                type:'line',
                yAxisIndex:1,
                animation: false,
                itemStyle: {normal: {areaStyle: {type: 'default'}}},
                data: influx
            }]
        }]
        ,elemarea = $('#LAY-index-area').children('div')
        ,renderarea = function(index){
            echarea[index] = echarts.init(elemarea[index], layui.echartsTheme);
            echarea[index].setOption(area[index]);
            window.onresize = echarea[index].resize;
        };
        if(!elemarea[0]) return;
        renderarea(0);

    });

    exports('pul', {})
});