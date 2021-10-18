from django.contrib import admin
from django.urls import path
from apollo import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('api/reply/<str:query>/', views.bot_search, name="search")
]
