<template>
  <div class="bg-light">
    <div v-if="isLoadingMask" class="lmask" ref="loading-mask"></div>
    <div :style="{visibility: !isLoadingMask ? 'visible' : 'hidden'}">
      <el-form :inline="true" class="m-3">
        <div class="d-flex flex-row">
          <el-form-item label="Member : ">
            <el-select v-model="memberChoose" placeholder="Pick a member" @change="memberChange">
              <el-option
                v-for="item in memberTeams"
                :key="item.profile_id" :label="item.name" :value="item.profile_id"
              ></el-option>
            </el-select>
          </el-form-item>
          <div v-if="statisticByMonth===true">
            <el-form-item label="Month : ">
              <el-select v-model="monthChoose" placeholder="Pick a Month" @change="getDataByMonthYear">
                <el-option
                  v-for="item in monthInYear"
                  :key="item" :label="item" :value="item"
                ></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="Year : ">
              <el-date-picker v-model="yearChoose" type="year" placeholder="Pick a Year" value-format="yyyy"
                              @change="getData">
              </el-date-picker>
            </el-form-item>
            <el-form-item>
              <download-excel
                :fetch="fetchDataForExportExcel"
                :fields="json_fields"
                :worksheet="yearChoose.toString()+ '-' + monthChoose.toString()"
                title="Export Excel"
                :name="yearChoose.toString()+ '-' + monthChoose.toString() + '.xls'">
                <el-button type="primary">
                  <font-awesome-icon :icon="['fas', 'file-export']"/>
                  Export Data
                </el-button>
              </download-excel>
            </el-form-item>
          </div>
          <div v-else>
            <el-form-item label="Year : ">
              <el-date-picker v-model="yearChoose" type="year" placeholder="Pick a Year" value-format="yyyy"
                              @change="getData">
              </el-date-picker>
            </el-form-item>
          </div>
        </div>
      </el-form>
      <el-button class="ml-3" type="primary" @click="statisticChange()">
        {{ titleButton }}
      </el-button>
      <div v-if="leaveUser.length > 0 && series.length > 0">
        <div v-if="loaded">
          <apexchart type="bar" height="450" :options="chartOptions" :series="series">
          </apexchart>
        </div>
      </div>
      <div v-else class="text-center">
        <h2 class="text-danger">No data to show.</h2>
      </div>
    </div>
  </div>
</template>

<script>
import TypeOffAdminServices from "@/services/leave_management/type_off/type_off_admin.services";
import StatisticDateOffService from "@/services/leave_management/statisticDateOffService";

