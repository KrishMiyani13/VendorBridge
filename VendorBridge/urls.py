from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('vendors/', include('vendors.urls')),
    path('rfq/', include('rfq.urls')),
    path('quotations/', include('quotations.urls')),
    path('approvals/', include('approvals.urls')),
    path('procurement/', include('procurement.urls')),
    path('analytics/', include('analytics_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
