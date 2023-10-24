from django.contrib import admin
from django.urls import path
from counters_app.views import counter_picks


urlpatterns = [
    path('admin/', admin.site.urls),
    path('counter_picks/', counter_picks, name='counter_picks'),
]
