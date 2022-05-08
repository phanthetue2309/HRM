from core.settings import base
from common.constants.base_const import Const


class SlackUrlConstants(Const):
    API_BASE_URL = "https://slack.com/api/"
    CONVERSATION_HISTORY_API = "conversations.history?channel="
    USER_INFO_API = "users.info?user="
    SLACK_BOT_USER_ID = base.SLACK_BOT_USER_ID
