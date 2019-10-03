from django.contrib import admin
from django.urls import path
from produtos import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('produtos/<int:pk>', views.produto_detalhe, name="detalhe")
]
