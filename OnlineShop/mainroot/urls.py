from django.urls import path, include
from .views import *


urlpatterns = [
    path('', homepage, name='home'),
    path('product/<int:product_id>', detailpage, name='product'),
    path('category/<str:cat_name>', Products_by_cat.as_view(), name='category'),
    path('signup/', sing_up_user, name='signup'),
    path('signin/', sign_in_user, name='signin'),
    path('signout/', signout, name = 'signout'),
    path('addtopacket/<int:product_id>', product_to_pocket, name='prodtopack'),
    path('packet/', Users_products.as_view(), name='packet'),
    path('odering/', Ordering_view.as_view(), name='ordering'),
    path('adminpanel/', AdminPanel.as_view(), name='adminka')
]
