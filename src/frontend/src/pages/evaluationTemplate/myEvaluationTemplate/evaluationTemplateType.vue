<template>
  <div>
    <restricted-view :scopes="['evaluation_template:create']">
      <template v-slot:default>
        <el-card style="width: 100%">
          <el-form>
            <el-row :gutter="16">
              <el-col :span="14">
                <el-form-item
                  label="New evaluation type"
                  class="mb-0"
                >
                  <el-input
                    required
                    id="type_name"
                    rows="2"
                    v-model="type_name"
                    class="input_data"
                  ></el-input>
                  <div class="error" v-if="!$v.type_name.required">
                    Field is required
                  </div>
                </el-form-item>
              </el-col>
              <div class="d-flex justify-content-end mt-5">
                <el-button type="danger" class="mr-2" @click="cancelDialog()">
                  Cancel
                </el-button>
                <div v-if="$v.type_name.$invalid">
                  <el-button
                    disabled
                    class="btn_submit"
                    @click="submit(type !== '' ? type : 0)"
                  >
                    {{ button_submit }}
                  </el-button>
                </div>
                <div v-else>
                  <el-button
                    class="btn_submit"
                    @click="submit(type !== '' ? type : 0)"
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
      :data="templateTypes"
      header-cell-class-name="bg-header-table"
      stripe
      border
      class="input_data"
    >
      <el-table-column type="index" sortable align="center" width="80">
      </el-table-column>
      <el-table-column
        prop="type_name"
        label="Type"
        align="center"
      ></el-table-column>
      <el-table-column label="Actions" width="180" align="center">
        <template slot-scope="scope">
          <restricted-view :scopes="['evaluation_template:edit']">
            <template v-slot:default>
              <img
                :src="require('@/static/images/IconEdit.svg')"
                @click="editTempleteType(scope.row)"
              />
              <img
                :src="require('@/static/images/IconDelete.svg')"
                @click="deleteTempleteType(scope.row)"
              />
            </template>
          </restricted-view>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>
<script>
import { mapActions, mapState } from "vuex";
import templateTypeServices from "@/services/probation/evaluation_template_type.services";
import { required } from "vuelidate/lib/validators";
import RestrictedView from "@/components/RestrictedView";
export default {
  name: "EvaluationTemplateFormType",
  components: {
    RestrictedView,
  },
  middleware: "authentication",
  async created() {
    await this.fetchTypes();
  },
  computed: {
    ...mapState("probation", ["templateTypes"]),
  },
  validations: {
    type_name: { required },
  },
  data() {
    return {
      BUTTON_SUBMIT: (title) => `${title}`,
      button_submit: "Add more",
      type_name: "",
      idTemplateType: "",
      type: 0,
    };
  },
  methods: {
    ...mapActions("probation", ["fetchTypes"]),
    editTempleteType(obj) {
      this.idTemplateType = obj.id;
      this.type_name = obj.type_name;
      this.type = 1; // return update status
      this.button_submit = this.BUTTON_SUBMIT("Save");
    },
    cancelDialog() {
      this.button_submit = this.BUTTON_SUBMIT("Add more");
      this.type_name = "";
    },
    async submit(type) {
      if (type === 0) {
        try {
          let res = await templateTypeServices.add({
            type_name: this.type_name,
          });
          if (res.status === 201) {
            this.$nextTick(() => {
              this.$toast.success(
                "Your evaluation template type was created successfully"
              );
            });
            this.fetchTypes();
          } else {
            let msg = "Your evaluation template type was created error";
            if (res.data.error[0]) {
              msg = res.data.error[0];
            }
            this.$toast.error(msg);
          }
        } catch {
          this.$toast.error("Your evaluation template type was created error");
        }
      } else {
        try {
          let res = await templateTypeServices.edit(this.idTemplateType, {
            type_name: this.type_name,
          });
          if (res.status === 200) {
            this.$nextTick(() => {
              this.$toast.success(
                "Your evaluation template type was updated successfully"
              );
            });
            this.fetchTypes();
          } else {
            let msg = "Your evaluation template type was updated error";
            if (res.data.error[0]) {
              msg = res.data.error[0];
            }
            this.$toast.error(msg);
          }
        } catch {
          this.$toast.error("Your evaluation template type was updated error");
        }
      }
      this.cancelDialog();
    },
    async deleteTempleteType(obj) {
      if (confirm("Are you sure you want to delete this item?")) {
        try {
          let res = await templateTypeServices.delete(obj.id);
          if (res.status === 204) {
            this.$nextTick(() => {
              this.$toast.success(
                "Your evaluation template type was deleted successfully"
              );
            });
            this.fetchTypes();
          } else {
            let msg = "Your evaluation template type was deleted error";
            if (res.data.error[0]) {
              msg = res.data.error[0];
            }
            this.$toast.error(msg);
          }
        } catch {
          this.$toast.error("Your evaluation template type was deleted error");
        }
      }
    },
  },
};
</script>

<style lang="scss" scoped></style>
