<template>
  <div class="mt-3">
    <div>
      <div class="d-flex justify-content-end mb-3" style="gap: 10px">
        <el-button round type="success" @click="handleApproved">
          Approved
        </el-button>
        <el-button
          round
          type="danger"
          @click="handleRejected"
          style="margin: 0px"
        >
          Rejected
        </el-button>
        <restricted-view :scopes="['request_off:delete']">
          <el-button round type="danger" @click="handleDelete">
            Delete
          </el-button>
        </restricted-view>
      </div>
    </div>
    <div>
      <el-table
        highlight-current-row
        @selection-change="handleUpdateStatusLeaveRequest"
        :data="desserts"
        header-cell-class-name="bg-header-table"
        border
      >
        <el-table-column type="selection" align="center"></el-table-column>
        <el-table-column
          sortable
          prop="request_off.profile.name"
          label="Employee"
          align="center"
        >
        </el-table-column>
        <el-table-column label="Date Off" width="200">
          <template slot-scope="scope">
            <div
              v-for="dateOff in scope.row.request_off.date_off"
              :key="dateOff.id"
            >
              {{ dateOff.date }} ({{ dateOff.type }})
            </div>
          </template>
        </el-table-column>
        <el-table-column
          sortable
          prop="request_off.leave_type.name"
          label="Leave Type"
          align="center"
        >
        </el-table-column>
        <el-table-column
          prop="request_off.reason"
          label="Reason"
          align="center"
        ></el-table-column>
        <el-table-column label="Status" align="center">
          <template slot-scope="scope">
            <el-tag type="info" v-if="scope.row.status === 'Cancel'">
              Cancel
            </el-tag>
            <el-tag type="danger" v-else-if="scope.row.status === 'Rejected'">
              Rejected
            </el-tag>
            <el-tag type="success" v-else-if="scope.row.status === 'Approved'">
              Approved
            </el-tag>
            <el-tag type="warning" v-else> Pending</el-tag>
          </template>
        </el-table-column>
      </el-table>
      <div class="text-center">
        <el-pagination
          v-if="desserts.length > 0"
          :current-page.sync="page"
          :page-size="pageSize"
          @current-change="changePages"
        >
        </el-pagination>
      </div>
    </div>
  </div>
</template>

<script>
import ManagementLeaveService from "@/services/leave_management/managementLeave.service";
import moment from "moment";
import RestrictedView from "@/components/RestrictedView";

export default {
  name: "Approval",
  middleware: "authentication",
  async created() {
    await this.asyncDataActive();
  },
  components: {
    RestrictedView,
  },
  data() {
    return {
      action: "",
      desserts: [],
      page: 1,
      pageSize: 12,
      year: moment().year(),
      isApprove: false,
      editedIndexRequest: -1,
      leaveRequestsUpdate: [],

      actionItem: {
        action: "",
        request_off: {
          id: [],
          profile: {
            name: "",
          },
        },
        Date: 0,
        Reason: 0,
        Status: 0,
        comment: "",
      },
      defaultItem: {
        action: "",
        request_off: {
          profile: {
            name: "",
          },
        },
        Date: 0,
        Reason: 0,
        Status: 0,
        comment: "",
      },
    };
  },
  computed: {
    requestOffIds() {
      return (
        this.action === "Delete"
          ? this.leaveRequestsUpdate
          : this.leaveRequestsUpdate.filter(
              (request) => request.request_off?.status === "Pending"
            )
      ).map((request) => request.request_off.id);
    },
  },
  methods: {
    async asyncDataActive() {
      let response = await ManagementLeaveService.getManagementRequestOff(
        this.page,
        this.pageSize,
        this.year
      );
      if (response && response.status === 200 && response.data) {
        this.desserts = response.data;
      }
    },

    handleUpdateStatusLeaveRequest(selection) {
      this.leaveRequestsUpdate = selection;
    },

    async handleApproved() {
      this.action = "Approved";
      this.actionRequest();
    },

    async handleDelete() {
      if (this.checkSelected(this.leaveRequestsUpdate)) {
        this.action = "Delete";
        const loading = this.$loading({
          lock: true,
          text: "Loading",
          spinner: "el-icon-loading",
          background: "rgba(0, 0, 0, 0.7)",
        });
        const result = await ManagementLeaveService.deleteLeaveRequest({
          request_off_ids: this.requestOffIds,
        });
        loading.close();
        if (result) {
          this.$toast.success("Success");
          this.asyncDataActive();
        } else {
          this.$toast.error("Error");
        }
      }
    },

    async handleRejected() {
      this.action = "Rejected";
      this.actionRequest();
    },

    checkSelected(leaveRequestsUpdate) {
      if (leaveRequestsUpdate.length > 0) return true;
      else {
        this.$toast.warning("You have to select at least one row");
        return false;
      }
    },

    removeStatusCancel() {
      return this.leaveRequestsUpdate.filter(
        (item) => item.status !== "Cancel"
      );
    },

    async actionRequest() {
      if (this.requestOffIds.length > 0) {
        const loading = this.$loading({
          lock: true,
          text: "Loading",
          spinner: "el-icon-loading",
          background: "rgba(0, 0, 0, 0.7)",
        });
        const result = await ManagementLeaveService.actionRequest({
          action: this.action,
          comment: "",
          request_off_ids: this.requestOffIds,
        });
        loading.close();
        if (result) {
          this.$toast.success("Success");
          this.asyncDataActive();
        } else {
          this.$toast.error("Error");
        }
      } else {
        this.$toast.warning(
          "You have to select at least one row have status is Pending"
        );
        return false;
      }
    },

    async changePages() {
      let response = await ManagementLeaveService.getManagementRequestOff(
        this.page,
        this.pageSize
      );
      if (response && response.status === 200 && response.data) {
        this.desserts = response.data;
      }
    },
  },
};
</script>

<style lang="scss">
@import "./style.scss";
</style>
