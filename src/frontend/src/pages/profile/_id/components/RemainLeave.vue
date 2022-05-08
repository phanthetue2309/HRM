<template>
  <div class="container-fluid">
    <div class="general-infor">
      <el-card class="box-card mb-4 card-detail">
        <div slot="header" class="clearfix">
          <span class="card-title">Remain Leave Information</span>
          <el-button class="edit-button mb-3" type="text" v-if="!isEditing && checkHasScope('remain_leave:edit')"
                     @click="isEditing = true">
            <img :src="require('@/static/images/IconCardEdit.svg')" class="edit-icon"/>
          </el-button>
          <el-button class="edit-button" type="text" v-if="isEditing && checkHasScope('remain_leave:edit')"
                     @click="isConfirming = true">
            <img :src="require('@/static/images/IconCardSave.svg')" class="edit-icon"/>
          </el-button>
        </div>
        <div v-if="isEditing && checkHasScope('remain_leave:edit')">
          <el-row :gutter="15" class="mb-2">
            <el-col :span="5">
              <el-input v-model="formData.year" type="number" :min="2000" :max="3000" placeholder="Year">
              </el-input>
              <div class="error" v-if="!$v.formData.year.required">
                Field is required
              </div>
            </el-col>
            <el-col :span="5">
              <el-input v-model="formData.annual_leave_last_year" type="number" :step="0.5" :min="0" :max="20"
                        placeholder="Remain Last Year"/>
              <div class="error" v-if="!$v.formData.annual_leave_last_year.required">
                Field is required
              </div>
            </el-col>
            <el-col :span="5">
              <el-input v-model="formData.annual_leave" type="number" :step="0.5" :min="0" :max="20"
                        placeholder="Total This Year"/>
              <div class="error" v-if="!$v.formData.annual_leave.required">
                Field is required
              </div>
            </el-col>
            <el-col :span="5">
              <el-input v-model="formData.current_days_off" type="number" :step="0.5" :min="0"
                        :max="formData.annual_leave" placeholder="Left"/>
              <div class="error" v-if="!$v.formData.current_days_off.required">
                Field is required
              </div>
            </el-col>
            <el-col :span="4">
              <div class="text-center">
                <el-button type="primary" @click="addRemainLeave">Add New</el-button>
              </div>
            </el-col>
          </el-row>
        </div>
        <el-table :data="remainLeaves" :cell-style="{ textAlign: 'center' }"
                  stripe header-cell-class-name="bg-header-table" border style="width: 100%">
          <el-table-column label="Year" prop="year">
            <template slot-scope="scope">
              <div
                v-if="isEditing && String(scope.row.year) !== String(yearNow) && String(scope.row.year) !== String(yearNow-1) ">
                <el-input v-model="scope.row.year" type="number" :min="2000" :max="3000"
                          :disabled="!scope.row.editMode"/>
              </div>
              <div v-else>
                {{ scope.row.year }}
              </div>
            </template>
          </el-table-column>
          <el-table-column label="Remain Last Year" prop="annual_leave_last_year">
            <template slot-scope="scope">
              <div v-if="isEditing">
                <el-input v-model="scope.row.annual_leave_last_year" type="number" :step="0.5" :min="0" :max="20"
                          :disabled="!scope.row.editMode"/>
              </div>
              <div v-else>
                {{ scope.row.annual_leave_last_year }}
              </div>
            </template>
          </el-table-column>
          <el-table-column label="Total This Year" prop="annual_leave">
            <template slot-scope="scope">
              <div v-if="isEditing">
                <el-input v-model="scope.row.annual_leave" type="number" :step="0.5" :min="0" :max="20"
                          :disabled="!scope.row.editMode"/>
              </div>
              <div v-else>
                {{ scope.row.annual_leave }}
              </div>
            </template>
          </el-table-column>
          <el-table-column label="Taken">
            <template slot-scope="scope">
              <div v-if="isEditing">
                <el-input :value="scope.row.annual_leave - scope.row.current_days_off" type="number" :step="0.5"
                          disabled/>
              </div>
              <div v-else>
                {{ scope.row.annual_leave - scope.row.current_days_off }}
              </div>
            </template>
          </el-table-column>
          <el-table-column label="Left" prop="current_days_off">
            <template slot-scope="scope">
              <div v-if="isEditing">

                <el-input v-model="scope.row.current_days_off" type="number" :step="0.5" :min="0"
                          :max="scope.row.annual_leave" :disabled="!scope.row.editMode"/>
              </div>
              <div v-else>
                {{ scope.row.current_days_off }}
              </div>
            </template>
          </el-table-column>
          <el-table-column label="Action">
            <template slot-scope="scope" v-if="isEditing">
              <div class="text-center"
                   v-if="!scope.row.editMode && checkHasScope('remain_leave:edit')">
                <img :src="require('@/static/images/IconEdit.svg')" @click="toggleEditing(scope.row)">
                <img :src="require('@/static/images/IconDelete.svg')" @click="toggleConfirmDelete(scope.row)">
              </div>
              <div class="text-center" v-else>
                <img :src="require('@/static/images/IconCheck.svg')" class="mr-3"
                     @click="updateRemainLeave(scope.row)">
                <img :src="require('@/static/images/IconCancel.svg')" class="ml-3"
                     @click="cancelUpdateRemainLeave(scope.row)">
              </div>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
      <el-dialog :visible.sync="dialogDelete" title="Confirm Delete">
        <slot>
          <h3 class="text-center">
            Do you want to remove?
          </h3>
          <div class="text-center">
            <el-button type="danger" class="mt-3" @click="removeRemainLeave">
              Delete
            </el-button>
          </div>
        </slot>
      </el-dialog>
      <el-dialog title="Confirm" :visible.sync="isConfirming" width="30%">
        <span>Do you want to save this change?</span>
        <span slot="footer" class="dialog-footer">
          <el-button @click="isConfirming = false">Cancel</el-button>
          <el-button type="primary" @click="saveConfirm">Save</el-button>
        </span>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import RemainLeaveService from "@/services/leave_management/remain_leave/remain_leave.services"
