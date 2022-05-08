<template>
  <div class="mt-3">
    <sync-buttons @refreshDesserts="asyncDataActive"></sync-buttons>
    <el-table
      highlight-current-row
      :data="desserts"
      header-cell-class-name="bg-header-table"
      border
    >
      <el-table-column sortable prop="profile.name" label="Employee">
        <template slot-scope="scope">
          <div class="text-center">
            {{ scope.row.profile.name }}
          </div>
        </template>
      </el-table-column>
      <el-table-column label="Date Off" width="200">
        <template slot-scope="scope">
          <div v-for="dateOff in scope.row.date_off" :key="dateOff.id">
            {{ dateOff.date }} ({{ dateOff.type }})
          </div>
        </template>
      </el-table-column>
      <el-table-column sortable prop="leave_type.name" label="Leave Type">
        <template slot-scope="scope">
          <div class="text-center">
            {{ scope.row.leave_type.name }}
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="reason" label="Reason"></el-table-column>
      <el-table-column prop="status" label="Status" width="150">
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
              <el-button round type="warning"> Pending </el-button>
            </div>
          </div>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import RequestOffService from "@/services/leave_management/request_off/request_off.services";
import syncButtons from "./sync-buttons.vue";

export default {
  components: { syncButtons },
  name: "OfficeRequest",
  data() {
    return {
      desserts: [],
    };
  },
  async created() {
    await this.asyncDataActive();
  },
  methods: {
    async asyncDataActive() {
      this.desserts = await RequestOffService.getAllRequest();
    },
  },
};
</script>

<style scoped></style>
