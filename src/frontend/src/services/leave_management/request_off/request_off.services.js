import BaseService from "../../base";

class RequestOffService extends BaseService {
  get entity() {
    return "workday/request-off";
  }

  async create(data) {
    const requestOff = await this.request().post(`/${this.entity}`, data);
    return requestOff;
  }

  async getAllRequest(year = "", month = "", day = "", status = "") {
    try {
      const res = await this.request().get(
        `/${this.entity}?year=${year}&month=${month}&day=${day}&status=${status}`
      );
      const requestOffs = res.data;
      return requestOffs;
    } catch (error) {
      return [];
    }
  }

  async getMyRequest(year = "", month = "", day = "", status = "") {
    try {
      const res = await this.request().get(
        `/${this.entity}/list_request_user?year=${year}&month=${month}&day=${day}&status=${status}`
      );
      const requestOffs = res.data;
      return requestOffs;
    } catch (error) {
      return [];
    }
  }

  async update({ data, id }) {
    const requestOff = await this.request().put(`/${this.entity}/${id}`, data);
    return requestOff;
  }

  async delete(id) {
    const requestOff = await this.request().delete(`/${this.entity}/${id}`);
    return requestOff;
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

export default new RequestOffService();
