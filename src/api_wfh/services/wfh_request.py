import datetime

from api_base.services import BaseService
from api_user.models.user import User
from api_wfh.models.wfh_date import WfhDate
from api_wfh.models.wfh_request import WfhRequest
from api_wfh.serializers.wfh_date import WfhDateSerializer
from api_wfh.serializers.wfh_request import WfhRequestSerializer
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response


class WfhRequestServices(BaseService):
    @classmethod
    def create_wfh_request(cls, data, user):
        if cls.check_out_of_join_date(data, user.id):
            return Response(
                {"error": "There was a request for out of join date"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if cls.check_overlap_date(data, user.id):
            return Response(
                {"error": "There was a request for this date!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        request_data = {"reason": data["reason"], "total": data["wfh_total"]}
        wfh_request_serializer = WfhRequestSerializer(data=request_data)
        with transaction.atomic():
            if wfh_request_serializer.is_valid():
                wfh_request = wfh_request_serializer.save(user=user)
            request_id = wfh_request_serializer.data["id"]
            for date in data["date"]:
                date_data = {
                    "date": date["date"],
                    "lunch": date["lunch"],
                    "wfh_request": request_id,
                }
                wfh_date_serializer = WfhDateSerializer(data=date_data)
                if wfh_date_serializer.is_valid():
                    wfh_date_serializer.save(wfh_request=wfh_request)

        return wfh_date_serializer.data

    @classmethod
    def check_overlap_date(cls, data, user_id):
        list_id_request = WfhRequest.objects.filter(user_id=user_id).values_list(
            "id", flat=True
        )
        list_dates = [date.get("date") for date in data.get("date")]
        wfh_date = WfhDate.objects.filter(
            date__in=list_dates, wfh_request_id__in=list_id_request
        )
        if wfh_date.exists():
            return True
        return False

    @classmethod
    def check_out_of_join_date(cls, data, user_id):
        user = User.objects.filter(id=user_id).first()
        if user:
            for date_wfh in data["date"]:
                date_time_obj = datetime.datetime.strptime(
                    date_wfh["date"], "%Y-%m-%d"
                ).date()
                if date_time_obj < user.timestamp.date():
                    return True
        return False
