from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from .models import Notification
from .services import mark_notification_as_read, mark_all_as_read, get_unread_notifications, get_recent_notifications

# For REST API (if using DRF, you would use viewsets/serializers instead)
@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notifications/notification_list.html', {'notifications': notifications})

@login_required
def notification_detail(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    mark_notification_as_read(notification)
    return render(request, 'notifications/notification_detail.html', {'notification': notification})

@login_required
def mark_all_notifications_read(request):
    if request.method == 'POST':
        mark_all_as_read(request.user)
        if request.is_ajax():
            return JsonResponse({'status': 'ok'})
        return redirect('notifications:notification_list')
    return HttpResponseForbidden()

@login_required
def unread_notifications_count(request):
    count = get_unread_notifications(request.user).count()
    return JsonResponse({'unread_count': count})

# You can add more endpoints for AJAX polling, deleting notifications, etc.