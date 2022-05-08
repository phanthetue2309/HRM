import BaseService from "../base";

class UserService extends BaseService {
  get entity() {
    return "user";
  }

  getAllProjectManager() {
    const pms = this.request().get(`${this.entity}/get_project_managers`);
    return pms;
  }

  getAllRoles() {
    const roles = this.request().get(`${this.entity}/title`);
    return roles;
  }

  searchEmployeeByName(nameCharacter) {
    const res = this.request().get(`${this.entity}/search_non_paginate`, {
      params: {
        name: nameCharacter,
      },
    });
    return res;
  }

  getAllEmployees() {
    return this.request().get(`${this.entity}/get_non_paginate`);
  }

  getAllEmployeesExcludeUserId(id) {
    const res = this.request().get(
      `${this.entity}/get_all_exclude_user?id=${id}`
    );
    return res;
  }

  addRole(title) {
    const roles = this.request().post(`${this.entity}/title`, { title: title });
    return roles;
  }

  removeRole(id) {
    return this.request().delete(`${this.entity}/title/${id}`);
  }

  getUsersIncludeNameAndTitle() {
    return this.request().get(
      `${this.entity}/get_users_include_name_and_title`
    );
  }

  async filterUser(data) {
    try {
      return await this.request().get(`/${this.entity}?name=${data}`);
    } catch (e) {
      console.log(e);
    }
  }

  async activeUser(id) {
    try {
      return await this.request().put(`${this.entity}/${id}/activate`, "");
    } catch (e) {
      console.log(e);
    }
  }

  async deactivateUser(id) {
    try {
      return await this.request().put(`${this.entity}/${id}/deactivate`, "");
    } catch (e) {
      console.log(e);
    }
  }

  async deleteUser(id) {
    try {
      return await this.request().delete(`${this.entity}/${id}`);
    } catch (e) {
      console.log(e);
    }
  }

  async changePassword(id, data) {
    return await this.request().put(
      `${this.entity}/${id}/change_password`,
      data
    );
  }

  async changeAvatar(profileId, data) {
    return await this.request().patch(
      `${this.entity}/profile/${profileId}/change_avatar`,
      data
    );
  }

  async getUsersFilterByTitle(title) {
    try {
      return await this.request().get(
        `${this.entity}/get_users_filter_title?title=${title}`
      );
    } catch (e) {
      console.log(e);
    }
  }

  async verifyUser(body) {
    try {
      const res = await this.request().post(`${this.entity}/verify`, body);
      return res.status == 200;
    } catch (e) {
      return e.response;
    }
  }
}

export default new UserService();
