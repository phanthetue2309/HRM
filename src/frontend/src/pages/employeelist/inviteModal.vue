<template>
  <div>
    <validation-observer
      ref="observer"
      align="center"
    >
      <div class="pt-3 row">
        <div class="col-12 col-sm-5">
          <validation-provider
            v-slot="{ errors }"
            name="Name"
            rules="required|max:50"
          >
            <el-input
              v-model="invite.name"
              :counter="50"
              :error-messages="errors"
              placeholder="Enter name"
              ref="nameA"
              outlined
              dense
              required
            ></el-input>
          </validation-provider>
        </div>
        <div class="col-12 col-sm-5">
          <validation-provider
            v-slot="{ errors }"
            name="Email"
            rules="required"
          >
            <el-input
              @keyup.enter="add"
              v-model="invite.email"
              :error-messages="errors"
              placeholder="E-mail"
              type="email"
              outlined
              dense
              required
            ></el-input>
          </validation-provider>
        </div>
        <div class="col-12 col-sm-2 d-flex justify-content-end align-items-center">
          <el-button type="primary" @click="add">Add</el-button>
        </div>
      </div>
      <div class="row">
        <div class="col-12 mt-3">
          <el-table
            :data="tableData"
            style="width: 100%"
            stripe
            header-cell-class-name="bg-header-table"
            :row-class-name="tableRowClassName"
          >
            <el-table-column prop="name" label="Name"></el-table-column>
            <el-table-column prop="email" label="Email"></el-table-column>
            <el-table-column prop="status" label="Status" v-if="showResult"></el-table-column>
            <el-table-column label="Action" v-if="!showResult">
              <el-button type="danger" @click="remove(item)">
                <font-awesome-icon
                  class="text-white fa-fw"
                  :icon="['fas', 'times']"
                />
              </el-button>
            </el-table-column>
          </el-table>
        </div>
      </div>
      <div>
        <div cols="12" sm="6">
          <div v-show="showResult" align="left" class="float-left">
            <div class="pt-2">
              <div class="text-success ml-3">
                Success: {{ validUser.length }}
              </div>
              <div class="text-danger ml-3" @click="sendList">
                Failure: {{ invalidUser.length }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </validation-observer>
    <div class="footer-dialog d-flex justify-content-end mt-2">
      <el-button type="info" @click="clearTable">Clear</el-button>
      <el-button type="primary" @click="sendList">Send invitations</el-button>
    </div>
  </div>
</template>
<script>
import InviteService from '@/services/employee/inviteModal.sercice'
import {required, email, max} from 'vee-validate/dist/rules'
import {extend, ValidationObserver, ValidationProvider, setInteractionMode} from 'vee-validate'
import messageResponse from '@/services/employee/responseMessage'
import env from '../../../env'

const STATUS_SUCCESS = 'Success';
const STATUS_EXISTED = 'Already existed'

setInteractionMode('eager')

extend('required', {
  ...required,
  message: messageResponse.REQUIRED,
})

extend('max', {
  ...max,
  message: messageResponse.MAX,
})

extend('email', {
  ...email,
  message: messageResponse.MESSAGE
})

export default {
  name: 'inviteModal',
  middleware: 'authentication',
  components: {
    ValidationProvider,
    ValidationObserver
  },
  data() {
    return {
      showResult: false,
      errors: '',
      listInvite: [],
      invalidUser: [],
      validUser: [],
      invite: {
        name: '',
        email: ''
      },
      defaultInvite: {
        name: '',
        email: ''
      },
      check: null,
      showbutton: true,
      character: '',
    }
  },
  methods: {
    async sendList() {
      if (!this.listInvite.length) {
        return
      }
      this.resetForm()
      let response = await InviteService.sendList(this.listInvite)
      if (response.status === 201 && response.data) {
        this.listInvite = []
        this.invalidUser = response.data.invalid_user
        this.validUser = response.data.valid_user
        if (this.invalidUser.length) {
          this.$toast.warning(`Failure: ${this.invalidUser.length}`)
        } else {
          this.$toast.success('Success')
        }
        this.showResult = true
      } else {
        this.$toast.error('Error')
      }
    },
    add() {
      if (this.invite.name && this.invite.email) {
        if (this.invite.email.indexOf('@') === -1) {
          this.invite.email += env.END_MAIL
        }
        this.listInvite.unshift(this.invite)
        this.resetForm()
        this.$refs.nameA.focus()
      }

    },
    tableRowClassName({row, rowIndex}) {
      if (row.status == STATUS_EXISTED) {
        return `text-danger ${rowIndex}`;
      } else if (row.status == STATUS_SUCCESS) {
        return `text-success ${rowIndex}`;
      }
      return '';
    },
    clearTable() {
      this.validUser = []
      this.listInvite = []
      this.invalidUser = []
      this.showResult = false
      this.resetForm()
    },
    resetForm() {
      this.invite = Object.assign({}, this.defaultInvite)
      this.$refs.observer.reset()
    },
    remove(item) {
      this.listInvite.splice(this.listInvite.indexOf(item), 1)
    }
  },
  computed: {
    noneData() {
      return !this.listInvite.length && !this.invalidUser.length && !this.validUser.length
    },
    tableData() {
      const listResult = []
      if (this.listInvite.length > 0) {
        return this.listInvite;
      } else {
        return listResult.concat(this.validUser, this.invalidUser)
      }
    }
  }
}
</script>
