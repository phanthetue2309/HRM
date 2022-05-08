<template>
  <div class="mt-3">
    <el-table highlight-current-row
              :data="desserts"
              header-cell-class-name="bg-header-table" border>
      <el-table-column sortable prop="user.name" label="Employee">
        <template slot-scope="scope">
          <div class="text-center">
            {{ scope.row.user.name }}
          </div>
        </template>
      </el-table-column>
      <el-table-column label="Dates" width="200" align="center">
        <template slot-scope="scope">
          <div v-for="dateOff in scope.row.wfh_date" :key="dateOff.id">
            {{ dateOff.date }}
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="reason" label="Reason" align="center"></el-table-column>
      <el-table-column prop="total" label="Total Days" align="center"></el-table-column>
    </el-table>
  </div>
</template>

<script>
import RequestWfhService from '@/services/wfh_management/request_wfh/request_wfh.services'

export default {
  name: 'WFHOfficeRequest',
  data() {
    return {
      desserts: [],
    }
  },
  async created(){
    await this.asyncDataActive()
  },
  methods: {
    async asyncDataActive(){
      this.desserts = await RequestWfhService.getAllRequest()
    }
  }
}
</script>
<style scoped>
</style>
