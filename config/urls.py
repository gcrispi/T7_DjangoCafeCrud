"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
# incorporar las rutas de la aplicación ticafe
# a la configuración de URLs del proyecto, lo que permite que las solicitudes
# a las URL definidas en ticafe sean manejadas correctamente por las vistas correspondientes.

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("ticafe.urls")),
]

# Configuracion necesaria para servir archivos estáticos
# y de medios durante el desarrollo, lo que permite que las imágenes y
# otros archivos asociados a los modelos se muestren correctamente en la aplicación.
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # en camdo producción
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
