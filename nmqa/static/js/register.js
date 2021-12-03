function bindCaptchaBtnClick() {
    // 绑定验证码按钮，添加一个事件
    $("#captcha-btn").on("click", function (event) {
        var $this = $(this);
        var email = $("input[name='email']").val();     // 获取email的input标签值
        if(!email){
            alert("请先输入邮箱！");
            return;
        }
        // 通过js发送异步网络请求：ajax,   Async Javascript And Xml(Json)
        $.ajax({
            url: "/user/captcha",    // 请求的视图函数url
            method: "POST",
            data: {
                "email": email
            },
            // 请求成功的处理函数，res是返回的字典
            success: function (res) {
                var code = res['code'];
                if(code == 200){
                    // 取消点击事件
                    $this.off("click");
                    // 倒计时
                    var countTime = 60;
                    // 定时器，单位是毫秒
                    var timer = setInterval(function () {
                        countTime -= 1;
                        if(countTime > 0){
                            $this.text(countTime+"秒后重新发送");
                        }
                        else {
                            $this.text("获取验证码");
                            // 重新执行这个函数，重新绑定点击事件
                            bindCaptchaBtnClick();
                            // 如果不需要倒计时了，需要清除定时器，否则会一直执行
                            clearInterval(timer);
                        }
                    }, 1000);
                    alert("验证码发送成功！");
                }
                else {
                    alert(res['message']);
                }
            }
        })
    });
}


// 等网页文档元素加载完成才执行
$(function () {
    bindCaptchaBtnClick();
});