// Login
import login from "@/pages/login/index.vue";
import id_change_password from "@/pages/changepassword/index.vue";
import id_verify from "@/pages/verify/index.vue";

// After Login
import loggedInLayout from "@/layouts/loggedInLayout.vue";
import companyCalendar from "@/pages/companyCalendar/index.vue";

// Skill
import Skill from "@/pages/skill/index";
import SearchSkill from "@/pages/skill/Search/index";
import ReportSkill from "@/pages/skill/Reports/index";
import LevelSkill from "@/pages/skill/Level/Levels";
import DefinitionSkill from "@/pages/skill/Definition";
import PositionSkill from "@/pages/skill/PositionSkill";

// Team
import CreateTeam from "@/pages/createteam/index.vue";
import id_team_table from "@/pages/team/_id/index.vue";
import team_table from "@/pages/team/index.vue";
import id_edit_team from "@/pages/addMember/_id/index.vue";

// Lunch Management
import LunchCalendar from "@/pages/lunchCalendar/index";
import ManageLunch from "@/pages/lunchSchedule/manage.vue";
import ManageProvider from "@/pages/lunchProvider/manage.vue";
import AutoBooking from "@/pages/lunchAutoBooking/autobooking.vue";

// Role
import ManageRole from "@/pages/role/index.vue";

// Evaluation Template
import listProbation from "@/pages/evaluationTemplate/listProbation/listProbation";
import EvaluationTemplateManage from "@/pages/evaluationTemplate/evaluationTemplateManage";
import MyEvaluationTemplate from "@/pages/evaluationTemplate/myEvaluationTemplate/myEvaluationTemplate";
import AddNewEvaluationTemplate from "@/pages/evaluationTemplate/myEvaluationTemplate/addNewEvaluationTemplate";
import id_evaluation_template from "@/pages/evaluationTemplate/myEvaluationTemplate/editEvaluationTemplate";
import EvaluationTemplateFormType from "@/pages/evaluationTemplate/myEvaluationTemplate/evaluationTemplateType";

// Title
import titles from "@/pages/titles/index.vue";

// Leave
import LeaveReport from "@/pages/leaveReport/leaveReport";
import MyReport from "@/pages/leaveReport/myReport/index";
import TeamReport from "@/pages/leaveReport/teamReport/index";
import OfficeReport from "@/pages/leaveReport/officeReport/index";
import LeaveManage from "@/pages/leaveManage/leaveManage";
import MyRequest from "@/pages/leaveManage/myRequest/myRequest";
import AddNewRequest from "@/pages/leaveManage/myRequest/addNewRequest";
import Approval from "@/pages/leaveManage/approval/approval";
import OfficeRequest from "@/pages/leaveManage/officeRequest/officeRequest";
import LeaveTypesMain from "@/pages/leaveTypeOff/index";
import LeaveType from "@/pages/leaveTypeOff/LeaveType";
import LeaveTypeGroup from "@/pages/leaveTypeOff/LeaveTypeGroup";

//Probation
import ProbationDetail from "@/pages/probationDetail/index.vue";
import NewProbation from "@/pages/probationDetail/addNewProbation.vue";
import ImportExcelProbation from "../pages/probationDetail/importExcel/importExcelProbation";
// User + Profile
import profile from "../pages/profile/_id/index.vue";
import id_list_table from "@/pages/employeelist/index.vue";
import ResetPassword from "@/pages/resetPassword/index.vue";

// Office
import office from "@/pages/office/index.vue";
import officeDetail from "@/pages/office/detail/index.vue";
import OrganizationChart from "@/pages/organizationChart/index.vue";

// Seat map
import SeatMap from "@/pages/seatMap/index.vue";

// Application
import IntegratedApplication from "@/pages/application/index";

// default
import Page404 from "@/pages/page404/index.vue";

//Work From Home
import WFHManage from "@/pages/wfhManage/wfhManage";
import WFHRequest from "@/pages/wfhManage/wfhRequest/wfhRequest";
import AddNewWFHRequest from "@/pages/wfhManage/wfhRequest/addNewWFHRequest";
import WFHOfficeRequest from "@/pages/wfhManage/wfhofficeRequest/wfhOfficeRequest";

