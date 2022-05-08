from api_base.views import BaseViewSet
from api_wfh.models.wfh_date import WfhDate
from api_wfh.models.wfh_request import WfhRequest
from api_wfh.serializers.wfh_request import WfhRequestSerializer
from api_wfh.services.wfh_request import WfhRequestServices
from api_workday.services.action_request import FilterRequestServices
from common.constants.api_constants import HttpMethod
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class WfhRequestViewSet(BaseViewSet):
    queryset = WfhRequest.objects.all()
    pagination_class = None
    serializer_class = WfhRequestSerializer
    required_alternate_scopes = {}

    def get_request(self, request, wfh_request):
        year = request.query_params.get("year")
        month = request.query_params.get("month")
        day = request.query_params.get("day")
        search = request.query_params.get("search")
        wfh_request = FilterRequestServices.filter_multipart(
            WfhDate, wfh_request, year, month, day, search
        )
        return wfh_request

    def list(self, request, *args, **kwargs):
        """
        Only use for admin
        """
        wfh_request = self.queryset.all().order_by("-created_at")
        data = WfhRequestSerializer(
            self.get_request(request, wfh_request), many=True
        ).data
        return Response(data)

    @action(methods=[HttpMethod.GET], detail=False)
    def list_request_user(self, request, *args, **kwargs):
        user = request.user
        wfh_request = self.queryset.filter(user=user).order_by("-created_at")
        data = WfhRequestSerializer(
            self.get_request(request, wfh_request), many=True
        ).data
        return Response(data)

    def create(self, request, *args, **kwargs):
        data = request.data
        user = request.user

        response = WfhRequestServices.create_wfh_request(data=data, user=user)

        if "error" in response:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(response, status=status.HTTP_201_CREATED)
