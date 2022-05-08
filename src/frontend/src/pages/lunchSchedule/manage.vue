<template>
  <div>
    <div>
      <div class="d-flex bd-highlight">
        <div class="mr-auto p-2 bd-highlight">
          <el-date-picker placeholder="Search by date" v-model="search" value-format="yyyy-MM-dd">
          </el-date-picker>
        </div>
        <restricted-view :scopes="['lunches:edit']">
          <template v-slot:default>
            <div class="p-2 bd-highlight">
              <el-button icon="el-icon-circle-plus-outline" type="primary" @click="addNewItem">
                Add
              </el-button>
            </div>
          </template>
        </restricted-view>
      </div>
      <el-table highlight-current-row
                :data="desserts.filter(data => !search || data.date.toLowerCase().includes(search.toLowerCase()))"
                header-cell-class-name="bg-header-table" border>
        <el-table-column label="Date" width="250" align="center">
          <template slot-scope="scope">
            <div v-if="scope.row.editMode">
              <el-date-picker :picker-options="{firstDayOfWeek: 1}" value-format="yyyy-MM-dd" class="data-input"
                              v-model="scope.row.date" type="date" placeholder="Pick a date*">
              </el-date-picker>
            </div>
            <div v-else>
              {{ scope.row.date }}
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="name_provider" label="Provider" align="center">
          <template slot-scope="scope">
            <div v-if="scope.row.editMode">
              <el-select v-model="scope.row.provider" placeholder="Provider*" class="data-input">
                <el-option v-for="provider in providers" :label="provider.name" :value="provider.id" :key="provider.id">
                </el-option>
              </el-select>
            </div>
            <div v-else>
              {{ scope.row.name_provider }}
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="note" label="Note">
          <template slot-scope="scope">
            <div v-if="scope.row.editMode">
              <el-input type="textarea" class="dont-break-out" v-model="scope.row.note" :rows="10"
                        :placeholder="scope.row.note === '' ? 'Note*' : scope.row.note">
              </el-input>
            </div>
            <div v-else class="dont-break-out">
              {{ scope.row.note }}
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="has_veggie" label="Veggie" width="100">
          <template slot-scope="scope">
            <el-checkbox v-model="scope.row.has_veggie" :disabled="!scope.row.editMode">Veggie</el-checkbox>
          </template>
        </el-table-column>
        <el-table-column label="Action" width="150" align="center">
          <template slot-scope="scope">
            <restricted-view :scopes="['lunches:edit']">
              <template v-slot:default>
                <div v-if="scope.row.editMode">
                  <img :src="require('@/static/images/IconCheck.svg')" class="ml-3"
                       @click="saveEdit(scope.row,scope.$index )">
                  <img :src="require('@/static/images/IconCancel.svg')" class="ml-4"
                       @click="cancelEdit(scope.$index)">
                </div>
                <div v-else>
                  <img :src="require('@/static/images/IconEdit.svg')" @click="editItem(scope.row)">
                  <img :src="require('@/static/images/IconDelete.svg')" @click="deleteItem(scope.row)">
                </div>
              </template>
            </restricted-view>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div class="text-center pt-2">
      <el-pagination :current-page.sync="page"
                     :page-size="itemsPerPage"
                     @current-change="changePages">
      </el-pagination>
    </div>
  </div>
</template>

<script>
import LunchScheduleService from '@/services/lunch_management/lunch_schedule'
import ProviderService from '@/services/lunch_management/provider'
import RestrictedView from "@/components/RestrictedView";

export default {
  middleware: 'authentication',
  components: {
    RestrictedView
  },
  data: () => ({
    page: 1,
    itemsPerPage: 12,
    desserts: [],
    editedIndex: -1,
    createdItem: {
      provider: '',
      note: '',
      date: '',
      has_veggie: false,
    },
    tempItem: {
      provider: '',
      note: '',
      date: '',
      has_veggie: false,
    },
    editedItem: {
      provider: '',
      note: '',
      date: '',
      has_veggie: false,
    },
    providers: [],
    isAdding: false,
    search: '',
  }),

  created() {
    this.getLunches()
    this.getProviders()
  },

  methods: {
    async getLunches() {
      this.desserts = await LunchScheduleService.get(this.page, this.itemsPerPage)
    },

    async getProviders() {
      const listProviders = await ProviderService.get()
      this.providers = listProviders.data ? listProviders.data : []
    },

    editItem(item) {
      this.$set(item, 'editMode', true)
      this.editedIndex = this.desserts.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.tempItem = Object.assign({}, item)
    },

    async deleteItem(item) {
      if (confirm('Are you sure you want to delete this item?') && this.desserts.splice(this.desserts.indexOf(item), 1)
        && await LunchScheduleService.delete(item.id)) {
        this.$toast.success('Deleted Successfully')
      } else {
        this.$toast.error('Deleted Failed')
      }
    },

    addNewItem() {
      this.desserts.unshift(this.createdItem)
      this.$set(this.createdItem, 'editMode', true)
      this.isAdding = true
    },

    async createNewItem(item) {
      try {
        const res = await LunchScheduleService.create(item)
        this.desserts.splice(0, 1)
        this.desserts.unshift(res.data)
        this.$toast.success('Created Successfully!')
      } catch (e) {
        console.log(e)
        this.$toast.error('Created Failed')
      }
      this.createdItem = {}
      this.isAdding = false
      this.$set(this.createdItem, 'editMode', false)
    },

    cancelCreate() {
      this.createdItem = {}
      this.$set(this.createdItem, 'editMode', false)
      this.desserts.splice(0, 1)
      this.isAdding = false
    },

    async changePages() {
      await this.getLunches(this.page, this.itemsPerPage)
    },

    async saveEdit(item, index) {
      if (!item.date || !item.provider || !item.note) {
        if (!this.isAdding) this.cancelEdit(index)
        this.$toast.error("Missing Data")
        return
      }
      if (this.isAdding) {
        await this.createNewItem(item)
        return
      }
      this.editedItem = Object.assign({}, item)
      Object.assign(this.desserts[this.editedIndex], this.editedItem)
      const data = {
        date: this.editedItem.date,
        note: this.editedItem.note,
        has_veggie: this.editedItem.has_veggie,
        provider: this.editedItem.provider
      }
      const lunch = await LunchScheduleService.update({
        id: this.editedItem.id,
        data
      })
      if (lunch && lunch.data.msg) {
        const content = lunch.data.msg
        this.$toast.error(content)
      }
      if (lunch && lunch.data.note) {
        this.$toast.success('Updated Successfully!')
      }
      this.$set(item, 'editMode', false)
    },

    cancelEdit(index) {
      if (this.isAdding) {
        this.cancelCreate()
        return
      }
      this.$set(this.tempItem, 'editMode', false)
      this.$set(this.desserts, index, this.tempItem)
    }

  }
}

</script>

<style lang="scss" scoped>
@import "./style.scss";
</style>
