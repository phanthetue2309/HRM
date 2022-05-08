<template>
  <div>
    <restricted-view :scopes="['type_off:edit']">
      <template v-slot:default>
        <el-card style="width: 100%">
          <el-form>
            <el-row :gutter="20">
              <el-col :span="8" class="mb-0">
                <el-form-item label="Name">
                  <el-input
                    required
                    v-model="titleOffTypes"
                    class="input_data"
                  />
                  <div class="error" v-if="!$v.titleOffTypes.required">
                    Field is required
                  </div>
                </el-form-item>
              </el-col>
              <el-col :span="6" class="mb-0">
                <el-form-item label="Group">
                  <el-select v-model="groupTypeOffChoose" class="input_data">
                    <el-option
                      v-for="typePay in listTypeOffGroup"
                      :label="typePay.name"
                      :value="typePay.id"
                      :key="typePay.id"
                    >
                    </el-option>
                  </el-select>
                  <div class="error" v-if="!$v.groupTypeOffChoose.required">
                    Field is required
                  </div>
                </el-form-item>
              </el-col>
              <el-col :span="4" class="mb-0 pr-0 p0">
                <el-form-item label="Limit leave days">
                  <el-input-number
                    class="input_data"
                    size="big"
                    v-model="totalDayLeaves"
                    :min="1"
                    :max="360"
                  ></el-input-number>
                </el-form-item>
              </el-col>
              <el-col :span="4" class="mb-0 ml-1">
                <el-form-item label="Is Count ?">
                  <br />
                  <el-checkbox v-model="isCount" border
                    >Count Day Leave</el-checkbox
                  >
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="18">
                <el-form-item label="Descriptions" class="mb-0">
                  <el-input
                    type="textarea"
                    id="descriptions"
                    rows="2"
                    v-model="descriptions"
                  ></el-input>
                  <div class="error" v-if="!$v.descriptions.required">
                    Field is required
                  </div>
                </el-form-item>
              </el-col>
              <div class="d-flex justify-content-end mt-5">
                <el-button type="danger" class="mr-2" @click="cancelLeave()">
                  Cancel
                </el-button>
                <div
                  v-if="
                    $v.groupTypeOffChoose.$invalid ||
                    $v.descriptions.$invalid ||
                    $v.titleOffTypes.$invalid
                  "
                >
                  <el-button
                    disabled
                    class="btn_submit"
                    @click="submitLeave(type !== '' ? type : 0)"
                  >
                    {{ button_submit }}
                  </el-button>
                </div>
                <div v-else>
                  <el-button
                    class="btn_submit"
                    @click="submitLeave(type !== '' ? type : 0)"
                  >
                    {{ button_submit }}
                  </el-button>
                </div>
              </div>
            </el-row>
          </el-form>
        </el-card>
      </template>
    </restricted-view>
    <el-table
      highlight-current-row
      :data="listTypeOff"
      :span-method="objectSpanMethod"
      stripe
      header-cell-class-name="bg-header-table"
      border
      class="input_data"
    >
      <el-table-column prop="name_type" label="Group" width="300">
        <template slot-scope="scope">
          <div v-if="scope.row.is_active === true">
            {{ scope.row.name_type }}
          </div>
          <div v-else>
            <s>{{ scope.row.name_type }}</s>
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="name" label="Name">
        <template slot-scope="scope">
          <div v-if="scope.row.is_active === true">
            {{ scope.row.name }}
          </div>
          <div v-else>
            <s>{{ scope.row.name }}</s>
          </div>
        </template>
      </el-table-column>
      <el-table-column
        prop="descriptions"
        label="Description"
      ></el-table-column>
      <el-table-column
        prop="is_count"
        label="Counted"
        width="80"
        align="center"
      >
        <template slot-scope="scope">
          {{ scope.row.is_count === true ? "Yes" : "No" }}
        </template>
      </el-table-column>
      <el-table-column
        prop="days"
        label="Limit Days"
        width="100"
        align="center"
      ></el-table-column>
      <el-table-column
        prop="is_active"
        label="Active"
        width="65"
        align="center"
      >
        <template slot-scope="scope">
          <el-switch
            active-color="#25c9d0"
            inactive-color="#ff4949"
            v-model="scope.row.is_active"
            @change="switchActive(scope.row)"
          >
          </el-switch>
        </template>
      </el-table-column>
      <el-table-column label="Actions" width="150" align="center">
        <template slot-scope="scope">
          <restricted-view :scopes="['type_off:edit']">
            <template v-slot:default>
              <img
                :src="require('@/static/images/IconEdit.svg')"
                @click="editLeaveType(scope.row)"
              />
              <img
                :src="require('@/static/images/IconDelete.svg')"
                @click="deleteOffType(scope.row)"
              />
            </template>
          </restricted-view>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import TypeOffAdminServices from "@/services/leave_management/type_off/type_off_admin.services";
import TypeOffGroupAdminServices from "@/services/leave_management/type_off/type_off_group.services";
import { required } from "vuelidate/lib/validators";
import RestrictedView from "@/components/RestrictedView";

