<template>
  <div class="my-2">
    <div class="bg-light">
      <el-row>
        <el-col :xs="24" :sm="24" :md="8" :lg="4" :xl="4" class="pr-2">
          <el-row style="height: 60px;"></el-row>
          <el-row>
            <div>
              <div class="text-center">
                <el-button type="danger" round class="btn-calendar">Calendar Type</el-button>
              </div>
              <br/>
              <div class="text-center">
                <el-checkbox v-model="leave" label="Show Leave" @change="checkBox">
                </el-checkbox>
              </div>
              <div class="text-center">
                <el-checkbox v-model="lunch" label="Show Lunch" @change="checkBox">
                </el-checkbox>
              </div>
            </div>
            <el-divider class="mr-2"><i class="el-icon-star-on"></i></el-divider>
            <div>
              <div class="text-center mb-3">
                <el-button type="primary" round class="btn-calendar">Today Information</el-button>
              </div>
              <div class="description-detail mt-1">
                <div class="box-description-leave ml-5"></div>
                <small class="ml-4"> {{ leavesToday }} - Leave</small>
              </div>
              <div class="description-detail mt-1">
                <div class="box-description-lunch ml-5"></div>
                <small class="ml-4">{{ lunchesToday }} - Lunch</small>
              </div>
              <div class="description-detail mt-1">
                <div class="box-description-veggie ml-5"></div>
                <small class="ml-4">{{ veggiesToday }} - Veggie</small>
              </div>
            </div>
            <el-divider class="mr-2"><i class="el-icon-star-on"></i></el-divider>
            <div>
              <div class="text-center mb-3">
                <el-button round type="warning" class="btn-calendar">Descriptions</el-button>
              </div>
              <div class="description-detail mt-1">
                <div class="box-description-lunar ml-5"></div>
                <small class="ml-3">Lunar Day</small>
              </div>
              <div class="description-detail mt-1">
                <div class="box-description-current ml-5"></div>
                <small class="ml-3">Current Day</small>
              </div>
            </div>
          </el-row>
        </el-col>
        <el-col :xs="24" :sm="24" :md="16" :lg="20" :xl="20">
          <FullCalendar ref="fullCalendar" :options="calendarOptions"/>
        </el-col>
      </el-row>
      <el-dialog :visible.sync="dialogDetail" :title="selectedEvent.title" max-width="400">
        <el-card v-if="selectedEvent.has_veggie != null">
          <div v-for="(item, index) in selectedEvent.detail" :key="index">
            {{ index + 1 }} - {{ item.profile.name }}
          </div>
        </el-card>
        <el-card v-else>
          <div v-for="(item, index) in selectedEvent.detail" :key="index">
            {{ index + 1 }} - {{ item.name }} - {{ item.typeOff }} - {{ item.timeType }}
          </div>
        </el-card>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import 'vue-cal/dist/vuecal.css'
import CalendarAdminServices from '@/services/company_calendar/company_calendar.services'
import UserLunchService from '@/services/company_calendar/user-lunch'
import FullCalendar from '@fullcalendar/vue'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import moment from 'moment'

