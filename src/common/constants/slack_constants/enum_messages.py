class SlackEnumMessages:
    NOOB_MESSAGE = "Okay, I'm noob :crying: please make your sentence more clearly, or check again your typo!"
    UN_IMPLEMENT_INTENT = "This intent's handler has not implemented!"
    USER_NOT_FOUND_MESSAGE = ":no_entry_sign: *Can not found you in system*\n_Please contact manager to know more!_"
    NO_MANAGER_AND_MAXIMUM_LEVEL = ":no_entry_sign: *You don't have any line manger, neither the maximum level!*\n_Please contact manager to know more!_"
    ERROR_HAPPENED_MESSAGE = (
        ":no_entry_sign: Some bad things happened, contact the developers to fix it!"
    )
    ONLY_WEEKEND_MESSAGE = "I'm smart enough to know that it's only weekend day, don't underestimate me! :pepeknife:"

    DUPLICATE_REQUEST_MESSAGE = ":warning: *There is another request on that time!* :warning:\n*What you would like to do?*"

    CREATE_NEW_WITH_DIFFERENT_DATE_MESSAGE = (
        "*Let's create new request with another time!* :wink:"
    )
    GET_LAST_REQUEST_MESSAGE = "*Just hold my :beers: I'm getting your last request!*"

    WAITING_MESSAGE = "*Just hold my :beers: I'm getting your intent!*"

    REQUEST_NOT_FOUND_MESSAGE = "*Your session is timeout!* \nPlease create a new one!"
    INVALID_QUANTITY_DAYS_MESSAGE = "Invalid quantity of requested leave days!"
    INVALID_END_DATE_MESSAGE = (
        "End date must not be smaller than the starting date! :pepeknife:"
    )
    ONE_FOR_HALF_DAY_ONLY_MESSAGE = (
        "Half-day leave can only be created for only one day per request!"
    )

    REQUEST_ACTIONED = (
        ":no_entry_sign: *This request has been approved or rejected!* :no_entry_sign:"
    )
    REQUEST_CANCELED = (
        "*:no_entry_sign: This request has been canceled by the owner! :no_entry_sign:*"
    )
    NOT_LINE_MANAGER = "*Can not action because you are not the line manager of this request's employee!* :hidepain:"

    EMPLOYEE_REQUEST_NOT_FOUND_OR_ERROR = (
        ":no_entry_sign: *This employee's request is not exist in the system or*\n"
        "*maybe some bad things happened, contact the developers to fix it!*"
    )
