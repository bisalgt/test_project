from django.urls import path

from .views import home, open_cam

urlpatterns = [
    path('', home, name='home'),
    path('cam/', open_cam, name='cam'),
]