import BaseService from "../base";

export class RoleService extends BaseService {
  get entity() {
    return "user/role";
  }

  async getRole(id) {
    try {
      return this.request().get(`${this.entity}/${id}`);
    } catch (e) {
      console.log(e);
    }
  }

  async getRoles(page_size, page, name) {
    try {
      return this.request().get(`${this.entity}`, {
        params: {
          page_size: page_size,
          page: page,
          name: name,
        },
      });
    } catch (e) {
      console.log(e);
    }
  }

  async createRole(role) {
    try {
      return this.request().post(`${this.entity}`, {
        name: role.name,
        description: role.description,
        scope: role.scope,
      });
    } catch (e) {
      console.log(e);
    }
  }

  async updateRole(role) {
    try {
      return this.request().put(`${this.entity}/${role.id}`, {
        id: role.id,
        name: role.name,
        description: role.description,
        scope: role.scope,
      });
    } catch (e) {
      console.log(e);
    }
  }

  async deleteRole(role_id) {
    try {
      return this.request().delete(`${this.entity}/${role_id}`);
    } catch (e) {
      console.log(e);
    }
  }
}

export default new RoleService();
