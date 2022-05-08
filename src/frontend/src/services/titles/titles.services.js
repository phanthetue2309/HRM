import BaseService from "../base";

class TitleService extends BaseService {
  get entity() {
    return "user/title";
  }

  getAll() {
    const titles = this.request().get(`/${this.entity}`);
    return titles;
  }

  update(id, data) {
    console.log(id,data)
    const title = this.request().put(`${this.entity}/${id}`, data);
    return title;
  }

  create(data) {
    const title  = this.request().post(`/${this.entity}`, data);
    return title;
  }

  removeTitle(titleId) {
    const response = this.request().delete(`${this.entity}/${titleId}`);
    return response;
  }
}

export default new TitleService();
