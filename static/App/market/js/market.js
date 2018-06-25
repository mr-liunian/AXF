$(function () {
    $('#all_type').click(function () {

        var $all_type_container = $('#all_type_container')
        var status = $all_type_container.css('display');

        if (status == 'none'){

            $all_type_container.show();

            $('#all_type_logo').removeClass('glyphicon glyphicon-chevron-down').addClass('glyphicon glyphicon-chevron-up');
            $('#sort_rule_container').hide();
            $('#sort_rule_logo').removeClass('glyphicon glyphicon-chevron-up').addClass('glyphicon glyphicon-chevron-down');

        }else{
            $all_type_container.hide();
            $('#all_type_logo').removeClass('glyphicon glyphicon-chevron-up').addClass('glyphicon glyphicon-chevron-down');

        }
    })
    $('#all_type_container').click(function () {
        $(this).hide();

        $('#all_type_logo').removeClass('glyphicon glyphicon-chevron-up').addClass('glyphicon glyphicon-chevron-down');

    })

    $('#sort_rule').click(function () {
        $('#sort_rule_container').show();
        $('#sort_rule_logo').removeClass('glyphicon glyphicon-chevron-down').addClass('glyphicon glyphicon-chevron-up');
        $('#all_type_container').hide();
        $('#all_type_logo').removeClass('glyphicon glyphicon-chevron-up').addClass('glyphicon glyphicon-chevron-down');

    })
    $('#sort_rule_container').click(function () {
        $(this).hide();
        $('#sort_rule_logo').removeClass('glyphicon glyphicon-chevron-up').addClass('glyphicon glyphicon-chevron-down');

    })

    $('.addShopping').click(function () {
        var addShopping = $(this);
        console.log(addShopping.attr('class'));
        console.log(addShopping.prop('class'));
        console.log(addShopping.attr('goodsid'));
        console.log(addShopping.prop('goodsid'));
        var goodsid = addShopping.attr('goodsid');

        $.getJSON('/app/addtocart/',{'goodsid':goodsid }, function (data) {
            console.log(data)
            if (data['status'] == '200'){

                var result = data['c_goods_num'];
                var span = addShopping.prev('span');
                span.html(result);


            }else if(data['status'] == '302'){
                console.log('3333')
                window.open('/app/userlogin/',target='_self');
            }
        })
    })
})