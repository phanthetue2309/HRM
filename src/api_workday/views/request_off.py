from api_base.views import BaseViewSet
from api_workday.models import DateOff
from api_workday.models.request_off import RequestOff
from api_workday.serializers.request_off import RequestOffSerializer
from api_workday.services.action_request import FilterRequestServices
from api_workday.services.request_off import RequestOffServices
from common.constants.api_constants import HttpMethod
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class RequestOffViewSet(BaseViewSet):
    queryset = RequestOff.objects.all()
    pagination_class = None
    serializer_class = RequestOffSerializer
    required_alternate_scopes = {
        "create": [["request_off:edit"]],
        "retrieve": [["request_off:view"]],
        "update": [["request_off:edit"]],
        "destroy": [["request_off:edit"]],
        "list": [["request_off:admin"]],
        "list_request_user": [["request_off:view"]],
        "count_type_off_days": [["request_off:edit"]],
    }

    @staticmethod
    def get_request(request, request_off):
        year = request.query_params.get("year")
        month = request.query_params.get("month")
        day = request.query_params.get("day")
        status_request = request.query_params.get("status")
        search = request.query_params.get("search")
        request_off = FilterRequestServices.filter_multipart(
            DateOff, request_off, year, month, day, status_request, search
        )
        return request_off

    def list(self, request, *args, **kwargs):
        """
        Only use for admin
        """
        request_off = self.queryset.all().order_by("-created_at")
        data = RequestOffSerializer(
            self.get_request(request, request_off), many=True
        ).data
        return Response(data)

    @action(methods=[HttpMethod.GET], detail=False)
    def list_request_user(self, request, *args, **kwargs):
        profile = request.user.profile
        request_off = self.queryset.filter(profile=profile).order_by("-created_at")
        data = RequestOffSerializer(
            self.get_request(request, request_off), many=True
        ).data
        return Response(data)

    def create(self, request, *args, **kwargs):
        data = request.data
        profile = request.user.profile

        response = RequestOffServices.create_request_off(
            request_data=data, profile=profile
        )

        if "error" in response:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(response, status=status.HTTP_201_CREATED)

    @action(methods=[HttpMethod.GET], detail=False)
    def total_off_by_types(self, request, *args, **kwargs):
        """
        Get total date off of type off in year
        """
        profile_id = request.query_params.get("profile")
        leave_type_id = request.query_params.get("leave_type")
        year = request.query_params.get("year")
        data = RequestOffServices.total_off_by_leave_types(
            profile_id=profile_id, leave_type_id=leave_type_id, year=year
        )
        return Response(data)
