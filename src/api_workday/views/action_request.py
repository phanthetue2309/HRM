from api_base.views import BaseViewSet
from api_workday.models.remain_leave import RemainLeave
from api_workday.models.request_detail import RequestDetail
from api_workday.models.request_off import RequestOff
from api_workday.serializers.action_request import RequestDetailSerializer
from api_workday.services.action_request import (
    ActionRequestService,
    FilterActionRequestServices,
)
from common.constants.api_constants import HttpMethod
from common.constants.workday_constants.date import Workday
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class ActionRequestDetailViewSet(BaseViewSet):
    queryset = RequestDetail.objects.all()
    serializer_class = RequestDetailSerializer
    required_alternate_scopes = {"destroy_multi_request": [["request_off:delete"]]}

    def create(self, request, *args, **kwargs):
        ActionRequestService.do_multi_action_request(request)
        return Response(f"{request.data.get('action')} success!")

    def get_request(self, request):
        profile = request.user.profile
        queryset = self.queryset.filter(approve=profile).order_by("-created_at")
        year = request.query_params.get("year")
        month = request.query_params.get("month")
        day = request.query_params.get("day")
        status_request = request.query_params.get("status")
        search = request.query_params.get("search")
        queryset = FilterActionRequestServices.filter_multipart(
            queryset, year, month, day, search, status_request
        )
        return queryset

    @action(methods=[HttpMethod.GET], detail=False)
    def get_request_detail(self, request, *args, **kwargs):
        data = RequestDetailSerializer(self.get_request(request), many=True).data
        return Response(data)

    @action(methods=[HttpMethod.GET], detail=False)
    def count(self, request, *args, **kwargs):
        count = ActionRequestService.count_request(request.user.profile)
        data = {"count": count}
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=[HttpMethod.POST], detail=False, url_path="multi")
    def destroy_multi_request(self, request):
        request_off_ids = request.data.get("request_off_ids")
        if request_off_ids:
            queryset = RequestOff.objects.filter(id__in=request_off_ids)
            date_off_profile = {}
            request_off_approved = queryset.filter(
                status=Workday.STATUS_APPROVED
            ).select_related("profile")

            for request_off in request_off_approved:
                off_day_count = request_off.total
                profile_id = request_off.profile.id
                date_off_profile.update(
                    {
                        str(profile_id): date_off_profile.get(str(profile_id), 0)
                        + off_day_count
                    }
                )
            queryset.delete()
            list_profile_id = date_off_profile.keys()
            bulk_update_data = RemainLeave.objects.filter(profile__in=list_profile_id)
            for remain_leave in bulk_update_data:
                old_current_days_off = remain_leave.current_days_off
                profile_id = remain_leave.profile_id
                new_current_days_off = old_current_days_off + date_off_profile.get(
                    str(profile_id)
                )
                remain_leave.current_days_off = new_current_days_off
            RemainLeave.objects.bulk_update(bulk_update_data, ["current_days_off"])

            return Response("Delete Success!", status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
