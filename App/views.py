import uuid

from django.core.cache import cache
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template import loader
from django.urls import reverse

from App.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow, FoodType, Goods, UserModel, CartModel, \
    Order, OrderGoods

PRICE_UP = '1'
PRICE_DOWN = '2'
SALE_DOWN = '3'

def home(request):
    wheels = MainWheel.objects.all()
    navs = MainNav.objects.all()
    mustbuys = MainMustBuy.objects.all()
    shops = MainShop.objects.all()

    mainshows = MainShow.objects.all()

    data = {
        'title':'首页',
        'wheels':wheels,
        'navs':navs,
        'mustbuys':mustbuys,
        'shops':shops,
        'mainshows': mainshows
    }

    return render(request, 'App/main/home/Home.html',context=data)
def market(request):
    return redirect(reverse('app:marketWithParams',kwargs={'typeid':'104749','childcid':'0','order_rule':'0'}))

def marketWithParams(request,typeid,childcid,order_rule):

    foodtypes = FoodType.objects.all()

    if childcid == '0':
        goods_list = Goods.objects.filter(categoryid=typeid)
    else:
        goods_list = Goods.objects.filter(categoryid=typeid).filter(childcid=childcid)

    if order_rule == PRICE_UP:
        goods_list = goods_list.order_by('price')
    elif order_rule == PRICE_DOWN:
        goods_list = goods_list.order_by('-price')
    elif order_rule == SALE_DOWN:
        goods_list = goods_list.order_by('-productnum')

    foodtype = FoodType.objects.get(typeid=typeid)

    childtypenames = foodtype.childtypenames

    childtype_list = childtypenames.split('#')
    child_type_list = []

    for childtype in childtype_list:
        child_type_list.append(childtype.split(':'))

    data = {
        'title': '闪购',
        'foodtypes': foodtypes,
        'goods_list': goods_list,
        'typeid':typeid,
        'childcid':childcid,
        'child_type_list': child_type_list,
    }

    return render(request,'App/main/market/Market.html',context=data)


def cart(request):

    username = request.session.get('username')
    if not username:

        return redirect(reverse('app:user_login'))

    user = UserModel.objects.get(u_name=username)
    carts = CartModel.objects.filter(c_user=user)

    is_all_select = True

    for cart_obj in carts:
        if not cart_obj.c_is_select:
            is_all_select = False
            break

    data = {
        'title': '购物车',
        'carts':carts,
        'is_all_select':is_all_select
    }

    return render(request,'App/main/cart/Cart.html',context=data)


def mine(request):

    username = request.session.get('username')


    data = {
        'title': '我的'
    }
    if username:
        user = UserModel.objects.get(u_name=username)
        data['is_login'] = True
        data['username'] = user.u_name
        data['usericon'] = '/static/uploads/' + user.u_icon.url

        data['order_wait_receive'] = Order.objects.filter(o_user=user).filter(o_status=2).count()
        data['order_wait_pay'] = Order.objects.filter(o_user=user).filter(o_status=1).count()

    return render(request,'App/main/mine/Mine.html',context=data)


def add_to_cart(request):
    username = request.session.get('username')
    if username:

        print(request.GET.get('goodsid'))
        goodsid = request.GET.get('goodsid')

        user = UserModel.objects.get(u_name=username)
        goods = Goods.objects.get(pk=goodsid)

        cart_objs = CartModel.objects.filter(c_user=user).filter(c_goods=goods)

        data = {
            'msg':'ok',
            'status':'200'
        }

        if cart_objs.exists():
            cart_obj = cart_objs.first()
            cart_obj.c_goods_num = cart_obj.c_goods_num + 1
            cart_obj.save()
        else:
            cart_obj = CartModel()
            cart_obj.c_user = user
            cart_obj.c_goods = goods
            cart_obj.save()
        data['c_goods_num'] = cart_obj.c_goods_num

        return JsonResponse(data)
    else:
        return JsonResponse({'status': '302', 'msg': 'ok'})


