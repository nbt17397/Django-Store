from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Category, Customer, Employee, Order, OrderDetail, Product, Shipper, Supplier, User


class UserSerializer(ModelSerializer):
    avatar = SerializerMethodField()

    def get_avatar(self, user):
        request = self.context['request']
        name = user.avatar.name
        if name.startswith("static/"):
            path = '/%s' % name
        else:
            path = '/static/%s' % name
        return request.build_absolute_uri(path)


class CustomerSerializer(ModelSerializer):

    class Meta:
        model = Customer
        fields = ["id", "customer_name", "contact_name",
                  "city", "address", "postalCode", "country", ]


class EmployeeSerializer(ModelSerializer):
    photo = SerializerMethodField()

    def get_photo(self, employee):
        request = self.context['request']
        name = employee.photo.name
        if name.startswith("static/"):
            path = '/%s' % name
        else:
            path = '/static/%s' % name
        return request.build_absolute_uri(path)

    class Meta:
        model = Employee
        fields = ["id", "last_name", "first_name",
                  "birth_day", "photo", "notes", ]


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "category_name", "description"]


class SupplierSerializer(ModelSerializer):

    class Meta:
        model = Supplier
        fields = ["id", "supplier_name", "contact_name",
                  "address",  "city", "postalCode", "country", "phone"]


class ShipperSerializer(ModelSerializer):

    class Meta:
        model = Shipper
        fields = ["id", "shipper_name", "phone"]


class ProductSerializer(ModelSerializer):
    category = CategorySerializer
    supplier = SupplierSerializer

    class Meta:
        model = Product
        fields = ["id", "product_name", "supplier",
                  "category", "unit", "price"]


class OrderSerializer(ModelSerializer):
    customer = CustomerSerializer
    employee = EmployeeSerializer
    shipper = ShipperSerializer

    class Meta:
        model = Order
        fields = ["id", "customer", "employee", "shipper", "order_date"]


class OrderDetailSerializer(ModelSerializer):
    order = OrderSerializer
    product = ProductSerializer

    class Meta:
        model = OrderDetail
        fields = ["id", "order", "product", "quantity"]
