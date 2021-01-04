from django.urls import path
from . import views

app_name = "env"

urlpatterns = [
    path('list/', views.EnvListView.as_view(), name='list'),
]
