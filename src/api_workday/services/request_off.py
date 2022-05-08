import datetime

from api_base.services import BaseService
from api_office.models import Department, Office
from api_team.models import Team
from api_user.models.profile import Profile
from api_workday.models.date_off import DateOff
from api_workday.models.leave_type import LeaveType
from api_workday.models.remain_leave import RemainLeave
from api_workday.models.request_off import RequestOff
from api_workday.serializers.date_off import DateOffSerializer
from api_workday.serializers.request_off import RequestOffSerializer
from api_workday.services.action_request import ActionRequestService
from api_workday.services.send_mail import SendMailRequestOff
from api_workday.services.send_notification_slack import SendNotificationSlack
from common.constants.workday_constants.date import Workday
from django.db import transaction
from django.db.models import Sum


class RequestOffServices(BaseService):
    @classmethod
    def create_request_off(cls, request_data, profile, is_sync_leave_request=False):
        if profile.office is not None:
            office = Office.objects.filter(pk=profile.office.id).first()
        else:
            team = Team.objects.filter(team__member=profile.user.id).first()
            office = team.office
            if office is None:
                department = Department.objects.filter(team=team.office_id).first()
                office = (
                    department.office
                    if department.office is not None
                    else Office.objects.all().first()
                )

        profile_manager = Profile.objects.filter(user=office.manager).first()
        if (
            profile.line_manager is None
            and profile.maximum_level_approved != 0
            and profile_manager is None
        ):
            return {
                "error": "You don't have any line manger, neither the maximum level and office's manager, office manager is also not found!"
            }

        leave_type_id = request_data.get("type_id")
        leave_type = LeaveType.objects.filter(id=leave_type_id).first()
        list_date_obj = request_data["date"]

        # Check condition of all date off
        if cls.check_out_of_join_date(request_data, profile.id):
            return {"error": "There was a request for out of join date"}
        elif cls.check_available_date_off(request_data, profile.id):
            return {"error": "There was a request for over available day!"}
        elif cls.check_overlap_date(list_date_obj, profile.id):
            return {"error": "There was a request for this date!"}

        # Save data in request_off
        request_off_data = {
            "reason": request_data["reason"],
            "total": request_data["total_leaves"],
        }
        request_off_serializer = RequestOffSerializer(data=request_off_data)
        with transaction.atomic():
            if request_off_serializer.is_valid():
                request_off = request_off_serializer.save(
                    leave_type=leave_type, profile=profile
                )
            request_off_id = request_off.id

            # Save data in date_off
            for date in list_date_obj:
                date_off_data = {
                    "date": date["date"],
                    "type": date["type"],
                    "lunch": date["lunch"],
                    "request_off": request_off_id,
                }
                date_off_serializer = DateOffSerializer(data=date_off_data)
                if date_off_serializer.is_valid():
                    date_off_serializer.save(request_off=request_off)

            if is_sync_leave_request:
                ActionRequestService.create_action_user(request_off, profile)
                ActionRequestService.action_approve(
                    request_off.id,
                    profile,
                    comment="OK",
                    is_sync_leave_request=is_sync_leave_request,
                )
            else:
                # Check and send request to line manager
                if profile.line_manager is not None:
                    ActionRequestService.create_action_user(
                        request_off, profile.line_manager
                    )
                    SendMailRequestOff.send_request(
                        leave_type=leave_type,
                        name_admin=profile.line_manager.name,
                        name_user=request_off.profile.name,
                        list_email=[profile.line_manager.user.email],
                        date_off=request_off.date_off.all(),
                    )
                    SendNotificationSlack.send_notification_request_off(
                        profile=profile,
                        request_off_data=dict(
                            list_dates=list_date_obj,
                            leave_type_id=leave_type_id,
                            reason=request_off_data.get("reason"),
                            date_quantity=str(request_off_data.get("total")),
                            request_off_id=request_off_id,
                        ),
                    )
                elif profile.maximum_level_approved == 0:
                    ActionRequestService.create_action_user(request_off, profile)
                    ActionRequestService.action_approve(
                        request_off.id, profile, comment="OK"
                    )
                else:
                    ActionRequestService.create_action_user(
                        request_off, profile_manager
                    )
                    SendMailRequestOff.send_request(
                        leave_type=leave_type,
                        name_admin=profile_manager.name,
                        name_user=request_off.profile.name,
                        list_email=[profile_manager.user.email],
                        date_off=request_off.date_off.all(),
                    )
        return request_off_serializer.data

    @classmethod
    def check_overlap_date(cls, list_date_obj, profile_id):
        status = [Workday.STATUS_REJECTED, Workday.STATUS_CANCEL]
        for date_obj in list_date_obj:
            date_off = (
                DateOff.objects.filter(date=date_obj["date"])
                .filter(request_off__profile_id=profile_id)
                .exclude(request_off__status__in=status)
            )
            if date_off.exists():
                return True
        return False

    @classmethod
    def check_out_of_join_date(cls, data, profile_id):
        profile = Profile.objects.filter(id=profile_id).first()
        if profile:
            for date_off in data["date"]:
                date_time_obj = datetime.datetime.strptime(
                    date_off["date"], "%Y-%m-%d"
                ).date()
                if date_time_obj < profile.join_date:
                    return True
        return False

    @classmethod
    def get_expired_annual_leave_last_year_in_office_settings(cls):
        office = Office.objects.all().first()
        if office:
            return office.expired_annual_leave_last_year
        return 8

    @classmethod
    def get_the_number_of_days_off(cls, list_date_off):
        date_leave = 0
        for date_off in list(list_date_off):
            try:
                if date_off["type"] == Workday.FULL:
                    date_leave += 1
                else:
                    date_leave += 0.5
            except Exception:
                if date_off.type == Workday.FULL:
                    date_leave += 1
                else:
                    date_leave += 0.5
        return date_leave

    @classmethod
    def get_list_date_off_by_year(cls, data):
        now = datetime.datetime.now().year
        month_check = cls.get_expired_annual_leave_last_year_in_office_settings()
        list_date_leave_last_year_after_month_reset = []
        list_date_leave_last_year = []
        list_date_leave_current_year_after_month_reset = []
        list_date_leave_current_year = []
        list_date_leave_next_year_after_month_reset = []
        list_date_leave_next_year = []
        for date_off in data["date"]:
            date_time_obj = datetime.datetime.strptime(
                date_off["date"], "%Y-%m-%d"
            ).date()
            if date_time_obj.year == now + 1:
                list_date_leave_next_year.append(date_off)
                if date_time_obj.month >= month_check:
                    list_date_leave_next_year_after_month_reset.append(date_off)
            if date_time_obj.year == now:
                list_date_leave_current_year.append(date_off)
                if date_time_obj.month >= month_check:
                    list_date_leave_current_year_after_month_reset.append(date_off)
            if date_time_obj.year == now - 1:
                list_date_leave_last_year.append(date_off)
                if date_time_obj.month >= month_check:
                    list_date_leave_last_year_after_month_reset.append(date_off)
        return {
            "last_year": list_date_leave_last_year,
            "current_year": list_date_leave_current_year,
            "next_year": list_date_leave_next_year,
            "last_year_month": list_date_leave_last_year_after_month_reset,
            "current_year_month": list_date_leave_current_year_after_month_reset,
            "next_year_month": list_date_leave_next_year_after_month_reset,
        }

    @classmethod
    def get_list_date_left_by_year(cls, list_id_request):
        now = datetime.datetime.now().year
        month_check = cls.get_expired_annual_leave_last_year_in_office_settings()
        list_date = DateOff.objects.filter(request_off__in=list_id_request)
        list_date_off_last_year = list_date.filter(date__year=now - 1)
        list_date_off_last_year_after_month_reset = list_date_off_last_year.filter(
            date__month__gte=month_check
        )
        list_date_off_current_year = list_date.filter(date__year=now)
        list_date_off_current_year_after_month_reset = (
            list_date_off_current_year.filter(date__month__gte=month_check)
        )
        list_date_off_next_year = list_date.filter(date__year=now + 1)
        list_date_off_next_year_after_month_reset = list_date_off_next_year.filter(
            date__month__gte=month_check
        )
        return {
            "last_year": list_date_off_last_year,
            "current_year": list_date_off_current_year,
            "next_year": list_date_off_next_year,
            "last_year_month": list_date_off_last_year_after_month_reset,
            "current_year_month": list_date_off_current_year_after_month_reset,
            "next_year_month": list_date_off_next_year_after_month_reset,
        }

    @classmethod
    def check_date_off_with_remain_leave(
        cls, total_date, total_date_after, year, profile_id
    ):
        remain = RemainLeave.objects.filter(profile=profile_id, year=year).first()
        if remain:
            if total_date_after > remain.current_days_off:
                return True
            if total_date > remain.current_days_off + remain.annual_leave_last_year:
                return True
        return False

    @classmethod
    def check_available_date_off(cls, data, profile_id):
        now = datetime.datetime.now().year
        status = [Workday.STATUS_PENDING, Workday.STATUS_FORWARDED]
        list_id_request = RequestOff.objects.filter(
            profile_id=profile_id, status__in=status
        )

        date_off = cls.get_list_date_left_by_year(list_id_request)

        list_date_off_last_year = date_off.get("last_year")
        list_date_off_current_year = date_off.get("current_year")
        list_date_off_next_year = date_off.get("next_year")
        list_date_off_last_year_after_month_reset = date_off.get("last_year_month")
        list_date_off_current_year_after_month_reset = date_off.get(
            "current_year_month"
        )
        list_date_off_next_year_after_month_reset = date_off.get("next_year_month")

        date_leave = cls.get_list_date_off_by_year(data)

        list_date_leave_last_year = date_leave.get("last_year")
        list_date_leave_current_year = date_leave.get("current_year")
        list_date_leave_next_year = date_leave.get("next_year")
        list_date_leave_last_year_after_month_reset = date_leave.get("last_year_month")
        list_date_leave_current_year_after_month_reset = date_leave.get(
            "current_year_month"
        )
        list_date_leave_next_year_after_month_reset = date_leave.get("next_year_month")

        total_date_last_year = cls.get_the_number_of_days_off(
            list_date_off_last_year
        ) + cls.get_the_number_of_days_off(list_date_leave_last_year)

        total_date_current_year = cls.get_the_number_of_days_off(
            list_date_off_current_year
        ) + cls.get_the_number_of_days_off(list_date_leave_current_year)

        total_date_next_year = cls.get_the_number_of_days_off(
            list_date_off_next_year
        ) + cls.get_the_number_of_days_off(list_date_leave_next_year)

        total_date_last_year_after_month_reset = cls.get_the_number_of_days_off(
            list_date_off_last_year_after_month_reset
        ) + cls.get_the_number_of_days_off(list_date_leave_last_year_after_month_reset)

        total_date_current_year_after_month_reset = cls.get_the_number_of_days_off(
            list_date_off_current_year_after_month_reset
        ) + cls.get_the_number_of_days_off(
            list_date_leave_current_year_after_month_reset
        )

        total_date_next_year_after_month_reset = cls.get_the_number_of_days_off(
            list_date_off_next_year_after_month_reset
        ) + cls.get_the_number_of_days_off(list_date_leave_next_year_after_month_reset)

        if cls.check_date_off_with_remain_leave(
            total_date_last_year,
            total_date_last_year_after_month_reset,
            now - 1,
            profile_id,
        ):
            return True
        if cls.check_date_off_with_remain_leave(
            total_date_current_year,
            total_date_current_year_after_month_reset,
            now,
            profile_id,
        ):
            return True
        if cls.check_date_off_with_remain_leave(
            total_date_next_year,
            total_date_next_year_after_month_reset,
            now + 1,
            profile_id,
        ):
            return True
        return False

    @classmethod
    def total_off_by_leave_types(cls, profile_id, leave_type_id, year):
        request_offs = {"total_date_off": 0}
        if profile_id and leave_type_id:
            request_offs = RequestOff.objects.filter(
                profile__id=profile_id,
                leave_type__id=leave_type_id,
                status=Workday.STATUS_APPROVED,
                created_at__year=year,
            ).aggregate(total_date_off=Sum("total"))

            if request_offs["total_date_off"] is None:
                request_offs = {"total_date_off": 0}

        return {"total_leaves": request_offs["total_date_off"]}

    @classmethod
    def get_request_off_by_id(cls, request_off_id):
        return RequestOff.objects.filter(pk=request_off_id).first()

    @classmethod
    def get_pending_request_off(cls, profile_id):
        return RequestOff.objects.filter(
            profile_id=profile_id, status=Workday.STATUS_PENDING
        )
