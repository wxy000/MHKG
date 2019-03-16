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
    }), layui.use("carousel", function () {
        var e = layui.$;
        e("#LAY-weather").children("div");
        function myFun(result){
            var cityName = result.name;

            e.ajax({
                url: 'http://saweather.market.alicloudapi.com/area-to-weather?',
                type: 'get',
                beforeSend: function (request) {
                    request.setRequestHeader("Authorization", "APPCODE da16f227edf747f980c0d7a41cdd30b7");
                },
                data: {
                    "area": cityName
                },
                dataType: 'json',
                success: function (data) {
                    console.log(data);
                    var cityInfo = data.showapi_res_body.cityInfo;
                    e(".chengshi").html(cityInfo.c7 + "-" + cityInfo.c5);
                    // 当前天气情况
                    var time = data.showapi_res_body.time;
                    var nian = time.substring(0, 4);
                    var yue = time.substring(4, 6);
                    var ri = time.substring(6, 8);
                    var tubiao = data.showapi_res_body.now.weather_pic;
                    var wendu = data.showapi_res_body.now.temperature;
                    var tianqi = data.showapi_res_body.now.weather;
                    var zuidi = data.showapi_res_body.f1.night_air_temperature;
                    var zuigao = data.showapi_res_body.f1.day_air_temperature;
                    var feng = data.showapi_res_body.now.wind_direction;
                    var fengji = data.showapi_res_body.now.wind_power;
                    e("#shijian").html(nian + "年" + yue + "月" + ri + "日 ");
                    e("#tubiao").attr("src", tubiao);
                    e("#wendu").html(wendu + "℃");
                    e("#tianqi").html(tianqi);
                    e("#zuidi").html(zuidi + "℃");
                    e("#zuigao").html(zuigao + "℃");
                    e("#feng").html(feng);
                    e("#fengji").html(" " + fengji);
                    // 明天天气情况
                    var time1 = data.showapi_res_body.f2.day;
                    var nian1 = time1.substring(0, 4);
                    var yue1 = time1.substring(4, 6);
                    var ri1 = time1.substring(6, 8);
                    e("#shijian1").html(nian1 + "年" + yue1 + "月" + ri1 + "日 ");
                    var tubiao1 = data.showapi_res_body.f2.day_weather_pic;
                    e("#tubiao1").attr("src", tubiao1);
                    var tianqi1 = data.showapi_res_body.f2.day_weather;
                    e("#tianqi1").html(tianqi1);
                    var zuidi1 = data.showapi_res_body.f2.night_air_temperature;
                    var zuigao1 = data.showapi_res_body.f2.day_air_temperature;
                    var feng1 = data.showapi_res_body.f2.day_wind_direction;
                    var fengji1 = data.showapi_res_body.f2.day_wind_power;
                    e("#zuidi1").html(zuidi1 + "℃");
                    e("#zuigao1").html(zuigao1 + "℃");
                    e("#feng1").html(feng1);
                    e("#fengji1").html(" " + fengji1);
                    // 后天天气情况
                    var time2 = data.showapi_res_body.f3.day;
                    var nian2 = time2.substring(0, 4);
                    var yue2 = time2.substring(4, 6);
                    var ri2 = time2.substring(6, 8);
                    e("#shijian2").html(nian2 + "年" + yue2 + "月" + ri2 + "日 ");
                    var tubiao2 = data.showapi_res_body.f3.day_weather_pic;
                    e("#tubiao2").attr("src", tubiao2);
                    var tianqi2 = data.showapi_res_body.f3.day_weather;
                    e("#tianqi2").html(tianqi2);
                    var zuidi2 = data.showapi_res_body.f3.night_air_temperature;
                    var zuigao2 = data.showapi_res_body.f3.day_air_temperature;
                    var feng2 = data.showapi_res_body.f3.day_wind_direction;
                    var fengji2 = data.showapi_res_body.f3.day_wind_power;
                    e("#zuidi2").html(zuidi2 + "℃");
                    e("#zuigao2").html(zuigao2 + "℃");
                    e("#feng2").html(feng2);
                    e("#fengji2").html(" " + fengji2);
                }
            })
        }
        var myCity = new BMap.LocalCity();
        myCity.get(myFun);
    }), e("console", {})
});
