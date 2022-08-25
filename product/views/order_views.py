from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from product.models import CategoryModel, StoreProductsModel, Order, OrderItem, ShippingAddress
from product.serializers import ProductSerializer, OrderItemSerializer, OrderSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class addOrderItems(APIView):
    def post(self, request):
        user = request.user
        data = request.data

        orderItems = data['orderItems']

        if orderItems and len(orderItems) == 0:
            return Response({'detail': 'No Order Items'}, status=status.HTTP_400_BAD_REQUEST)
        else:

            

            order = Order.objects.create(
                user=user,
                paymentMethod=data['paymentMethod'],
                taxPrice=data['taxPrice'],
                shippingPrice=data['shippingPrice'],
                totalPrice=data['totalPrice']
            )

            

            shipping = ShippingAddress.objects.create(
                order=order,
                address=data['shippingAddress']['address'],
                city=data['shippingAddress']['city'],
                postalCode=data['shippingAddress']['postalCode'],
                country=data['shippingAddress']['country'],
            )

            
            for i in orderItems:
                product = StoreProductsModel.objects.get(_id=i['product_name'])

                item = OrderItem.objects.create(
                    product=product,
                    order=order,
                    name=product.product_name,
                    qty=i['qty'],
                    price=i['price'],
                    image=product.images.url,
                )

                product.countInStock -= item.qty
                product.save()

            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)