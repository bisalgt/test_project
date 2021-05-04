from django.urls import path

from .views import home, open_cam, click_done

urlpatterns = [
    path('', home, name='home'),
    path('cam/', open_cam, name='cam'),
    path('done/', click_done, name='done'),
]