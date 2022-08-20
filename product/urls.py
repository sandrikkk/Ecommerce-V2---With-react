from django.urls import path
from product import views

urlpatterns = [
    path('latest-products/', views.LatestProductList.as_view()),
    path('products/<slug:category_slug>/<slug:product_slug>/', views.ProductDetail.as_view()),
    path('products/', views.Shop.as_view()),
]
    