import {required} from "vuelidate/lib/validators";
import moment from 'moment'

const NO_DATA = "Empty";

export default {
  name: "RemainLeave",
  data() {
    return {
      isEditing: false,
      isConfirming: false,
      isCreating: false,
      dialogDelete: false,
      dataInfo: null,
      userId: Number,
      remainLeaves: [],
      remainLeaveToDelete: '',
      profileTemp: '',
      yearNow: moment().year(),
      NO_DATA,
      formData: {
        year: '',
        profile: '',
        annual_leave: '',
        annual_leave_last_year: '',
        current_days_off: '',
      },
    };
  },
  validations: {
    formData: {
      year: {
        required
      },
      annual_leave: {
        required
      },
      annual_leave_last_year: {
        required
      },
      current_days_off: {
        required
      },
    }
  },

  async created() {
    this.userId = this.$route.params.id;
    await this.fetchData()
  },
  methods: {
    checkHasScope(scope) {
      return this.$store.state.scope.tokenInfo.scope.indexOf(scope) !== -1
    },

    async fetchData() {
      const response = await RemainLeaveService.getRemainLeaveUser(this.userId);
      if (response && response.status === 200) {
        this.remainLeaves = response.data
        this.profileTemp = this.remainLeaves[0].profile
      }
    },

    showConfirmDialog() {
      this.isConfirming = true;
    },

    cancelConfirm() {
      this.isConfirming = false;
    },

    showEditForm() {
      this.isEditing = true;
    },

    saveForm() {
      this.isEditing = false;
      this.isConfirming = true;
    },

    saveConfirm() {
      this.isEditing = false;
      this.isConfirming = false;
    },

    toggleEditing(remainLeave) {
      this.$set(remainLeave, 'editMode', true)
      this.formData.year = remainLeave.year
      remainLeave.oldYear = remainLeave.year
      remainLeave.oldAnnualLeaveLastYear = remainLeave.annual_leave_last_year
      remainLeave.oldAnnualLeave = remainLeave.annual_leave
      remainLeave.oldCurrentDaysOff = remainLeave.current_days_off
    },

    toggleConfirmDelete(remainLeave) {
      this.remainLeaveToDelete = remainLeave
      this.dialogDelete = true
    },

    async updateRemainLeave(remainLeave) {
      await RemainLeaveService.update(remainLeave.id, remainLeave).then(res => {
        try {
          if (res && res.status === 200) {
            this.$set(remainLeave, 'editMode', false)
            this.$toast.success("Updated Successfully")
          } else {
            this.cancelUpdateRemainLeave(remainLeave)
            this.$toast.error("Updated Failed. Year update has been exist")
          }
        } catch (error) {
          if (error.response && error.response.data) {
            this.$emit('openSnack', error.response.data, 'error')
          }
        }
      })
    },

    cancelUpdateRemainLeave(remainLeave) {
      this.$set(remainLeave, 'editMode', false)
      remainLeave.year = remainLeave.oldYear
      remainLeave.annual_leave_last_year = remainLeave.oldAnnualLeaveLastYear
      remainLeave.annual_leave = remainLeave.oldAnnualLeave
      remainLeave.current_days_off = remainLeave.oldCurrentDaysOff
    },

    async addRemainLeave() {
      this.formData.profile = this.profileTemp
      await RemainLeaveService.create(this.formData).then(res => {
        try {
          if (res && res.status === 201) {
            this.$toast.success("Created Successfully")
            this.remainLeaves.push(res.data)
          } else {
            this.$toast.error("Created Failed. Year create has been exist")
          }
        } catch (error) {
          if (error.response && error.response.data) {
            this.$emit('openSnack', error.response.data, 'error')
          }
        }
      })
    },

    async removeRemainLeave() {
      if (this.remainLeaveToDelete.year <= moment().year() - 2 || this.remainLeaveToDelete.year > moment().year()) {
        await RemainLeaveService.destroy(this.remainLeaveToDelete.id).then(res => {
          try {
            if (res && res.status === 204) {
              this.remainLeaves.splice(this.remainLeaves.indexOf(this.remainLeaveToDelete), 1)
              this.$toast.success("Deleted Successfully")
            }
          } catch (error) {
            if (error.response && error.response.data) {
              this.$emit('openSnack', error.response.data, 'error')
            }
          }
        })
      } else {
        this.$toast.error("You can not delete data in this year.")
      }
      this.dialogDelete = false
    }

  }
}
</script>

<style scoped>
</style>
