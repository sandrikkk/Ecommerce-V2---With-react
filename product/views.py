from urllib import response
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from product.models import StoreProductsModel
from product.models import CategoryModel
from product.serializer import ProductSerializer
from django.http import Http404
class LatestProductList(APIView):
    def get(self, request, format = None):
        products = StoreProductsModel.objects.all()[0:6]
        serializer = ProductSerializer(products, many = True)
        return Response(serializer.data)

class ProductDetail(APIView):
    def get_object(self,category_slug, product_slug):
        try:
            print(StoreProductsModel.objects.filter(category__slug = category_slug).get(product_slug = product_slug))
            return StoreProductsModel.objects.filter(category__slug = category_slug).get(product_slug = product_slug)
        except StoreProductsModel.DoesNotExist:
            raise Http404

    def get(self,request, category_slug, product_slug):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product)
        return response(serializer.data)     