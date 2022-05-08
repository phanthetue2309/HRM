<template>
  <nav ref="dropdown" class="nav-menu-expanded" id="side-menu">
    <ul class="list-unstyled components">
      <li id="siderbar_header" class="bg-color-primary">
        <router-link to="/">
          <img src="@/static/images/logoParadox.png" class="logoParadox" />
        </router-link>
      </li>
      <div id="button_container" class="font-weight-bold">
        <div :class="buttonIsHighlighted[0] ? 'clicked' : 'unClicked'">
          <li @click="highlightButtons(0)" class="category">
            <router-link to="/" class="btn font-weight-bold text-left">
              <div class="sidebar-item-icon first-level-item">
                <img
                  :src="require('@/static/images/companyCalendar.svg')"
                  class="filter icon"
                />
              </div>
              <span>Company Calendar</span>
            </router-link>
          </li>
        </div>
        <li class="dropdown_list_container category">
          <div class="dropdown">
            <div
              class="dropdown_header mx-auto d-flex align-items-center"
              @mouseover="show_employee_dropdown_collapse()"
              @click="show_employee_dropdown()"
            >
              <div class="sidebar-item-icon first-level-item">
                <img
                  :src="require('@/static/images/employee.svg')"
                  class="filter icon"
                />
              </div>
              <span>Employee Management</span>
              <img
                :src="require('@/static/images/iconDropdown.svg')"
                :class="{ iconDropdown: isCollapse }"
                class="filter ml-auto"
              />
            </div>
          </div>
        </li>
        <div @mouseleave="hideMenuItem()">
          <div class="dropdown_content" :class="{ active: checkEmployee }">
            <ul class="list-unstyled components p-0">
              <restricted-view
                :scopes="['user:view_public_user_information_list']"
              >
                <template v-slot:default>
                  <div
                    :class="buttonIsHighlighted[14] ? 'clicked' : 'unClicked'"
                  >
                    <li @click="highlightButtons(14)" class="category">
                      <router-link
                        to="/employeelist"
                        class="btn font-weight-bold text-left"
                      >
                        <div class="sidebar-item-icon">
                          <img
                            :src="require('@/static/images/Account.svg')"
                            class="filter icon"
                          />
                        </div>
                        <span>Accounts</span>
                      </router-link>
                    </li>
                  </div>
                </template>
              </restricted-view>
              <restricted-view :scopes="['skill:view']">
                <template v-slot:default>
                  <div
                    :class="buttonIsHighlighted[1] ? 'clicked' : 'unClicked'"
                  >
                    <li @click="highlightButtons(1)" class="category">
                      <router-link
                        to="/skill"
                        class="btn font-weight-bold text-left"
                      >
                        <div class="sidebar-item-icon">
                          <img
                            :src="require('@/static/images/Skill.svg')"
                            class="filter icon"
                          />
                        </div>
                        <span>Skills</span>
                      </router-link>
                    </li>
                  </div>
                </template>
              </restricted-view>
              <restricted-view :scopes="['title:view']">
                <template v-slot:default>
                  <div :class="buttonIsHighlighted[17] ? 'clicked' : 'unClicked'">
                    <li @click="highlightButtons(17)" class="category">
                      <router-link
                        to="/titles"
                        class="btn font-weight-bold text-left"
                      >
                        <div class="sidebar-item-icon">
                          <img
                            :src="require('@/static/images/position.svg')"
                            class="filter icon"
                          />
                        </div>
                        <span>Titles</span>
                      </router-link>
                    </li>
                  </div>
                </template>
              </restricted-view>
            </ul>
          </div>
        </div>
        <li class="dropdown_list_container category">
          <div class="dropdown">
            <div
              class="dropdown_header mx-auto d-flex align-items-center"
              @mouseover="show_organization_dropdown_collapse()"
              @click="show_organization_dropdown()"
            >
              <div class="sidebar-item-icon first-level-item">
                <img
                  :src="require('@/static/images/Organization.svg')"
                  class="filter icon"
                />
              </div>
              <span>Organization</span>
              <img
                :src="require('@/static/images/iconDropdown.svg')"
                class="filter ml-auto"
              />
            </div>
          </div>
        </li>
        <div @mouseleave="hideMenuItem()">
          <div class="dropdown_content" :class="{ active: checkOrganization }">
            <ul class="list-unstyled components p-0">
              <div :class="buttonIsHighlighted[15] ? 'clicked' : 'unClicked'">
                <li @click="highlightButtons(15)" class="category">
                  <router-link
                    to="/organization-chart"
                    class="btn font-weight-bold text-left"
                  >
                    <div class="sidebar-item-icon">
                      <img
                        :src="require('@/static/images/OrganizationChart.svg')"
                        class="filter icon"
                      />
                    </div>
                    <span>Organization Chart</span>
                  </router-link>
                </li>
              </div>
              <restricted-view :scopes="['team:view']">
                <template v-slot:default>
                  <div
                    :class="buttonIsHighlighted[2] ? 'clicked' : 'unClicked'"
                  >
                    <li @click="highlightButtons(2)" class="category">
                      <router-link
                        to="/teams"
                        class="btn font-weight-bold text-left"
                      >
                        <div class="sidebar-item-icon">
                          <img
                            :src="require('@/static/images/Team.svg')"
                            class="filter icon"
                          />
                        </div>
                        <span>Teams</span>
                      </router-link>
                    </li>
                  </div>
                </template>
              </restricted-view>
              <div :class="buttonIsHighlighted[3] ? 'clicked' : 'unClicked'">
                <li @click="highlightButtons(3)" class="category">
                  <router-link
                    to="/seat-map"
                    class="btn font-weight-bold text-left"
                  >
                    <div class="sidebar-item-icon">
                      <img
                        :src="require('@/static/images/SeatMap.svg')"
                        class="filter icon"
                      />
                    </div>
                    <span>Seat Map</span>
                  </router-link>
                </li>
              </div>
              <div :class="buttonIsHighlighted[4] ? 'clicked' : 'unClicked'">
                <li @click="highlightButtons(4)" class="category">
                  <router-link
                    to="/events"
                    class="btn font-weight-bold text-left"
                  >
                    <div class="sidebar-item-icon">
                      <img
                        :src="require('@/static/images/Event.svg')"
                        class="filter icon"
                      />
                    </div>
                    <span>Events</span>
                  </router-link>
                </li>
              </div>
            </ul>
          </div>
        </div>

        <li class="dropdown_list_container category">
          <div class="dropdown">
            <div
              class="dropdown_header mx-auto d-flex align-items-center"
              @mouseover="show_probation_dropdown_collapse()"
              @click="show_probation_dropdown()"
            >
              <div class="sidebar-item-icon first-level-item">
                <img
                  :src="require('@/static/images/ProbationManagement.svg')"
                  class="filter icon"
                />
              </div>
              <span
                v-show="showNotification"
                class="
                  position-absolute
                  top-0
                  countNoti
                  translate-middle
                  badge
                  rounded-pill
                  bg-danger
                "
                >{{ this.showNotification }}
                <span class="visually-hidden">unread messages</span>
              </span>
              <span v-show="showNotification"
                >Evaluation Management
                <span
                  class="
                    position-absolute
                    top-110
                    translate-middle
                    badge
                    rounded-pill
                    bg-danger
                  "
                  >{{ this.showNotification }}
                  <span class="visually-hidden">unread messages</span>
                </span>
              </span>
              <span v-show="!showNotification">Evaluation Management </span>
              <img
                :src="require('@/static/images/iconDropdown.svg')"
                class="filter ml-auto"
              />
            </div>
          </div>
        </li>
        <div @mouseleave="hideMenuItem()">
          <div class="dropdown_content" :class="{ active: checkProbation }">
            <ul class="list-unstyled components p-0">
              <restricted-view :scopes="['evaluation_template:view']">
                <template v-slot:default>
                  <div
                    :class="buttonIsHighlighted[15] ? 'clicked' : 'unClicked'"
                  >
                    <li @click="highlightButtons(15)" class="category">
                      <router-link
                        to="/evaluation-form-templates"
                        class="btn font-weight-bold text-left"
                      >
                        <div class="sidebar-item-icon">
                          <img
                            :src="
                              require('@/static/images/EvaluationTemplate.svg')
                            "
                            class="filter icon"
                          />
                        </div>
                        <span> Form Templates</span>
                      </router-link>
                    </li>
                  </div>
                </template>
              </restricted-view>
              <div :class="buttonIsHighlighted[16] ? 'clicked' : 'unClicked'">
                <li @click="highlightButtons(16)" class="category">
                  <router-link
                    to="/evaluations"
                    class="btn font-weight-bold text-left"
                  >
                    <div class="sidebar-item-icon">
                      <img
                        :src="require('@/static/images/MyProbation.svg')"
                        class="filter icon"
                      />
                    </div>
                    <span v-show="showNotification"
                      >Evaluations
                      <span
                        class="
                          position-absolute
                          countNotiItem
                          translate-middle
                          rounded-pill
                          bg-danger
                        "
                        >{{ this.showNotification }}
                        <span class="visually-hidden">unread messages</span>
                      </span>
                    </span>
                    <span v-show="!showNotification"> Evaluations </span>
                  </router-link>
                </li>
              </div>
            </ul>
          </div>
        </div>

        <li class="dropdown_list_container category">
          <div class="dropdown">
            <div
              class="dropdown_header mx-auto d-flex align-items-center"
              @mouseover="show_leave_dropdown_collapse()"
              @click="show_leave_dropdown()"
            >
              <div class="sidebar-item-icon first-level-item">
                <img
                  :src="require('@/static/images/LeaveManagement.svg')"
                  class="filter icon"
                />
              </div>
              <span
                v-show="showNotification"
                class="
                  position-absolute
                  top-0
                  countNoti
                  translate-middle
                  badge
                  rounded-pill
                  bg-danger
                "
                >{{ this.showNotification }}
                <span class="visually-hidden">unread messages</span>
              </span>
              <span v-show="showNotification"
                >Leave Management
                <span
                  class="
                    position-absolute
                    top-110
                    translate-middle
                    badge
                    rounded-pill
                    bg-danger
                  "
                  >{{ this.showNotification }}
                  <span class="visually-hidden">unread messages</span>
                </span>
              </span>
              <span v-show="!showNotification">Leave Management </span>
              <img
                :src="require('@/static/images/iconDropdown.svg')"
                class="filter ml-auto"
              />
            </div>
          </div>
        </li>
        <div @mouseleave="hideMenuItem()">
          <div class="dropdown_content" :class="{ active: checkLeave }">
            <ul class="list-unstyled components p-0">
              <div :class="buttonIsHighlighted[5] ? 'clicked' : 'unClicked'">
                <li @click="highlightButtons(5)" class="category">
                  <router-link
                    to="/leaves"
                    class="btn font-weight-bold text-left"
                  >
                    <div class="sidebar-item-icon">
                      <img
                        :src="require('@/static/images/RequestLeave.svg')"
                        class="filter icon"
                      />
                    </div>
                    <span v-show="showNotification"
                      >Request
                      <span
                        class="
                          position-absolute
                          countNotiItem
                          translate-middle
                          rounded-pill
                          bg-danger
                        "
                        >{{ this.showNotification }}
                        <span class="visually-hidden">unread messages</span>
                      </span>
                    </span>
                    <span v-show="!showNotification"> Requests </span>
                  </router-link>
                </li>
              </div>
              <restricted-view
                :scopes="[
                  'statistic_dateoff:user',
                  'statistic_dateoff:team',
                  'statistic_dateoff:office',
                ]"
              >
                <template v-slot:default>
                  <div
                    :class="buttonIsHighlighted[6] ? 'clicked' : 'unClicked'"
                  >
                    <li @click="highlightButtons(6)" class="category">
                      <router-link
                        to="/leave-reports"
                        class="btn font-weight-bold text-left"
                      >
                        <div class="sidebar-item-icon">
                          <img
                            :src="require('@/static/images/LeaveReports.svg')"
                            class="filter icon"
                          />
                        </div>
                        <span>Reports</span>
                      </router-link>
                    </li>
                  </div>
                </template>
              </restricted-view>
              <restricted-view :scopes="['type_off:view']">
                <template v-slot:default>
                  <div
                    :class="buttonIsHighlighted[7] ? 'clicked' : 'unClicked'"
                  >
                    <li @click="highlightButtons(7)" class="category">
                      <router-link
                        to="/leave-types"
                        class="btn font-weight-bold text-left"
                      >
                        <div class="sidebar-item-icon">
                          <img
                            :src="require('@/static/images/LeaveType.svg')"
                            class="filter icon"
                          />
                        </div>
                        <span>Leave Types</span>
                      </router-link>
                    </li>
                  </div>
                </template>
              </restricted-view>
            </ul>
          </div>
        </div>

        <li class="dropdown_list_container category">
          <div class="dropdown">
            <div
              class="dropdown_header mx-auto d-flex align-items-center"
              @mouseover="show_WFH_dropdown_collapse()"
              @click="show_WFH_dropdown()"
            >
              <div class="sidebar-item-icon first-level-item">
                <img
                  :src="require('@/static/images/wfh.svg')"
                  class="filter icon"
                />
              </div>
              <span
                v-show="showNotification"
                class="
                  position-absolute
                  top-0
                  countNoti
                  translate-middle
                  badge
                  rounded-pill
                  bg-danger
                "
                >{{ this.showNotification }}
                <span class="visually-hidden">unread messages</span>
              </span>
              <span v-show="showNotification"
                >WFH Management
                <span
                  class="
                    position-absolute
                    top-110
                    translate-middle
                    badge
                    rounded-pill
                    bg-danger
                  "
                >
                  {{ this.showNotification }}
                  <span class="visually-hidden">unread messages</span>
                </span>
              </span>
              <span v-show="!showNotification">WFH Management</span>
              <img
                :src="require('@/static/images/iconDropdown.svg')"
                class="filter ml-auto"
              />
            </div>
          </div>
        </li>
        <div @mouseleave="hideMenuItem()">
          <div class="dropdown_content" :class="{ active: checkWFH }">
            <ul class="list-unstyled components p-0">
              <div :class="buttonIsHighlighted[15] ? 'clicked' : 'unClicked'">
                <li @click="highlightButtons(15)" class="category">
                  <router-link
                    to="/workfromhome"
                    class="btn font-weight-bold text-left"
                  >
                    <div class="sidebar-item-icon">
                      <img
                        :src="require('@/static/images/edit.svg')"
                        class="filter icon"
                      />
                    </div>
                    <span v-show="showNotification">
                      WFH Request
                      <span
                        class="
                          position-absolute
                          countNotiItem
                          translate-middle
                          rounded-pill
                          bg-danger
                        "
                      >
                        {{ this.showNotification }}
                        <span class="visually-hidden">unread messages</span>
                      </span>
                    </span>
                    <span v-show="!showNotification"> WFH Requests </span>
                  </router-link>
                </li>
              </div>
            </ul>
          </div>
        </div>

        <li class="dropdown_list_container category">
          <div class="dropdown">
            <div
              class="dropdown_header mx-auto d-flex align-items-center"
              @mouseover="show_lunch_dropdown_collapse"
              @click="show_lunch_dropdown()"
            >
              <div class="sidebar-item-icon first-level-item">
                <img
                  :src="require('@/static/images/LuchManagement.svg')"
                  class="filter icon"
                />
              </div>
              <span>Lunch Management</span>
              <img
                :src="require('@/static/images/iconDropdown.svg')"
                class="filter ml-auto"
              />
            </div>
          </div>
        </li>

        <div @mouseleave="hideMenuItem()">
          <div class="dropdown_content" :class="{ active: checkLunch }">
            <ul class="list-unstyled components p-0">
              <div :class="buttonIsHighlighted[8] ? 'clicked' : 'unClicked'">
                <li @click="highlightButtons(8)" class="category">
                  <router-link
                    to="/lunches"
                    class="btn font-weight-bold text-left"
                  >
                    <div class="sidebar-item-icon">
                      <img
                        :src="require('@/static/images/Meals.svg')"
                        class="filter icon"
                      />
                    </div>
                    <span>Meals</span>
                  </router-link>
                </li>
              </div>
              <restricted-view :scopes="['lunches:view']">
                <template v-slot:default>
                  <div
                    :class="buttonIsHighlighted[9] ? 'clicked' : 'unClicked'"
                  >
                    <li @click="highlightButtons(9)" class="category">
                      <router-link
                        to="/lunch-schedules"
                        class="btn font-weight-bold text-left"
                      >
                        <div class="sidebar-item-icon">
                          <img
                            :src="require('@/static/images/Schedule.svg')"
                            class="filter icon"
                          />
                        </div>
                        <span>Schedule</span>
                      </router-link>
                    </li>
                  </div>
                </template>
              </restricted-view>
              <restricted-view :scopes="['provider:view']">
                <template v-slot:default>
                  <div
                    :class="buttonIsHighlighted[10] ? 'clicked' : 'unClicked'"
                  >
                    <li @click="highlightButtons(10)" class="category">
                      <router-link
                        to="/lunch-providers"
                        class="btn font-weight-bold text-left"
                      >
                        <div class="sidebar-item-icon">
                          <img
                            :src="require('@/static/images/Provider.svg')"
                            class="filter icon"
                          />
                        </div>
                        <span>Provider</span>
                      </router-link>
                    </li>
                  </div>
                </template>
              </restricted-view>
              <restricted-view
                :scopes="['user_lunch:update_list_auto_booking']"
              >
                <template v-slot:default>
                  <div
                    :class="buttonIsHighlighted[11] ? 'clicked' : 'unClicked'"
                  >
                    <li @click="highlightButtons(11)" class="category">
                      <router-link
                        to="/lunch-bookings"
                        class="btn font-weight-bold text-left"
                      >
                        <div class="sidebar-item-icon">
                          <img
                            :src="require('@/static/images/AutoBooking.svg')"
                            class="filter icon"
                          />
                        </div>
                        <span>Auto Booking</span>
                      </router-link>
                    </li>
                  </div>
                </template>
              </restricted-view>
            </ul>
          </div>
        </div>
        <li class="dropdown_list_container category">
          <div class="dropdown">
            <div
              class="dropdown_header mx-auto d-flex align-items-center"
              @mouseover="show_setting_dropdown_collapse"
              @click="show_setting_dropdown()"
            >
              <div class="sidebar-item-icon first-level-item">
                <img
                  :src="require('@/static/images/Setting.svg')"
                  class="filter icon"
                />
              </div>
              <span>Settings</span>
              <img
                :src="require('@/static/images/iconDropdown.svg')"
                class="filter ml-auto"
              />
            </div>
          </div>
        </li>
        <div @mouseleave="hideMenuItem()">
          <div class="dropdown_content" :class="{ active: checkSetting }">
            <ul class="list-unstyled components p-0">
              <restricted-view :scope="['application:list']">
                <template v-slot:default>
                  <div
                    :class="buttonIsHighlighted[12] ? 'clicked' : 'unClicked'"
                  >
                    <li @click="highlightButtons(12)" class="category">
                      <router-link
                        to="/setting/integrated-application"
                        class="btn font-weight-bold text-left"
                      >
                        <div class="sidebar-item-icon">
                          <img
                            :src="require('@/static/images/Integrated.svg')"
                            class="filter icon"
                          />
                        </div>
                        <span>Integrated Application</span>
                      </router-link>
                    </li>
                  </div>
                </template>
              </restricted-view>
              <restricted-view :scope="['office:view']">
                <template v-slot:default>
                  <div
                    :class="buttonIsHighlighted[13] ? 'clicked' : 'unClicked'"
                  >
                    <li @click="highlightButtons(13)" class="category">
                      <router-link
                        to="/setting/offices"
                        class="btn font-weight-bold text-left"
                      >
                        <div class="sidebar-item-icon">
                          <img
                            :src="require('@/static/images/Ofiices.svg')"
                            class="filter icon"
                          />
                        </div>
                        <span>Offices</span>
                      </router-link>
                    </li>
                  </div>
                </template>
              </restricted-view>

              <restricted-view :scopes="['role:view']">
                <template v-slot:default>
                  <div
                    :class="buttonIsHighlighted[14] ? 'clicked' : 'unClicked'"
                  >
                    <li @click="highlightButtons(14)" class="category">
                      <router-link
                        to="/roles"
                        class="btn font-weight-bold text-left"
                      >
                        <div class="sidebar-item-icon">
                          <img
                            :src="require('@/static/images/role.svg')"
                            class="filter icon"
                          />
                        </div>
                        <span>Manage Role</span>
                      </router-link>
                    </li>
                  </div>
                </template>
              </restricted-view>
            </ul>
          </div>
        </div>
      </div>
    </ul>
  </nav>
