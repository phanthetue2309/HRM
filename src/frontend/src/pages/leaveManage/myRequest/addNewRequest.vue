<template>
  <div>
    <el-card>
      <div class="main-leaves row">
        <el-form
          class="bg-white px-4 text-info mb-2"
          label-width="200px"
          style="width: 100%"
        >
          <el-form-item label="Name">
            <el-input
              v-model="userName"
              placeholder="Your User Name"
              disabled
            ></el-input>
          </el-form-item>
          <el-form-item label="Available leave days">
            <el-input
              v-model="leaveDayNumber"
              placeholder="Leave days remaining"
              disabled
            ></el-input>
          </el-form-item>
          <el-form-item label="Types">
            <el-select v-model="typeLeave" @change="getTypeLeave">
              <div v-for="typeOff in listTypeOff" v-bind:key="typeOff.id">
                <div class="background">
                  <strong class="ml-3"> {{ typeOff.name }} </strong>
                </div>
                <el-option
                  v-for="typeOffDetail in typeOff.data"
                  :key="typeOffDetail.index"
                  :value="typeOffDetail.id"
                  :label="typeOffDetail.name"
                  v-bind:disabled="leaveDayNumber === 0"
                >
                  {{ typeOffDetail.name }} (maximum:
                  {{ typeOffDetail.days }} days)
                </el-option>
              </div>
            </el-select>
            <div v-if="typeLeave !== ''" class="mt-2">
              <el-table
                stripe
                header-cell-class-name="bg-header-table"
                border
                style="width: 100%"
                :data="typeLeaveTable"
              >
                <el-table-column
                  prop="name"
                  label="Name"
                  width="200"
                ></el-table-column>
                <el-table-column prop="is_count" label="Counted" width="80">
                  <template slot-scope="scope">
                    <div v-if="scope.row.is_count === true">Yes</div>
                    <div v-else>No</div>
                  </template>
                </el-table-column>
                <el-table-column
                  prop="days"
                  label="Limit Days"
                  width="100"
                ></el-table-column>
                <el-table-column prop="descriptions" label="Descriptions">
                  <template slot-scope="scope">
                    <div class="dont-break-out">
                      {{ scope.row.descriptions }}
                    </div>
                  </template>
                </el-table-column>
              </el-table>
              <div class="mt-2">
                You have {{ totalTypeOffLeaves }} date off using this request
              </div>
            </div>
          </el-form-item>
          <el-form-item label="Days">
            <div
              v-if="
                (totalTypeOffLeaves < maxLeaveDays && isCount) ||
                isCount === false
              "
            >
              From
              <flat-pickr
                v-model="startDay"
                :config="{
                  altInput: true,
                  altFormat: 'd-m-Y',
                  minDate: this.joinDate,
                  dateFormat: 'Y-m-d',
                  locale: { firstDayOfWeek: 1 },
                  disable: this.disable(),
                }"
                class="mr-2 ml-2"
                placeholder="Select date"
                name="date"
                @input="getDays()"
              />
              To
              <flat-pickr
                v-model="endDay"
                :config="{
                  altInput: true,
                  altFormat: 'd-m-Y',
                  dateFormat: 'Y-m-d',
                  minDate: this.startDay,
                  locale: { firstDayOfWeek: 1 },
                  disable: this.disable(),
                }"
                class="mr-2 ml-2"
                placeholder="Select date"
                name="date"
                @input="getDays()"
              />

              <div class="border-top rounded text-secondary">
                <div v-if="days.length > 0">
                  <table class="table">
                    <thead class="thead-light">
                      <tr>
                        <th scope="col" class="stt">No</th>
                        <th scope="col" class="date">Date</th>
                        <th scope="col" class="session">Session</th>
                        <th scope="col" class="lunch">Lunch</th>
                        <th scope="col" class="action">Action</th>
                      </tr>
                    </thead>
                    <tbody v-for="(item, index) in days" :key="item.startDay">
                      <tr>
                        <td>
                          <div class="text-center">
                            {{ index + 1 }}
                          </div>
                        </td>
                        <td>
                          <div class="text-center">
                            {{ formatDate(item.date) }}
                          </div>
                        </td>
                        <td>
                          <div class="text-center">
                            <el-checkbox
                              v-model="item.offMorning"
                              @change="changeTypeOff(item, $event)"
                            >
                              {{ formatSessionTime(item.date)[0] }} -
                              {{ formatSessionTime(item.date)[1] }}
                            </el-checkbox>
                            <el-checkbox
                              v-model="item.offAfternoon"
                              @change="changeTypeOff(item, $event)"
                            >
                              {{ formatSessionTime(item.date)[2] }} -
                              {{ formatSessionTime(item.date)[3] }}
                            </el-checkbox>
                          </div>
                        </td>
                        <td>
                          <div class="text-center">
                            <input
                              type="checkbox"
                              class="form-check-input"
                              v-on:click="changeLunch(item)"
                            />
                          </div>
                        </td>
                        <td>
                          <div class="text-center">
                            <font-awesome-icon
                              v-on:click="removeDay(item)"
                              class="fa-fw"
                              :icon="['fas', 'trash']"
                            />
                          </div>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
              <div v-if="totalLeaveCheck || isCount === false">
                Total Leave Days : {{ getNumberDayOffs() }}
              </div>
              <div v-if="errorRequest && isCount">
                <div class="text-danger">
                  Not enough day remain of this type. Please choose another
                  types.
                </div>
              </div>
            </div>
            <div v-else>
              <div class="text-danger">
                This types reach maximum days. Please choose another types.
              </div>
            </div>
          </el-form-item>
          <el-form-item label="Reason">
            <el-input
              type="textarea"
              :rows="2"
              v-model="reason"
              form="leaves"
              placeholder="Tell me your reasons"
            />
          </el-form-item>
          <div class="d-flex justify-content-end">
            <div v-if="isCount">
              <el-button
                @click="openDialog"
                type="primary"
                :disabled="sendCheck"
              >
                SEND
              </el-button>
            </div>
            <div v-else>
              <el-button @click="openDialog" type="primary"> SEND </el-button>
            </div>
            <router-link to="/leaves/" class="ml-3">
              <el-button type="danger"> CANCEL </el-button>
            </router-link>
          </div>
        </el-form>
        <el-dialog
          :visible.sync="dialog"
          title="Request Off"
          class="font-weight-bold"
        >
          <div class="justify-content-between">
            <div><strong>User Name :</strong> {{ this.userName }}</div>
            <br />
            <div>
              <strong>Type :</strong>
              {{
                this.tempListTypeOff.find((item) => item.id === this.typeLeave)
                  ? this.tempListTypeOff.find(
                      (item) => item.id === this.typeLeave
                    ).name
                  : ""
              }}
            </div>
            <br />
            <el-table
              :data="days"
              header-cell-class-name="bg-header-table"
              border
            >
              <el-table-column prop="date" label="Day Off">
                <template slot-scope="scope">
                  {{ formatDate(scope.row.date) }}
                </template>
              </el-table-column>
              <el-table-column prop="type" label="Session"></el-table-column>
              <el-table-column prop="lunch" label="Lunch">
                <template slot-scope="scope">
                  <div v-if="scope.row.lunch === true">Yes</div>
                  <div v-else>No</div>
                </template>
              </el-table-column>
            </el-table>
            <br />
            <div>
              <strong>Total Leave Days : </strong> {{ getNumberDayOffs() }}
            </div>
            <br />
            <div><strong>Reason :</strong> {{ this.reason }}</div>
          </div>

          <div id="user-lunch-modal-bottom">
            <div id="modify-button">
              <div class="row">
                <el-button
                  class="mt-3 mx-auto col-4"
                  type="primary"
                  :disabled="isSending"
                  @click="submit"
                >
                  Send
                </el-button>
                <el-button
                  class="mt-3 mx-auto col-4"
                  type="danger"
                  @click="closeDialog"
                >
                  Cancel
                </el-button>
              </div>
            </div>
          </div>
        </el-dialog>
      </div>
    </el-card>
  </div>
