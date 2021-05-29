"""ericcart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from myapp import views
from cutphoto.views import cuthello,cutphoto,cutphotos
from django.conf.urls import url,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('hello/', views.sayhello),
    path('myhello/', cuthello),  

    path('listall/',views.listall),
    path('knitshop/',views.knitshop),
    path('subcata/<str:pk>/', views.subcata, name="subcata"),  
    path('cata/<str:pk>/', views.cata, name="cata"),

    path('knitgallery/',views.knitgallery),
    path('blog/',views.blog),
    path('aboutus/',views.aboutus),

    path('main/',views.main),   
    path('product/<str:pk>/', views.product, name="product"),  #後面的name="???" 是指在HTML的代號, 原則上寫一樣就好/
    path('addtocart/<str:pk>/',views.addtocart,name="addtocart"),
    path('addcart/', views.addcart,name='product'),   
    
    
    path('cart/', views.cart),
    path('removecart/',views.removecart),
    path('checkout/',views.checkout),
    path('addorder/',views.addorder),
    path('getorder/<str:pk>/',views.getorder,name="getorder"),
    
    # 裁切照片的小工具
    path('cutphoto/', cutphoto),
    path('cutphoto/<str:pk>/', cutphotos, name="cutphoto"),

    path('adminlistpro/',views.adminlistpro),
    path('adminformpro/<str:pk>/', views.adminformpro,name="adminformpro"),
    path('adminupdatepro/',views.adminupdatepro),
    path('adminuploadphoto/<str:pk>/',views.adminuploadphoto,name="adminuploadphoto"),

    path('adminlistorder/',views.adminlistorder),
    path('admindelorder/<str:pk>/', views.admindelorder,name="admindelorder"),
    path('adminlistordersearch1/',views.adminlistordersearch1),
    path('adminlistordersearch2/',views.adminlistordersearch2),
    path('adminformorder/<str:pk>/',views.adminformorder,name="adminformorder"),
    path('adminupdateorder/',views.adminupdateorder),

    path('mknitshop/',views.mknitshop),
    path('mario/',views.mario),
    path('fishing/',views.fishing),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# 後面這段很重要, 上傳圖片到資料庫會放在media資料夾, 不加會無法正常顯示圖面


# 如果 Models.py 的資料庫有做修改, 必須同步
# >> python3 manage.py makemigrations
# >> python3 manage.py migrate
