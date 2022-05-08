import datetime

from api_base.services import BaseService
from api_office.models import Holiday
from api_workday.models import LeaveType, RemainLeave
from api_workday.models.date_off import DateOff
from api_workday.serializers.date_off import DateOffSerializer
from api_workday.serializers.profile_detail import ProfileDetailSerizlizer
from common.constants.workday_constants import Workday
from django.db.models import Q


class StatisticServices(BaseService):
    @classmethod
    def get_holidays(cls, month, year, office):
        holidays = Holiday.objects.filter(
            end_date__year=year, end_date__month=month, office=office
        ).values_list("start_date", "end_date")
        total = 0
        for holiday in holidays:
            total += (int((holiday[1] - holiday[0]).days)) + 1
        return total

    @classmethod
    def get_the_number_of_days_off(cls, list_date_off):
        date_leave = 0
        for date_off in list_date_off:
            if date_off.get("type") == Workday.FULL:
                date_leave += 1
            else:
                date_leave += 0.5
        return date_leave

    @classmethod
    def get_dynamic_type_for_statistic(cls, month, date_off_full):
        data = {}
        leave_types = LeaveType.objects.all().values_list("name", flat=True)
        if not leave_types.exists():
            return data
        date_off_in_month = date_off_full.filter(date__month=month)
        serializer_date = DateOffSerializer(date_off_in_month, many=True)
        list_date_off = [
            {
                "date": date.get("date"),
                "type": date.get("type"),
                "lunch": date.get("lunch"),
                "leave_type_name": date.get("request_off").get("type_name"),
            }
            for date in serializer_date.data
        ]
        for leave_type in leave_types:
            detail = []
            for detail_date_off in list_date_off:
                if detail_date_off.get("leave_type_name") == leave_type:
                    detail.append(detail_date_off)
            data[leave_type] = detail
        return data

    @classmethod
    def get_date_off_for_statistic_user_dynamic(cls, year, profile):
        data = []
        try:
            year = int(year)
        except Exception:
            return data
        if year not in range(profile.join_date.year, datetime.datetime.now().year + 1):
            return data
        start_month = Workday.FIRST_MONTH + 1
        if year == profile.join_date.year:
            start_month = profile.join_date.month
        date_off_full_in_year = DateOff.objects.filter(
            request_off__status=Workday.STATUS_APPROVED,
            request_off__profile=profile,
            date__year=year,
        )
        remain = RemainLeave.objects.filter(profile=profile, year=year).first()
        if remain is None:
            return data
        leave_types = LeaveType.objects.all().values_list("name", flat=True)
        if not leave_types.exists():
            return data
        for month in range(start_month, Workday.LAST_MONTH + 1):
            details = cls.get_dynamic_type_for_statistic(month, date_off_full_in_year)
            profile_date = {
                "profile_id": profile.id,
                "month": month,
                "holidays": cls.get_holidays(
                    month=month, year=year, office=profile.office
                ),
                "annual_leave": remain.annual_leave,
                "current_days_off": remain.current_days_off,
                "annual_leave_last_year": remain.annual_leave_last_year,
                "join_date": profile.join_date,
            }
            for leave_type in leave_types:
                profile_date[leave_type] = details[leave_type]
                profile_date[f"number_{leave_type}"] = cls.get_the_number_of_days_off(
                    details[leave_type]
                )
            data.append(profile_date)
        return data

    @classmethod
    def get_date_off_for_statistic_admin_dynamic(
        cls, name, email, month, year, profile, type_par
    ):
        data = []
        try:
            year = int(year)
            month = int(month)
        except Exception:
            return data
        if name is not None:
            profile = profile.filter(Q(name__icontains=name))
        if email is not None:
            profile = profile.filter(Q(user__email__icontains=email))
        if year > datetime.datetime.now().year or month > Workday.LAST_MONTH:
            return data
        leave_types = list(LeaveType.objects.all().values_list("name", flat=True))
        if not leave_types:
            return data
        for profile_id in profile:
            if year in range(
                profile_id.join_date.year, datetime.datetime.now().year + 1
            ):
                if year == profile_id.join_date.year:
                    date_off_full_in_year = DateOff.objects.filter(
                        request_off__status=Workday.STATUS_APPROVED,
                        request_off__profile=profile_id,
                        date__year=year,
                    )
                    if month >= profile_id.join_date.month:
                        details = cls.get_dynamic_type_for_statistic(
                            month, date_off_full_in_year
                        )
                    else:
                        continue
                else:
                    date_off_full_in_year = DateOff.objects.filter(
                        request_off__status=Workday.STATUS_APPROVED,
                        request_off__profile=profile_id,
                        date__year=year,
                    )
                    details = cls.get_dynamic_type_for_statistic(
                        month, date_off_full_in_year
                    )
                serializer_profile = ProfileDetailSerizlizer(profile_id)
                remain = RemainLeave.objects.filter(
                    profile=profile_id, year=year
                ).first()
                if remain is None:
                    continue
                profile_date = {
                    "id": profile_id.id,
                    "name": profile_id.name,
                    "email": serializer_profile.data.get("user").get("email"),
                    "holidays": cls.get_holidays(
                        month=month, year=year, office=profile_id.office
                    ),
                }
                for leave_type in leave_types:
                    if type_par:
                        profile_date[type_par] = details[type_par]
                        profile_date[
                            f"number_{type_par}"
                        ] = cls.get_the_number_of_days_off(details[type_par])
                    else:
                        profile_date[leave_type] = details[leave_type]
                        profile_date[
                            f"number_{leave_type}"
                        ] = cls.get_the_number_of_days_off(details[leave_type])
                data.append(profile_date)
            else:
                continue
        return data

    @classmethod
    def get_total_date_off_year_by_team(cls, year, profiles):
        data = []
        try:
            year = int(year)
        except Exception:
            return data
        for profile in profiles:
            profile_data = cls.get_date_off_for_statistic_user_dynamic(
                year=year, profile=profile
            )
            data.append(profile_data)
        return data
