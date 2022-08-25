from django.urls import path
from product.views import order_views as views


urlpatterns = [
    path('add/', views.addOrderItems.as_view(), name = 'orders-add'),
]
    