import BaseService from "../base";

class SearchUserService extends BaseService {
  get entity() {
    return "user/search";
  }

  getTitleOption() {
    const res = this.request().get("user/get_all_title");
    return res;
  }

  getTeamOption() {
    const res = this.request().get("team/?limit=1");
    return res;
  }

  get(
    name,
    email,
    birthdayMonth,
    joinDate,
    gender,
    title,
    team,
    active,
    page,
    page_size
  ) {
    let temp_active = active === true ? 1 : 0;
    const res = this.request().get(`${this.entity}`, {
      params: {
        email: email,
        name: name,
        title: title,
        birthday: birthdayMonth,
        joindate: joinDate,
        gender: gender,
        team: team,
        active: temp_active,
        page: page,
        page_size: page_size,
      },
    });
    return res;
  }
}

export default new SearchUserService();
