import random

from django.db.models import Sum
from django.http import request
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response

from account.models import Payment, Person
from store.models import Category, Product, Cart, CartItem, Transaction, Order
from store.serializer.store_serializer import CategorySerializer, ProductSerializer, CartSerializer, CartItemSerializer, \
    TransactionSerializer, OrderSerializer


# Create your views here.

class CategoryView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ListCategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class FetchCategoryProductView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, pk):
        categoryproduct = Product.objects.filter(category=pk)
        serializer = ProductSerializer(categoryproduct, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ListProductView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CartView(generics.CreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def post(self, request, *args, **kwargs):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['cartSession'] = random.randint(1, 10000000000000000)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateCartView(generics.RetrieveUpdateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class ListCartView(generics.ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class GetItemCart(generics.ListAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def list(self, request, pk):
        itemcart = CartItem.objects.filter(cart=pk)
        serializer = CartItemSerializer(itemcart, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReduceCartView(generics.DestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class OrderView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def post(self, request):
        products = Product.objects.filter()
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            # cartCreate = Cart(cartSession=random.randint, person=)
            # cartCreate.save()
            carts = serializer.validated_data['cart']
            cartitem = CartItem.objects.filter(cart=carts)
            product_is_valid = False
            cost = 0
            for cart in cartitem:
                if cart.product in products:
                    item = Product.objects.get(pk=cart.product.pk)
                    if cart.quantity <= item.available_quantity:
                        cost += cart.cost
                        item.available_quantity -= cart.quantity
                        product_is_valid = True
                    else:
                        return Response({'error': "The Quantity of the Product is not available"})
                        break
                else:
                    return Response({'error': "cart does not exist"})

                if product_is_valid == True:
                    # payment = serializer.validated_data['payment']
                    # balance = payment.balance
                    # order_payment = Payment.objects.get(pk=payment.pk)
                    payment = Payment.objects.get(person=carts.person)
                    if cost <= payment.balance:
                        payment.balance - cost
                        payment.save() 

                        transaction = Transaction(ref=payment.cardNumber, amount=cost, paymentMethod=payment,
                                                  person=carts.person, status=serializer.validated_data['status'],
                                                  cart=carts)
                        transaction.save()

                    # serializer.validated_data['transaction'] = transaction
                    serializer.save()

                    return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({'error': "Order not created"})

        #    product = serializer.validated_data['product']
        #     if serializer.validated_data['product'] in products:
        #         quantity = serializer.validated_data['quantity']
        #         trans = Product.objects.get(pk=product.pk)
        #         if quantity <= trans.available_quantity:
        #             trans.available_quantity = trans.available_quantity - quantity
        #             trans.save()
        #
        #             price = serializer.validated_data['price']
        #             payment = serializer.validated_data['payment']
        #             balance = payment.balance
        #             order_payment = Payment.objects.get(pk=payment.pk)
        #             if price <= balance:
        #                 order_payment.balance = order_payment.balance - price
        #                 order_payment.save()
        #                 serializer.save()
        #
        #                 statu = serializer.validated_data['status']
        #                 cart = serializer.validated_data['cart']
        #                 transaction = Transaction(ref=order_payment.cardNumber, amount=price * quantity, person=cart.person, status=statu, cart=cart, )
        #                 return Response(serializer.data)
        #
        # return Response({'error': "the product does not exist"}, status=status.HTTP_400_BAD_REQUEST)

    # def create(self, request, *args, **kwargs):
    #     serializer = OrderSerializer(data=request.data)
    #     serializer = ProductSerializer(data=request.data)
    #     if serializer.is_valid():
    #         quantity = serializer.validated_data['quantity']
    #         available_quantity = serializer.validated_data['available_quantity']
    #         if available_quantity < quantity:
    #             print("not enough")
    #             return Response({'error': "we don't have enough quantity you need"}, status=status.HTTP_400_BAD_REQUEST)
    #         else:
    #             serializer.validated_data['remaining quantity'] = available_quantity - quantity
    #     return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateOrderView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class ListOrderView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class CartItemView(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def post(self, request, *args, **kwargs):
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            cart = serializer.validated_data['cart']
            cartItems = CartItem.objects.filter(cart=cart)

            product = serializer.validated_data['product']
            is_valid = True
            for cartItem in cartItems:
                if product == cartItem.product:
                    cartItem.quantity += serializer.validated_data['quantity']
                    cartItem.cost = cartItem.productPrice * cartItem.quantity
                    cartItem.save()
                    is_valid = False
                    return Response({'The quantity has been increased'})

            if is_valid:
                serializer.validated_data['productPrice'] = product.price
                quantity = serializer.validated_data['quantity']
                productPrice = serializer.validated_data['productPrice']
                serializer.validated_data['cost'] = quantity * productPrice
                serializer.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': 'Error creating Cart Item'}, status=status.HTTP_400_BAD_REQUEST)


class UpdateCartItemView(generics.RetrieveUpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class ListCartItemView(generics.ListAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class TransactionView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class UpdateTransactionView(generics.RetrieveUpdateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class ListTransactionView(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
