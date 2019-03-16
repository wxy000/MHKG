from django.urls import path

from . import taggingData_view
from . import taggingDataGet_view
from . import views

# 正在部署的应用的名称
app_name = 'ManualAnnotation'

urlpatterns = [
    path('', taggingDataGet_view.tagging_push),
    path('tagging_data/', taggingData_view.show),
    path('tagging-get/', taggingDataGet_view.tagging_push),
]