export default {
  name: 'TeamReport',
  data() {
    return {
      isLoadingMask: true,
      profile: localStorage.getItem('profile_id'),
      load: false,
      leaveUser: [],
      listTypeOff: [],
      memberTeams: [],
      listTotalLeaveDays: [],
      monthInYear: [],
      dataAllYear: [],
      headers: [],
      monthChoose: String(new Date().getMonth() + 1), //January is 0
      yearChoose: String(new Date().getFullYear()),
      memberChoose: '0',
      statisticByMonth: true,
      titleButton: 'Statistic by Month',
      json_fields: {
        'Name': 'name',
        'Email': 'email',
        'Holidays': 'holidays',
      },
      series: [],
      chartOptions: {
        chart: {
          type: 'bar',
          height: 300,
          stacked: true,
          toolbar: {
            show: true,
          },
          zoom: {
            enabled: true,
          },
        },
        responsive: [
          {
            breakpoint: 480,
            options: {
              legend: {
                position: 'bottom',
                offsetX: -10,
                offsetY: 0,
              },
            },
          },
        ],
        plotOptions: {
          bar: {
            horizontal: false,
            borderRadius: 10,
          },
        },
        xaxis: {
          categories: ['Holidays', 'Lefts Days'],
        },
        legend: {
          position: 'right',
          offsetY: 40,
        },
        fill: {
          opacity: 1,
        },
      },
    }
  },
  async created() {
    setTimeout(this.disableMask, 500)
    await this.getTypeOff()
    await this.getData()
    await this.getItemForExportTotal()
  },
  methods: {
    disableMask() {
      this.isLoadingMask = false
    },

    async getTypeOff() {
      const res = await TypeOffAdminServices.getTypeOff()
      this.listTypeOff = res.data
      for (let i = 0; i < this.listTypeOff.length; i++) {
        if (this.listTypeOff[i].type != 1) {
          let data = {
            text: `${this.listTypeOff[i].name} days in month`,
            value: `number_${this.listTypeOff[i].name}`,
            detail: `${this.listTypeOff[i].name}`,
          }
          this.headers.push(data)
          this.listTotalLeaveDays.push(0)
        }
      }
      for (let i = 1; i < 13; i++) {
        this.monthInYear.push(i)
      }
    },

    async getData() {
      if (this.statisticByMonth === true) {
        this.titleButton = 'Statistic by Year'
        await this.getDataByMonthYear()
      } else {
        this.titleButton = 'Statistic by Month'
        await this.getDataByYear()
      }
    },

    async getDataByMonthYear() {
      this.loaded = false
      this.series = []
      this.memberTeams = []
      const allMember = {
        profile_id: '0',
        email: 'All',
        name: 'All',
      }
      this.memberTeams.push(allMember)
      this.listTotalLeaveDays.fill(0)
      const res = await StatisticDateOffService.getMyTeam(this.profile, this.monthChoose, this.yearChoose)
      if (res.data.length > 0) {
        this.leaveUser = res.data
        for (const user in this.leaveUser) {
          const teamMember = {
            profile_id: this.leaveUser[user].id,
            email: this.leaveUser[user].email,
            name: this.leaveUser[user].name
          }
          this.memberTeams.push(teamMember)
        }
        await this.getDataChange()
      } else this.leaveUser = []
    },

    async getDataByYear() {
      this.loaded = false
      this.series = []
      const res = await StatisticDateOffService.getMyTeamYear(this.profile, this.yearChoose)
      if (res.data.length > 0) {
        this.dataAllYear = res.data
        await this.getDataChange()
      } else {
        this.dataAllYear = []
      }
    },

    getDetailData(name, value) {
      return this.leaveUser.find((data) => data.name === name)[value]
    },

    statisticChange() {
      this.statisticByMonth = !this.statisticByMonth
      if (this.statisticByMonth === false) {
        this.titleButton = 'Statistic by Month'
        this.getDataByYear()
      } else {
        this.titleButton = 'Statistic by Year'
        this.getDataByMonthYear()
      }
    },

    memberChange() {
      this.series = []
      if (this.memberChoose === '0') {
        this.getDataChange()
      } else {
        if (this.statisticByMonth) {
          const detailUser = this.leaveUser.find((data) => data.id === this.memberChoose)
          const holidays = {
            name: "Holidays",
            data: [detailUser.holidays, 0]
          }
          this.series.push(holidays)
          for (const header in this.headers) {
            const leftDay = {
              name: this.headers[header].detail,
              data: [0, detailUser[this.headers[header].value]]
            }
            this.series.push(leftDay)
          }
        } else {
          this.listTotalLeaveDays.fill(0)
          for (const month in this.dataAllYear) {
            if (this.dataAllYear[month].length > 0) {
              for (const profile in this.dataAllYear[month]) {
                if (this.memberChoose === this.dataAllYear[month][profile].profile_id) {
                  for (const header in this.headers) {
                    this.listTotalLeaveDays[header] += this.dataAllYear[month][profile][this.headers[header].value]
                  }
                }
              }
            }
          }
          for (const header in this.headers) {
            const leftDay = {
              name: this.headers[header].detail,
              data: [0, this.listTotalLeaveDays[header]]
            }
            this.series.push(leftDay)
          }
        }
      }
    },

    getDataChange() {
      this.listTotalLeaveDays.fill(0)
      let holidayTotal = 0
      if (this.statisticByMonth) {
        // calculate by month
        for (const detail in this.leaveUser) {
          holidayTotal += this.leaveUser[detail].holidays
          for (const header in this.headers) {
            this.listTotalLeaveDays[header] += this.leaveUser[detail][this.headers[header].value]
          }
        }
      } else {
        //calculate by year
        for (const month in this.dataAllYear) {
          if (this.dataAllYear[month].length > 0) {
            for (const profile in this.dataAllYear[month]) {
              holidayTotal += this.dataAllYear[month][profile].holidays
              for (const header in this.headers) {
                this.listTotalLeaveDays[header] += this.dataAllYear[month][profile][this.headers[header].value]
              }
            }
          }
        }
      }
      // add data to series
      const holidays = {
        name: "Holidays",
        data: [holidayTotal / (this.memberTeams.length - 1), 0]
      }
      this.series.push(holidays)
      for (const header in this.headers) {
        const leftDay = {
          name: this.headers[header].detail,
          data: [0, this.listTotalLeaveDays[header]]
        }
        this.series.push(leftDay)
      }
      this.loaded = true
    },

    async fetchDataForExportExcel() {
      const res = await StatisticDateOffService.getMyTeam(this.profile, this.monthChoose, this.yearChoose)
      return res.data
    },

    getItemForExportTotal() {
      for (let i = 0; i < this.listTypeOff.length; i++) {
        this.json_fields[`Number of ${this.listTypeOff[i].name} days`] = `number_${this.listTypeOff[i].name}`
        this.json_fields[`${this.listTypeOff[i].name} days detail`] = {
          field: `${this.listTypeOff[i].name}`,
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
  }
}

</script>

<style lang="scss" scoped>
.lmask {
  position: sticky;
  height: calc(100vh - 110px);
  width: 100%;
  bottom: 0;
  left: 0;
  right: 0;
  top: 0;
  z-index: 0;
  opacity: 0.4;

  &.fixed {
    position: fixed;
  }

  &:before {
    content: "";
    background-color: rgba(0, 0, 0, 0);
    border: 5px solid rgba(0, 183, 229, 0.9);
    opacity: 0.9;
    border-right: 5px solid rgba(0, 0, 0, 0);
    border-left: 5px solid rgba(0, 0, 0, 0);
    border-radius: 50px;
    box-shadow: 0 0 35px #2187e7;
    width: 50px;
    height: 50px;
    -moz-animation: spinPulse 1s infinite ease-in-out;
    -webkit-animation: spinPulse 1s infinite linear;

    margin: -25px 0 0 -25px;
    position: absolute;
    top: 50%;
    left: 50%;
  }

  &:after {
    content: "";
    background-color: rgba(0, 0, 0, 0);
    border: 5px solid rgba(0, 183, 229, 0.9);
    opacity: 0.9;
    border-left: 5px solid rgba(0, 0, 0, 0);
    border-right: 5px solid rgba(0, 0, 0, 0);
    border-radius: 50px;
    box-shadow: 0 0 15px #2187e7;
    width: 30px;
    height: 30px;
    -moz-animation: spinoffPulse 1s infinite linear;
    -webkit-animation: spinoffPulse 1s infinite linear;

    margin: -15px 0 0 -15px;
    position: absolute;
    top: 50%;
    left: 50%;
  }
}

@-moz-keyframes spinPulse {
  0% {
    -moz-transform: rotate(160deg);
    opacity: 0;
    box-shadow: 0 0 1px #2187e7;
  }
  50% {
    -moz-transform: rotate(145deg);
    opacity: 1;
  }
  100% {
    -moz-transform: rotate(-320deg);
    opacity: 0;
  }
}

@-moz-keyframes spinoffPulse {
  0% {
    -moz-transform: rotate(0deg);
  }
  100% {
    -moz-transform: rotate(360deg);
  }
}

@-webkit-keyframes spinPulse {
  0% {
    -webkit-transform: rotate(160deg);
    opacity: 0;
    box-shadow: 0 0 1px #2187e7;
  }
  50% {
    -webkit-transform: rotate(145deg);
    opacity: 1;
  }
  100% {
    -webkit-transform: rotate(-320deg);
    opacity: 0;
  }
}

@-webkit-keyframes spinoffPulse {
  0% {
    -webkit-transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(360deg);
  }
}
</style>
