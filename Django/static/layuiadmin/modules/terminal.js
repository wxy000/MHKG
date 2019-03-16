layui.define(function(exports){

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
                url: 'getTerminalData?id=' + id + '&day=' + options.val(),
                async: false,
                success: function (data) {
                    datas = data;
                    console.log(data);
                }
            });
            return datas;
        }

        var liulanqidata = cg("liulanqi");
        var xitongdata = cg("xitong");

        var liulanqi = liulanqidata.liulanqi;
        var liulanqivalue = liulanqidata.liulanqivalue;
        var xitong = xitongdata.xitong;
        var xitongvalue = xitongdata.xitongvalue;

        $("#liulanqi").change(function(){
            var liulanqidata = cg("liulanqi");
            // 重新渲染
            // echnormline[0].setOption(normline[0]);
            $('#LAY-index-liulanqi').children('div').removeAttr('_echarts_instance_');
            // window.onresize = echnormline[0].resize;
            options[0].legend.data = liulanqidata.liulanqi;
            options[0].series[0].data = liulanqidata.liulanqivalue;
            renderDataView(0);

        });
        $("#xitong").change(function(){
            var xitongdata = cg("xitong");
            $('#LAY-index-xitong').children('div').removeAttr('_echarts_instance_');
            xitongoption[0].legend.data = xitongdata.xitong;
            xitongoption[0].series[0].data = xitongdata.xitongvalue;
            renderxitong(0);
        });

        var echartsApp = [], options = [{
            title : {
                text: '访客浏览器分布',
                x: 'center',
                textStyle: {
                    fontSize: 14
                }
            },
            tooltip : {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
                orient : 'vertical',
                x : 'left',
                data: liulanqi
            },
            series : [{
                name:'访问来源',
                type:'pie',
                radius : '55%',
                center: ['50%', '50%'],
                data: liulanqivalue
            }]
        }]
        ,elemDataView = $('#LAY-index-liulanqi').children('div')
        ,renderDataView = function(index){
            echartsApp[index] = echarts.init(elemDataView[index], layui.echartsTheme);
            echartsApp[index].setOption(options[index]);
            window.onresize = echartsApp[index].resize;
        };

        //没找到DOM，终止执行
        if(!elemDataView[0]) return;
        renderDataView(0);


        var echartsxitong = [], xitongoption = [{
            title : {
                text: '访客系统分布',
                x: 'center',
                textStyle: {
                    fontSize: 14
                }
            },
            tooltip : {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
                orient : 'vertical',
                x : 'left',
                data: xitong
            },
            series : [{
                name:'访问来源',
                type:'pie',
                radius : '55%',
                center: ['50%', '50%'],
                data: xitongvalue
            }]
        }]
        ,elemDataView1 = $('#LAY-index-xitong').children('div')
        ,renderxitong = function(index){
            echartsxitong[index] = echarts.init(elemDataView1[index], layui.echartsTheme);
            echartsxitong[index].setOption(xitongoption[index]);
            window.onresize = echartsxitong[index].resize;
        };

        //没找到DOM，终止执行
        if(!elemDataView1[0]) return;
        renderxitong(0);

    });
    exports('terminal', {})
});