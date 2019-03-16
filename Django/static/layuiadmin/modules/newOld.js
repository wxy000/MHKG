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
                url: 'getNewOldData?day=' + options.val(),
                async: false,
                success: function (data) {
                    datas = data;
                    // console.log(data);
                }
            });
            return datas;
        }

        var newOldData = cg("newOld");
        var giftImageUrl = "../../../static/layuiadmin/style/newOldUser.png";
        var legendName = newOldData.title;
        var datavalue = newOldData.value;

        $("#newOld").change(function(){
            var newOldData = cg("newOld");
            // 重新渲染
            // echnormline[0].setOption(normline[0]);
            $('#LAY-index-newOld').children('div').removeAttr('_echarts_instance_');
            // window.onresize = echnormline[0].resize;
            options[0].legend.data = newOldData.title;
            options[0].series[0].data = newOldData.value;
            renderDataView(0);

        });

        var echartsApp = [], options = [{
            tooltip: {
                trigger: 'item',
                formatter: "{b} : {c} ({d}%)"
            },
            graphic: {
                elements: [{
                    type: 'image',
                    style: {
                        image: giftImageUrl,
                        width: 90,
                        height: 59
                    },
                    left: 'center',
                    top: 'center'
                }]
            },
            legend: {
                orient : 'horizontal',
                x: 'center',
                y: 'bottom',
                data: legendName
            },
            series : [{
                type: 'pie',
                radius: ['37%', '65%'],
                center: ['50%', '50%'],
                // color: ['#0E7CE2', '#FF8352', '#E271DE', '#F8456B', '#00FFFF', '#4AEAB0'],
                data: datavalue
            }]
        }]
        ,elemDataView = $('#LAY-index-newOld').children('div')
        ,renderDataView = function(index){
            echartsApp[index] = echarts.init(elemDataView[index], layui.echartsTheme);
            echartsApp[index].setOption(options[index]);
            window.onresize = echartsApp[index].resize;
        };

        //没找到DOM，终止执行
        if(!elemDataView[0]) return;
        renderDataView(0);

    });
    exports('newOld', {})
});