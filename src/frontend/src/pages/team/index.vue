<template>
  <div>
    <div v-if="!checked">
      <h2 class="text-info text-center m-4">There's no team yet</h2>
      <restricted-view :scopes="['team:create']">
        <template v-slot:default>
          <div class="d-flex justify-content-center">
            <router-link to="/create-team/" style="color: #ffffff">
              <el-button type="primary">
                <font-awesome-icon :icon="['fas', 'user-friends']" />
                Create Team
              </el-button>
            </router-link>
          </div>
        </template>
      </restricted-view>
    </div>
    <div v-if="checked">
      <el-row
        class="mt-3 mb-3 d-flex justify-content-between align-items-center"
      >
        <el-input
          class="ml-3"
          placeholder="Search here"
          v-model="searchName"
          style="width: 25%; order: -1"
        ></el-input>
        <restricted-view :scopes="['team:create']" style="order: 1">
          <template v-slot:default>
            <el-row>
              <router-link
                to="/create-team/"
                style="color: #ffffff; text-decoration: none"
                class="mb-3 mt-3"
              >
                <el-button type="primary" class="mt-3">
                  <font-awesome-icon :icon="['fas', 'user-friends']" />
                  Create New Team
                </el-button>
              </router-link>
            </el-row>
          </template>
        </restricted-view>
      </el-row>
      <el-table
        highlight-current-row
        :data="search"
        header-cell-class-name="bg-header-table"
        border
      >
        <el-table-column prop="team_name" sortable label="Team Name">
          <template slot-scope="scope">
            <div class="text-center">
              <router-link
                :to="'/teams/' + scope.row.id"
                style="text-decoration: none"
              >
                <strong> {{ scope.row.team_name }}</strong>
              </router-link>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="team_email" sortable label="Team Email">
          <template slot-scope="scope">
            <div class="text-center">
              <a
                :href="'mailto:' + scope.row.team_email"
                style="text-decoration: none"
                title="Click to send mail"
              >
                {{ scope.row.team_email }}
              </a>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="leader_name" sortable label="Team Leader">
          <template slot-scope="scope">
            <div class="text-center">
              <router-link
                :to="'/teams/' + scope.row.id"
                style="text-decoration: none"
                :class="{
                  'text-danger': scope.row.leader_name === 'No leader',
                }"
                title="Click to move to another page"
              >
                {{ scope.row.leader_name }}
              </router-link>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="department_name" sortable label="Department">
          <template slot-scope="scope">
            <div class="text-center">
              {{ scope.row.department_name }}
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="office_name" sortable label="Office">
          <template slot-scope="scope">
            <div class="text-center">
              {{ scope.row.office_name }}
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="group_name" sortable label="Group">
          <template slot-scope="scope">
            <div class="text-center">
              {{ scope.row.group_name }}
            </div>
          </template>
        </el-table-column>
        <el-table-column
          sortable
          prop="employee_number"
          label="Members"
          width="120"
        >
          <template slot-scope="scope">
            <div class="text-center">
              {{ scope.row.employee_number }}
            </div>
          </template>
        </el-table-column>
        <el-table-column label="Action" width="80">
          <template slot-scope="scope">
            <restricted-view :scopes="['team:edit_all_team']">
              <template v-slot:default>
                <img
                  :src="require('@/static/images/IconDelete.svg')"
                  @click="showModal(scope.row.id, scope.row.team_name)"
                />
              </template>
            </restricted-view>
          </template>
        </el-table-column>
      </el-table>
      <el-dialog :visible.sync="dialog" hide-footer hide-header="">
        <div class="d-block text-center text-danger">
          <h3>Remove team</h3>
          <hr />
        </div>
        <div class="d-block text-center mb-4">
          Do you want to remove team
          <p class="text-danger d-inline">{{ currentTeamName }}</p>
        </div>
        <div class="d-flex justify-content-center">
          <el-button type="primary" @click="del">Remove</el-button>
          <el-button type="danger" @click="hideModal">Cancel</el-button>
        </div>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import TeamService from "@/services/team/team.services";
import RestrictedView from "@/components/RestrictedView";

export default {
  name: "team_table",
  middleware: "authentication",
  components: {
    RestrictedView,
  },
  data() {
    return {
      rows: [],
      admin: localStorage.getItem("is_admin"),
      profile_id: localStorage.getItem("profile_id"),
      currentId: "",
      currentTeamName: "",
      color: {
        color: "#25c9d0",
        fontSize: "40px",
        marginLeft: "16px",
      },
      text: {
        fontSize: "20px",
      },
      errors: "",
      subject: "",
      dialog: false,
      searchName: "",
      searchOffice: "",
    };
  },

  created() {
    this.asyncData();
  },
  computed: {
    checked: function () {
      if (
        (this.rows !== null) &
        (this.rows !== undefined) &
        (this.rows.length !== 0)
      ) {
        return true;
      }
      return false;
    },
    search: function () {
      return this.rows.filter((data) => {
        const seachValue = this.searchName.toLowerCase();

        return (
          data.team_name.toLowerCase().includes(seachValue) ||
          (data.office_name &&
            data.office_name.toLowerCase().includes(seachValue)) ||
          (data.department_name &&
            data.department_name.toLowerCase().includes(seachValue)) ||
          (data.group_name &&
            data.group_name.toLowerCase().includes(seachValue))
        );
      });
    },
  },
  methods: {
    async asyncData() {
      const res = await TeamService.getAll();
      this.rows = res.data;
    },

    showModal(id, name) {
      this.currentId = id;
      this.currentTeamName = name;
      this.dialog = true;
    },

    hideModal() {
      this.dialog = false;
    },

    del: async function () {
      try {
        await TeamService.removeTeam(this.currentId);
        const index = this.rows.indexOf(
          this.rows.find((i) => i.id === this.currentId)
        );
        this.rows.splice(index, 1);
        this.$toast.success("Remove Team Success");
      } catch (e) {
        console.log(e);
        this.$toast.error("Remove Team Failed");
      }
      this.dialog = false;
    },
  },
};
</script>

<style lang="scss">
@import "./style.scss";
</style>
