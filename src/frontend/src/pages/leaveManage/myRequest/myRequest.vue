<template>
  <div>
    <el-card class="mb-3">
      <div>
        <el-button
          type="primary"
          icon="el-icon-circle-plus"
          @click="addNewRequest"
        >
          New Request
        </el-button>
      </div>
    </el-card>
    <el-table
      highlight-current-row
      :data="requestOffs"
      header-cell-class-name="bg-header-table"
      border
    >
      <el-table-column label="List Date Off" width="240">
        <template slot-scope="scope">
          <div v-for="dateOff in scope.row.date_off" :key="dateOff.id">
            {{ dateOff.date }} ({{ dateOff.type }})
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="leave_type.name" label="Type Off" align="center">
      </el-table-column>
      <el-table-column
        prop="reason"
        label="Reason"
        align="center"
      ></el-table-column>
      <el-table-column prop="total" label="Total Leaves" width="110">
        <template slot-scope="scope">
          <div class="text-center">
            {{ scope.row.total }}
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="Status" width="200">
        <template slot-scope="scope">
          <div class="text-center">
            <div v-if="scope.row.status === 'Approved'">
              <el-button round type="success"> Approved </el-button>
            </div>
            <div v-else-if="scope.row.status === 'Rejected'">
              <el-button round type="danger"> Rejected </el-button>
            </div>
            <div v-else-if="scope.row.status === 'Cancel'">
              <el-button round type="danger"> Cancel </el-button>
            </div>
            <div v-else>
              <el-row>
                <el-button round type="warning"> Pending </el-button>
              </el-row>
              <el-row class="mt-2">
                <el-button round type="danger" @click="cancelDialog(scope.row)">
                  Cancel
                </el-button>
              </el-row>
            </div>
          </div>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog title="Cancel Request" :visible.sync="dialog">
      <div class="text-center text-danger">
        <h2>Do you want to cancel this request ?</h2>
      </div>
      <div class="mt-3 text-center">
        <el-button type="primary" @click="cancelRequest()">Confirm</el-button>
        <el-button type="danger" @click="closeDialog()">Cancel</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import moment from "moment";
import RequestOffService from "@/services/leave_management/request_off/request_off.services";
import ManagementLeaveService from "@/services/leave_management/managementLeave.service";

export default {
  name: "MyRequest",
  data() {
    return {
      dialog: false,
      year: moment().year(),
      month: moment().month(),
      requestOffs: [],
      editedIndexRequest: -1,
      actionItem: {
        action: "",
        request_off: {
          id: "",
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

  created() {
    this.getRequestOffs();
  },

  methods: {
    addNewRequest() {
      this.$router.push("/leaves/new-request");
    },

    async getRequestOffs() {
      this.requestOffs = await RequestOffService.getMyRequest();
    },

    cancelDialog(requestItem) {
      this.editedIndex = this.requestOffs.indexOf(requestItem);
      this.$set(this.actionItem, "action", "Cancel");
      this.actionItem = Object.assign({}, requestItem);
      this.$set(this.actionItem, "action", "Cancel");
      this.dialog = true;
    },

    closeDialog() {
      this.dialog = false;
      this.$nextTick(() => {
        this.actionItem = {};
      });
    },

    async cancelRequest() {
      let temp = this.requestOffs[this.editedIndex];
      temp.status = "Cancel";
      let formData = new FormData();
      formData.append("comment", "Cancel Request");
      formData.append("request_off_id", this.actionItem.id);
      formData.append("action", this.actionItem.action);
      let response = await ManagementLeaveService.actionRequest(formData);
      if (response.status === 201 && response.data) {
        this.$set(this.requestOffs, this.editedIndex, temp);
        this.$toast.success("Success");
      } else {
        this.$toast.error("Error");
      }
      this.closeDialog();
    },
  },
};
</script>

<style scoped></style>
