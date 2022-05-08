<template>
  <div>
    <restricted-view :scopes="['type_pay:edit']">
      <template v-slot:default>
        <el-card style="width: 100%">
          <el-form>
            <el-row :gutter="20">
              <el-col :span="10">
                <el-form-item label="Name:">
                  <el-input v-model="titlePaymentType"></el-input>
                  <div class="error" v-if="!$v.titlePaymentType.required">
                    Field is required
                  </div>
                </el-form-item>
              </el-col>
              <el-col :span="10">
                <el-form-item label="Pay choices:">
                  <br />
                  <el-checkbox
                    v-model="isCompanyPay"
                    label="Company Pay"
                    border
                    size="big"
                  ></el-checkbox>
                  <el-checkbox
                    v-model="isInsurancePay"
                    label="Insurance Pay"
                    border
                    size="big"
                  ></el-checkbox>
                </el-form-item>
              </el-col>
            </el-row>
            <div class="d-flex justify-content-end">
              <el-button type="danger" @click="cancelPayment()">
                Cancel
              </el-button>
              <el-button
                class="btn_submit"
                :disabled="$v.titlePaymentType.$invalid"
                @click="submitPay(type !== '' ? type : 0)"
              >
                {{ button_submit }}
              </el-button>
            </div>
          </el-form>
        </el-card>
      </template>
    </restricted-view>
    <el-table
      highlight-current-row
      :data="listTypeOffGroup"
      stripe
      header-cell-class-name="bg-header-table"
      border
      style="width: 100%"
    >
      <el-table-column prop="name" label="Name"></el-table-column>
      <el-table-column label="Pay Choices" width="360">
        <template slot-scope="scope">
          <el-checkbox
            v-model="scope.row.is_company_pay"
            label="Company Pay"
            border
            size="big"
            @change="changeCheckboxCompany(scope.row)"
          ></el-checkbox>
          <el-checkbox
            v-model="scope.row.is_insurance_pay"
            label="Insurance Pay"
            border
            size="big"
            @change="changeCheckboxInsurance(scope.row)"
          ></el-checkbox>
        </template>
      </el-table-column>
      <el-table-column label="Actions" width="150" align="center">
        <template slot-scope="scope">
          <restricted-view :scopes="['type_pay:edit']">
            <template v-slot:default>
              <img
                :src="require('@/static/images/IconEdit.svg')"
                @click="editPaymentType(scope.row)"
              />
              <img
                :src="require('@/static/images/IconDelete.svg')"
                @click="deletePaymentType(scope.row)"
              />
            </template>
          </restricted-view>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import TypeOffGroupAdminServices from "@/services/leave_management/type_off/type_off_group.services";
import { required } from "vuelidate/lib/validators";
import RestrictedView from "@/components/RestrictedView";

export default {
  name: "LeaveTypeGroup",
  components: {
    RestrictedView,
  },
  created: function () {
    TypeOffGroupAdminServices.getTypeOffGroup().then((res) => {
      this.getListTypeOffGroup(res.data);
    });
  },
  computed: {
    ...mapGetters({
      showNotification: "showNotification",
      listTypeOffGroup: "offTypeGroup/listTypeOffGroup",
    }),
  },
  validations: {
    titlePaymentType: { required },
  },
  data() {
    return {
      BUTTON_SUBMIT: (title) => `${title}`,
      button_submit: "Add more",
      isCompanyPay: false,
      isInsurancePay: false,
      idPayEditDelete: "",
      idPayTemp: "",
      isCompanyPayTemp: false,
      isInsurancePayTemp: false,
      titlePaymentType: "",
      type: 0,
    };
  },
  methods: {
    ...mapActions({
      getListTypeOffGroup: "offTypeGroup/getListTypeOffGroup",
      addNewTypeOffGroup: "offTypeGroup/addNewTypeOffGroup",
      editListTypeOffGroup: "offTypeGroup/editListTypeOffGroup",
      deleteListTypeOffGroup: "offTypeGroup/deleteListTypeOffGroup",
    }),
    changeCheckboxCompany(typeOffGroup) {
      if (this.idPayTemp === "" || this.idPayTemp !== typeOffGroup.id) {
        this.idPayTemp = typeOffGroup.id;
        typeOffGroup.is_company_pay = !typeOffGroup.is_company_pay;
        this.isCompanyPayTemp = typeOffGroup.is_company_pay;
        this.isInsurancePayTemp = typeOffGroup.is_insurance_pay;
      } else {
        typeOffGroup.is_company_pay = this.isCompanyPayTemp;
        typeOffGroup.is_insurance_pay = this.isInsurancePayTemp;
      }
    },
    changeCheckboxInsurance(typeOffGroup) {
      if (this.idPayTemp === "" || this.idPayTemp !== typeOffGroup.id) {
        this.idPayTemp = typeOffGroup.id;
        typeOffGroup.is_insurance_pay = !typeOffGroup.is_insurance_pay;
        this.isCompanyPayTemp = typeOffGroup.is_company_pay;
        this.isInsurancePayTemp = typeOffGroup.is_insurance_pay;
      } else {
        typeOffGroup.is_company_pay = this.isCompanyPayTemp;
        typeOffGroup.is_insurance_pay = this.isInsurancePayTemp;
      }
    },

    editPaymentType(obj) {
      this.idPayEditDelete = obj.id;
      this.titlePaymentType = obj.name;
      this.isCompanyPay = obj.is_company_pay;
      this.isInsurancePay = obj.is_insurance_pay;
      this.type = 1; // return update status
      this.button_submit = this.BUTTON_SUBMIT("Save");
    },
    cancelPayment() {
      this.titlePaymentType = "";
      this.isCompanyPay = false;
      this.isInsurancePay = false;
      this.type = 0; // return add status
      this.button_submit = this.BUTTON_SUBMIT("Add more");
    },
    submitPay(pk) {
      let data = null;
      data = {
        name: this.titlePaymentType,
        is_company_pay: this.isCompanyPay,
        is_insurance_pay: this.isInsurancePay,
      };
      if (data) {
        if (pk === 0) {
          TypeOffGroupAdminServices.addTypeOffGroup(data)
            .then((res) => {
              if (res.status === 201) {
                this.addNewTypeOffGroup(res.data);
                this.$toast.success("Add new Group successfully");
              }
            })
            .catch(() => {
              this.$toast.error("An error occurred");
            });
        } else {
          let dataUpdate = {
            id: this.idPayEditDelete,
            data: data,
          };
          TypeOffGroupAdminServices.editTypeOffGroup(this.idPayEditDelete, data)
            .then((res) => {
              if (res.status === 200) {
                this.editListTypeOffGroup(dataUpdate);
                this.$toast.success("Edit successfully");
              }
            })
            .catch(() => {
              this.$toast.error("An error occurred");
            });
        }
        this.cancelPayment();
      }
    },
    deletePaymentType(obj) {
      if (confirm("Are you sure you want to delete this item?")) {
        TypeOffGroupAdminServices.deleteTypeOffGroup(obj.id)
          .then((res) => {
            if (res.status === 204) {
              this.deleteListTypeOffGroup(obj);
              this.$toast.success("Delete successfully");
            }
          })
          .catch(() => {
            this.$toast.error("An error occurred");
          });
      }
    },
  },
};
</script>

<style lang="scss" scoped>
@import "./style.scss";
</style>
