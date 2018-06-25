from django.conf.urls import url

from App import views

urlpatterns = [
    url(r'^home/',views.home,name='home'),
    url(r'^market/',views.market,name='market'),
    url(r'^marketwithparams/(?P<typeid>\d+)/(?P<childcid>\d+)/(?P<order_rule>\d+)/',views.marketWithParams,name='marketWithParams'),
    url(r'^cart/',views.cart,name='cart'),
    url(r'^mine/',views.mine,name='mine'),
    url(r'^addtocart/',views.add_to_cart,name='add_to_cart'),
    url(r'^userregister/',views.user_register,name='user_register'),
    url(r'^userlogout/',views.user_logout,name='user_logout'),
    url(r'^userlogin/',views.user_login,name='user_login'),
    url(r'^checkuser/',views.check_user,name='check_user'),
    url(r'^subtocart/',views.sub_to_cart,name='sub_to_cart'),
    url(r'^changecartstatus/',views.change_cart_status,name='change_cart_status'),
    url(r'^changecartstatusmulti/',views.change_cart_status_multi,name='change_cart_status_multi'),
    url(r'^generateorder/',views.generate_order,name='generate_order'),
    url(r'^orderdetail/',views.order_detail,name='order_detail'),
    url(r'^alipay/',views.alipay,name='alipay'),
    url(r'^orderlistwaitpay/',views.order_list_wait_pay,name='order_list_wait_pay'),
    # url(r'^testemail/',views.test_email,name='test_email'),
    # url(r'^useractive/',views.user_active,name='user_active'),

]