export default {
  name: "LeaveType",
  components: {
    RestrictedView,
  },
  middleware: "authentication",
  created: async function () {
    await TypeOffAdminServices.getTypeOff().then((res) => {
      this.getListTypeOff(res.data);
    });
    await TypeOffGroupAdminServices.getTypeOffGroup().then((res) => {
      this.getListTypeOffGroup(res.data);
    });
    this.groupTable();
  },
  computed: {
    ...mapGetters({
      listTypeOff: "offType/listTypeOff",
      listTypeOffGroup: "offTypeGroup/listTypeOffGroup",
      showNotification: "showNotification",
    }),
  },
  validations: {
    titleOffTypes: { required },
    descriptions: { required },
    groupTypeOffChoose: { required },
  },
  data() {
    return {
      BUTTON_SUBMIT: (title) => `${title}`,
      button_submit: "Add more",
      descriptions: "",
      isCount: false,
      idOffEditDelete: "",
      titleOffTypes: "",
      groupTypeOffChoose: "",
      type: 0,
      totalDayLeaves: 1,
      tempTitle: "",
      id_array: [],
      id_pos: 0,
      row: "",
      column: "",
    };
  },
  methods: {
    ...mapActions({
      getListTypeOffGroup: "offTypeGroup/getListTypeOffGroup",
      getListTypeOff: "offType/getListTypeOff",
      addNewTypeOff: "offType/addNewTypeOff",
      editListTypeOff: "offType/editListTypeOff",
      deleteListTypeOff: "offType/deleteListTypeOff",
    }),
    editLeaveType(obj) {
      this.idOffEditDelete = obj.id;
      this.titleOffTypes = obj.name;
      const index = this.listTypeOffGroup.indexOf(
        this.listTypeOffGroup.find((item) => item.id === obj.leave_type_group)
      );
      this.groupTypeOffChoose = this.listTypeOffGroup[index].id;
      this.isCount = obj.is_count;
      this.totalDayLeaves = obj.days;
      this.descriptions = obj.descriptions;
      this.type = 1; // return update status
      this.button_submit = this.BUTTON_SUBMIT("Save");
    },
    cancelLeave() {
      this.titleOffTypes = "";
      this.isCount = false;
      this.groupTypeOffChoose = "";
      this.type = 0; // return add status
      this.button_submit = this.BUTTON_SUBMIT("Add more");
      this.descriptions = "";
      this.totalDayLeaves = 1;
    },
    submitLeave(pk) {
      let data = null;
      data = {
        name: this.titleOffTypes,
        leave_type_group: this.groupTypeOffChoose,
        days: this.totalDayLeaves,
        is_count: this.isCount,
        descriptions: this.descriptions,
      };
      if (data) {
        if (pk === 0) {
          TypeOffAdminServices.addTypeOff(data)
            .then((res) => {
              if (res.status === 201) {
                this.addNewTypeOff(res.data);
                this.groupTable();
                this.$toast.success("Add new Leave Type successfully");
              }
            })
            .catch(() => {
              this.$toast.error("An error occurred");
            });
        } else {
          let dataUpdate = {
            id: this.idOffEditDelete,
            data: data,
          };
          TypeOffAdminServices.editTypeOff(this.idOffEditDelete, data)
            .then((res) => {
              if (res.status === 200) {
                this.editListTypeOff(dataUpdate);
                this.groupTable();
                this.$toast.success("Edit Leave Type successfully");
              }
            })
            .catch(() => {
              this.$toast.error("An error occurred");
            });
        }
        this.cancelLeave();
      }
    },
    switchActive(obj) {
      TypeOffAdminServices.handleActiveTypeOff(obj.id).then((res) => {
        if (res.status === 200) {
          this.$toast.success(
            `${res.data.is_active ? "Active" : "Hidden"} successfully`
          );
        } else {
          this.$toast.error("An error occurred");
        }
      });
    },
    deleteOffType(obj) {
      if (confirm("Are you sure you want to delete this item?")) {
        TypeOffAdminServices.deleteTypeOff(obj.id)
          .then((res) => {
            if (res.status === 204) {
              this.deleteListTypeOff(obj);
              this.$toast.success("Delete Leave Type successfully");
            }
          })
          .catch(() => {
            this.$toast.error("An error occurred");
          });
      }
    },
    groupTable() {
      this.id_array = [];
      this.id_pos = 0;
      for (let i = 0; i < this.listTypeOff.length; i++) {
        if (i == 0) {
          this.id_array.push(1);
          this.id_pos = 0;
        } else {
          if (
            this.listTypeOff[i].name_type === this.listTypeOff[i - 1].name_type
          ) {
            this.id_array[this.id_pos] += 1;
            this.id_array.push(0);
          } else {
            this.id_array.push(1);
            this.id_pos = i;
          }
        }
      }
    },
    objectSpanMethod({ row, column, rowIndex, columnIndex }) {
      this.row = row;
      this.column = column;
      if (columnIndex === 0) {
        const _row = this.id_array[rowIndex];
        const _col = _row > 0 ? 1 : 0;
        return {
          rowspan: _row,
          colspan: _col,
        };
      }
    },
  },
};
</script>

<style lang="scss" scoped>
@import "./style.scss";
</style>
