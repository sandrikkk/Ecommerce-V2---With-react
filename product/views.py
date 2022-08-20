from django.shortcuts import get_object_or_404,render
from rest_framework.views import APIView
from rest_framework.response import Response
from product.models import StoreProductsModel
from product.serializer import ProductSerializer

def index(request):
    return render(request, 'index.html')

class LatestProductList(APIView):
    def get(self, request, format = None):
        products = StoreProductsModel.objects.all()[0:6]
        serializer = ProductSerializer(products, many = True)
        return Response(serializer.data)

class ProductDetail(APIView):
    def get(self,request, category_slug, product_slug):
        single_product = get_object_or_404(StoreProductsModel,category__slug = category_slug, slug = product_slug)
        serializer = ProductSerializer(single_product, many = False)
        return Response(serializer.data)