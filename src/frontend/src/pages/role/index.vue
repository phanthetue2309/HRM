<template>
  <restricted-view :scopes="['role:view']">
    <template v-slot:default>
      <div>
        <div class="">
          <div class="row my-2">
            <div class="col-10 col-md-4">
              <el-input
                  class="pt-0"
                  append-icon="mdi-magnify"
                  label="Search"
                  single-line
                  hide-details
                  v-model="roleName"
                  placeholder="Enter role"
                  @change="search(1)"
              >
              </el-input>

            </div>

            <restricted-view :scope="['role:edit']">
              <template v-slot:default>
                <div style="display:flex">
                  <el-button type="primary" size="small" style="height: 40px;" icon=el-icon-plus
                             @click="handelClickAdd"></el-button>
                </div>
              </template>
            </restricted-view>

          </div>
          <restricted-view :scope="['role:view']">
            <template v-slot:default>
              <el-table
                  :data="roleList.rows"
                  stripe
                  header-cell-class-name="bg-header-table"
                  style="width: 100%">
                <el-table-column
                    prop="name"
                    label="Roles"
                    width="180"
                    align="center">
                  <template v-slot:default="table">
            <span>{{
                table.row.name
              }}</span>
                  </template>
                </el-table-column>
                <el-table-column
                    prop="description"
                    align="center"
                    label="Descriptions">
                  <template v-slot:default="table">
                    <span style="word-break: break-word;">{{ table.row.description }}</span>
                  </template>
                </el-table-column>
                <el-table-column
                    prop="last_modified_by"
                    label="Last modified by"
                    align="center"
                    width="180"
                >
                  <template v-slot:default="table">
                    <span>{{ table.row.last_modified_by }}</span>
                  </template>
                </el-table-column>
                <restricted-view :scopes="['role:view']">
                  <el-table-column
                      fixed="right"
                      label="Operations"
                      align="center"
                      width="180">
                    <template v-slot:default="table">
                      <restricted-view :scopes="['role:view']">
                        <template v-slot:default>
                          <img :src="require('@/static/images/view.svg')"
                               @click="handleViewRole(table.row.id,table.row.description,table.row.name)"
                               style="cursor: pointer;width: 34px">
                        </template>
                      </restricted-view>
                      <restricted-view :scopes="['role:edit']">
                        <template v-slot:default>
                          <img :src="require('@/static/images/IconEdit.svg')"
                               @click="handleUpdateRole(table.row.id,table.row.description,table.row.name)"
                               style="cursor: pointer">
                        </template>
                      </restricted-view>
                      <restricted-view :scope="['role:edit']">
                        <template v-slot:default>
                          <img :src="require('@/static/images/IconDelete.svg')"
                               @click="handleClickDeleteRole(table.row.id)" style="cursor: pointer">
                        </template>
                      </restricted-view>

                    </template>
                  </el-table-column>
                </restricted-view>


              </el-table>
            </template>
          </restricted-view>

          <div class="d-flex justify-content-center mt-5">
            <el-pagination
                background
                layout="prev, pager, next"
                :page-size="roleList.page_size"
                :page-count="roleList.totalPage"
                :total="roleList.count"
                :current-page="roleList.currentPage"
                @current-change="setPage"
            >
            </el-pagination>
          </div>
          <div style="overflow: hidden">
            <el-dialog
                :visible.sync="dialogAdd"
                top='-5vh'
            >
              <Dialog ref="Dialog"></Dialog>
            </el-dialog>

          </div>

        </div>

      </div>
    </template>
  </restricted-view>

</template>

<script>

import 'vue2-datepicker/index.css'
import Dialog from './Dialog'
import {mapActions, mapGetters} from 'vuex'
import RoleService from "@/services/role/role_service";
import RestrictedView from "@/components/RestrictedView";

export default {
  components: {
    Dialog,
    RestrictedView
  },
  name: 'ManageRole',
  middleware: 'authentication',
  computed: {
    ...mapGetters({
      roleList: 'role/roleList',
    })
  },
  data() {
    return {
      roleName: '',
      dialogAdd: false,
      page_size: 8,
    }
  },

  async created() {
    await this.search(1)
  },

  methods: {
    ...mapActions({
      getRoleList: 'role/getRoleList',
    }),
    async setPage(page) {
      await this.search(page)
    },
    async search(page = 1) {
      await this.getRoleList({
        page_size: this.roleList.page_size,
        page: page,
        name: this.roleName,
      })

    },
    async handleViewRole(id, description, name) {

      this.dialogAdd = true
      await RoleService.getRole(id).then(res => {
        this.$nextTick(function () {
          this.$refs.Dialog.setChecked(res.data.scope.split(' '))
          this.$refs.Dialog.currentRole = {id, description, name}
          this.$refs.Dialog.mode = 'view'
          this.$refs.Dialog.validate = false
        })
      })

    },

    async handleUpdateRole(id, description, name) {

      this.dialogAdd = true
      await RoleService.getRole(id).then(res => {
        this.$nextTick(function () {
          this.$refs.Dialog.setChecked(res.data.scope.split(' '))
          this.$refs.Dialog.currentRole = {id, description, name}
          this.$refs.Dialog.mode = 'update'
          this.$refs.Dialog.validate = false
          this.$refs.Dialog.reset_all = false
          this.$refs.Dialog.select_all = false
        })
      })

    },

    handelClickAdd() {
      this.title = 'Create Role'
      this.dialogAdd = true
      this.$nextTick(function () {
        this.$refs.Dialog.setChecked()
        this.$refs.Dialog.mode = 'create'
        this.$refs.Dialog.validate = false
        this.$refs.Dialog.reset_all = false
        this.$refs.Dialog.select_all = false
      })
    },
    async handleClickDeleteRole(role_id) {
      await this.$confirm('This will permanently delete the role. Continue?', 'Warning', {
        confirmButtonText: 'OK',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }).then(() => {
        RoleService.deleteRole(role_id).then(
            res => {
              if (res.status === 204) {
                this.$toast.success('Success delete')
              }
            }
        ).then(() => this.getRoleList({page_size: this.page_size, page: 1, name: ""}))
      })
          .catch(res => {
            console.log(res)
            this.$toast.error('An error occurred')
          })

    },


  }
}
</script>
<style lang="scss" scoped>
@import "index";

.el-dialog__wrapper {
  overflow: hidden;
  margin-top: 10vh;
}

.modal-active {
  display: block;
}

.img-fluid {
  width: 60px;
}

</style>
