from django.urls import path
...
from main.views import show_main, create_product, show_product, show_xml, show_json, show_xml_by_id, show_json_by_id
from main.views import register
from main.views import login_user
from main.views import logout_user
from main.views import edit_product
from main.views import delete_product
from main.views import add_product_entry_ajax
from main.views import ajax_login, ajax_register, ajax_edit_product, ajax_delete_product, ajax_logout, increment_views_ajax
from main.views import proxy_image, create_product_flutter, show_json_my_product

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),

    path('create-product/', create_product, name='create_product'),
    path('product/<str:id>/', show_product, name='show_product'),
    path('product/<uuid:id>/edit', edit_product, name='edit_product'),
    path('product/<uuid:id>/delete', delete_product, name='delete_product'),

    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('json/my/', show_json_my_product, name='show_json_my_product'),
    
    path('xml/<str:product_id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:product_id>/', show_json_by_id, name='show_json_by_id'),

    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),

    path('create-product-ajax', add_product_entry_ajax, name='add_product_entry_ajax'),
    path('ajax-login/', ajax_login, name='ajax_login'),
    path("ajax-register/", ajax_register, name="ajax_register"),
    path("ajax-edit-product/<uuid:id>/", ajax_edit_product, name="ajax_edit_product"),
    path("ajax-delete-product/<uuid:id>/", ajax_delete_product, name="ajax_delete_product"),
    path("ajax-logout/", ajax_logout, name="ajax_logout"),
    path('ajax-increment-views/<uuid:product_id>/', increment_views_ajax, name='increment_views_ajax'),

    path('proxy-image/', proxy_image, name='proxy_image'),
    path('create-flutter/', create_product_flutter, name='create_product_flutter'),
]