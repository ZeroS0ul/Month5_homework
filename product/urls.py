from django.urls import path
from . import views

urlpatterns = [

    path('categories/', views.CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', views.CategoryRetrieveUpdateDestroyAPIView.as_view(), name='category-detail-update-destroy'),
    path('products/', views.ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', views.ProductRetrieveUpdateDestroyAPIView.as_view(), name='product-detail-update-destroy'),

    path('products/reviews/', views.ProductReviewListAPIView.as_view(), name='product-reviews-list'),
    
    path('reviews/', views.ReviewListCreateAPIView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', views.ReviewRetrieveUpdateDestroyAPIView.as_view(), name='review-detail-update-destroy'),
    
]