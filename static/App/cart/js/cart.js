$(function () {
    $('.subShopping').click(function () {
        var $sub = $(this);
        var $li = $sub.parents('li');
        var cartid = $li.attr('cartid');
        console.log(cartid);
        $.getJSON('/app/subtocart/',{'cartid':cartid},function (data) {
            console.log(data);
            if(data['status'] == '200'){
                var total_money = data['total_money'];
                $('#total_money').html(total_money);
                var $span = $sub.next('span');
                $span.html(data['goods_num']);
                if (data['goods_num'] == 0){
                    $li.remove();
                }
            }
        })
    })
    $('.is_choose').click(function () {
        var $span = $(this);
        var $li = $span.parents('li');
        var cartid = $li.attr('cartid');

        console.log(cartid);
        $.get('/app/changecartstatus/',{'cartid':cartid},function (data) {
            console.log(data);
            if(data['status'] == '200'){
                var total_money = data['total_money'];
                $('#total_money').html(total_money);
                if(data['is_select']){
                    console.log('选中');
                    $span.find('span').html('√');
                    if(data['is_all_select']){
                        $('#all_select').find('span').html('√');
                    }

                }else {
                    $span.find('span').html('');
                    $('#all_select').find('span').html('');
                }
            }
        },'json')

    })

    $('#all_select').click(function () {

        var cart_select = [];
        var cart_unselect = [];
        var $all_select = $(this);
        var menulist = $('.menuList');

        menulist.each(function () {
            var $li = $(this);
            if ($li.find('.is_choose').find('span').html().trim() == ''){
                var cartid = $li.attr('cartid');
                cart_unselect.push(cartid);
            }else{
                var cartid = $li.attr('cartid');
                cart_select.push(cartid);
            }
        })
        if (cart_unselect.length == 0 ){
            console.log('全都变成未选中');
            $all_select.find('span').html('');
            $.getJSON('/app/changecartstatusmulti/',{'cart_select':cart_select.join('#')}, function (data) {
                console.log(data);
                if(data['status'] == '200'){
                    var change_list = data['change_list'].split('#');
                    console.log(change_list);
                    for (var i = 0;i<change_list.length;i++){
                        var cart = change_list[i];
                        $('.menuList').each(function () {
                            var $li = $(this);
                            if($li.attr('cartid') == cart){
                                $li.find('.is_choose').find('span').html('');
                            }
                        })
                    }
                }
            })
        }else {
            console.log('全都变成选中的');
            $all_select.find('span').html('√');
            $.getJSON('/app/changecartstatusmulti/',{'cart_select':cart_unselect.join('#')},function (data) {
                console.log(data);

                if (data['status'] == '200'){
                    var change_list = data['change_list'].split('#');
                    for(var i=0; i<change_list.length;i++){
                        var cart = change_list[i];
                        $('.menuList').each(function () {
                            var $li = $(this);
                            if($li.attr('cartid') == cart){
                                $li.find('.is_choose').find('span').html('√');
                            }

                        })
                    }
                }
            })
        }

    })

    $('#make_order').click(function () {

        var cart_select = [];
        $('.menuList').each(function () {
            var $li = $(this);
            if ($li.find('.is_choose').find('span').html().trim() != '') {
                cart_select.push($li.attr('cartid'));
            }
        })
        if (cart_select.length == 0){
            alert('请剁手');
        }else {
            console.log('下单');
            console.log(cart_select);
            $.getJSON('/app/generateorder/',{'goods_list':cart_select.join('#')},function (data) {
                console.log(data);
                if (data['status'] == '200'){
                    window.open('/app/orderdetail/?orderid=' + data['order_id'],target='_self');
                }
            })
        }
    })

})