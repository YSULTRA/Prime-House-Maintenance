"""
URL configuration for prime_house_maintenance_co project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from prime_house_maintenance_co import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.homePage,name = 'home'),
    path('register/',views.register,name='register'),
    path('login/',views.loginUser,name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('privacy-policy/',views.privacyPolicy,name='privacy-policy'),
    path('terms-condition/',views.termsCondition,name='terms-condition'),
    path('list-property/',views.listProperty,name='list-property'),
    path('property/<int:pk>',views.propertyPage,name='product-page'),
    path('profile/<int:pk>',views.showProfilePage,name='profile-page'),
    path('updateOwnership/<int:user_id>/<int:property_id>/',views.updateOwnership,name='update-ownership'),
    path('removeFromSaleProperty/<int:user_id>/<int:property_id>/', views.removeFromSale, name='remove-from-sale-property'),
    path('putonsaleProperty/<int:user_id>/<int:property_id>/',views.putonSaleProperty,name='put-on-sale-property'),
    path('updateproperty/<int:property_id>/', views.updateProperty, name='update-property'),
    path('deleteproperty/<int:user_id>/<int:property_id>/',views.deleteProperty,name='delete-property'),
    path('adminPortal/',views.adminPortal,name='admin-portal'),
    path('services/',views.showServices,name='services'),
    path('services-page/<int:pk>',views.servicePage,name='service-page'),
    path('booking/<int:sk>',views.bookService,name='booking'),
    path('cancel-proposal/<int:property_id>/<int:user_id>/', views.cancel_proposal, name='cancel-proposal')

]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


