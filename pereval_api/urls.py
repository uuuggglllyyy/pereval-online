from django.urls import path
from pereval.views import (SubmitDataView, PerevalDetailView,
                    PerevalUpdateView, UserPerevalListView)

urlpatterns = [
    path('submitData/', SubmitDataView.as_view(), name='submit-data'),
    path('submitData/<int:pk>/', PerevalDetailView.as_view(), name='pereval-detail'),
    path('submitData/<int:pk>/', PerevalUpdateView.as_view(), name='pereval-update'),
    path('submitData/', UserPerevalListView.as_view(), name='user-perevals-list'),
]