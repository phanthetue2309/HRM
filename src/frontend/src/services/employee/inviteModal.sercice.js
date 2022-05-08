import BaseService from "../base";

class InviteService extends BaseService {
  get entity() {
    return "admins";
  }

  async sendList(data) {
    return this.request().post(`${this.entity}/invite-users`, data);
  }
}

export default new InviteService();
