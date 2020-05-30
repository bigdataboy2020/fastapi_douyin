// api 访问接口
var setting = {
    url: "http://api接口域名/douyin" // 修改api请求地址
}

//注意：导航 依赖 element 模块，否则无法进行功能性操作
layui.use(['element'], function () {
});
layui.use(['jquery', 'form'], function () {
    var from = layui.form;
    var $ = layui.jquery;
    $('#jx').click(function () {
        var loading = layer.load(4, {shade: false});
        $.ajax({
            type: "GET",
            url: setting.url,
            dataType: "json",
            async: true,
            scriptCharset: 'GBK',
            data: {'url': $('#inturl').val()},
            // 请求之前
            beforeSend: function () {
                $('#jx').attr('disabled', true).html('正在解析中');
            },
            // 请求成功
            success: function (data) {
                console.log(data)
                $("#infor").show()
                $("#title").text(data.title)
                $("#img").attr('src', data.img_run)
                $("#img1").attr('href', data.img)
                $("#img_run").attr('href', data.img_run)
                $("#copyUrl").attr('data-clipboard-text', data.url)
                $("#vUrl").attr('href', data.url)
            },
            // 请求失败
            error: function (data) {
                console.log(data)
                layer.alert(data.responseJSON.msg, {icon: 2});
            },
            // 请求完成
            complete: function () {
                $('#jx').attr('disabled', false).html('一键解析');
                layer.close(loading);
            }
        });
    });


    // 连接复制
    $(function () {
        var btn = document.getElementById('copyUrl');
        var clipboard = new Clipboard(btn);
        clipboard.on('success', function (e) {
            // 复制成功动画
            $('#show').stop().slideDown().delay(1500).slideUp(300);
            console.log(e);
        });
        clipboard.on('error', function (e) {
            // 复制失败动画
            $('#show').stop().slideDown().delay(1500).slideUp(300);
            console.log(e);
        });

    })

})