layui.define(function(exports){

    layui.use('layim', function(layim){
        var $ = layui.$;

        var device = layui.device();
        var mobileHome = '../../../static/layuiadmin/layui/css/modules/layim/html/mobile.html';
        if(device.android || device.ios){
            return location.href = mobileHome;
        }

        var adminDict = {
            username: '康康',
            avatar: '../../../static/layuiadmin/style/kangkang.png',
            id: -2,
            type: 'friend'
        };
        var mine = eval('(' + $("#hiddenmine").html() + ')');
        layim.config({
            brief: true,
            init: {mine: mine},
            initSkin: "3.jpg",
            voice: false
        }).chat({
            name: adminDict.username,
            type: adminDict.type,
            avatar: adminDict.avatar,
            id: adminDict.id
        });
        layim.setChatMin();

        //产生随机数函数
        function RndNum(n){
            var rnd = "";
            for(var i = 0; i < n; i++)
                rnd += Math.floor(Math.random() * 10);
            return rnd;
        }

        // 防止多个游客聊天导致的回复混乱
        var roomId = '';
        if (mine.id === -1) {
            roomId = RndNum(5) + Math.random();
        } else {
            roomId = "" + mine.id
        }

        var socket = new WebSocket('ws://119.29.225.142:8001/robot/' + roomId + '/');
        // 监听页面关闭，然后主动关闭websocket连接，防止卡死
        // window.onbeforeunload = function() {
        //     socket.close();
        // };
        socket.onopen = function(){
            // 系统消息
            mine['content'] = "CONNECT SUCCEED";
            socket.send(JSON.stringify({
                type: 'robotMessage',
                data: {'mine': mine}
            }));
        };
        layim.on("sendMessage", function (data) {
            var To = data.to;
            socket.send(JSON.stringify({
                type: 'robotMessage',
                data: data
            }));
        });
        socket.onmessage = function (res) {
            var msg = JSON.parse(res.data);
            layim.getMessage({
                username: adminDict.username,
                avatar: adminDict.avatar,
                id: adminDict.id,
                type: adminDict.type,
                content: msg.message
            });
        };

        // 将机器人客服的问候链接作为要发送的信息发送给客服
        window.toto = function(obj) {
            layer.msg(obj);
        };

    });
    exports('im', {})
});