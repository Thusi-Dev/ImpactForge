from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notification_list, name='notification_list'),
    path('<int:pk>/', views.notification_detail, name='notification_detail'),
    path('mark-all-read/', views.mark_all_notifications_read, name='mark_all_read'),
    path('unread-count/', views.unread_notifications_count, name='unread_count'),
]