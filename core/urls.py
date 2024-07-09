from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path

def login_page(request):
    return redirect('admin:login')

urlpatterns = [
    path('', login_page),
    path('admin/', admin.site.urls),
    path('results/', include('result.urls'))
]
