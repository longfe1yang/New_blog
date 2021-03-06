/**
 * Created by gua on 7/11/16 4:28:01
 */

// log
var log = function () {
    console.log(arguments);
};

var visitor_count = {
    'username': 'visitor',
    'password': '123'
};

// form,其作用就是构造并返回一个js对象
var formFromKeys = function(keys, prefix) {
    var form = {};
    for(var i = 0; i < keys.length; i++) {
        var key = keys[i];
        var tagid = prefix + key;
        var value = $('#' + tagid).val();
        // if (value.length < 1) {
            // alert('字段不能为空');
            // break;
        // }
        form[key] = value;
    }
    return form;
};

// vip API
var vip = {
  data:{}
};

vip.ajax = function(url, method, form, success, error) {
    var request = {
        url: url,
        type: method,
        contentType: 'application/json',
        success: function (r) {
            log('vip post success', url, r);
            success(r);
        },
        error: function (err) {
            r = {
                success: false,
                data: err
            };
            log('vip post err', url, err);
            error(r);
        }
    };
    if(method === 'post') {
        var data = JSON.stringify(form);
        request.data = data;
    }
    $.ajax(request);
};

vip.get = function(url, response) {
    var method = 'get';
    var form = {};
    this.ajax(url, method, form, response, response);
};

vip.post = function(url, form, success, error) {
    var method = 'post';
    this.ajax(url, method, form, success, error);
};

// API normal
vip.register = function(form, success, error) {
    var url = '/register';
    this.post(url, form, success, error);
};

vip.login = function(form, success, error) {
    var url = '/login';
    this.post(url, form, success, error);
};

// tweet API
vip.tweetAdd = function(form, success, error) {
    var url = '/api/tweet/add';
    this.post(url, form, success, error);
};

//
vip.tweetDelete = function(success,tweet_id){
    var url = '/api/tweet/delete/' + tweet_id;
    log('这是vip删除中的tweet_id', tweet_id);
    this.get(url, success);
};

// 加载所有人的tweet
vip.tweetDeliver = function (success) {
    var url = '/api/tweet/deliver';
    log('加载成功没');
    this.get(url, success)
};

// 自己的tweet
vip.tweetMyOwn = function (success, user_id) {
    var url = '/api/tweet/' + user_id;
    log('加载成功没');
    this.get(url, success)
};


// tweet更新
vip.tweetUpdate = function (form, success, error, tweet_id) {
    var url = '/api/tweet/update/' + tweet_id;
    this.post(url, form, success, error)
};


// comment添加
vip.commentAdd = function (form, success, error, tweet_id) {
   var url = '/api/comment/add/' + tweet_id;
   this.post(url, form, success, error)
};

// comment删除
vip.commentDelete = function(success, comment_id){
    var url = '/api/comment/delete/' + comment_id;
    this.get(url, success)
};

// user删除
vip.userDelete = function (success, userId) {
    var url = '/api/user/delete/' + userId;
    this.get(url, success)
};