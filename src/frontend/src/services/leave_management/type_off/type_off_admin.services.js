import BaseService from "../../base";

export class TypeOffAdminServices extends BaseService {
  get entity() {
    return "workday/admin/leave-types";
  }

  getTypeOff() {
    return this.request().get(`${this.entity}`);
  }

  getTypeOffUser() {
    return this.request().get(`${this.entity}/list_type_true`);
  }

  addTypeOff(data) {
    return this.request().post(`${this.entity}`, data);
  }

  handleActiveTypeOff(id) {
    return this.request().patch(`${this.entity}/${id}`);
  }

  editTypeOff(id, data) {
    return this.request().put(`${this.entity}/${id}`, data);
  }

  deleteTypeOff(id) {
    return this.request().delete(`${this.entity}/${id}`);
  }
}

export default new TypeOffAdminServices();
