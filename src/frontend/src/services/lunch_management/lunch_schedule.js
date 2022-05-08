import BaseService from "../base";

class LunchScheduleService extends BaseService {
  get entity() {
    return "lunches";
  }

  async create(data) {
    const lunch = await this.request().post(`/${this.entity}/`, data);
    return lunch;
  }

  async get(page, pageSize) {
    const res = await this.request().get(
      `/${this.entity}/?page=${page}&page_size=${pageSize}`
    );
    const lunches = res.data.results;
    if (lunches) {
      return lunches;
    } else return [];
  }

  async update({ data, id }) {
    const lunch = await this.request().put(`/${this.entity}/${id}`, data);
    return lunch;
  }

  async delete(id) {
    const lunch = await this.request().delete(`/${this.entity}/${id}`);
    return lunch;
  }
}

export default new LunchScheduleService();
