<template>
  <div class="d-flex justify-content-center">
    <div class="table-responsive p-3 col-md-7">
      <div class="text-danger pb-2 pl-4 pt-2 text-center" v-show="error.length > 0">
        <span>{{ error }}</span>
      </div>
      <el-form label-width="120px">
        <el-form-item label="Team Name*">
          <div>
            <el-input v-model="formData.team_name" placeholder="Team Name" />
            <div class="error" v-if="!$v.formData.team_name.required">Field is required</div>
          </div>
        </el-form-item>
        <el-form-item label="Team Email*">
          <div>
            <el-input v-model="formData.team_email" placeholder="Email" />
            <div class="error" v-if="!$v.formData.team_email.email">Not a valid email</div>
          </div>
        </el-form-item>
        <el-form-item label="Team Leader*">
          <div>
            <el-select
              v-model="formData.team_leader"
              filterable
              :filter-method="searchLikeName"
              placeholder="Team Leader"
            >
              <el-option
                v-for="user in filteredUsers"
                :value="user.email"
                :key="user.id"
                :label="user.profile.name"
              >
                <span style="float: left">{{ user.profile.name }}</span>
                <span style="float: right; color: #8492a6; font-size: 13px">{{ user.email }}</span>
              </el-option>
            </el-select>
            <div class="error" v-if="!$v.formData.team_leader.required">Field is required</div>
          </div>
        </el-form-item>
        <el-form-item label="Office*">
          <div>
            <el-select v-model="formData.office" placeholder="Office">
              <el-option
                v-for="office in offices"
                :label="office.name"
                :value="office.id"
                :key="office.id"
              ></el-option>
            </el-select>
            <div class="error" v-if="!$v.formData.office.required">Field is required</div>
          </div>
        </el-form-item>
        <el-form-item label="Slack Channel">
          <el-input v-model="formData.slack_channel" placeholder="Team Slack Channel" />
        </el-form-item>
        <br />
        <el-form-item>
          <el-button type="primary" @click="submit()">Create</el-button>
          <router-link to="/teams" class="ml-3">
            <el-button type="danger">Cancel</el-button>
          </router-link>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>
<script>
import TeamService from "@/services/team/team.services";
import officeServices from "@/services/office/office.service";
import { required, email } from "vuelidate/lib/validators";
import { mapGetters } from "vuex";

export default {
  name: "CreateTeam",
  middleware: "authentication",
  data() {
    return {
      error: "",
      team_email: "",
      team_name: "",
      team_leaders: "",
      team_leader_email: "",
      formData: {
        team_name: "",
        team_email: "",
        team_leader: "",
        slack_channel: "",
        office: "",
      },
      offices: [],
      filteredUsers: [],
    };
  },
  validations: {
    formData: {
      team_name: {
        required,
      },
      team_email: {
        email,
      },
      team_leader: {
        required,
      },
      office: {
        required,
      },
    },
  },
  created() {
    this.getOffices();
    this.filteredUsers = this.allUsers;
  },
  computed: {
    ...mapGetters("user", ["allUsers"]),
  },
  methods: {
    searchLikeName(val) {
      if (val.trim() !== "") {
        this.filteredUsers = this.allUsers.filter((el) =>
          el.profile.name
            .toLowerCase()
            .trim()
            .includes(val.toLowerCase().trim())
        );
      } else {
        this.filteredUsers = this.allUsers;
      }
    },
    async submit() {
      return await TeamService.create(this.formData)
        .then((res) => {
          if (res.data) {
            this.$router.push("/teams");
            this.$toast.success("Add new team success");
          } else {
            this.$toast.error("Input is not valid");
          }
        })
        .catch(() => {
          this.$toast.error("Input is not valid");
        });
    },

    async getOffices() {
      const res = await officeServices.getOffices();
      this.offices = res.data.results;
    },
  },
};
</script>

<style lang="scss" scoped>
@import "./style.scss";
</style>
