<template>
  <restricted-view :scopes="['user_lunch:update_list_auto_booking']">
    <template v-slot:default>
      <div>
        <el-col :span="10">
          <el-row style="height: 30px"></el-row>
          <el-input
            placeholder="Search by name"
            v-model="searchEmployeeList"
            style="width: 60%"
          ></el-input>
          <el-table
            :data="
              listNotAutoBookingLunch.filter(
                (data) =>
                  !searchEmployeeList ||
                  data.name
                    .toLowerCase()
                    .includes(searchEmployeeList.toLowerCase())
              )
            "
            stripe
            header-cell-class-name="bg-header-table"
            class="mt-2"
          >
            <el-table-column width="30">
              <template slot-scope="scope">
                <el-checkbox
                  v-model="scope.row.auto_booking_lunch"
                  @change="addListCheckBoxNotAuto(scope.row)"
                >
                </el-checkbox>
              </template>
            </el-table-column>
            <el-table-column prop="name" label="Employee List">
              <template slot-scope="scope">
                {{ scope.row.name }} ({{ scope.row.personal_email }})
              </template>
            </el-table-column>
            <el-table-column width="42">
              <template slot-scope="scope">
                <img
                  @click="addAutoBookingLunchProfile(scope.row)"
                  class="img-action"
                  :src="require('@/static/images/send-to-right.svg')"
                />
              </template>
            </el-table-column>
          </el-table>
        </el-col>
        <el-col :span="4" style="min-width: 150px">
          <el-row style="height: 150px"></el-row>
          <el-row>
            <div class="text-center">
              <el-button
                type="primary"
                class="mb-3"
                icon="el-icon-caret-right"
                :disabled="listCheckBoxNotAuto.length === 0"
                @click="changeListNotAutoBooking()"
              >
              </el-button>
              <br />
              <el-button
                type="primary"
                class="mb-3"
                icon="el-icon-caret-left"
                :disabled="listCheckBoxAuto.length === 0"
                @click="changeListAutoBooking()"
              >
              </el-button>
            </div>
          </el-row>
        </el-col>
        <el-col :span="10">
          <el-row style="height: 30px"></el-row>
          <el-row>
            <el-input
              placeholder="Search by name"
              v-model="searchAutoBookingList"
              style="width: 60%"
            ></el-input>
            <el-button type="primary" class="ml-4">
              <download-excel
                :fetch="fetchDataForExportExcel"
                :fields="json_fields"
                worksheet="My Worksheet"
                title="Auto Booking Lunch"
                name="auto-booking.xls"
              >
                <font-awesome-icon :icon="['fas', 'file-export']" />
                Export file
              </download-excel>
            </el-button>
          </el-row>
          <el-table
            :data="
              listAutoBookingLunch.filter(
                (data) =>
                  !searchAutoBookingList ||
                  data.name
                    .toLowerCase()
                    .includes(searchAutoBookingList.toLowerCase())
              )
            "
            stripe
            header-cell-class-name="bg-header-table"
            class="mt-2"
          >
            <el-table-column width="30">
              <template slot-scope="scope">
                <el-checkbox
                  v-model="scope.row.auto_booking_lunch"
                  @change="addListCheckBoxAuto(scope.row)"
                >
                </el-checkbox>
              </template>
            </el-table-column>
            <el-table-column prop="name" label="Auto Booking">
              <template slot-scope="scope">
                {{ scope.row.name }} ({{ scope.row.personal_email }})
              </template>
            </el-table-column>
            <el-table-column width="42">
              <template slot-scope="scope">
                <img
                  @click="removeAutoBookingLunchProfile(scope.row)"
                  class="img-action"
                  :src="require('@/static/images/send-to-left.svg')"
                />
              </template>
            </el-table-column>
          </el-table>
        </el-col>
      </div>
    </template>
  </restricted-view>
</template>
<script>
import ProfileService from "@/services/profile/profile";
import RestrictedView from "@/components/RestrictedView";

