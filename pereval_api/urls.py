from django.contrib import admin
from django.urls import path
from pereval.views import SubmitDataView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('submitData/', SubmitDataView.as_view(), name='submit-data'),
]