export default {
  name: 'companyCalendar',
  components: {
    FullCalendar
  },
  middleware: 'authentication',
  data() {
    return {
      selectedEvent: {},
      title: '',
      today: new Date().toISOString().substr(0, 10),
      dialogDetail: false,
      lunch: true,
      leave: true,
      showDialog: false,
      calendarOptions: {
        themeSystem: 'bootstrap',
        firstDay: 1,
        plugins: [
          dayGridPlugin,
          timeGridPlugin,
          interactionPlugin // needed for dateClick
        ],
        headerToolbar: {
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        events: [],
        eventClick: this.handleEventClick
      },
      leaveEvents: [],
      lunchEvents: [],
      lunarDay: [],
      leavesToday: 0,
      lunchesToday: 0,
      veggiesToday: 0,
    }
  },
  async mounted() {
    this.lunarDays()
    await this.getLeave()
    await this.getUserLunches()
  },
  methods: {
    lunarDays() {
      let calendarApi = this.$refs.fullCalendar.getApi()
      let dateCalendar = calendarApi.getDate()
      let year = dateCalendar.getFullYear()
      let month = dateCalendar.getMonth()
      for (let day = 0; day < 32; day++) {
        let lunarDate = moment().year(year).month(month).date(day).lunar().format('DD')
        if (lunarDate == 15 || lunarDate == 1) {
          let date = `${year}-${month + 1}-${day}`
          let nextDate = `${year}-${month + 1}-${day + 1}`
          if (month < 9) {
            date = `${year}-0${month + 1}-${day}`
            nextDate = `${year}-0${month + 1}-${day + 1}`
            if (day == 31) {
              nextDate = `${year}-0${month + 2}-01`
            }
            if (day < 10) {
              date = `${year}-0${month + 1}-0${day}`
              nextDate = `${year}-0${month + 1}-0${day + 1}`
            }
          } else {
            if (day == 31) {
              nextDate = `${year}-${month + 2}-01`
            }
            if (day < 10) {
              date = `${year}-${month + 1}-0${day}`
              nextDate = `${year}-${month + 1}-0${day + 1}`
            }
          }
          let dataDay = {
            start: date,
            end: nextDate,
            display: 'background',
            backgroundColor: '#45BCF3'
          }
          this.lunarDay.push(dataDay)
        }
      }
    },
    async getLeave() {
      await CalendarAdminServices.getCalendar()
        .then(res => {
          let off = []
          for (let i = 0; i < res.length; i++) {
            res[i].title = 'Days off'
            res[i].color = '#25c9d0'
            off.push(res[i])
          }
          this.leaveEvents = this.changeFormatLeave(off)
        })
    },
    checkBox() {
      if (this.leave === false && this.lunch === true) {
        this.calendarOptions.events = this.lunchEvents.concat(this.lunarDay)
      } else if (this.leave === false && this.lunch === false) {
        this.calendarOptions.events = this.lunarDay
      } else if (this.leave === true && this.lunch === false) {
        this.calendarOptions.events = this.leaveEvents.concat(this.lunarDay)
      } else {
        this.calendarOptions.events = this.leaveEvents.concat(this.lunchEvents, this.lunarDay)
      }
    },
    handleEventClick(e) {
      this.selectedEvent = this.calendarOptions.events.find(item => item.id === e.event.id)
      this.dialogDetail = true
    },
    changeFormatLunch(arr) {
      let dataArr = arr.map(item => {
        return [item.date, item]
      })
      let mapArr = new Map(dataArr)
      let result = [...mapArr.values()]
      return result.map(item => {
        let len = []
        for (const element of arr) {
          if (item.date === element.date) {
            len.push(element)
            if (element.date === this.today) {
              if (!item.has_veggie)
                this.lunchesToday += 1
              else
                this.veggiesToday += 1
            }

          }
        }
        return {
          title: item.has_veggie ? `Veggie Lunch : ${len.length}` : `Lunch: ${len.length}`,
          id: item.id,
          detail: len,
          start: item.date,
          end: item.date,
          has_veggie: item.has_veggie,
          color: item.has_veggie ? '#90BE6D' : '#F9C74F'
        }
      })
    },
    changeFormatLeave(arr) {
      let dataArr = arr.map(item => {
        return [item.start, item]
      })
      let mapArr = new Map(dataArr)
      let result = [...mapArr.values()]
      return result.map(item => {
        let len = []
        for (const element of arr) {
          if (item.start === element.start) {
            len.push(element)
            if (element.start === this.today)
              this.leavesToday += 1
          }
        }
        return {
          title: item.title + ': ' + len.length,
          id: item.id,
          detail: len,
          start: item.start,
          end: item.end,
          color: item.color
        }
      })
    },
    async getUserLunches() {
      const userLunches = await UserLunchService.getAll()
      let notVeg = userLunches.data.filter(item => item.has_veggie === false)
      let hasVeg = userLunches.data.filter(item => item.has_veggie === true)
      let newNotVeg = this.changeFormatLunch(notVeg)
      let newHasVeg = this.changeFormatLunch(hasVeg)
      this.lunchEvents = newNotVeg.concat(newHasVeg)
      this.calendarOptions.events = this.leaveEvents.concat(this.lunchEvents, this.lunarDay)
    },
  }
}
</script>

<style lang="scss" scoped>
@import "./style.scss";
</style>
