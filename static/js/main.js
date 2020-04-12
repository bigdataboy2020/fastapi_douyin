 //注意：导航 依赖 element 模块，否则无法进行功能性操作
    layui.use(['element'],function () {
    });
	layui.use(['jquery','form'],function () {
	    var from = layui.form;
	    var $ = layui.jquery;

            $('#jx').click(function(){
                var loading = layer.load(4, { shade: false });
                var url = $('#inturl').val();
                console.log(url)
                $.ajax({
                    type:"GET",
                    url:"douyin?way=json",
                    dataType:"json",
                    async:true,
                    scriptCharset: 'GBK',
                    data:{'url':url},
                    beforeSend:function(){
                        $('#jx').attr('disabled',true).html('正在解析中');
                    },
                    success:function(data){
                        if(data.code=="200"){
                            $("#infor").show()
                            $("#title").text(data.title)
                            $("#img").attr('src', data.img_run)
                            $("#img1").attr('href', data.img)
                            $("#img_run").attr('href', data.img_run)
                            $("#copyUrl").attr('data-clipboard-text', data.url)
                            $("#vUrl").attr('href', data.url)
                        }else{
                            layer.alert(data.info,{icon:2});
                        }
                        $('#jx').attr('disabled',false).html('一键解析');
                        layer.close(loading);
                    },
                    error:function(){
                        layer.msg("解析失败")
                    }
                });
            });


        // 连接复制
        $(function () {
        var btn=document.getElementById('copyUrl');
        var clipboard=new Clipboard(btn);
        clipboard.on('success', function(e){
            // 复制成功动画
            $('#show').stop().slideDown().delay(1500).slideUp(300);
            console.log(e);
        });
        clipboard.on('error', function(e){
            // 复制失败动画
            $('#show').stop().slideDown().delay(1500).slideUp(300);
            console.log(e);
        });

//        var btnu=document.getElementById('aa');
//        var clipboardu=new Clipboard(btnu);
//        clipboardu.on('success', function(e){
//            console.log(e);
//        });
//        clipboardu.on('error', function(e){
//            console.log(e);
//        });
})

    })