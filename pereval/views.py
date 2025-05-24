from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .models import Pereval
from .serializers import PerevalSerializer


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


class PerevalDetailView(APIView):
    def get(self, request, pk):
        pereval = get_object_or_404(Pereval, pk=pk)
        serializer = PerevalSerializer(pereval)
        return Response(serializer.data)


class PerevalUpdateView(APIView):
    def patch(self, request, pk):
        pereval = get_object_or_404(Pereval, pk=pk)

        if pereval.status != 'new':
            return Response({
                'state': 0,
                'message': 'Редактирование запрещено: запись уже прошла модерацию'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Проверка изменения пользовательских данных
        if 'user' in request.data:
            user_data = request.data['user']
            original_user = {
                'email': pereval.user.email,
                'fam': pereval.user.fam,
                'name': pereval.user.name,
                'otc': pereval.user.otc,
                'phone': pereval.user.phone
            }
            if user_data != original_user:
                return Response({
                    'state': 0,
                    'message': 'Редактирование персональных данных запрещено'
                }, status=status.HTTP_400_BAD_REQUEST)

        serializer = PerevalSerializer(pereval, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'state': 1,
                'message': None
            })
        return Response({
            'state': 0,
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class UserPerevalsListView(APIView):
    def get(self, request):
        email = request.query_params.get('user__email')
        if not email:
            raise ValidationError("Не указан email пользователя")

        perevals = Pereval.objects.filter(user__email=email)
        serializer = PerevalSerializer(perevals, many=True)
        return Response(serializer.data)