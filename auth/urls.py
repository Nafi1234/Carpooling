from .import views
from django.urls import path


urlpatterns = [
    path('accesstoken',views.get_access_token,name="accesstoken")
]