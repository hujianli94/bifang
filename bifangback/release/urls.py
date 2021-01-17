from django.urls import path
from . import views
from . import build_views

urlpatterns = [
    path('list/', views.ReleaseListView.as_view(), name='list'),
    path('create/', views.ReleaseCreateView.as_view(), name='create'),
    path('build/', build_views.ReleaseBuildView.as_view(), name='build'),
    path('build_status/', build_views.ReleaseBuildStatusView.as_view(), name='build_status'),
]
