import BaseService from "../base";

class UserLunchService extends BaseService {
  get entity() {
    return "user-lunch";
  }

  create(data) {
    const userLunch = this.request().post(`/${this.entity}/create`, data);
    return userLunch;
  }

  adminCreate(list_data) {
    const userLunch = this.request().post(`/${this.entity}/admin-create`, {
      list_data,
    });
    return userLunch;
  }

  createMany(data) {
    const lunch = this.request().post(`/${this.entity}/create-many`, data);
    return lunch;
  }

  get() {
    const userLunch = this.request().get(`/${this.entity}/`);
    return userLunch;
  }

  getAll() {
    const userLunch = this.request().get(`/${this.entity}/all`);
    return userLunch;
  }

  getPagi(date) {
    const userLunch = this.request().get(
      `/${this.entity}/get-paginate?date=${date}`
    );
    return userLunch;
  }

  update({ data, id }) {
    const userLunch = this.request().put(`/${this.entity}/action/${id}`, data);
    return userLunch;
  }

  updateByAdmin({ data, id }) {
    const userLunch = this.request().put(
      `/${this.entity}/admin-update/${id}`,
      data
    );
    return userLunch;
  }

  delete(id) {
    const userLunch = this.request().delete(`/${this.entity}/action/${id}`);
    return userLunch;
  }

  deleteMany(data) {
    const userLunch = this.request().put(`/${this.entity}/delete-many`, data);
    return userLunch;
  }

  setVeggieMonth(data) {
    const userLunch = this.request().put(`/${this.entity}/set-veggie`, data);
    return userLunch;
  }

  cancelSetVeggieMonth(data) {
    const userLunch = this.request().put(`/${this.entity}/cancel-veggie`, data);
    return userLunch;
  }

  statistic(data) {
    const statistics = this.request().post(`/${this.entity}/statistic`, data);
    return statistics;
  }
}

export default new UserLunchService();
