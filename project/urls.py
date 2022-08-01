from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', views.UserViewSet, "user")
router.register('departments', views.DepartmentViewSet, 'department')
router.register('projects', views.ProjectViewSet, "project")
router.register('stages', views.StageViewSet, "stage")
router.register('categories', views.CategoryViewSet, "category")
router.register('positions', views.PositionViewSet, "position")
router.register('boxChats', views.BoxChatViewSet, "boxChats")
router.register('messages', views.MessageViewSet, "messages")
router.register('process', views.ProcessViewSet, "process")
router.register('steps', views.StepViewSet, "step")
router.register('works', views.WorkViewSet, "work")
router.register('additionalWorks',
                views.AdditionalWorkViewSet, "additionalWork")
router.register('documents', views.DocumentViewSet, "document")
router.register('notifications', views.NotificationViewSet, 'notification')

urlpatterns = [
    path('', include(router.urls)),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('oauth2_info/', views.AuthInfo.as_view()),
    path('api/login/', views.login_api),
    path('api/user/', views.get_user_data)
]
