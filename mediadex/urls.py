from django.urls import path

from .views import home, explorer

app_name = "mediadex"

urlpatterns = [
    path('', home.index, name="index"),
    path('explorer', explorer.explorer_home, name="explorer_home"),
    path('explorer/sources/<str:source_name>/', explorer.explorer_source, name="sources")
]
