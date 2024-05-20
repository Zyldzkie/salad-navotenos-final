from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('signin/', views.signin, name="signin"),
    path('signup/', views.signup, name="signup"),
    path('signout/', views.signout, name='signout'),
    path('create/', views.create_product, name='create_product'),
    path('transaction/', views.transaction, name='transaction'),
    path('orders/', views.orders, name='orders'),
    path('finalize_order/', views.finalize_order , name='finalize_order'),
    path('about/', views.about, name='about'),
    path('developers/', views.developers, name='developers'),
    path('shop/', views.shop, name='shop'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)