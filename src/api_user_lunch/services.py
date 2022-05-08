import datetime
from calendar import monthrange

from api_user_lunch.models import UserLunch
from lunarcalendar import Converter, Solar


class UserLunchServices:
    @classmethod
    def get_users_lunch(cls, profile):
        users_lunch = UserLunch.objects.filter(profile=profile)
        if not users_lunch.exists():
            return []
        return users_lunch

    @classmethod
    def create(cls, serializer, profile, date):
        today = datetime.date.today()
        convert_to_datetime = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        week_day = convert_to_datetime.weekday()
        if cls.is_weekday(day=week_day):
            raise Exception("Cant set lunch at weekend")
        if datetime.datetime.strptime(
            str(today), "%Y-%m-%d"
        ) <= datetime.datetime.strptime(str(date), "%Y-%m-%d"):
            if UserLunch.objects.filter(date=date, profile=profile).exists():
                raise Exception(f"user_lunch have been created with date {date}")
            return serializer.save(profile=profile)
        raise Exception("Create Error")

    @classmethod
    def create_many(cls, data, list_dates, profile):
        list_user_lunches = []
        if not list_dates:
            raise Exception("list_dates are empty")
        today = datetime.date.today()
        for date in list_dates:
            convert_to_datetime = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            week_day = convert_to_datetime.weekday()
            if cls.is_weekday(day=week_day):
                continue
            if datetime.datetime.strptime(
                str(today), "%Y-%m-%d"
            ) <= datetime.datetime.strptime(str(date), "%Y-%m-%d"):
                user_lunch = UserLunch.objects.filter(date=date, profile=profile)
                if not user_lunch.exists():
                    list_user_lunches.append(
                        UserLunch(
                            date=date,
                            profile=profile,
                            has_veggie=data.get("has_veggie"),
                        )
                    )
        return UserLunch.objects.bulk_create(list_user_lunches)

    @classmethod
    def create_many_by_admin(cls, list_data, profile):
        if not list_data:
            raise Exception("list_data is empty")
        list_user_lunches = []
        for data in list_data:
            list_user_lunches.append(
                UserLunch(
                    date=data["date"], profile=profile, has_veggie=data["has_veggie"]
                )
            )
        return UserLunch.objects.bulk_create(list_user_lunches)

    @classmethod
    def is_lunar_day(cls, date):
        solar = Solar(date.year, date.month, date.day)
        lunar = Converter.Solar2Lunar(solar)
        if lunar.day == 1 or lunar.day == 15:
            return True
        return False

    @classmethod
    def is_weekday(cls, day):
        return True if day in [5, 6] else False

    @classmethod
    def set_veggie(cls, profile):
        now = datetime.datetime.now()
        last_day = now.replace(day=monthrange(now.year, now.month)[1])
        list_existed_lunar = []
        user_lunches = UserLunch.objects.filter(
            date__gte=now, date__lte=last_day, profile=profile
        ).values_list("date", flat=True)
        if not user_lunches.exists():
            list_user_lunches = []
            list_lunar_days = []
            step = datetime.timedelta(days=1)
            while now <= last_day:
                week_day = now.weekday()
                if cls.is_weekday(day=week_day):
                    now += step
                    continue
                if cls.is_lunar_day(date=now):
                    list_lunar_days.append(now)
                    list_user_lunches.append(
                        UserLunch(date=now, profile=profile, has_veggie=True)
                    )
                now += step
            if not list_lunar_days:
                raise Exception("Not found lunar day")
            return UserLunch.objects.bulk_create(list_user_lunches)
        for date in user_lunches:
            if cls.is_lunar_day(date=date):
                list_existed_lunar.append(date)
        UserLunch.objects.filter(profile=profile, date__in=list_existed_lunar).update(
            has_veggie=True
        )
        if not list_existed_lunar:
            raise Exception("Not found lunar day")
        return

    @classmethod
    def get_object(cls, pk):
        try:
            user_lunch = UserLunch.objects.get(id=pk)
            return user_lunch
        except UserLunch.DoesNotExist:
            raise Exception("Lunch is empty")

    @classmethod
    def update(cls, serializer, pk, date):
        user_lunch_instance = cls.get_object(pk)
        get_user_lunch = UserLunch.objects.filter(date=date).first()
        lunch_date = user_lunch_instance.date
        date_instance = datetime.date(
            lunch_date.year, lunch_date.month, lunch_date.day
        ).strftime("%Y-%m-%d")
        if date and date != date_instance and get_user_lunch is not None:
            raise Exception(f"Lunch have been updated with date {date}")
        return serializer.save()

    @classmethod
    def delete(cls, pk):
        today = datetime.date.today()
        lunch = UserLunch.objects.filter(id=pk, date__gte=today)
        if not lunch.exists():
            raise Exception("Can not delete lunch with date lunch little than now")
        return lunch.delete()
