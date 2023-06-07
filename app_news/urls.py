from . import views
from django.urls import path

urlpatterns = [
    path("",views.IndexView.as_view(),name="index"),
    path("<str:model>/",views.SpecificCategoryView.as_view(),name="allXCategory"),
]
