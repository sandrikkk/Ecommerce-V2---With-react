from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from product.models import CategoryModel, Review, StoreProductsModel
from product.serializers import ProductSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class LatestProductList(APIView):
    def get(self, request, format=None):
        products = StoreProductsModel.objects.all()[0:6]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetail(APIView):
    def get(self, request, category_slug, product_slug):
        single_product = get_object_or_404(StoreProductsModel, category__slug=category_slug, slug=product_slug)
        serializer = ProductSerializer(single_product, many=False)
        return Response(serializer.data)


class StoreProduts(APIView):
    def get(self, request, category_slug=None):
        categories = None
        products = None
        if category_slug != None:
            categories = get_object_or_404(CategoryModel, slug=category_slug)
            products = StoreProductsModel.objects.filter(category=categories, is_avaible=True)
            page = request.query_params.get('page')# ?page = {request page number}
            paginator = Paginator(products,3)

            try:
                products = paginator.page(page)
            except PageNotAnInteger:
                products = paginator.page(1)
            except EmptyPage:
                products = paginator.page(paginator.num_pages) #Last Page
            
            if page == None:
                page = 1
            
            page = int(page)
            serializer = ProductSerializer(products, many=True)
        else:
            #Search
            query = request.query_params.get('keyword')# ?keyword = {request Word}
            if query == None:
                query = ''
            products = StoreProductsModel.objects.filter(product_name__icontains = query,is_avaible=True)
            #SearchEnd

            page = request.query_params.get('page')# ?page = {request page number}
            paginator = Paginator(products,3)

            try:
                products = paginator.page(page)
            except PageNotAnInteger:
                products = paginator.page(1)
            except EmptyPage:
                products = paginator.page(paginator.num_pages) #Last Page
            
            if page == None:
                page = 1
            
            page = int(page)



            serializer = ProductSerializer(products, many=True)
        return Response({'products':serializer.data, 'page': page, 'pages': paginator.num_pages})

class createProductReview(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, category_slug, product_slug):
        user = request.user
        product = StoreProductsModel.objects.get(category__slug=category_slug, slug=product_slug)
        data = request.data

        # review already exists
        alreadyexist = product.review_set.filter(user = user).exists()

        if alreadyexist:
            content = {'details': 'Product already reviewed'}
            return Response(content, status = status.HTTP_400_BAD_REQUEST)

        # no rating or 0
        elif data['rating'] == 0:
            content = {'details': 'Please select a rating'}
            return Response(content, status = status.HTTP_400_BAD_REQUEST)
        
        else:
            review = Review.objects.create(
                user = user,
                product = product,
                name = user.first_name,
                rating = data['rating'],
                comment = data['comment']
            )
            reviews = product.review_set.all()
            product.numReviews = len(reviews)

            total = 0
            for i in reviews:
                total += i.rating

            product.rating = total / len(reviews)
            product.save()

            return Response('Review Added')
