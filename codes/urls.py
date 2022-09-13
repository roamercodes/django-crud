from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/', views.product, name='product'),
    path('customer/<str:pk>', views.customer, name='customer'),
    path('create_order/', views.createOrder, name='create_order'),
    path('create_product/', views.createProduct, name='create_product'),
    path('update_order/<str:pk>', views.updateOrder, name='update_order'),
    path('update_product/<str:pk>', views.updateProduct, name='update_product'),
    path('delete_product/<str:pk>', views.deleteProduct, name='delete_product'),
    path('delete_order/<str:pk>', views.deleteOrder, name='delete_order'),
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutPage, name='logout'),
    path('user/', views.userPage, name='user-page'),
    path('account/', views.accountSetting, name='account-page'),
]