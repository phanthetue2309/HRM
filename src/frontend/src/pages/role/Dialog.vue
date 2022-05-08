<template>
  <div style="max-height: 86vh;overflow-y: auto ; overflow-x:hidden">
    <div class="pt-3 row">
      <div class="col-12 col-sm-5">
        <el-input
            v-model="currentRole.name"
            placeholder="Enter role name"
            outlined
            dense
            required
        ></el-input>
      </div>
      <div class="col-12 col-sm-5">
        <el-input
            v-model="currentRole.description"
            placeholder="Enter role description"
            outlined
            dense
            required
        ></el-input>

      </div>

    </div>
    <div style=" margin-top: 2%">
      <span style="color:red" v-show="validate">
            Please input valid field
    </span>
    </div>

    <div style="padding: 2%">
      <strong v-show="mode !== 'view'">Please choose permissions</strong>
      <strong v-show="mode === 'view'">All permissions</strong>
    </div>
    <el-input
        placeholder="Filter keyword"
        v-model="filterText">
    </el-input>
    <div class="d-flex justify-content-end">
      <el-checkbox style="margin-right: -1%;" v-model="selectAll" @change="checkAll" label="Option1" size="small"
                   border v-show="mode!=='view'">
        Select all
      </el-checkbox>
      <el-checkbox v-model="resetAll" @change="reset" label="Option1" size="small" border v-show="mode!=='view'">
        Reset
      </el-checkbox>
    </div>


    <div class="row">
      <div class="col-12 mt-3">
        <el-tree
            class="filter-tree"
            :data="scope_tree"
            :props="defaultProps"
            :show-checkbox="true"
            node-key="scope"
            :check-strictly="false"
            :highlight-current="true"
            :expand-on-click-node="false"
            ref="tree"
            :filter-node-method="filterNode"
            @check-change="handleCheckChange"
            @check="handleClick"
        >
        </el-tree>
      </div>
    </div>
    <div class="footer-dialog d-flex justify-content-end mt-2">
      <el-button type="primary" @click="handleClickCreateRole" style="margin-left: 2%;" v-show="mode==='create'">
        Create
      </el-button>
      <restricted-view :scope="['role:edit']">
        <template v-slot:default>
          <el-button type="primary" @click="handleClickUpdateRole" style="margin-left: 10%;" v-show="mode==='update'">
            Update
          </el-button>
        </template>
      </restricted-view>
    </div>
  </div>
</template>
<script>

import ScopeService from "@/services/role/scope_service";
import RoleService from "@/services/role/role_service";
import {mapActions} from "vuex";
import RestrictedView from "@/components/RestrictedView";


export default {
  name: 'Dialog',
  middleware: 'authentication',
  components: {RestrictedView},

  async created() {
    await this.getAddedData()
  },
  data() {
    return {
      filterText:"",
      validate: false,
      mode: '',
      defaultProps: {
        children: 'children',
        label: 'label'
      },
      currentRole: {
        id: '',
        name: '',
        description: '',
        scope: '',
      },
      errors: '',
      scope_tree: [],
      page_size: 8,
      full_scope: [],
      selectAll: false,
      resetAll: false,
    }
  },
  watch: {
      filterText(val) {
        this.$refs.tree.filter(val);
      }
    },
  methods: {
    ...mapActions({
      getRoleList: 'role/getRoleList'
    }),
    filterNode(value, data) {
      if (!value) return true;
      return data.label.toLowerCase().includes(value.toLowerCase()) ;
    },
    checkAll() {
      if (this.selectAll) {
        this.setChecked(this.full_scope)
        this.resetAll = false
      }
    },
    reset() {
      if (this.resetAll) {
        this.setChecked([])
        this.selectAll = false
      }
    },
    handleClick() {
      if (this.mode === 'view') this.$toast.error('You chose view,so you only view!!!')
    },
    setChecked(checkedList = []) {
      if (!checkedList.length) {
        this.currentRole.name = ''
        this.currentRole.description = ''
      }
      this.$refs.tree.setCheckedKeys(checkedList)
    },
    handleCheckChange() {
      this.currentRole.scope = this.$refs.tree.getCheckedKeys(true).join(" ")
    },

    async handleClickCreateRole() {
      if (!this.currentRole.name) {
        this.validate = true
        return
      }
      await RoleService.createRole(this.currentRole).then(
          res => {
            if (res.status === 201) {
              this.$toast.success('Success Created')
            }
          }
      )
          .catch(res => {
            console.log(res)
            this.$toast.error('An error occurred')
          })
      await this.getRoleList({page_size: this.page_size, page: 1, name: ""})
      this.mode = 'create'

    },
    async handleClickUpdateRole() {
      if (!this.currentRole.name) {
        this.validate = true
        return
      }
      await RoleService.updateRole(this.currentRole).then(
          res => {
            if (res.status === 200) {
              this.$toast.success('Success Updated')
            }
          }
      )
          .catch(res => {
            console.log(res)
            this.$toast.error('An error occurred')
          })
      await this.getRoleList({page_size: this.page_size, page: 1, name: ""})
    },
    async getAddedData() {
      let responseData = await ScopeService.getScopes()
      if (responseData && responseData.data) {
        this.scope_tree = responseData.data.scope
        this.full_scope = this.transformDicToArr(this.scope_tree)
      }
    },
    transformDicToArr(scopeTreeArray) {
      const result = []
      for (let node of scopeTreeArray) {
        for (let el of node.children) {
          result.push(el.scope)
        }
      }
      return result
    }
  },
}
</script>

<style scoped>

</style>