export const routes = [
  {
    path: "/login",
    name: "Login",
    meta: {
      title: "Title",
    },
    component: login,
  },
  {
    path: "/resetPassword",
    name: "ResetPassword",
    meta: {
      title: "Reset Password",
    },
    component: ResetPassword,
  },

  {
    path: "",
    component: loggedInLayout,
    children: [
      {
        path: "/",
        name: "Calendar",
        meta: {
          title: "Company Calendar",
        },
        component: companyCalendar,
      },
      {
        path: "/profile/:id",
        name: "profile",
        component: profile,
        meta: {
          title: "Personal Information",
        },
      },
      {
        path: "/create-team",
        name: "CreateTeam",
        meta: {
          title: "Create New Team",
        },
        component: CreateTeam,
      },
      {
        path: "/addMember/:id",
        name: "AddMember",
        meta: {
          title: "Add New Member",
        },
        component: id_edit_team,
      },
      {
        path: "/employeelist",
        name: "EmployeeList",
        meta: {
          title: "Employee Accounts",
        },
        component: id_list_table,
      },
      {
        path: "/evaluations",
        name: "Evaluations",
        meta: {
          title: "Evaluations",
        },
        component: listProbation,
      },
      {
        path: "/evaluations/new",
        name: "New Evaluation",
        meta: {
          title: "New Evaluation",
        },
        component: NewProbation,
      },
      {
        path: "/evaluations/import",
        name: "Import Excel",
        meta: {
          title: "Import Excel",
        },
        component: ImportExcelProbation,
      },
      {
        path: "/evaluations/:id",
        name: "Evaluation Detail",
        meta: {
          title: "Evaluation Detail",
        },
        component: ProbationDetail,
      },
      {
        path: "leave-reports",
        name: "LeaveReport",
        component: LeaveReport,
        children: [
          {
            path: "/",
            name: "MyReport",
            meta: {
              title: "My Report",
            },
            component: MyReport,
          },
          {
            path: "teams",
            name: "MyTeamReport",
            meta: {
              title: "Team Report",
            },
            component: TeamReport,
          },
          {
            path: "offices",
            name: "OfficeReport",
            meta: {
              title: "Office Report",
            },
            component: OfficeReport,
          },
        ],
      },
      {
        path: "/evaluation-form-templates",
        name: "EvaluationTemplateManage",
        component: EvaluationTemplateManage,
        children: [
          {
            path: "/",
            name: "MyEvaluationTemplate",
            meta: {
              title: "Evaluation Form Template",
            },
            component: MyEvaluationTemplate,
          },
          {
            path: "evaluation-templates-types",
            name: "EvaluationTemplateFormType",
            meta: {
              title: "Evaluation Template Form Type",
            },
            component: EvaluationTemplateFormType,
          },
          {
            path: "new-evaluation-form-template",
            name: "AddNewEvaluationTemplate",
            meta: {
              title: "Add New Evaluation Template",
            },
            component: AddNewEvaluationTemplate,
          },
          {
            path: ":id",
            name: "EditEvaluationTemplate",
            meta: {
              title: "Edit Evaluation Template",
            },
            component: id_evaluation_template,
          },
        ],
      },
      {
        path: "/leaves",
        name: "LeaveManage",
        component: LeaveManage,
        children: [
          {
            path: "/",
            name: "MyRequest",
            meta: {
              title: "My Request",
            },
            component: MyRequest,
          },
          {
            path: "new-request",
            name: "AddNewRequest",
            meta: {
              title: "Add New Request",
            },
            component: AddNewRequest,
          },
          {
            path: "approvals",
            name: "RequestApproval",
            meta: {
              title: "Approval",
            },
            component: Approval,
          },
          {
            path: "office-requests",
            name: "OfficeRequest",
            meta: {
              title: "Office Request",
            },
            component: OfficeRequest,
          },
        ],
      },
      {
        path: "/workfromhome",
        name: "WFHManage",
        component: WFHManage,
        children: [
          {
            path: "/",
            name: "WFHRequest",
            meta: {
              title: "WFH Request",
            },
            component: WFHRequest,
          },
          {
            path: "new-wfh-request",
            name: "AddNewWFHRequest1",
            meta: {
              title: "Add New WFH Request",
            },
            component: AddNewWFHRequest,
          },
          {
            path: "wfh-office-requests",
            name: "WFHOfficeRequest",
            meta: {
              title: "WFH Office Request",
            },
            component: WFHOfficeRequest,
          },
        ],
      },
      {
        path: "/changepassword",
        name: "ChangePassword",
        meta: {
          title: "Change Password",
        },
        component: id_change_password,
      },
      {
        path: "/teams/:id",
        name: "Team-id",
        meta: {
          title: "Team Profile",
        },
        component: id_team_table,
      },
      {
        path: "/teams",
        name: "Team",
        meta: {
          title: "Team",
        },
        component: team_table,
      },
      {
        path: "/verify",
        name: "Verify",
        meta: {
          title: "Verify",
        },
        component: id_verify,
      },
      {
        path: "/lunch-providers",
        name: "lunch-providers",
        meta: {
          title: "Manage Provider",
        },
        component: ManageProvider,
      },
      {
        path: "/lunch-bookings",
        name: "lunch-bookings",
        meta: {
          title: "Auto Booking Lunch",
        },
        component: AutoBooking,
      },
      {
        path: "/lunch-schedules",
        name: "lunch-schedules",
        meta: {
          title: "Schedule",
        },
        component: ManageLunch,
      },
      {
        path: "/leave-types",
        component: LeaveTypesMain,
        children: [
          {
            path: "/",
            name: "leave-types",
            meta: {
              title: "Leave Types",
            },
            component: LeaveType,
          },
          {
            path: "leave-type-groups",
            name: "leave-type-groups",
            meta: {
              title: "Group Leave Types",
            },
            component: LeaveTypeGroup,
          },
        ],
      },
      {
        path: "/lunches",
        name: "LunchCalendar",
        meta: {
          title: "Meals",
        },
        component: LunchCalendar,
      },
      {
        path: "/organization-chart",
        name: "OrganizationChart",
        component: OrganizationChart,
        meta: {
          title: "Organization Chart",
        },
      },
      {
        path: "/skill",
        name: "Skill",
        component: Skill,
        children: [
          {
            path: "/",
            name: "Search",
            meta: {
              title: "Search",
            },
            component: SearchSkill,
          },
          {
            path: "reports",
            name: "Reports",
            meta: {
              title: "Reports",
            },
            component: ReportSkill,
          },
          {
            path: "levels",
            name: "Levels",
            meta: {
              title: "Levels",
            },
            component: LevelSkill,
          },
          {
            path: "definitions",
            name: "Definitions",
            meta: {
              title: "Definitions",
            },
            component: DefinitionSkill,
          },
          {
            path: "position",
            name: "Position",
            meta: {
              title: "Position",
            },
            component: PositionSkill,
          },
        ],
      },
      {
        path: "/titles",
        name: "Titles",
        meta: {
          title: "Titles",
        },
        component: titles,
      },
      {
        path: "setting/integrated-application",
        name: "IntegratedApplication",
        component: IntegratedApplication,
        meta: {
          title: "Integrated Application",
        },
      },
      {
        path: "/roles",
        name: "ManageRole",
        component: ManageRole,
        meta: {
          title: "Manage Role",
        },
      },
      {
        path: "/setting/offices",
        name: "Office",
        component: office,
        meta: {
          title: "Office",
        },
      },
      {
        path: "/setting/offices/:id",
        name: "OfficeInformation",
        component: officeDetail,
        meta: {
          title: "Office Information",
        },
      },
      {
        path: "/seat-map",
        name: "SeatMap",
        component: SeatMap,
        meta: {
          title: "Seat Map",
        },
      },
      {
        path: "*",
        name: "Page404",
        component: Page404,
      },
    ],
  },
];
