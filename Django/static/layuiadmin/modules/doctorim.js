layui.define(function(exports){

    layui.use('layim', function(layim){
        var $ = layui.$;

        var device = layui.device();
        var mobileHome = '../../../static/layuiadmin/layui/css/modules/layim/html/mobile.html';
        if(device.android || device.ios){
            return location.href = mobileHome;
        }

        var mine = eval('(' + $("#hiddenmine").html() + ')');
        var friends = eval('(' + $("#hiddenfriends").html() + ')');
        // var groupname = "专家会诊";
        // var fdStart = mine.id.toString().indexOf("YS");
        // if(fdStart === 0) {
        //     groupname = "患者";
        // }
        layim.config({
            title: mine.username + '的IM',
            min: true,
            init: {
                mine: mine,
                friend: friends
            },
            initSkin: "3.jpg",
            notice: true,
            // chatLog: layui.cache.dir + 'css/modules/layim/html/chatlog.html',
            voice: false
        });

        var socket = new WebSocket('ws://119.29.225.142:8001/ws/chat/' + mine.id + '/');
        layim.on("sendMessage", function (data) {
            var To = data.to;
            socket.send(JSON.stringify({
                type: 'chatMessage',
                data: data
            }));
        });
        socket.onmessage = function (res) {
            var msg = JSON.parse(res.data);
            layim.getMessage({
                username: msg.message.username,
                avatar: msg.message.avatar,
                id: msg.message.id,
                type: 'friend',
                content: msg.message.content
            });
        };

    });
    exports('doctorim', {})
});