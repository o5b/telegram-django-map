from django.urls import path

from . import views

urlpatterns = [
    path(
        '',
        views.IndexView.as_view(),
        name='index',
    ),

    path(
        'about/',
        views.AboutView.as_view(),
        name='about',
    ),

    path(
        'page/<str:slug>/',
        views.PageDetailView.as_view(),
        name='page_detail',
    ),
]
