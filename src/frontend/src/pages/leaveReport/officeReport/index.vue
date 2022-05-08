<template>
  <div>
    <el-card>
      <el-row :gutter="12" class="mb-3">
        <el-col :span="4">
          <el-input v-model="search" placeholder="Search name or email" @change="updatePageSearch">
          </el-input>
        </el-col>
        <el-col :span="3">
          <el-date-picker v-model="date" type="month" placeholder="Select month"
                          @change="updatePageSearch" style="width: 100%"></el-date-picker>
        </el-col>
        <el-col :span="6">
          <el-select v-model="select" placeholder="Type" @change="updatePageSearch" style="width: 100%">
            <el-option v-for="data in selectData" :label="data" :value="data" :key="data">
            </el-option>
          </el-select>
        </el-col>
        <el-col :span="3">
          <download-excel
            :fetch="fetchDataForExportExcel"
            :fields="json_fields"
            :worksheet="year.toString()+ '-' + month.toString()"
            title="Export Excel"
            :name="year.toString()+ '-' + month.toString() + '.xls'">
            <el-button type="primary">
              <font-awesome-icon :icon="['fas', 'file-export']"/>
              {{ select }}
            </el-button>
          </download-excel>
        </el-col>
      </el-row>
      <el-table highlight-current-row :data="data" header-cell-class-name="bg-header-table" border style="width: 100%">
        <el-table-column v-for="(item,key) in headers"
                         :key="key"
                         :prop="item.value"
                         :label="item.text"
                         :fixed="item.text === 'Name' || item.text === 'Email'"
                         :width="item.text.length > 18 ? 300 : 200"
                         sortable
                         align="center"
        >
        </el-table-column>
      </el-table>
      <div class="text-center">
        <el-pagination :current-page.sync="page"
                       @current-change="getData">
        </el-pagination>
      </div>
    </el-card>
  </div>
</template>

<script>

import TypeOffAdminServices from '@/services/leave_management/type_off/type_off_admin.services'
import StatisticDateOffService from '@/services/leave_management/statisticDateOffService'

export default {
  name: 'OfficeReport',
  data() {
    return {
      page: 1,
      pageSize: 12,
      select: 'All',
      dataType: null,
      date: new Date(),
      menu: false,
      count: 0,
      search: '',
      dialog: false,
      data: [],
      detailData: [],
      month: new Date().getMonth() + 1,
      year: new Date().getFullYear(),
      selectData: [],
      json_fields_detail: {},
      json_fields: {
        'Name': 'name',
        'Email': 'email',
        'Holidays': 'holidays',
      },
      headers: [
        {
          text: 'Name',
          value: 'name',
          class: 'specialClass'
        },
        {
          text: 'Email',
          sortable: false,
          value: 'email',
          class: 'specialClass'
        },
        {
          text: 'Holidays',
          value: 'holidays',
          class: 'specialClass'
        }
      ],
    }
  },
  watch: {
    page() {
      this.getData()
    },
    pageSearch() {
      this.searchData()
    }
  },
  async created() {
    await this.getTypeOff()
    await this.getData()
    await this.getItemForExportTotal()
  },
  methods: {
    async getTypeOff() {
      const res = await TypeOffAdminServices.getTypeOff()
      let title = res.data
      let data = []
      for (let i = 0; i < title.length; i++) {
        data.push(title[i].name)
      }
      this.getDataForType(data)
      this.dataType = data
      this.selectData = this.dataType.concat(['All'])
    },

    getDataForType(listType) {
      for (let i = 0; i < listType.length; i++) {
        if (listType[i] !== 'All') {
          let data = {
            text: `${listType[i]} days`,
            value: `number_${listType[i]}`,
            detail: `${listType[i]}`,
            class: 'specialClass-1'
          }
          this.headers.push(data)
        }
      }
    },

    getItemForExportTotal() {
      for (let i = 0; i < this.dataType.length; i++) {
        this.json_fields[`Number of ${this.dataType[i]} days`] = `number_${this.dataType[i]}`
        this.json_fields[`${this.dataType[i]} days detail`] = {
          field: `${this.dataType[i]}`,
          callback: (value) => {
            return this.getCallBack(value)
          }
        }
      }
    },

    getCallBack(value) {
      const data = []
      for (let i = 0; i < value.length; i++) {
        let detailData = `${i + 1}: ${value[i].date} - ${value[i].type}`
        if (value[i].lunch) {
          detailData = detailData + ' - Have eat lunch'
        } else {
          detailData = detailData + ' - Don\'t have eat lunch'
        }
        data.push(detailData)
      }
      return data
    },

    async fetchDataForExportExcel() {
      const data = await StatisticDateOffService.getByAdmin(this.month, this.year, 1, this.count, '', '', '')
      return data.data.results
    },

    async updatePageSearch() {
      await this.searchData()
    },

    async searchData() {
      this.month = this.date.getMonth() + 1
      this.year = this.date.getFullYear()
      let name = ''
      let email = ''
      let type = ''
      if (this.select != null) {
        type = this.select
        this.headers = [
          {
            text: 'Name',
            value: 'name'
          },
          {
            text: 'Email',
            sortable: false,
            value: 'email'
          },
          {
            text: 'Holidays',
            value: 'holidays'
          },
        ]
        this.getDataForType([this.select])
      }
      if (this.select === 'All') {
        type = ''
        this.getDataForType(this.dataType)
      }
      if (this.search != '') {
        name = this.search
      }
      if (this.search.includes('@')) {
        email = this.search
        name = ''
      }
      if (this.date) {
        this.month = this.date.getMonth() + 1
        this.year = this.date.getFullYear()
      }
      const data = await StatisticDateOffService.getByAdmin(this.month, this.year, this.page, this.pageSize, name, email, type)
      if (data) {
        this.data = data.data.results
        return this.data
      }
      return []

    },

    async getData() {
      const data = await StatisticDateOffService.getByAdmin(this.month, this.year, this.page, this.pageSize, '', '', '')
      if (data) {
        this.data = data.data.results
        this.count = data.data.count
      }

    },
  },
}
</script>

<style>

</style>
