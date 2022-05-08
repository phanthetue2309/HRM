import BaseService from "../base";

class TeamService extends BaseService {
  get entity() {
    return "team";
  }

  create(data) {
    const team = this.request().post(`/${this.entity}/`, data);
    return team;
  }

  getAll() {
    const teams = this.request().get(`/${this.entity}/`);
    return teams;
  }

  get(id) {
    const team = this.request().get(`/${this.entity}/${id}`);
    return team;
  }

  update(id, data) {
    return this.request().put(`${this.entity}/${id}`, data);
  }

  delete(id) {
    return this.request().delete(`${this.entity}/${id}`);
  }

  addMember(id, data) {
    const response = this.request().put(
      `${this.entity}/${id}/add_member`,
      data
    );
    return response;
  }

  modifyMembers(id, data) {
    const response = this.request().put(
      `${this.entity}/${id}/modify_members`,
      data
    );
    return response;
  }

  removeMember(id, data) {
    const response = this.request().put(
      `${this.entity}/${id}/remove_member`,
      data
    );
    return response;
  }

  getNewTeams(userId) {
    const response = this.request().get(
      `${this.entity}/${userId}/get_new_teams`
    );
    return response;
  }

  getLeaders(name) {
    const response = this.request().get(
      `${this.entity}/send_leader?name=${name}`
    );
    return response;
  }

  moveTeam(data) {
    const response = this.request().put(`${this.entity}/move_team`, data);
    return response;
  }

  setLeader(teamId, data) {
    const response = this.request().put(
      `${this.entity}/${teamId}/set_leader`,
      data
    );
    return response;
  }

  setManager(teamId, data) {
    const response = this.request().put(
      `${this.entity}/${teamId}/set_project_manager`,
      data
    );
    return response;
  }

  removeTeam(teamId) {
    const response = this.request().delete(`${this.entity}/${teamId}`);
    return response;
  }

  getFloatMembers() {
    return this.request().get(`${this.entity}/float_members`);
  }
}

export default new TeamService();
