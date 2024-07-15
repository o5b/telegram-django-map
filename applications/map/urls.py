from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    # path('marker/create-update/', views.marker_create_update_view, name='marker_create_update'),
    # path('marker/<int:pk>/delete/', views.marker_delete_view, name='marker_delete'),
    # path('test/', views.Home.as_view()),

    path("markers/", views.MarkerList.as_view(), name='marker_list'),
    path("markers/create/", views.MarkerCreate.as_view(), name='marker_create'),
    path("markers/<int:pk>/update/", views.MarkerUpdate.as_view(), name='marker_update'),
    path("markers/<int:pk>/delete/", views.MarkerDelete.as_view(), name='marker_delete'),
]
