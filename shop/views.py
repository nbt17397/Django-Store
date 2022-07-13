import django
from django.http import Http404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework import viewsets, permissions, status, generics
from .models import (Category, Customer, Employee, Order, OrderDetail, Product, Shipper, Supplier, User
                     )
from .serializers import (
    CategorySerializer,
    CustomerSerializer,
    EmployeeSerializer,
    OrderDetailSerializer,
    OrderSerializer,
    ProductSerializer,
    ShipperSerializer,
    SupplierSerializer,
    UserSerializer)
from django.conf import settings
from rest_framework.views import APIView


class UserViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.RetrieveAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser]

    def get_permissions(self):
        if self.action == 'get_current_user':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['get'], detail=False, url_path='current-user')
    def get_current_user(seft, request):
        return Response(seft.serializer_class(request.user).data, status=status.HTTP_200_OK)


class AuthInfo(APIView):
    def get(seft, request):
        return Response(settings.OAUTH2_INFO, status=status.HTTP_200_OK)


class CustomerViewSet(viewsets.ViewSet,  generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):

    serializer_class = CustomerSerializer

    def get_queryset(self):
        try:
            customers = Customer.objects.filter(active=True)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            customer_name = self.request.query_params.get('customer_name')
            if customer_name is not None:
                customers = customers.filter(
                    customer_name__icontains=customer_name)

            country = self.request.query_params.get('country')
            if country is not None:
                customers = customers.filter(country=country)
            return customers


class EmployeeViewSet(viewsets.ViewSet,  generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = Employee.objects.filter(active=True)
    serializer_class = EmployeeSerializer


class CategoryViewSet(viewsets.ViewSet,  generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = Category.objects.filter(active=True)
    serializer_class = CategorySerializer


class SupplierViewSet(viewsets.ViewSet,  generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = Supplier.objects.filter(active=True)
    serializer_class = SupplierSerializer


class ShipperViewSet(viewsets.ViewSet,  generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = Shipper.objects.filter(active=True)
    serializer_class = ShipperSerializer


class ProductViewSet(viewsets.ViewSet,  generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):

    serializer_class = ProductSerializer

    def get_queryset(self):
        try:
            products = Product.objects.filter(active=True)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            cate_id = self.request.query_params.get('cate_id')
            if cate_id is not None:
                products = products.filter(category_id=cate_id)

            supplier_id = self.request.query_params.get('supplier_id')
            if supplier_id is not None:
                products = products.filter(supplier_id=supplier_id)
            return products

    @action(methods=['get'], detail=True, url_path='orders')
    def get_orders(self, request, pk):

        product = self.get_object()
        orders = OrderDetail.objects.filter(
            active=True).filter(product_id=product.id)
        return Response(data={'listOrders': OrderDetailSerializer(orders, many=True).data}, status=status.HTTP_200_OK)


class OrderViewSet(viewsets.ViewSet,  generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):

    serializer_class = OrderSerializer

    def get_queryset(self):
        orders = Order.objects.filter(active=True)
        shipper_id = self.request.query_params.get('shipper_id')
        if shipper_id is not None:
            orders = orders.filter(shipper_id=shipper_id)

        customer_id = self.request.query_params.get('customer_id')
        if customer_id is not None:
            orders = orders.filter(customer_id=customer_id)

        employee_id = self.request.query_params.get('employee_id')
        if employee_id is not None:
            orders = orders.filter(employee_id=employee_id)
        return orders


class OrderDetailViewSet(viewsets.ViewSet,  generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    serializer_class = OrderDetailSerializer

    def get_queryset(self):
        orderDetails = OrderDetail.objects.filter(active=True)
        order_id = self.request.query_params.get('order_id')
        if order_id is not None:
            orderDetails = orderDetails.filter(order_id=order_id)

        product_id = self.request.query_params.get('product_id')
        if product_id is not None:
            orderDetails = orderDetails.filter(product_id=product_id)

        return orderDetails
