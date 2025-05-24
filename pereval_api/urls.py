from django.urls import path
from pereval.views import SubmitDataView, PerevalDetailView, PerevalUpdateView, UserPerevalsListView

urlpatterns = [
    path('submitData/', SubmitDataView.as_view(), name='submit-data'),
    path('submitData/<int:pk>/', PerevalDetailView.as_view(), name='pereval-detail'),
    path('submitData/<int:pk>/update/', PerevalUpdateView.as_view(), name='pereval-update'),
    path('submitData/user/', UserPerevalsListView.as_view(), name='user-perevals'),
]