export default {
  name: "AutoBooking",
  components: {
    RestrictedView,
  },
  data() {
    return {
      listAutoBookingLunch: [],
      listNotAutoBookingLunch: [],
      json_fields: {
        Name: "name",
        "Personal Email": "personal_email",
        "Birth day": "birth_day",
        Phone: "phone",
        "Join date": "join_date",
        Veggie: "veggie",
      },
      searchEmployeeList: "",
      searchAutoBookingList: "",
      listCheckBoxAuto: [],
      listCheckBoxNotAuto: [],
    };
  },

  created() {
    this.getListAutoBookingLunch();
  },

  methods: {
    async getListAutoBookingLunch() {
      const res = await ProfileService.getAutoBookingLunchProfile();
      if (res.status === 200) {
        this.listAutoBookingLunch = res.data.pfs_lunch_booking;
        this.listNotAutoBookingLunch = res.data.pfs_lunch_not_booking;
      } else {
        this.$toast.error(res.data);
      }
    },

    async addAutoBookingLunchProfile(profile) {
      try {
        const data = {
          auto_booking_lunch: "True",
        };
        profile.auto_booking_lunch = true;
        await ProfileService.updateAutoBookingLunch(profile.id, data);
        this.listNotAutoBookingLunch.splice(
          this.listNotAutoBookingLunch.indexOf(profile),
          1
        );
        this.listAutoBookingLunch.push(profile);
        this.$toast.success("Update Status Success");
      } catch (e) {
        console.log(e);
        this.$toast.error("Update Status Failed");
      }
    },

    async removeAutoBookingLunchProfile(profile) {
      try {
        const data = {
          auto_booking_lunch: "False",
        };
        profile.auto_booking_lunch = false;
        await ProfileService.updateAutoBookingLunch(profile.id, data);
        this.listAutoBookingLunch.splice(
          this.listAutoBookingLunch.indexOf(profile),
          1
        );
        this.listNotAutoBookingLunch.unshift(profile);
        this.$toast.success("Update Status Success");
      } catch (e) {
        console.log(e);
        this.$toast.error("Update Status Failed");
      }
    },

    async fetchDataForExportExcel() {
      return this.listAutoBookingLunch;
    },

    addListCheckBoxNotAuto(profile) {
      if (profile.auto_booking_lunch === true) {
        this.listCheckBoxNotAuto.push(profile);
      } else {
        this.listCheckBoxNotAuto.splice(
          this.listCheckBoxNotAuto.indexOf(profile),
          1
        );
      }
    },

    addListCheckBoxAuto(profile) {
      if (profile.auto_booking_lunch === false) {
        this.listCheckBoxAuto.push(profile);
      } else {
        this.listCheckBoxAuto.splice(this.listCheckBoxAuto.indexOf(profile), 1);
      }
    },

    async changeListNotAutoBooking() {
      try {
        const data = {
          auto_booking_lunch: "True",
          list_change: this.listCheckBoxNotAuto,
        };
        await ProfileService.updateListAutoBookingLunch(data);
        for (let key in this.listCheckBoxNotAuto) {
          let profile = this.listCheckBoxNotAuto[key];
          profile.auto_booking_lunch = true;
          this.listAutoBookingLunch.push(profile);
          this.listNotAutoBookingLunch.splice(
            this.listNotAutoBookingLunch.indexOf(profile),
            1
          );
        }
        this.$toast.success("Update Status Success");
      } catch (e) {
        console.log(e);
        this.$toast.error("Update Status Failed");
      }
      this.listCheckBoxNotAuto = [];
    },

    async changeListAutoBooking() {
      try {
        const data = {
          auto_booking_lunch: "False",
          list_change: this.listCheckBoxAuto,
        };
        await ProfileService.updateListAutoBookingLunch(data);
        for (let key in this.listCheckBoxAuto) {
          let profile = this.listCheckBoxAuto[key];
          profile.auto_booking_lunch = false;
          this.listNotAutoBookingLunch.unshift(profile);
          this.listAutoBookingLunch.splice(
            this.listAutoBookingLunch.indexOf(profile),
            1
          );
        }
        this.$toast.success("Update Status Success");
      } catch (e) {
        console.log(e);
        this.$toast.error("Update Status Failed");
      }
      this.listCheckBoxAuto = [];
    },
  },
};
</script>

<style lang="scss" scoped>
@import "./style.scss";
</style>
