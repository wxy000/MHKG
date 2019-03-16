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
        if (mine.id === -1 && mine.username === '游客') {
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
        } else {
            layim.config({
                title: mine.username + '的IM',
                min: true,
                init: {
                    mine: mine,
                    friend: [{
                        groupname: '客服',
                        id: -10,
                        list: [adminDict]
                    }, {
                        groupname: '专家会诊',
                        id: -20,
                        list: [{
                            username: 'wxy000',
                            id: 2
                        }, {
                            username: 'wxy',
                            id: 1
                        }]
                    }]
                },
                initSkin: "3.jpg",
                notice: true,
                // chatLog: layui.cache.dir + 'css/modules/layim/html/chatlog.html',
                voice: false
            });
        }

        var socket = new WebSocket('ws://119.29.225.142:80/getAnswer/');
        // 监听页面关闭，然后主动关闭websocket连接，防止卡死
        window.onbeforeunload = function() {
            socket.close();
        };
        socket.onopen = function(){
            // 系统消息
            layim.setChatStatus('<span style="color:#FF5722;">在线</span>');
            layim.getMessage({system: true, id: adminDict.id, type: adminDict.type, content: '康康上线啦'});
            socket.onmessage = function (res) {
                layim.getMessage({
                    username: adminDict.username,
                    avatar: adminDict.avatar,
                    id: adminDict.id,
                    type: adminDict.type,
                    content: res.data
                });
            };
        };
        layim.on("sendMessage", function (data) {
            var To = data.to;
            socket.send(JSON.stringify({
                type: 'chatMessage',
                data: data
            }));
            if(To.type === 'friend'){
                layim.setChatStatus('<span style="color:#FF5722;">对方正在输入。。。</span>');
            }
            socket.onmessage = function (res) {
                layim.setChatStatus('<span style="color:#FF5722;">在线</span>');
                layim.getMessage({
                    username: To.username ? To.username : To.name,
                    avatar: To.avatar,
                    id: To.id,
                    type: To.type,
                    content: res.data
                });
            };
        });

        // 将机器人客服的问候链接作为要发送的信息发送给客服
        window.toto = function(obj) {
            layer.msg(obj);
        };

    });
    exports('im', {})
});