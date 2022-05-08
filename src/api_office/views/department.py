from api_base.views import BaseViewSet
from api_office.models import Department
from api_office.serializers import DepartmentSerializer
from common.constants.api_constants import HttpMethod
from rest_framework.decorators import action
from rest_framework.response import Response


class DepartmentViewSet(BaseViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    required_alternate_scopes = {
        "create": [["office:edit"]],
        "retrieve": [["office:view"]],
        "update": [["office:edit"]],
        "destroy": [["office:edit"]],
        "list": [["office:view"]],
    }

    @action(methods=[HttpMethod.GET], detail=False)
    def get_all(self, request, *args, **kwargs):
        return Response(self.get_queryset().values("id", "name"))
