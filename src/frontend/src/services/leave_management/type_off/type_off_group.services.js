import BaseService from "../../base";

export class TypeOffGroupAdminServices extends BaseService {
  get entity() {
    return "workday/admin/group-leave-types";
  }

  getTypeOffGroup() {
    return this.request().get(`${this.entity}`);
  }

  addTypeOffGroup(data) {
    return this.request().post(`${this.entity}`, data);
  }

  handleActiveTypeOffGroup(id) {
    return this.request().patch(`${this.entity}/${id}`);
  }

  editTypeOffGroup(id, data) {
    return this.request().put(`${this.entity}/${id}`, data);
  }

  deleteTypeOffGroup(id) {
    return this.request().delete(`${this.entity}/${id}`);
  }
}

export default new TypeOffGroupAdminServices();
