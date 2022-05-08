<template>
  <div data-app class="m-4">
    <div class="text-danger">{{ errors }}</div>
    <div>
      <div class="row d-flex" v-if="show">
        <restricted-view :scopes="['team:edit_all_team']">
          <template v-slot:default>
            <el-col :span="2">
              <img
                :src="require('@/static/images/IconEdit.svg')"
                @click="showEdit()"
              />
            </el-col>
          </template>
        </restricted-view>
        <div v-if="teamLeader === user_id">
          <el-col :span="2">
            <img
              :src="require('@/static/images/IconEdit.svg')"
              @click="showEdit()"
            />
          </el-col>
        </div>
        <el-col :span="16">
          <h2 :style="color">{{ teamName }}</h2>
          <h4 :style="colorEmail">Email : {{ updateData.teamEmail }}</h4>
          <h4 :style="colorEmail">Group : {{ updateData.teamGroup }}</h4>
          <h4 :style="colorEmail">Office : {{ updateData.teamOffice }}</h4>
          <h4 :style="colorEmail">
            Department : {{ updateData.teamDepartment }}
          </h4>
          <h4 :style="colorEmail">
            Slack Channel : {{ updateData.teamSlack }}
          </h4>

          <h4 :style="colorEmail">
            Team Leader : {{ updateData.nameTeamLeader }}
          </h4>
        </el-col>

        <template v-if="team.team_leader === user_id">
          <el-col :span="6">
            <div class="ml-auto">
              <router-link
                :to="'/addMember/' + team.id"
                style="color: #ffffff; text-decoration: none"
              >
                <el-button type="primary">
                  <font-awesome-icon :icon="['fas', 'user-plus']" />Add Member
                </el-button>
              </router-link>
            </div>
          </el-col>
        </template>
        <restricted-view v-else :scopes="['team:edit_all_team']">
          <template>
            <el-col :span="6">
              <div class="ml-auto">
                <router-link
                  :to="'/addMember/' + team.id"
                  style="color: #ffffff; text-decoration: none"
                >
                  <el-button type="primary">
                    <font-awesome-icon :icon="['fas', 'user-plus']" />Add Member
                  </el-button>
                </router-link>
              </div>
            </el-col>
          </template>
        </restricted-view>
      </div>
      <div v-else>
        <el-col :span="8">
          <el-form label-width="120px">
            <el-form-item label="Team Name">
              <el-input :style="[borderRadius]" v-model="teamNameUpdate" />
            </el-form-item>
            <el-form-item label="Team Email">
              <el-input :style="[borderRadius]" v-model="teamEmailUpdate" />
            </el-form-item>
            <el-form-item label="Slack Channel">
              <el-input :style="[borderRadius]" v-model="teamSlackUpdate" />
            </el-form-item>
            <el-form-item label="Leader">
              <el-select
                filterable
                :filter-method="searchLikeName"
                :style="[borderRadius]"
                v-model="teamLeaderUpdate"
              >
                <el-option
                  v-for="user in filteredUsers"
                  :label="user.profile.name"
                  :value="user.id"
                  :key="user.id"
                ></el-option>
              </el-select>
            </el-form-item>
            <el-row>
              <div class="org-question-title">
                Which organization manage your team?
              </div>
            </el-row>
            <el-form-item label="Group">
              <el-select :style="[borderRadius]" v-model="teamGroupUpdate">
                <el-option
                  v-for="group in groups"
                  :label="group.name"
                  :value="group.name"
                  :key="group.id"
                ></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="Office">
              <el-select :style="[borderRadius]" v-model="teamOfficeUpdate">
                <el-option
                  v-for="office in offices"
                  :label="office.name"
                  :value="office.name"
                  :key="office.id"
                ></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="Department">
              <el-select :style="[borderRadius]" v-model="teamDepartmentUpdate">
                <el-option
                  v-for="department in departments"
                  :label="department.name"
                  :value="department.name"
                  :key="department.id"
                ></el-option>
              </el-select>
            </el-form-item>
            <el-form-item>
              <div class="align-self-center">
                <el-button
                  size="medium"
                  type="primary"
                  round
                  @click="updateTeam()"
                  >Update</el-button
                >
                <el-button size="medium" type="danger" round @click="cancel()"
                  >Cancel</el-button
                >
              </div>
            </el-form-item>
          </el-form>
        </el-col>
      </div>
    </div>
    <div
      class="text-center col-sm-12"
      v-show="teamLeader === 'No leader' && rows.length !== 0"
    >
      <label class="col-sm-12 col-form-label alert alert-danger"
        >This team has no leader</label
      >
    </div>
    <div class="table-responsive mt-3">
      <el-table
        highlight-current-row
        :data="members"
        header-cell-class-name="bg-header-table"
        border
      >
        <el-table-column sortable label="Member Name">
          <template prop="name" slot-scope="scope">
            <router-link
              :to="'/profile/' + scope.row.user"
              title="Click to go to Profile page"
            >
              <strong class="text-dark">{{ scope.row.name }}</strong>
            </router-link>
          </template>
        </el-table-column>
        <el-table-column prop="email" sortable label="Member Email">
          <template slot-scope="scope">
            <el-link
              :href="'mailto:' + scope.row.email"
              title="Click to send mail"
              >{{ scope.row.email }}</el-link
            >
          </template>
        </el-table-column>
        <el-table-column prop="phone" label="Phone"></el-table-column>
        <el-table-column label="Action" width="180">
          <template
            v-if="hasScope('team:edit_all_team') || teamLeader === user_id"
            slot-scope="scope"
          >
            <div class="text-center">
              <el-button
                size="mini"
                plain
                type="primary"
                class="btn m-1 btn-sm"
                @click="showMoveTeamModal(scope.row)"
                v-show="scope.row.title !== 'Leader'"
                title="Click to move this member to another team"
              >
                <font-awesome-icon
                  class="fa-fw text-info"
                  :icon="['fas', 'exchange-alt']"
                />
              </el-button>
              <el-button
                size="mini"
                plain
                type="primary"
                class="btn m-1 btn-sm"
                @click="showModal(scope.row)"
                v-show="scope.row.title !== 'Leader'"
                title="Click to remove this member"
              >
                <font-awesome-icon
                  class="fa-fw text-danger"
                  :icon="['fas', 'user-times']"
                />
              </el-button>
            </div>
            <div v-if="scope.row.title === 'Leader'">
              <div class="text-center">Team Leader</div>
            </div>
          </template>

          <!-- <restricted-view slot-scope="scope" :scopes="['team:edit_all_team']">

          </restricted-view>
          <template v-if="teamLeader === user_id" slot-scope="scope">
            <div class="text-center">
              <el-button
                size="mini"
                plain
                type="primary"
                class="btn m-1 btn-sm"
                @click="showMoveTeamModal(scope.row)"
                v-show="scope.row.title !== 'Leader'"
                title="Click to move this member to another team"
              >
                <font-awesome-icon
                  class="fa-fw text-info"
                  :icon="['fas', 'exchange-alt']"
                />
              </el-button>
              <el-button
                size="mini"
                plain
                type="primary"
                class="btn m-1 btn-sm"
                @click="showModal(scope.row)"
                v-show="scope.row.title !== 'Leader'"
                title="Click to remove this member"
              >
                <font-awesome-icon
                  class="fa-fw text-danger"
                  :icon="['fas', 'user-times']"
                />
              </el-button>
            </div>

            <div v-if="scope.row.title === 'Leader'">
              <div class="text-center">Team Leader</div>
            </div>
          </template> -->
        </el-table-column>
      </el-table>
    </div>
    <div class="text-center col-sm-12" v-show="members.length === 0">
      <label class="col-sm-12 col-form-label alert alert-danger"
        >This team has no member</label
      >
    </div>
    <div class="text-center">
      <el-dialog :visible.sync="dialog" width="500" title="Team Management">
        <el-container class="fixed-top">
          <el-card class="mx-auto" max-width="500">
            <div slot="header" style="color: #25c9d0">
              <h3>Removing member</h3>
            </div>
            <div class="d-block text-center mb-4">
              Do you want to remove
              <p class="text-danger d-inline">{{ currentUser.name }}</p>
              from team?
            </div>
            <el-button type="danger" @click="closeDialog()">Cancel</el-button>
            <el-button type="primary" @click="del()">Confirm</el-button>
          </el-card>
        </el-container>
      </el-dialog>
    </div>
    <div class="text-center">
      <el-dialog :visible.sync="dialogMove" width="500" title="Team Management">
        <el-container class="fixed-top">
          <el-card class="mx-auto" max-width="500">
            <div slot="header" style="color: #25c9d0">
              <h3>Moving member</h3>
            </div>
            <div class="col-sm-12 ml-2">
              <div class="text-center m-2">Please choose new team:</div>
              <el-select v-model="newTeam" type="text" class="mb-2 mt-2">
                <el-option
                  v-for="team in newTeams"
                  :key="team.id"
                  :label="team.team_name"
                  placeholder="Teams"
                  :value="team.id"
                ></el-option>
              </el-select>
            </div>
            <el-button type="danger" @click="closeDialogMove()"
              >Cancel</el-button
            >
            <el-button type="primary" @click="move()">Confirm</el-button>
          </el-card>
        </el-container>
      </el-dialog>
    </div>
    <div class="text-center">
      <el-dialog :visible.sync="dialogLead" width="500" title="Team Management">
        <el-container class="fixed-top">
          <el-card class="mx-auto" max-width="500">
            <div slot="header" style="color: #25c9d0">
              <h3>Set Leader</h3>
            </div>
            <div class="d-block text-center mb-4">
              Do you want to set
              <p class="text-danger d-inline">{{ currentUser.name }}</p>
              as leader?
            </div>
            <el-button type="danger" @click="hideModalLead()">Cancel</el-button>
            <el-button type="primary" @click="lead()">Confirm</el-button>
          </el-card>
        </el-container>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import TeamService from "@/services/team/team.services.js";
