from api_base.services.slack import SlackResponseService
from api_slackbot.services.slack.response.slack_response_builder import (
    SlackResponseBuilder,
    slack_exception_message_builder,
)
from api_team.models.team import Team
from common.constants.workday_constants.date import Workday
from django.conf import settings


class SendNotificationSlack:
    slack_response_service = SlackResponseService(settings.SLACK_LEAVE_CHANNEL)

    @classmethod
    def send_notification_request_off(cls, profile, request_off_data):
        """
        To send notification to line manager from user to request off
        @param profile: profile of user who request off
        """
        channel = cls.get_channel(
            profile=profile,
            default_channel=settings.DEV_SLACK_USER_ID,
        )
        try:
            if channel:
                response_message = (
                    SlackResponseBuilder.create_leave_request_notification_line_manager(
                        profile, request_off_data
                    )
                )
                if response_message.get("is_exception"):
                    slack_text = "Error with line manager notification new request!"
                else:
                    slack_text = "New leave request!"
                cls.slack_response_service.send_message(
                    text=slack_text,
                    channel=channel,
                    blocks=response_message.get("response_blocks"),
                )
        except Exception as e:
            cls.slack_response_service.send_message(
                text="Error when sending you new leave request notification!",
                channel=channel,
                blocks=slack_exception_message_builder(
                    e,
                    error_title="Error when sending to line-manager "
                    "notification about new leave request!",
                ),
            )

    @classmethod
    def send_notification_approve_request_off(cls, leader_profile, request_off_data):
        """
        To send notification to Team about request off of user
        @param leader_profile: use to find Slack channel
        @param request_off_data: current user who request off
        """
        team = Team.objects.filter(team_leader_id=leader_profile.user_id).first()
        # This is just for demo purpose in dev, change this channel later in production
        team_channel = cls.get_channel(
            specific_channel=None if team is None else team.slack_channel,
            default_channel=settings.SLACK_LEAVE_CHANNEL,
        )
        employee_slack_id = request_off_data.profile.slack_id
        try:
            from_date = request_off_data.date_off.last().date
            from_time = (
                Workday.DEFAULT_START_HOUR_AFTERNOON
                if request_off_data.date_off.last().type == Workday.AFTERNOON_SHIFT_TIME
                else Workday.DEFAULT_START_HOUR
            )
            to_date = request_off_data.date_off.first().date
            to_time = (
                Workday.DEFAULT_END_HOUR_MORNING
                if request_off_data.date_off.last().type == Workday.MORNING_SHIFT_TIME
                else Workday.DEFAULT_END_HOUR
            )

            response_message_to_team = (
                SlackResponseBuilder.create_request_approved_notification_to_team(
                    request_off_data, from_date, from_time, to_date, to_time
                )
            )

            if response_message_to_team.get("is_exception"):
                slack_text_to_team = (
                    "Error with team notification new approved request!"
                )
            else:
                slack_text_to_team = (
                    "Some team members will not go to the office today!"
                )

            cls.slack_response_service.send_message(
                channel=team_channel,
                text=slack_text_to_team,
                blocks=response_message_to_team.get("response_blocks"),
            )

            response_message_to_employee = (
                SlackResponseBuilder.create_request_actioned_notification_to_employee(
                    user_profile=request_off_data.profile,
                    title="Your request has been approved :nhanmetrai:",
                    date_time=dict(
                        from_datetime=f"{from_date} {from_time}",
                        to_datetime=f"{to_date} {to_time}",
                        total=str(request_off_data.total),
                    ),
                    leave_type=request_off_data.leave_type.name,
                    reason=request_off_data.reason,
                )
            )

            if response_message_to_employee.get("is_exception"):
                slack_text_to_employee = (
                    "Error with employee notification with their approved request!"
                )
            else:
                slack_text_to_employee = "Request approved!"

            cls.slack_response_service.send_message(
                channel=employee_slack_id,
                text=slack_text_to_employee,
                blocks=response_message_to_employee.get("response_blocks"),
            )
        except Exception as e:
            cls.slack_response_service.send_message(
                text="Error when sending to team the approved leave request notification!",
                channel=team_channel,
                blocks=slack_exception_message_builder(
                    e,
                    error_title="Error when sending to team notification "
                    "about new approved leave request!",
                ),
            )

            cls.slack_response_service.send_message(
                text="Error when sending you notification about your approved leave request!",
                channel=employee_slack_id,
                blocks=slack_exception_message_builder(
                    e,
                    error_title="Error when sending employee notification"
                    " about their approved leave request!",
                ),
            )

    @classmethod
    def send_notification_reject_request_off(cls, request_off_data):
        """
        To send notification to User who request off
        @param request_off_data: request off of user
        """
        employee_slack_id = request_off_data.profile.slack_id
        try:
            from_date = request_off_data.date_off.last().date
            from_time = (
                Workday.DEFAULT_START_HOUR_AFTERNOON
                if request_off_data.date_off.last().type == Workday.AFTERNOON_SHIFT_TIME
                else Workday.DEFAULT_START_HOUR
            )
            to_date = request_off_data.date_off.first().date
            to_time = (
                Workday.DEFAULT_END_HOUR_MORNING
                if request_off_data.date_off.last().type == Workday.MORNING_SHIFT_TIME
                else Workday.DEFAULT_END_HOUR
            )
            if employee_slack_id:
                response_message_to_employee = SlackResponseBuilder.create_request_actioned_notification_to_employee(
                    user_profile=request_off_data.profile,
                    title="Your request has been rejected :hidepain:",
                    date_time=dict(
                        from_datetime=f"{from_date} {from_time}",
                        to_datetime=f"{to_date} {to_time}",
                        total=str(request_off_data.total),
                    ),
                    leave_type=request_off_data.leave_type.name,
                    reason=request_off_data.reason,
                )
                if response_message_to_employee.get("is_exception"):
                    slack_text_to_employee = (
                        "Error with employee notification with their rejected request!"
                    )
                else:
                    slack_text_to_employee = "Request rejected!"

                cls.slack_response_service.send_message(
                    channel=employee_slack_id,
                    text=slack_text_to_employee,
                    blocks=response_message_to_employee.get("response_blocks"),
                )
        except Exception as e:
            cls.slack_response_service.send_message(
                text="Error when sending you notification about your rejected leave request!",
                channel=employee_slack_id,
                blocks=slack_exception_message_builder(
                    e,
                    error_title="Error when sending employee notification "
                    "about their rejected leave request!",
                ),
            )

    @classmethod
    def send_notification_create_lunch(cls, profile, days):
        """
        Send notification to Lunch manager
        @param profile: profile of user who create lunch
        @param days : number of days set lunch
        """
        try:
            response_msg = (
                f"{profile.name} have have just created lunch for {days} days"
            )
            cls.slack_response_service.send_message(text=response_msg)
        except Exception as e:
            cls.slack_response_service.send_message(
                text="Error when sending you notification about new lunch request!",
                blocks=slack_exception_message_builder(
                    e,
                    error_title="Error when sending lunch manager "
                    "notification about new lunch request!",
                ),
            )

    @classmethod
    def send_notification_update_lunch(cls, profile):
        """
        Send notification to Lunch manager
        @param profile: profile of user who update lunch
        """
        try:
            response_msg = f"{profile.name} have have just delete lunch from now to the end of month"
            cls.slack_response_service.send_message(text=response_msg)
        except Exception as e:
            cls.slack_response_service.send_message(
                text="Error when sending you notification about new lunch updating request!",
                blocks=slack_exception_message_builder(
                    e,
                    error_title="Error when sending lunch manager notification "
                    "about new lunch updating request!",
                ),
            )

    @staticmethod
    def get_channel(
        profile=None,
        specific_channel=None,
        default_channel=settings.DEV_LINE_MANAGER_SLACK_USER_ID,
    ):
        if profile is not None and profile.line_manager is not None:
            return profile.line_manager.slack_id
        elif specific_channel is not None and specific_channel != "":
            return specific_channel
        else:
            return default_channel
