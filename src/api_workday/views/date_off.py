from api_base.views.base import BaseViewSet
from api_workday.models.date_off import DateOff
from api_workday.serializers.date_off import DateOffSerializer
from rest_framework import status
from rest_framework.response import Response


class DateOffViewSet(BaseViewSet):
    queryset = DateOff.objects.all()
    serializer_class = DateOffSerializer

    def create(self, request, *args, **kwargs):
        serializer = DateOffSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
