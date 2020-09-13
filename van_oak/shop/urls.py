from django.urls import path
from . import views

urlpatterns = [
	path("", views.product_list, name='product_list'),
	path("product/<int:id>", views.product, name='product'),
	path("cart/", views.cart, name='cart'),
	path("cart/remove_from_cart/<int:product_id>", views.remove_from_cart, name='remove_from_cart'),
	path("cart/increase_item_count_in_order/<int:product_id>", views.increase_item_count_in_order, name='increase_item_count_in_order'),
	path("cart/decrease_item_count_in_order/<int:product_id>", views.decrease_item_count_in_order, name='decrease_item_count_in_order'),
	path("thanks", views.thanks_for_order, name='thanks'),
]