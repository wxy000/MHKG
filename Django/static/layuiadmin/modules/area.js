layui.define(function(exports){


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

    layui.use(['carousel', 'echarts', 'world', 'china', 'anhui', 'aomen', 'beijing', 'chongqing', 'fujian',
            'gansu', 'guangdong', 'guangxi', 'guizhou', 'hainan', 'hebei', 'heilongjiang', 'henan',
            'hubei', 'hunan', 'jiangsu', 'jiangxi', 'jilin', 'liaoning', 'neimenggu', 'ningxia',
            'qinghai', 'shandong', 'shanghai', 'shanxi', 'shanxi1', 'sichuan', 'taiwan', 'tianjin',
            'xianggang', 'xinjiang', 'xizang', 'yunnan', 'zhejiang'], function(){
        var $ = layui.$
        ,carousel = layui.carousel
        ,echarts = layui.echarts;

        var countryAndProvince = {
            'china': '1', '安徽': '1', '澳门': '1', '北京': '1', '重庆': '1', '福建': '1', '甘肃': '1',
            '广东': '1', '广西': '1', '贵州': '1', '海南': '1', '河北': '1', '黑龙江': '1', '河南': '1',
            '湖北': '1', '湖南': '1', '江苏': '1', '江西': '1', '吉林': '1', '辽宁': '1', '内蒙古': '1',
            '宁夏': '1', '青海': '1', '山东': '1', '上海': '1', '山西': '1', '陕西': '1', '四川': '1',
            '台湾': '1', '天津': '1', '香港': '1', '新疆': '1', '西藏': '1', '云南': '1', '浙江': '1',
            'world': '1'
        };

        function cg(id) {
            var datas = '';
            var options = $("#" + id + " option:selected");  //获取选中的项
            // alert(id);
            // alert(options.val());   //拿到选中项的值
            // alert(options.text());   //拿到选中项的文本
            $.ajax({
                url: 'getMapData?day=' + options.val(),
                async: false,
                success: function (data) {
                    datas = data;
                    console.log(data);
                }
            });
            return datas;
        }

        $("#ditu").change(function(){
            var ditudata = cg("ditu");
            // 重新渲染
            $('#LAY-index-plat').children('div').removeAttr('_echarts_instance_');
            var echplat = loadMap('world', ditudata.citynum, ditudata.cityaddress);
            echplatEvent(echplat, ditudata.citynum, ditudata.cityaddress);
            tabledata(ditudata.citynum);

        });

        var convertData = function (data, geoCoordMap) {
            var res = [];
            for (var i = 0; i < data.length; i++) {
                var geoCoord = geoCoordMap[data[i].name];
                if (geoCoord) {
                    res.push({
                        name: data[i].name,
                        value: geoCoord.concat(data[i].value)
                    });
                }
            }
            return res;
        };

        function loadMap(mapName, data, geoCoordMap) {
            var echplat = [], plat = [{
                // backgroundColor: '#404a59',
                title: {
                    text: '全球用户分布',
                    subtext: '不完全统计',
                    left: 'left'
                },
                tooltip : {
                    trigger: 'item'
                },
                legend: {
                    orient: 'vertical',
                    y: 'bottom',
                    x:'left',
                    data:['IP']
                },
                geo: {
                    map: mapName,
                    label: {
                        emphasis: {
                            show: true,
                            color: '#2a333d'
                        }
                    },
                    roam: false,
                    itemStyle: {
                        normal: {
                            areaColor: '#5ab1ef',
                            borderColor: '#fff'
                        },
                        emphasis: {
                            areaColor: '#A4D3EE'
                        }
                    }
                },
                series : [{
                    name: 'IP',
                    type: 'scatter',
                    coordinateSystem: 'geo',
                    data: convertData(data, geoCoordMap),
                    symbolSize: function (val) {
                        return (val[2] / 10) < 50 ? (val[2] / 10) : 50;
                    },
                    label: {
                        normal: {
                            formatter: '{b}',
                            position: 'right',
                            show: false
                        },
                        emphasis: {
                            show: true
                        }
                    },
                    itemStyle: {
                        normal: {
                            color: '#ddb926'
                        }
                    }
                }, {
                    name: 'Top 5',
                    type: 'effectScatter',
                    coordinateSystem: 'geo',
                    data: convertData(data.sort(function (a, b) {
                        return b.value - a.value;
                    }).slice(0, 6), geoCoordMap),
                    symbolSize: function (val) {
                        return (val[2] / 10) < 50 ? (val[2] / 10) : 50;
                    },
                    showEffectOn: 'render',
                    rippleEffect: {
                        brushType: 'stroke'
                    },
                    hoverAnimation: true,
                    label: {
                        normal: {
                            formatter: '{b}',
                            position: 'right',
                            show: true
                        }
                    },
                    itemStyle: {
                        normal: {
                            color: '#f4e925',
                            shadowBlur: 10,
                            shadowColor: '#333'
                        }
                    },
                    zlevel: 1
                }]
            }]
            ,elemplat = $('#LAY-index-plat').children('div')
            ,renderplat = function(index){
                echplat[index] = echarts.init(elemplat[index], layui.echartsTheme);
                echplat[index].setOption(plat[index]);
                window.onresize = echplat[index].resize;
            };
            if(!elemplat[0]) return;
            renderplat(0);

            return echplat[0];
        }

        var tabledata = function tabledata(d) {
            d.sort(function (a, b) {
                return b.value - a.value;
            });
            $("#tabledata").empty();
            for (var i = 0; i < d.slice(0, 6).length; i++) {
                $("#tabledata").append('<tr>' +
                    '<td>' + (i + 1) + '</td>' +
                    '<td>' + d[i].name + '</td>' +
                    '<td>' + d[i].value + '</td>' +
                    '</tr>')
            }
        };

        // 初始化
        var ditudata = cg("ditu");
        layer.msg("双击返回上一级");

        var data = ditudata.citynum;
        var geoCoordMap = ditudata.cityaddress;
        var echplat = loadMap('world', data, geoCoordMap);
        tabledata(data);

        var echplatEvent = function (echplat, data, geoCoordMap) {
            var timeFn = null;
            echplat.off('click');
            echplat.on('click', function(params) {
                clearTimeout(timeFn);
                //由于单击事件和双击事件冲突，故单击的响应事件延迟250毫秒执行
                timeFn = setTimeout(function() {
                    var name = params.name.toLowerCase();
                    console.log(params);
                    if (params.componentIndex === 0) {
                        if (!countryAndProvince[name]) {
                            alert("无该区域地图");
                            return;
                        }
                        loadMap(name, data, geoCoordMap);
                    }
                }, 250);
            });

            // 绑定双击事件，返回全球地图
            echplat.on('dblclick', function(params) {
                //当双击事件发生时，清除单击事件，仅响应双击事件
                clearTimeout(timeFn);

                //返回全球地图
                loadMap('world', data, geoCoordMap);
            });
        };
        echplatEvent(echplat, data, geoCoordMap);

    });

    exports('area', {})

});