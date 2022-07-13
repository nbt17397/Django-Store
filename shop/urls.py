from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('users', views.UserViewSet, "user")
router.register('customers', views.CustomerViewSet, "customer")
router.register('employees', views.EmployeeViewSet, "employee")
router.register('categories', views.CategoryViewSet, "category")
router.register('suppliers', views.SupplierViewSet, "supplier")
router.register('shippers', views.ShipperViewSet, "shipper")
router.register('products', views.ProductViewSet, "product")
router.register('orders', views.OrderViewSet, "order")
router.register('orderDetails', views.OrderDetailViewSet, "orderDetail")


urlpatterns = [
    path('', include(router.urls)),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('oauth2_info/', views.AuthInfo.as_view()),
]
