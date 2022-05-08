<template>
  <div>
    <el-card>
      <div>
        <el-button type="primary" icon="el-icon-circle-plus" @click="addNewRequest">
            New WFH Request
        </el-button>
      </div>
    </el-card>
    <el-table highlight-current-row :data="wfhRequests" header-cell-class-name="bg-header-table" border>
      <el-table-column label="Dates" width="240" align="center">
        <template slot-scope="scope">
          <div v-for="WFHdate in scope.row.wfh_date" :key="WFHdate.id">
              {{ WFHdate.date }}
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="reason" label="Reason" align="center"></el-table-column>
      <el-table-column prop="total" label="Total" align="center"></el-table-column>
    </el-table>
  </div>
</template>

<script>
import moment from 'moment'
import RequestWfhService from '@/services/wfh_management/request_wfh/request_wfh.services'

export default {
  name: 'WFHRequest',
  data() {
    return {
      dialog: false,
      year: moment().year(),
      month: moment().month(),
      wfhRequests: [],
      Reason: 0,
    }
  },
  created(){
      this.getWfhRequest()
  },
  methods: {
      addNewRequest(){
          this.$router.push('/workfromhome/new-wfh-request')
      },
      async getWfhRequest(){
          this.wfhRequests = await RequestWfhService.getMyWfhRequest()
      },
  }
}
</script>

<style scoped>

</style>
