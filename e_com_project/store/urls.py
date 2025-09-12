from django.urls import path
from . import views

urlpatterns = [
    path('', views.store , name='store'),
    path('Category/<slug:category_slug>/', views.store , name='product_by_category'),
    path('Category/<slug:category_slug>/<slug:product_slug>/', views.product_details , name='product_details'),
    path('search/', views.search , name='search'),
    
]
