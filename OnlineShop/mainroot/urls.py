from django.urls import path, include
from .views import *


urlpatterns = [
    path('', homepage, name='home'),
    path('product/<int:product_id>', detailpage, name='product'),
    path('category/<str:cat_name>', get_products_by_cat, name='category'),
    path('signup/', sing_up_user, name='signup'),
    path('signin/', sign_in_user, name='signin'),
    path('signout/', signout, name = 'signout'),
    path('addtopacket/<int:product_id>', product_to_pocket, name='prodtopack'),
    path('packet/', users_packet, name='packet'),
]
