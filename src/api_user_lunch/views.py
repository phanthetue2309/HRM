import datetime

from api_oauth2.permissions.oauth2_permissions import CustomTokenMatchesOASRequirements
from api_workday.services.send_notification_slack import SendNotificationSlack
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserLunch
from .serializers import CreateUserLunchSerializer, UserLunchSerializer
from .services import UserLunchServices


class GetUserLunches(ListAPIView):
    queryset = UserLunch.objects.all()
    filterset_fields = ["date"]
    serializer_class = UserLunchSerializer
    ordering_fields = ["date"]
    permission_classes = [CustomTokenMatchesOASRequirements]
    required_alternate_scopes = {
        "GET": [["user:view_public_user_information_list"]],
    }

    def get_queryset(self):
        return self.queryset


class GetAllUserLunches(APIView):
    permission_classes = [CustomTokenMatchesOASRequirements]
    required_alternate_scopes = {
        "GET": [["user_lunch:get_all"]],
    }

    def get(self, request):
        queryset = UserLunch.objects.all()
        serializer = UserLunchSerializer(queryset, many=True)
        return Response(serializer.data)


class HandleUserLunch(APIView):
    permission_classes = [CustomTokenMatchesOASRequirements]
    required_alternate_scopes = {
        "GET": [["user:view_public_user_information_list"]],
        "POST": [["user_lunch:edit"]],
        "PUT": [["user_lunch:edit"]],
        "DELETE": [["user_lunch:edit"]],
    }

    def get(self, request):
        user_lunches = UserLunchServices.get_users_lunch(profile=request.user.profile)
        serializer = UserLunchSerializer(user_lunches, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CreateUserLunchSerializer(data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            try:
                UserLunchServices.create(
                    serializer=serializer,
                    profile=request.user.profile,
                    date=request.data.get("date"),
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error_msg": str(e)})

    def get_object(self, pk):
        try:
            lunch = UserLunch.objects.get(id=pk)
            return lunch
        except UserLunch.DoesNotExist:
            return Response(dict(msg="Lunch not found"))

    def put(self, request, pk):
        serializer = UserLunchSerializer(
            instance=self.get_object(pk), data=request.data, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            try:
                UserLunchServices.update(
                    serializer=serializer, pk=pk, date=request.data.get("date")
                )
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"msg": str(e)})

    def delete(self, request, pk):
        try:
            UserLunchServices.delete(pk=pk)
            return Response(dict(msg="user_lunch have been deleted"))
        except Exception as e:
            return Response({"msg": str(e)})


class HandleManyUserLunch(APIView):
    permission_classes = [CustomTokenMatchesOASRequirements]
    required_alternate_scopes = {
        "POST": [["user_lunch:edit"]],
        "PUT": [["user_lunch:edit"]],
    }

    def post(self, request):
        serializer = CreateUserLunchSerializer(data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            try:
                list_dates = request.data.get("list_dates")
                profile = request.user.profile
                list_user_lunches = UserLunchServices.create_many(
                    data=serializer.validated_data,
                    profile=profile,
                    list_dates=list_dates,
                )

                SendNotificationSlack.send_notification_create_lunch(
                    profile=profile, days=len(list_user_lunches)
                )

                return Response(
                    dict(
                        msg=f"You have just created lunch for {len(list_user_lunches)} days"
                    )
                )
            except Exception as e:
                return Response({"error_msg": str(e)})

    def put(self, request):
        today = datetime.date.today()
        list_lunches = UserLunch.objects.filter(
            date__gt=today, profile=request.user.profile
        )
        if not list_lunches.exists():
            return Response(dict(msg="Have no any lunches from now to delete"))
        list_lunches.delete()
        SendNotificationSlack.send_notification_update_lunch(
            profile=request.user.profile
        )
        return Response(dict(msg="Deleted successfully from today to the end up month"))


class HandleUserLunchByAdmin(APIView):
    permission_classes = [CustomTokenMatchesOASRequirements]
    required_alternate_scopes = {
        "POST": [["user_lunch:edit"]],
        "PUT": [["user_lunch:edit"]],
    }

    def post(self, request):
        serializer = CreateUserLunchSerializer(data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            try:
                list_data = request.data.get("list_data")
                profile = request.user.profile
                list_user_lunches = UserLunchServices.create_many_by_admin(
                    list_data=list_data,
                    profile=profile,
                )
                return Response(
                    dict(
                        msg=f"You have just created lunch for {len(list_user_lunches)} days"
                    )
                )
            except Exception as e:
                return Response({"error_msg": str(e)})

    def get_object(self, pk):
        try:
            lunch = UserLunch.objects.get(id=pk)
            return lunch
        except UserLunch.DoesNotExist:
            return Response(dict(msg="Lunch not found"))

    def put(self, request, pk):
        serializer = UserLunchSerializer(
            instance=self.get_object(pk), data=request.data, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class SetVeggieUserLunch(APIView):
    permission_classes = [CustomTokenMatchesOASRequirements]
    required_alternate_scopes = {}

    def put(self, request):
        try:
            UserLunchServices.set_veggie(profile=request.user.profile)
            return Response(dict(msg="You have just set veggie lunch for this month"))
        except Exception as e:
            return Response({"msg": str(e)})


class CancelSetVeggieUserLunch(APIView):
    permission_classes = [CustomTokenMatchesOASRequirements]
    required_alternate_scopes = {}

    def put(self, request):
        now = datetime.datetime.now()
        user_lunches = UserLunch.objects.filter(
            date__gte=now, profile=request.user.profile
        ).values_list("date", flat=True)
        UserLunch.objects.filter(
            date__in=list(user_lunches), profile=request.user.profile
        ).update(has_veggie=False)
        return Response(
            dict(msg="You have just cancel setting veggie lunch for this month")
        )
