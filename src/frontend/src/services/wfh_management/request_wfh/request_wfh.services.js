import BaseService from "../../base";

class RequestWfhService extends BaseService {
  get entity() {
    return "wfh/wfh-request";
  }

  async create(data) {
    const wfhRequest = await this.request().post(`/${this.entity}`, data);
    return wfhRequest;
  }

  async getAllRequest(year = "", month = "", day = "", status = "") {
    try {
      const res = await this.request().get(
        `/${this.entity}?year=${year}&month=${month}&day=${day}&status=${status}`
      );
      const wfhRequests = res.data;
      return wfhRequests;
    } catch (error) {
      return [];
    }
  }

  async getMyWfhRequest(year = "", month = "", day = "", status = "") {
    try {
      const res = await this.request().get(
        `/${this.entity}/list_request_user?year=${year}&month=${month}&day=${day}&status=${status}`
      );
      const wfhRequests = res.data;
      return wfhRequests;
    } catch (error) {
      return [];
    }
  }

  async update({ data, id }) {
    const wfhRequest = await this.request().put(`/${this.entity}/${id}`, data);
    return wfhRequest;
  }

  async delete(id) {
    const wfhRequest = await this.request().delete(`/${this.entity}/${id}`);
    return wfhRequest;
  }

  async countTotalTypeOffDays(profile, typeOff, year) {
    const res = await this.request().get(
      `/${this.entity}/total_off_by_types?profile=${profile}&leave_type=${typeOff}&year=${year}`
    );
    const totalTypeOffLeaves = res.data;
    if (totalTypeOffLeaves) return totalTypeOffLeaves;
    else return 0;
  }
}

export default new RequestWfhService();
