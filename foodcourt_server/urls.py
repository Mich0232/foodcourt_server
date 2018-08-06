from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

urlpatterns = [
    path('', include('core.urls')),
    path('api/', include('api.urls', namespace='api')),
    path('api/login/', TokenObtainPairView.as_view(), name='api-login'),
    path('api/refresh/', TokenRefreshView.as_view(), name='api-refresh'),
    path('admin/', admin.site.urls),

]