</template>

<script>
import { mapGetters } from "vuex";
import RestrictedView from "./RestrictedView";

export default {
  name: "id_sidebar",
  components: {
    RestrictedView,
  },
  data() {
    return {
      checkSetting: false,
      checkLunch: false,
      checkProbation: false,
      checkLeave: false,
      checkWFH: false,
      checkOrganization: false,
      checkEmployee: false,
      admin: localStorage.getItem("is_admin"),
      buttonIsHighlighted: [],
    };
  },
  computed: {
    ...mapGetters({
      showNotification: "showNotification",
      isCollapse: "value",
    }),
  },
  methods: {
    fetchData() {},
    highlightButtons(n) {
      this.buttonIsHighlighted = [];
      this.buttonIsHighlighted[n] = true;
    },
    toggle: function () {
      const myvar = this.$refs.dropdown;
      if (myvar.style.display === "none") {
        myvar.style.display = "grid";
      } else {
        myvar.style.display = "none";
      }
    },
    show_employee_dropdown() {
      this.checkEmployee = !this.checkEmployee;
      this.checkOrganization = false;
      this.checkLeave = false;
      this.checkSetting = false;
      this.checkLunch = false;
      this.checkWFH = false;
      this.checkProbation = false;
    },
    show_employee_dropdown_collapse() {
      if (this.isCollapse) {
        this.checkEmployee = this.isCollapse;
        this.checkOrganization = false;
        this.checkLeave = false;
        this.checkSetting = false;
        this.checkLunch = false;
        this.checkWFH = false;
        this.checkProbation = false;
      }
    },
    hideMenuItem() {
      if (this.isCollapse) {
        this.checkEmployee = false;
        this.checkOrganization = false;
        this.checkLeave = false;
        this.checkSetting = false;
        this.checkLunch = false;
        this.checkWFH = false;
        this.checkProbation = false;
      }
    },
    show_organization_dropdown() {
      this.checkOrganization = !this.checkOrganization;
      this.checkEmployee = false;
      this.checkLeave = false;
      this.checkSetting = false;
      this.checkLunch = false;
      this.checkWFH = false;
      this.checkProbation = false;
    },
    show_organization_dropdown_collapse() {
      if (this.isCollapse) {
        this.checkOrganization = this.isCollapse;
        this.checkEmployee = false;
        this.checkLeave = false;
        this.checkSetting = false;
        this.checkLunch = false;
        this.checkWFH = false;
        this.checkProbation = false;
      }
    },
    show_probation_dropdown() {
      this.checkProbation = !this.checkProbation;
      this.checkEmployee = false;
      this.checkLeave = false;
      this.checkSetting = false;
      this.checkOrganization = false;
      this.checkLunch = false;
      this.checkWFH = false;
    },
    show_probation_dropdown_collapse() {
      if (this.isCollapse) {
        this.checkProbation = this.isCollapse;
        this.checkEmployee = false;
        this.checkLeave = false;
        this.checkSetting = false;
        this.checkOrganization = false;
        this.checkLunch = false;
        this.checkWFH = false;
      }
    },
    show_leave_dropdown() {
      this.checkLeave = !this.checkLeave;
      this.checkEmployee = false;
      this.checkOrganization = false;
      this.checkSetting = false;
      this.checkLunch = false;
      this.checkWFH = false;
      this.checkProbation = false;
    },
    show_leave_dropdown_collapse() {
      if (this.isCollapse) {
        this.checkLeave = this.isCollapse;
        this.checkEmployee = false;
        this.checkOrganization = false;
        this.checkSetting = false;
        this.checkLunch = false;
        this.checkWFH = false;
      }
    },
    show_WFH_dropdown() {
      this.checkWFH = !this.checkWFH;
      this.checkEmployee = false;
      this.checkLeave = false;
      this.checkSetting = false;
      this.checkOrganization = false;
      this.checkLunch = false;
      this.checkProbation = false;
    },
    show_WFH_dropdown_collapse() {
      if (this.isCollapse) {
        this.checkLunch = this.isCollapse;
        this.checkEmployee = false;
        this.checkLeave = false;
        this.checkSetting = false;
        this.checkOrganization = false;
        this.checkWFH = false;
        this.checkProbation = false;
      }
    },
    show_setting_dropdown() {
      this.checkSetting = !this.checkSetting;
      this.checkEmployee = false;
      this.checkLeave = false;
      this.checkOrganization = false;
      this.checkLunch = false;
      this.checkWFH = false;
      this.checkProbation = false;
    },
    show_setting_dropdown_collapse() {
      if (this.isCollapse) {
        this.checkSetting = this.isCollapse;
        this.checkEmployee = false;
        this.checkLeave = false;
        this.checkOrganization = false;
        this.checkLunch = false;
        this.checkWFH = false;
        this.checkProbation = false;
      }
    },
    show_lunch_dropdown() {
      this.checkLunch = !this.checkLunch;
      this.checkEmployee = false;
      this.checkLeave = false;
      this.checkSetting = false;
      this.checkOrganization = false;
      this.checkWFH = false;
      this.checkProbation = false;
    },
    show_lunch_dropdown_collapse() {
      if (this.isCollapse) {
        this.checkLunch = this.isCollapse;
        this.checkEmployee = false;
        this.checkLeave = false;
        this.checkSetting = false;
        this.checkOrganization = false;
        this.checkWFH = false;
        this.checkProbation = false;
      }
    },
  },
};
</script>

<style lang="scss" scoped>
@import "../assets/scss/sidebar.scss";
</style>
