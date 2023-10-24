from django.contrib import admin
from django.urls import path
from counters_app.views import counter_picks, index, meta


urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('counter_picks/', counter_picks, name='counter_picks'),
    path('meta/', meta, name='meta'),
]
