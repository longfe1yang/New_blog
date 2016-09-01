/**
 * Created by Administrator on 2016/9/1.
 */

var add0 = function(m){return m<10?'0'+m:m };
var dateTrans = function (timeStamp) {

    var time = new Date(timeStamp * 1000);
    var y = time.getFullYear();
    var m = time.getMonth() + 1;
    var d = time.getDate();
    var h = time.getHours();
    var mm = time.getMinutes();
    return y + '-' + add0(m) + '-' + add0(d) + ' ' + add0(h) + ':' + add0(mm);
};
