from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("main_app.api.urls", "post_api")),
    path("api/account/", include("account.api.urls", "account_api")),
]
