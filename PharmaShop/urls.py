"""PharmaShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.views.generic import RedirectView

from app import views
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls.static import static
from PharmaShop import settings

urlpatterns = [
    path('', RedirectView.as_view(url='index/')),
    path("admin/", admin.site.urls),
    path("login/", LoginView.as_view(template_name='login.html'), name="login"),
    path("logout/", LogoutView.as_view(template_name='logout.html'), name="logout"),
    path("index/", views.index, name="index"),
    path("category/<str:slug>", views.products_by_category, name="products_by_category"),
    path("checkout/<str:total>", views.checkout, name="checkout"),
    path("profile/", views.profile, name="profile"),
    path("product/<str:slug>", views.product_details, name="product"),
    path("cart/", views.cart_view, name="cart"),
    path("register/", views.register, name="register"),
    path("success/", views.success, name="success"),
    path("orders/", views.orders, name="orders"),
    path("add_to_cart/<str:slug>-<str:page>", views.add_to_cart, name="add_to_cart"),
    path("remove_from_cart/<str:slug>", views.remove_from_cart, name="remove_from_cart")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
