import BaseService from "../base";

class StatisticDateOffService extends BaseService {
  get entity() {
    return "workday/statistic";
  }

  getByUser(year) {
    const res = this.request().get(`${this.entity}/user?y=${year}`);
    return res;
  }

  getMyTeam(profile, month, year) {
    const res = this.request().get(
      `${this.entity}/team?p=${profile}&m=${month}&y=${year}`
    );
    return res;
  }

  getMyTeamYear(profile, year) {
    const res = this.request().get(
      `${this.entity}/team_all_year?p=${profile}&y=${year}`
    );
    return res;
  }

  getByAdmin(month, year, page, size, name, email, type) {
    const res = this.request().get(
      `${this.entity}/office?m=${month}&y=${year}&page_size=${size}&page=${page}&n=${name}&e=${email}&t=${type}`
    );
    return res;
  }
}

export default new StatisticDateOffService();
