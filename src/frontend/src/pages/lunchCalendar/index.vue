<template>
  <div class="my-2">
    <div class="bg-light">
      <el-col :xs="24" :sm="24" :md="8" :lg="4" :xl="4" class="pr-2">
        <el-row style="height: 60px;">
        </el-row>
        <el-row>
          <div class="text-center">
            <el-dropdown placement="top-end">
              <div class="text-center mb-3 mx-2">
                <el-button class="btn_lunch" type="primary">
                  SET LUNCH
                </el-button>
              </div>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item @click.native="dialog = true">
                  Range
                </el-dropdown-item>
                <el-dropdown-item @click.native="setToday">
                  Today
                </el-dropdown-item>
                <el-dropdown-item v-if="!userVeggie" @click.native="setVeggieLunch()">
                  Veggie
                </el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
            <el-dropdown>
              <div class="text-center mx-2">
                <el-button class="btn_lunch" type="danger">
                  CANCEL LUNCH
                </el-button>
              </div>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item v-if="userVeggie" @click.native="cancelSetVeggieLunch()">
                  Veggie
                </el-dropdown-item>
                <el-dropdown-item @click.native="deleteMany()">
                  Set
                </el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </div>
          <div class="group-checkbox">
            <div class="checkbox-calendar d-flex justify-content-center mt-3">
              <el-checkbox v-model="userVeggie" label="Auto Veggie" size="medium"
                           @change="updateVeggieOfUser">
              </el-checkbox>
            </div>
            <div class="checkbox-calendar d-flex justify-content-center ">
              <el-checkbox v-model="autoBooking" label="Auto Booking" size="medium"
                           @change="updateStatusAutoBooking">
              </el-checkbox>
            </div>
          </div>
          <el-divider class="mr-2"><i class="el-icon-star-on"></i></el-divider>
          <div>
            <div class="text-center mb-3">
              <el-button round type="warning" class="btn_lunch">Descriptions</el-button>
            </div>
            <div class="description-detail">
              <div class="box-description-lunar ml-5"></div>
              <small class="ml-3">Lunar Day</small>
            </div>
            <div class="description-detail">
              <div class="box-description-current ml-5"></div>
              <small class="ml-3">Current Day</small>
            </div>
          </div>
        </el-row>
      </el-col>
      <el-col :xs="24" :sm="24" :md="16" :lg="20" :xl="20">
        <FullCalendar ref="fullCalendar" :options="calendarOptions"/>
      </el-col>
      <el-dialog title="SET LUNCH RANGE" :visible.sync="dialog" max-width="500">
        <el-card>
          <el-container>
            <el-form>
              <div class="d-flex flex-row">
                From
                <flat-pickr
                  v-model="startDate" class="bg-white ml-3 mb-2 mr-3" placeholder="Select date"
                  :config="{
                         altInput: true,
                         altFormat: 'd-m-Y',
                         minDate: this.today,
                         dateFormat: 'Y-m-d',
                         locale: { firstDayOfWeek: 1 },
                         }"
                />
                To
                <flat-pickr
                  v-model="endDate" class="bg-white ml-3 mb-2" placeholder="Select date"
                  :config="{
                         altInput: true,
                         altFormat: 'd-m-Y',
                         minDate: this.startDate? this.startDate : this.today,
                         dateFormat: 'Y-m-d',
                         locale: { firstDayOfWeek: 1 },
                         }"
                />
                <p class="ml-3">Has Veggie</p>
                <font-awesome-icon :icon="['fas', 'leaf']" class="text-success fa-fw"/>
                <input v-model="has_veggie" type="checkbox" class="form-check-input ml-2"/>
                <span class="checkmark"/>
              </div>
              <div class="d-flex justify-content-end">
                <el-button @click="addEvent()" class="btn_submit ml-2">
                  Create Lunch
                </el-button>
              </div>
            </el-form>
          </el-container>
        </el-card>
      </el-dialog>
      <el-dialog :visible.sync="dialogDetail" max-width="300">
        <el-card v-if="selectedEvent.title === 'Lunch' || selectedEvent.title === 'Veggie Lunch'">
          <div slot="header">
            <span>{{ selectedEvent.title }}</span>
          </div>
          <div class="d-flex flex-row">
            <p class="mt-3">Do you want to cancel lunch today ? </p>
            <el-button class="ml-3" type="danger" @click="deleteEvent(selectedEvent)">
              <i class="el-icon-delete"></i>
            </el-button>
            <div v-if="checkLunarDay() === true">
              <el-checkbox class="mt-3 ml-4" v-model="selectedEvent.has_veggie">
                Has veggie
              </el-checkbox>
              <font-awesome-icon :icon="['fas', 'leaf']" class="mt-3 ml-3"/>
              <el-button class="ml-3" type="primary" @click="updateEvent(selectedEvent)">
                Update
              </el-button>
            </div>
          </div>
        </el-card>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import FullCalendar from '@fullcalendar/vue'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import UserLunchService from '@/services/company_calendar/user-lunch'