def user_register(request):
    if request.method == 'GET':
        return render(request,'App/user/user_register.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        icon = request.FILES.get('icon')

        user = UserModel()
        user.u_name = username
        user.u_email = email
        # user.u_password = password
        user.set_password(password)
        user.u_icon = icon

        user.save()

        # temp = loader.get_template('App/active_email.html')
        #
        # token = str(uuid.uuid4())
        #
        # cache.set(token,user.id,timeout=10*60)
        #
        # temp_content = temp.render({'username':username,'active_url':'http://127.0.0.1:8004/app/useractive/?u_token='+token})
        #
        # send_mail('项目激活邮件','','17888806804@163.com',[email,],html_message=temp_content)

        request.session['username'] = username

        request.session.flush()

        return redirect(reverse('app:mine'))


def user_logout(request):
    request.session.flush()
    return redirect(reverse('app:mine'))


def check_user(request):
    username = request.GET.get('username')
    # password = request.GET.get('password')
    users = UserModel.objects.filter(u_name=username)
    # passwords = UserModel.objects.filter(u_password=password)
    data = {
        'msg':'ok',
        'status':'200'
    }
    if users.exists():
        data['msg'] = 'user exit'
        data['status'] = '901'

    return JsonResponse(data=data)


def user_login(request):
    if request.method == 'GET':
        return render(request, 'App/user/user_login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        users = UserModel.objects.filter(u_name=username)
        if users.exists():
            user = users.first()
            if user.verify_password(password):
                # if user.is_active:

                request.session['username'] = username
                return redirect(reverse('app:mine'))
                # else:
                #     return HttpResponse('请激活后登录')
            else:
                return redirect(reverse('app:user_login'))

        else:
            return redirect(reverse('app:user_login'))


def sub_to_cart(request):
    cartid = request.GET.get('cartid')
    cart_obj = CartModel.objects.get(pk=cartid)

    data = {
        'msg':'ok',
        'status':'200',
        'goods_num': 0
    }

    if cart_obj.c_goods_num == 1:
        cart_obj.delete()
    else:
        cart_obj.c_goods_num = cart_obj.c_goods_num - 1
        cart_obj.save()
        data['goods_num'] = cart_obj.c_goods_num

    username = request.session.get('username')

    total = cal_total(username)

    data['total_money'] = total

    return JsonResponse(data)


def change_cart_status(request):

    cartid = request.GET.get('cartid')
    cart_obj = CartModel.objects.get(pk=cartid)
    cart_obj.c_is_select = not cart_obj.c_is_select
    cart_obj.save()

    is_all_select = True


    data = {
        'msg':'ok',
        'status':'200',
        'is_select': cart_obj.c_is_select,

    }
    total_money = 0
    user = UserModel.objects.get(u_name=request.session.get('username'))
    carts = CartModel.objects.filter(c_user=user)
    for car in carts:
        if not car.c_is_select:
            is_all_select = False
        else:
            total_money += car.c_goods_num*car.c_goods.price


    data['is_all_select'] = is_all_select
    data['total_money'] = total_money
    return JsonResponse(data)


def change_cart_status_multi(request):

    change_list = request.GET.get('cart_select')

    print(change_list)

    changelist = change_list.split('#')

    print(change_list)

    for change in changelist:
        car_obj = CartModel.objects.get(pk=change)
        car_obj.c_is_select = not car_obj.c_is_select
        car_obj.save()

    data = {
        'msg':'ok',
        'status':'200',
        'change_list': change_list
    }

    return JsonResponse(data)

def cal_total(username):
    total_money = 0
    user = UserModel.objects.get(u_name=username)
    carts = CartModel.objects.filter(c_user=user).filter(c_is_select=True)
    for car in carts:
        total_money += car.c_goods_num * car.c_goods.price

    return total_money

def generate_order(request):

    cart_list = request.GET.get('goods_list')

    cart_list = cart_list.split('#')

    user = UserModel.objects.get(u_name=request.session.get('username'))
    order = Order()
    order.o_user = user
    order.save()

    for cart_id in cart_list:
        ordergoods = OrderGoods()
        ordergoods.order = order

        cart_obj = CartModel.objects.get(pk=cart_id)
        ordergoods.goods_num = cart_obj.c_goods_num
        ordergoods.goods = cart_obj.c_goods

        ordergoods.save()
        cart_obj.delete()

    data={
        'status':'200',
        'msg':'ok',
        'order_id':order.id
    }
    return JsonResponse(data)


def order_detail(request):

    order_id = request.GET.get('orderid')

    order = Order.objects.get(pk=order_id)

    data = {
        'order':order
    }

    return render(request,'App/order/order_detail.html',context=data)


def alipay(request):
    orderid = request.GET.get('orderid')

    order = Order.objects.get(pk=orderid)
    order.o_status = 2
    order.save()
    data = {
        'msg':'ok',
        'status':'200',
        'redirect':reverse('app:mine')
    }

    return JsonResponse(data=data)


def order_list_wait_pay(request):

    user = UserModel.objects.get(u_name=request.session.get('username'))
    orders = Order.objects.filter(o_user=user).filter(o_status=1)
    data = {
        'orders':orders
    }
    return render(request,'App/order/order_list.html',context=data)


# def test_email(request):
#     send_mail('激活邮件', 'message', '17888806804@163.com', ['1654571350@qq.com', ])
#
#     return HttpResponse('发送成功')


# def user_active(request):
#
#     u_token = request.GET.get('u_token')
#     if not u_token:
#         return HttpResponse('激活过期，请重新激活')
#     u_id = cache.get(u_token)
#     user = UserModel.objects.get(pk=u_id)
#     user.is_active = True
#     user.save()
#     cache.delete(u_token)
#
#     return HttpResponse('用户激活成功')