</template>
<script>
import RequestOffService from "@/services/leave_management/request_off/request_off.services";
import holidayServices from "@/services/office/holiday.service";
import TypeOffAdminServices from "@/services/leave_management/type_off/type_off_admin.services";
import RemainLeaveService from "@/services/leave_management/remain_leave/remain_leave.services";
import officeSessionService from "@/services/office/office.session";
import moment from "moment";
import "vue-cal/dist/vuecal.css";
import flatPickr from "vue-flatpickr-component";
import "flatpickr/dist/flatpickr.css";
import { mapGetters } from "vuex";
import _ from "lodash";

export default {
  name: "AddNewRequest",
  middleware: "authentication",
  components: {
    flatPickr,
  },
  computed: {
    ...mapGetters({
      showNotification: "showNotification",
    }),
  },
  data() {
    return {
      days: [],
      holidays: [],
      userName: "",
      startDay: null,
      endDay: null,
      joinDate: null,
      typeLeave: "",
      typeLeaveTable: "",
      listTypeOff: [],
      tempListTypeOff: [],
      reason: "",
      leaveDayNumber: "",
      remainDay: 0,
      annualLeaveLastYear: 0,
      currentDaysOff: 0,
      month: moment().year(),
      dialog: false,
      sessionTimes: [],
      profileID: "",
      year: new Date().getFullYear(),
      totalTypeOffLeaves: 0,
      maxLeaveDays: 1,
      sendCheck: true,
      totalLeaveCheck: false,
      errorRequest: false,
      isCount: true,
      officeID: "",
      monthExpiredAnnualLeave: 0,
      isSending: false,
    };
  },

  created: async function () {
    await RemainLeaveService.getRetrieveDate().then((res) => {
      this.currentDaysOff = res.data.current_days_off;
      this.annualLeaveLastYear = res.data.annual_leave_last_year;
      this.userName = res.data.profile.name;
      this.profileID = res.data.profile.id;
      this.officeID = res.data.profile.office;
      this.joinDate = new Date(res.data.profile.join_date).toISOString();
      this.monthExpiredAnnualLeave = res.data.month;
      this.getTotalLeaveDays();
    });
    await holidayServices.get(this.officeID).then((res) => {
      this.holidays = res.data.results;
    });
    await TypeOffAdminServices.getTypeOffUser().then((res) => {
      this.tempListTypeOff = res.data;
      this.listTypeOff = this.handleDataAPI(res.data);
    });
    await this.getSessionTimes();
  },
  methods: {
    disable() {
      if (this.typeLeave !== "") {
        if (
          this.tempListTypeOff.find((item) => item.id === this.typeLeave) ===
          this.tempListTypeOff.find((item) => item.id === this.typeLeave)
        ) {
          return [this.datePicker];
        } else {
          return [this.datePickerEnable];
        }
      } else {
        return [this.datePickerUnEnable];
      }
    },

    changeTypeOff(item) {
      let index = this.days.indexOf(
        this.days.find((i) => i.date === item.date)
      );
      let newType = "All day";
      if (item.offMorning === false && item.offAfternoon === false) {
        this.removeDay(item);
      } else {
        if (item.offMorning === true && item.offAfternoon === false) {
          newType =
            String(this.formatSessionTime(item.date)[0]) +
            "-" +
            String(this.formatSessionTime(item.date)[1]);
        } else if (item.offMorning === false && item.offAfternoon === true) {
          newType =
            String(this.formatSessionTime(item.date)[2]) +
            "-" +
            String(this.formatSessionTime(item.date)[3]);
        }
        this.days = [
          ...this.days.slice(0, index),
          {
            ...item,
            type: newType,
          },
          ...this.days.slice(index + 1),
        ];
      }
    },

    changeLunch(item) {
      let index = this.days.indexOf(
        this.days.find((i) => i.date === item.date)
      );
      this.days = [
        ...this.days.slice(0, index),
        {
          ...item,
          lunch: !item.lunch,
        },
        ...this.days.slice(index + 1),
      ];
    },

    removeDay: function (item) {
      const index = this.days.indexOf(
        this.days.find((i) => i.date === item.date)
      );
      if (index > -1) {
        this.days = [
          ...this.days.slice(0, index),
          ...this.days.slice(index + 1),
        ];
      }
    },

    submit: async function () {
      this.isSending = true;
      let listDates = [];
      this.days.forEach((item) =>
        listDates.push({
          ...item,
          date: item.date.toISOString().slice(0, 10),
        })
      );
      const data = {
        type_id: this.typeLeave,
        reason: this.reason,
        date: listDates,
        total_leaves: this.getNumberDayOffs(),
      };
      await RequestOffService.create(data)
        .then(async (res) => {
          if (res.status === 201) {
            await RemainLeaveService.getRetrieveDate().then((res) => {
              this.currentDaysOff = res.data.current_days_off;
              this.annualLeaveLastYear = res.data.annual_leave_last_year;
              this.userName = res.data.profile.name;
              this.joinDate = new Date(
                res.data.profile.join_date
              ).toISOString();
              this.monthExpiredAnnualLeave = res.data.month;
              this.getTotalLeaveDays();
            });
            this.$nextTick(() => {
              this.$toast.success(
                "Your leave day request was sent successfully"
              );
            });
          }
          this.isSending = false;
          listDates = [];
          await this.$router.push("/leaves");
        })
        .catch((e) => {
          let error = "Your leave day request was sent error";
          if (e.response && e.response.data.error !== "") {
            error = e.response.data.error;
          }
          this.$toast.error(error);
        });
    },

    datePicker: function (date) {
      const holiday = this.holidays.filter(
        (item) =>
          item.start_date <= moment(date).format("YYYY-MM-DD") &&
          item.end_date >= moment(date).format("YYYY-MM-DD")
      );
      if (holiday.length > 0) {
        return true;
      }
      return date.getDay() === 0 || date.getDay() === 6;
    },

    datePickerUnEnable: function (date) {
      date = true;
      return date;
    },

    datePickerEnable: function (date) {
      date = false;
      return date;
    },

    getTotalLeaveDays() {
      if (
        new Date().getMonth() > this.monthExpiredAnnualLeave ||
        this.annualLeaveLastYear === 0
      ) {
        this.leaveDayNumber = `${this.currentDaysOff} days`;
      } else {
        this.leaveDayNumber = `${
          this.currentDaysOff + this.annualLeaveLastYear
        } days (${this.currentDaysOff} days this years + ${
          this.annualLeaveLastYear
        } days remain last year)`;
      }
    },

    getDays() {
      this.days = [];
      if (
        new Date(this.startDay).getMonth() <= this.monthExpiredAnnualLeave &&
        this.annualLeaveLastYear > 0
      ) {
        this.leaveDayNumber = `${
          this.currentDaysOff + this.annualLeaveLastYear
        } days (${this.currentDaysOff} days this years + ${
          this.annualLeaveLastYear
        } days remain last year)`;
        this.remainDay = this.currentDaysOff + this.annualLeaveLastYear;
      } else {
        this.leaveDayNumber = `${this.currentDaysOff} days`;
        this.remainDay = this.currentDaysOff;
      }
      if (this.startDay !== null && this.endDay !== null) {
        let endDay = new Date(this.endDay);
        let start = new Date(this.startDay);
        for (; start <= endDay; ) {
          const holiday = this.holidays.filter(
            (item) =>
              item.start_date <= moment(start).format("YYYY-MM-DD") &&
              item.end_date >= moment(start).format("YYYY-MM-DD")
          );
          if (
            start.getDay() !== 0 &&
            start.getDay() !== 6 &&
            holiday.length === 0
          ) {
            const date = new Date(
              start.getFullYear(),
              start.getMonth(),
              start.getDate(),
              12,
              0
            );
            this.days.push({
              date: date,
              type: "All day",
              lunch: false,
              offMorning: true,
              offAfternoon: true,
            });
          }
          start.setDate(start.getDate() + 1);
        }
      }
      if (this.days.length > 0) this.totalLeaveCheck = true;
      this.isSending = false;
    },

    getNumberDayOffs() {
      let number = 0;
      if (this.totalLeaveCheck) {
        this.days.forEach((item) => {
          if (item.type === "All day") number += 1;
          else number += 0.5;
        });
        this.sendCheck =
          number + this.totalTypeOffLeaves > this.maxLeaveDays ||
          number > this.currentDaysOff;
        this.errorRequest = this.sendCheck;
        return number;
      }
    },

    openDialog() {
      if (this.days.length === 0) {
        this.$toast.error("No days off yet");
      } else if (
        this.getNumberDayOffs() > this.remainDay &&
        this.isCount === true
      ) {
        this.$toast.error("Total leave days can not more Available leave days");
      } else {
        this.dialog = true;
      }
    },

    closeDialog() {
      this.dialog = false;
    },

    async getTypeLeave() {
      if (this.typeLeave !== "") {
        const tempTypeLeave = this.tempListTypeOff.find(
          (item) => item.id === this.typeLeave
        );
        this.typeLeaveTable = [tempTypeLeave];
        this.maxLeaveDays = tempTypeLeave.days;
        this.isCount = tempTypeLeave.is_count;
        const res = await RequestOffService.countTotalTypeOffDays(
          this.profileID,
          this.typeLeave,
          this.year
        );
        this.totalTypeOffLeaves = res.total_leaves;
        this.isSending = false;
      }
    },

    formatDate(value) {
      if (value) {
        return moment(String(value)).format("MM-DD-YYYY");
      }
    },

    async getSessionTimes() {
      this.sessionTimes = await officeSessionService.getSessionTimesByProfile();
    },

    formatSessionTime(value) {
      if (value) {
        const data = this.sessionTimes.filter(
          (data) => data.dow === new Date(value).getDay() - 1
        );
        const sessionTime = [];
        if (data.length > 0) {
          for (const day in data) {
            sessionTime.push(data[day].start_time.slice(0, 5));
            sessionTime.push(data[day].end_time.slice(0, 5));
          }
          return sessionTime;
        }
      }
      return [];
    },

    handleDataAPI(dataAPI) {
      const uniqueGroup = _.uniqBy(dataAPI, "leave_type_group");
      return uniqueGroup.map((typeOff) => {
        const newData = {
          id: typeOff.id,
          group: typeOff.leave_type_group,
          name: typeOff.name_type,
          data: [],
        };
        dataAPI.forEach((item) => {
          if (item.leave_type_group === typeOff.leave_type_group) {
            newData.data.push(item);
          }
        });
        return newData;
      });
    },
  },
};
</script>

<style lang="scss" scoped>
@import "./addNewRequest.scss";
</style>
