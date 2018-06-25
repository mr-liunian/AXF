$(function () {
    $('#username').change(function () {

        var username = $(this).val();
        console.log(username);

        $.getJSON('/app/checkuser/',{'username':username},function (data) {
            console.log(data);
            if (data['status'] == '200'){
                $('#username_info').css('color','green').html('用户名可用');

            }else if(data['status'] == '901'){
                $('#username_info').css('color','red').html('用户已存在');           }
        })

    })
    $('#password_confirm').change(function () {
        var password = $('#password').val();
        var password_confirm = $(this).val();
        if (password == password_confirm){
            $('#password_confirm_info').html('两次密码一致').css('color','green');
        }else {
            $('#password_confirm_info').html('两次密码不一致').css('color','red');
        }
    })
})

function data_safe() {
    console.log('进来了');
    console.log('wsad');

    var password = $('#password').val();
    var password_confirm = $('#password_confirm').val();
    if (password == password_confirm){
        var password_new = md5(password);
        $('#password').val(password_new);
        return true;
    }else {
        $('#password_confirm_info').html('两次输入不一致').css('color','red');
        return false;
    }

}