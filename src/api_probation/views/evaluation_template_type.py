from api_base.views import BaseViewSet
from api_probation.models.evaluation_template_type import EvaluationTemplateType
from api_probation.serializers.evaluation_template_type import (
    EvaluationTemplateTypeSerializer,
)
from rest_framework import status
from rest_framework.response import Response


class EvaluationTemplateTypeViewSet(BaseViewSet):
    queryset = EvaluationTemplateType.objects.all()
    serializer_class = EvaluationTemplateTypeSerializer
    pagination_class = None
    required_alternate_scopes = dict()

    def create(self, request, *args, **kwargs):
        serializer = EvaluationTemplateTypeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {"message": "Create Type Evaluation Template Failed"},
            status=status.HTTP_400_BAD_REQUEST,
        )