import GetUserService from "@/services/user/getUser.js";
import officeServices from "@/services/office/office.service";
import departmentServices from "@/services/office/department.service";
import groupServices from "@/services/office/group.service";
import RestrictedView from "@/components/RestrictedView";
import { mapGetters } from "vuex";

export default {
  name: "id_team_table",
  middleware: "authentication",
  components: {
    RestrictedView,
  },
  data() {
    return {
      employeesData: [],
      dialog: false,
      dialogLead: false,
      dialogMove: false,
      show: true,
      memberEmail: "",
      memberRows: [],
      teamId: "",
      rows: [],
      offices: [],
      departments: [],
      groups: [],
      teamName: "",
      teamNameUpdate: "",
      teamEmail: "",
      teamEmailUpdate: "",
      teamGroup: "",
      teamGroupUpdate: "",
      teamOffice: "",
      teamOfficeUpdate: "",
      teamDepartment: "",
      teamDepartmentUpdate: "",
      teamSlack: "",
      teamSlackUpdate: "",
      nameTeamLeader: "",
      teamLeader: "",
      teamLeaderUpdate: "",
      currentUser: "",
      admin: localStorage.getItem("is_admin"),
      user_id: localStorage.getItem("user_id"),
      borderRadius: {
        borderradius: "1.25rem",
        textAlign: "center",
        width: "100%",
      },
      color: {
        color: "#25c9d0",
        fontSize: "40px",
      },
      colorEmail: {
        color: "#25c9d0",
        fontSize: "16px",
      },
      text: {
        fontSize: "20px",
      },
      errors: "",
      newTeams: [],
      newTeam: "",

      //my code
      team: {},
      members: [],
      pms: [],
      currentPM: {},
      filteredUsers: [],
      showButton: true,
    };
  },

  computed: {
    updateData() {
      return {
        teamName: this.teamName,
        teamEmail: this.teamEmail,
        teamSlack: this.teamSlack,
        teamOffice: this.teamOffice,
        teamGroup: this.teamGroup,
        teamDepartment: this.teamDepartment,
        nameTeamLeader: this.nameTeamLeader,
      };
    },
    ...mapGetters({
      allUsers: "user/allUsers",
      tokenInfo: "scope/tokenInfo",
    }),
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
    async getData() {
      this.teamId = this.$route.params.id;
      this.team = (await TeamService.get(`${this.teamId}`)).data;
      this.members = this.team.employee_list;
      this.teamName = this.team.team_name;
      this.teamEmail = this.team.team_email;
      this.teamGroup = this.team.group_name;
      this.teamOffice = this.team.office_name;
      this.teamDepartment = this.team.department_name;
      this.teamSlack = this.team.slack_channel;
      this.teamLeader = this.team.team_leader;
      this.nameTeamLeader = this.team.leader_name;
    },

    updateTeam: async function () {
      if (
        this.teamNameUpdate.length !== 0 ||
        this.teamEmailUpdate.length !== 0 ||
        this.teamSlackUpdate.length !== 0 ||
        this.teamOfficeUpdate !== "" ||
        this.teamGroupUpdate !== "" ||
        this.teamDepartmentUpdate !== "" ||
        this.teamLeaderUpdate !== ""
      ) {
        const office = this.offices.find(
          (office) => office.name === this.teamOfficeUpdate
        );
        const group = this.groups.find(
          (group) => group.name === this.teamGroupUpdate
        );
        const department = this.departments.find(
          (department) => department.name === this.teamDepartmentUpdate
        );
        const data = {
          team_name: this.teamNameUpdate,
          team_email: this.teamEmailUpdate,
          slack_channel: this.teamSlackUpdate,
          office: office === undefined ? null : office.id,
          group: group === undefined ? null : group.id,
          department: department === undefined ? null : department.id,
          team_leader: this.teamLeaderUpdate,
          current_leader: this.teamLeader,
        };

        try {
          await TeamService.update(this.teamId, data);
          this.teamName = this.teamNameUpdate;
          this.teamEmail = this.teamEmailUpdate;
          this.teamOffice = this.teamOfficeUpdate;
          this.teamGroup = this.teamGroupUpdate;
          this.teamDepartment = this.teamDepartmentUpdate;
          this.teamSlack = this.teamSlackUpdate;
          this.teamLeader = this.teamLeaderUpdate;
          this.nameTeamLeader = this.allUsers.find(
            (user) => user.id === this.teamLeader
          ).profile.name;
          this.$toast.success("Update Team Success");
          if (this.teamLeader !== this.user_id) {
            this.showButton = false;
          }
        } catch (e) {
          this.$toast.error("Update Team Failed");
        }
      } else {
        this.teamNameUpdate = this.teamName;
        this.teamEmailUpdate = this.teamEmail;
        this.teamOfficeUpdate = this.teamOffice;
        this.teamGroupUpdate = this.teamGroup;
        this.teamDepartmentUpdate = this.teamDepartment;
        this.teamSlackUpdate = this.teamSlack;
        this.teamLeaderUpdate = this.teamLeader;
        this.errors = "Missing Data";
      }
      this.cancel();
    },
    showEdit: function () {
      this.teamNameUpdate = this.teamName;
      this.teamEmailUpdate = this.teamEmail;
      this.teamOfficeUpdate = this.teamOffice;
      this.teamGroupUpdate = this.teamGroup;
      this.teamDepartmentUpdate = this.teamDepartment;
      this.teamSlackUpdate = this.teamSlack;
      this.teamLeaderUpdate = this.teamLeader;
      this.show = !this.show;
      this.errors = "";
    },
    cancel: function () {
      this.errors = "";
      this.show = !this.show;
    },
    showModal(user) {
      this.currentUser = user;
      this.dialog = true;
      this.errors = "";
    },
    closeDialog() {
      this.currentUser = "";
      this.dialog = false;
    },

    async setManager() {
      let formData = new FormData();
      formData.append("email", this.currentPM);
      let response = await TeamService.setManager(
        this.$route.params.id,
        formData
      );
      if (response.data && response.data.Success) {
        this.$toast.success("Success");
        this.$set(
          this.members,
          this.members.indexOf(this.currentUser),
          this.currentUser
        );
      } else {
        this.$toast.error("Error");
      }
      await this.getData();
    },
    async showMoveTeamModal(user) {
      this.dialogMove = true;
      let response = await TeamService.getNewTeams(user.user);
      this.newTeams = response.data;
      this.errors = "";
      this.currentUser = user;
    },
    hideModal() {
      this.$refs.mymodal.hide();
    },

    showModalLead(user) {
      this.currentUser = user;
      this.dialogLead = true;
    },
    hideModalLead() {
      this.currentUser = false;
      this.dialogLead = false;
    },
    async lead() {
      const formData = new FormData();
      const teamId = this.$route.params.id;
      this.show = true;
      this.errors = "";
      formData.append("email", this.currentUser.email);
      let response = await TeamService.setLeader(teamId, formData);
      if (response.data && response.data.Success) {
        this.$toast.success("Success");
        await this.getData();
      } else {
        this.$toast.error("Error");
      }
      this.currentUser = "";
      this.dialogLead = false;
    },
    async del() {
      const formData = new FormData();
      this.errors = "";
      formData.append("email", this.currentUser.email);
      let response = await TeamService.removeMember(
        this.$route.params.id,
        formData
      );
      if (response.data && response.data.Success) {
        this.members.splice(this.members.indexOf(this.currentUser), 1);
        this.$toast.success("Success");
      } else {
        this.$toast.error("Error");
      }
      this.currentUser = "";
      this.dialog = false;
    },
    async move() {
      const formData = new FormData();
      formData.append("current_team_id", this.$route.params.id);
      formData.append("user_id", this.currentUser.user);
      formData.append("new_team_id", this.newTeam);
      let response = await TeamService.moveTeam(formData);
      if (response.data && response.data.Success) {
        this.members.splice(this.members.indexOf(this.currentUser), 1);
        this.$toast.success("Success");
      } else {
        this.$toast.error("Error");
      }
      this.dialogMove = false;
    },
    closeDialogMove() {
      this.dialogMove = false;
      this.currentUser = "";
    },
    async getOffices() {
      const res = await officeServices.getOffices();
      res.data.results.unshift({
        id: null,
        name: "None",
      });
      this.offices = res.data.results;
    },
    async getGroups() {
      const res = await groupServices.getAll();
      res.data.unshift({
        id: null,
        name: "None",
      });
      this.groups = res.data;
    },
    async getDepartments() {
      const res = await departmentServices.getAll();
      res.data.unshift({
        id: null,
        name: "None",
      });
      this.departments = res.data;
    },
    hasScope(scope) {
      return this.tokenInfo["scope"].indexOf(scope) !== -1;
    },
  },

  async created() {
    await this.getData();
    await this.getOffices();
    await this.getGroups();
    await this.getDepartments();
    this.filteredUsers = this.allUsers;
  },
};
</script>
<style lang="scss" scoped>
@import "./style.scss";
</style>
