from django.urls import re_path
from .views import ProxyView

app_name = "newsapp"

urlpatterns = [
    re_path(r'^(?P<path>.*)$', ProxyView.as_view()),  # все запросы перенаправляются на ProxyView
]