import ProfileService from '@/services/profile/profile'
import flatPickr from 'vue-flatpickr-component'
import 'flatpickr/dist/flatpickr.css'
import moment from 'moment'
import 'moment-lunar'

export default {
  name: 'LunchCalendar',
  middleware: 'authentication',
  components: {
    FullCalendar,
    flatPickr
  },
  data() {
    return {
      lunch: true,
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
        contentHeight: 800,
        events: [],
        eventClick: this.handleEventClick
      },
      selectedEvent: {},
      content: '',
      eventsLunch: [],
      today: new Date().toISOString().substr(0, 10),
      focus: new Date().toISOString().substr(0, 10),
      name: 'Lunch',
      start: null,
      userVeggie: false, // using when user want to set auto has veggie in lunar day
      has_veggie: false, // using in lunar day
      end: null,
      color: '#20B2AA', // default event color
      currentlyEditing: null,
      dialog: false,
      startDate: new Date().toISOString().substr(0, 10),
      endDate: null,
      dialogDetail: false,
      lunarDay: [],
      autoBooking: false,
      profile: '',
    }
  },
  async mounted() {
    this.lunarDays()
    await this.getEvents()
    await this.getMyProfile()
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

    checkLunarDay() {
      const data = this.lunarDay.find((item) => item.start === this.selectedEvent.start)
      return !(typeof (data) === "undefined" || data.length === 0)
    },

    async getEvents() {
      this.eventsLunch = await this.$store.dispatch('event/getUserLunches')
      this.calendarOptions.events = this.eventsLunch.concat(this.lunarDay)
      this.eventsLunch.map(e => {
        if (e.has_veggie === true) {
          this.userVeggie = true
        }
      })
    },

    handleEventClick(e) {
      this.selectedEvent = this.calendarOptions.events.find(item => item.id === e.event.id)
      this.dialogDetail = true
    },
    async deleteMany() {
      const data = {
        date: this.today
      }
      const userLunch = await UserLunchService.deleteMany(data)
      await this.getEvents()
      if (userLunch && userLunch.data.msg) {
        const content = userLunch.data.msg
        this.$toast.success(content)
        this.userVeggie = false
      }
    },

    async setVeggieLunch() {
      const date = new Date()
      const hours = date.getHours()
      if (hours >= 9) {
        return this.$toast.error('Out of time to set lunch')
      }
      const data = {
        date: this.today
      }
      const userLunch = await UserLunchService.setVeggieMonth(data)
      const contentRes = 'Not found lunar day'
      await this.getEvents()
      if (userLunch && userLunch.data.msg !== contentRes) {
        const content = userLunch.data.msg
        this.$toast.success(content)
        this.userVeggie = true
      }
      if (userLunch && userLunch.data.msg === contentRes) {
        this.$toast.error(contentRes)
      }
    },

    async cancelSetVeggieLunch() {
      const date = new Date()
      const hours = date.getHours()
      if (hours >= 9) {
        return this.$toast.error('Out of time to set lunch')
      }
      const data = {
        date: this.today
      }
      const userLunch = await UserLunchService.cancelSetVeggieMonth(data)
      await this.getEvents()
      if (userLunch && userLunch.data.msg) {
        const content = userLunch.data.msg
        this.$toast.success(content)
      }
      this.userVeggie = false
    },

    async setToday() {
      const date = new Date()
      const hours = date.getHours()
      if (hours >= 9) {
        return this.$toast.error('Out of time to set lunch')
      }
      this.focus = this.today
      const data = {
        name: this.name,
        has_veggie: this.has_veggie || false,
        date: this.today
      }
      const userLunch = await UserLunchService.create(data)
      await this.getEvents()
      if (userLunch && userLunch.data.date) {
        this.$toast.success('You have setted lunch for today')
      }
      if (userLunch && userLunch.data.error_msg) {
        this.$toast.error(userLunch.data.error_msg)
      }
    },

    async addEvent() {
      this.dialog = false
      const date = new Date()
      const hours = date.getHours()
      const today = moment()
      if (this.startDate > this.endDate) {
        return this.$toast.error('End day must be greater than start day')
      }
      if (this.startDate < this.today) {
        return this.$toast.error('Start day must be greater than today')
      }
      if (this.startDate === this.today && hours >= 9) {
        this.startDate = moment(today).add(1, 'days')
      }
      if (this.startDate && this.endDate) {
        const data = {
          name: this.name,
          has_veggie: this.has_veggie,
          list_dates: this.getDatesUnRange(this.startDate, this.endDate)
        }
        const userLunches = await UserLunchService.createMany(data)
        await this.getEvents()
        if (userLunches && userLunches.data.msg) {
          const content = userLunches.data.msg
          this.$toast.success(content)
        }
      } else alert('You must enter start and end time')
    },

    editEvent(ev) {
      this.currentlyEditing = ev.id
    },

    async updateEvent(ev) {
      const date = new Date()
      const hours = date.getHours()
      if (hours >= 9 && ev.start <= this.today) {
        return this.$toast.error('Out of time to set lunch')
      }
      const data = {
        has_veggie: ev.has_veggie
      }
      await UserLunchService.update({data, id: ev.id})
      this.currentlyEditing = null
      await this.getEvents()
      this.dialogDetail = false
    },

    async deleteEvent(ev) {
      const date = new Date()
      const hours = date.getHours()
      if (hours >= 9 && ev.start <= this.today) {
        return this.$toast.error('Out of time to set lunch')
      }
      const userLunch = await UserLunchService.delete(ev.id)
      await this.getEvents()
      if (userLunch && userLunch.data.msg) {
        const content = userLunch.data.msg
        this.$toast.success(content)
      }
      this.dialogDetail = false
    },

    getDatesUnRange(startDate, stopDate) {
      const dateArray = []
      let currentDate = moment(startDate)
      let endDate = moment(stopDate)
      while (currentDate <= endDate) {
        dateArray.push(moment(currentDate).format('YYYY-MM-DD'))
        currentDate = moment(currentDate).add(1, 'days')
      }
      return dateArray
    },

    async getMyProfile() {
      const user = this.$store.state.user.currentUser
      const res = await ProfileService.getOneProfile(user.profile_id)
      this.profile = res.data
      this.autoBooking = this.profile.auto_booking_lunch
      this.userVeggie = this.profile.veggie
    },

    async updateStatusAutoBooking() {
      try {
        const data = {
          auto_booking_lunch: this.autoBooking
        }
        const date = new Date()
        const hours = date.getHours()
        const today = moment()
        await ProfileService.updateAutoBookingLunch(this.profile.id, data)
        this.$toast.success('Update Status Success')
        if (this.autoBooking == true) {
          this.startDate = this.today
          if (hours >= 9) {
            this.startDate = moment(today).add(1, 'days').format('YYYY-MM-DD')
          }
          this.endDate = moment().endOf('month').format('YYYY-MM-DD')
          const dataSetLunch = {
            name: this.name,
            has_veggie: this.has_veggie,
            list_dates: this.getDatesUnRange(this.startDate, this.endDate)
          }
          const userLunches = await UserLunchService.createMany(dataSetLunch)
          await this.getEvents()
          if (userLunches && userLunches.data.msg) {
            const content = userLunches.data.msg
            this.$toast.success(content)
          }
        }
      } catch (e) {
        console.log(e)
        this.$toast.error('Update Status Failed')
      }
    },

    async updateVeggieOfUser() {
      const data = {
        veggie: this.userVeggie
      }
      await ProfileService.updateUserVeggie(this.profile.id, data).then(async (res) => {
          try {
            console.log(res)
            if (res.status == 204) {
              for (const date in this.lunarDay) {
                let userLunch = this.calendarOptions.events.find(item => (item.start === this.lunarDay[date].start)
                  && (new Date(item.start).getDate() > new Date(this.today).getDate()))
                if (userLunch && userLunch.has_veggie != this.userVeggie) {
                  userLunch.has_veggie = this.userVeggie
                  await this.updateEvent(userLunch)
                }
              }
              this.$toast.success("Updated Status Successfully")
            }
          } catch (e) {
            let error = 'Updated Status Failed'
            if (e.response && e.response.data.error !== '') {
              error = e.response.data.error
            }
            this.$toast.error(error)
          }
        }
      )
    }

  }
}

</script>

<style lang="scss" scoped>
@import "./style.scss";
</style>
