from api_slackbot.services.slack.interactive_components_handler.created_button_service import (
    CreatedButtonService,
)
from api_slackbot.services.slack.response.base_components_builder import (
    SubComponentBuilder,
)
from api_slackbot.services.temp_leave_request.temp_leave_request_service import (
    TempLeaveRequestService,
)
from api_wfh.services.wfh_request import WfhRequestServices
from api_workday.services.leave_type import LeaveTypeService
from api_workday.services.request_off import RequestOffServices
from common.constants.slack_constants.dialog_content import RequestDialogContent


class UserRequestBaseHandler:
    def __init__(
        self,
        slack_service,
        button_values,
        profile,
        temp_leave_request,
        exception_handler,
    ):
        self.slack_service = slack_service
        self.button_values = button_values
        self.profile = profile
        self.temp_leave_request = temp_leave_request
        self.exception_handler = exception_handler
        self.service_mapped_data = self.map_data_to_service()

    def send_response_message(self, text):
        self.slack_service.send_response_to_interacting(text)

    def delete_temp_request(self):
        TempLeaveRequestService.delete_temp_leave_request_if_exist_by_id(
            self.temp_leave_request.id.hex
        )

    def map_data_to_service(self):
        return CreatedButtonService.create_request_data_processing(
            profile=self.profile,
            button_values=self.button_values,
            temp_leave_request=self.temp_leave_request,
        )

    @staticmethod
    def get_lunch_dates(service_mapped_dates: list):
        lunch_dates = [
            date.get("date") for date in service_mapped_dates if date.get("lunch")
        ]
        if len(lunch_dates) <= 2:
            return ", ".join(lunch_date for lunch_date in lunch_dates)
        else:
            return "You will have lunch in all your requesting dates"


class UserWFHRequestHandler(UserRequestBaseHandler):
    def __init__(
        self,
        slack_service,
        button_values,
        profile,
        temp_leave_request,
        exception_handler,
    ):
        super().__init__(
            slack_service,
            button_values,
            profile,
            temp_leave_request,
            exception_handler,
        )

    def handling(self):
        if self.service_mapped_data.get("is_exception"):
            self.delete_temp_request()
            return self.exception_handler.send_exception_blocks(
                self.service_mapped_data.get("response_blocks")
            ).return_http_no_retires_response(self.service_mapped_data.get("error"))

        else:
            response = WfhRequestServices.create_wfh_request(
                data=self.service_mapped_data, user=self.profile.user
            )
            if "error" in response:
                exception_blocks = [
                    SubComponentBuilder().section_mrkdwn_text_builder(
                        mrkdwn_text=response.get("error")
                    )
                ]
                self.delete_temp_request()
                return self.exception_handler(exception_blocks, response.get("error"))

            else:
                self.send_response_message(
                    text="*Created work from home request* :nhanmetrai:\n"
                    + ":point_right: Duration: *"
                    + self.temp_leave_request.from_date
                    + " "
                    + self.temp_leave_request.from_time
                    + "* to *"
                    + self.temp_leave_request.to_date
                    + " "
                    + self.temp_leave_request.to_time
                    + "* \n"
                    + ":point_right: Quantity: *"
                    + str(self.service_mapped_data.get("wfh_total"))
                    + "* \n"
                    + ":point_right: Reason: *"
                    + self.service_mapped_data.get("reason")
                    + "* \n"
                    + ":point_right: Having lunch: *"
                    + (
                        self.get_lunch_dates(self.service_mapped_data.get("date"))
                        if self.temp_leave_request.lunch_status
                        else "No"
                    )
                    + "*"
                )
                self.delete_temp_request()


class UserLeaveRequestHandler(UserRequestBaseHandler):
    def __init__(
        self,
        slack_service,
        button_values,
        profile,
        temp_leave_request,
        exception_handler,
    ):
        super().__init__(
            slack_service,
            button_values,
            profile,
            temp_leave_request,
            exception_handler,
        )

    def handling(self):
        if self.service_mapped_data.get("is_exception"):
            self.delete_temp_request()
            return self.exception_handler.send_exception_blocks(
                self.service_mapped_data.get("response_blocks")
            ).return_http_no_retires_response(self.service_mapped_data.get("error"))

        else:
            response = RequestOffServices.create_request_off(
                request_data=self.service_mapped_data, profile=self.profile
            )
            if "error" in response:
                exception_blocks = [
                    SubComponentBuilder().section_mrkdwn_text_builder(
                        mrkdwn_text=response.get("error")
                    )
                ]
                self.delete_temp_request()
                return self.exception_handler.send_exception_blocks(exception_blocks)

            else:
                leave_type_name = LeaveTypeService.get_leave_type_by_id(
                    self.temp_leave_request.leave_type_id
                ).name
                self.send_response_message(
                    text="*Created leave request* :nhanmetrai:\n"
                    + ":point_right: Duration: *"
                    + self.temp_leave_request.from_date
                    + " "
                    + self.temp_leave_request.from_time
                    + "* to *"
                    + self.temp_leave_request.to_date
                    + " "
                    + self.temp_leave_request.to_time
                    + "* \n"
                    + ":point_right: Quantity: *"
                    + str(self.service_mapped_data.get("total_leaves"))
                    + "* \n"
                    + ":point_right: Leave type: *"
                    + leave_type_name
                    + "* \n"
                    + ":point_right: Reason: *"
                    + self.service_mapped_data.get("reason")
                    + "* \n"
                    + ":point_right: Having lunch: *"
                    + (
                        self.get_lunch_dates(self.service_mapped_data.get("date"))
                        if self.temp_leave_request.lunch_status
                        else "No"
                    )
                    + "*\n"
                    + (
                        RequestDialogContent.WAITING_LINE_MANAGER_APPROVAL
                        if self.profile.line_manager is not None
                        else RequestDialogContent.NO_NEED_LINE_MANAGER_APPROVE
                    )
                )
                self.delete_temp_request()
