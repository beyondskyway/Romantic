/**
 * Created by skyway on 2015/1/18.
 */

/*============================= WeiXin Share ======================================*/
var imgUrl = 'http://xxx.vipsinaapp.com/static/img/logo2.jpg';  //pic
var lineLink = 'http://xxx.vipsinaapp.com/store'; //网址
var descContent = '武汉xxx，这里是武汉乃至全国最具影响力的婚恋服务平台，欢迎你的加入！'; //内容
var shareTitle = '武汉xxx——线下大型相亲活动等你来'; //标题
var appid = 'Joey';

function shareFriend() {
    WeixinJSBridge.invoke('sendAppMessage', {
        "appid": appid,
        "img_url": imgUrl,
        "img_width": "640",
        "img_height": "640",
        "link": lineLink,
        "desc": descContent,
        "title": shareTitle
    }, function(res) {
        _report('send_msg', res.err_msg);
    })
}

function shareTimeline() {
    WeixinJSBridge.invoke('shareTimeline', {
        "img_url": imgUrl,
        "img_width": "640",
        "img_height": "640",
        "link": lineLink,
        "desc": descContent,
        "title": shareTitle
    }, function(res) {
        _report('timeline', res.err_msg);
    });
}
// 当微信内置浏览器完成内部初始化后会触发WeixinJSBridgeReady事件。
document.addEventListener('WeixinJSBridgeReady', function onBridgeReady() {

    // 发送给好友
    WeixinJSBridge.on('menu:share:appmessage', function(argv) {
        shareFriend();
    });

    // 分享到朋友圈
    WeixinJSBridge.on('menu:share:timeline', function(argv) {
        shareTimeline();
    });

    // 分享到微博
    WeixinJSBridge.on('menu:share:weibo', function(argv) {
        shareWeibo();
    });
}, false);
var _share_node = $('#share'),
	_cover = $('#cover');
_share_node.on('click', function() {
        _cover.hasClass('hidden') && _cover.removeClass('hidden');
 });
_cover.on('click', function(){
		_cover.addClass('hidden');
});