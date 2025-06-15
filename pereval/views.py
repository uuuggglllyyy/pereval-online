from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Pereval
from .serializers import PerevalSerializer
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.generics import ListAPIView


class SubmitDataView(APIView):
    def post(self, request):
        serializer = PerevalSerializer(data=request.data)
        if serializer.is_valid():
            pereval = serializer.save()
            return Response({
                'status': status.HTTP_200_OK,
                'message': 'Данные успешно добавлены',
                'id': pereval.id
            }, status=status.HTTP_200_OK)
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': serializer.errors,
            'id': None
        }, status=status.HTTP_400_BAD_REQUEST)

class PerevalDetailView(RetrieveAPIView):
    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializer


class PerevalUpdateView(UpdateAPIView):
    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializer

    def patch(self, request, *args, **kwargs):
        pereval = self.get_object()
        if pereval.status != 'new':
            return Response(
                {'state': 0, 'message': 'Запись нельзя редактировать, так как её статус не "new"'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Запрещаем изменение данных пользователя
        user_data = request.data.pop('user', None)
        if user_data:
            return Response(
                {'state': 0, 'message': 'Нельзя изменять данные пользователя'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().patch(request, *args, **kwargs)

class UserPerevalsListView(ListAPIView):
    serializer_class = PerevalSerializer

    def get_queryset(self):
        email = self.request.query_params.get('user__email', None)
        if email:
            return Pereval.objects.filter(user__email=email)
        return Pereval.objects.none()

class UserPerevalListView(ListAPIView):  # Добавленный класс
    serializer_class = PerevalSerializer

    def get_queryset(self):
        email = self.request.query_params.get('email')
        if email:
            return Pereval.objects.filter(user__email=email)
        return Pereval.objects.none()