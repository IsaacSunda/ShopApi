from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status

from account.models import Person, Address, Payment
from account.serializer.account_serializer import PersonSerializer, AddressSerializer, PaymentSerializer


# Create your views here.
class CreateUser(APIView):

    def post(self, request, format=None):
        print(request.data)
        serializer = PersonSerializer(data=request.data)

        if serializer.is_valid():
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            serializer.validated_data['is_active'] = True
            serializer.save()
            return Response({'user': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"error": 'Error creating user'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, format=None):
        usernames = [user.username for user in Person.objects.all()]
        return Response({'users': usernames}, status=status.HTTP_200_OK)


class AddressView(generics.CreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    # def list(self, request):
    #     serializer = AddressSerializer(Address.objects.all(), many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


class AddressUpdateView(generics.UpdateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class SingleAddressDetail(generics.RetrieveAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class AddressViewUser(generics.ListAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def list(self, request, *args, **kwargs):
        user = self.request.query_params.get('user')
        userAddresses = Address.objects.filter(person=user)

        serializer = AddressSerializer(userAddresses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PaymentView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class UpdatePaymentView(generics.RetrieveUpdateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class ListPaymentDetail(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
