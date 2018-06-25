function password_safe() {

    var password_input = $('#password');

    var password = password_input.val();
    var password_new = md5(password);

    password_input.val(password_new);

    return true
}