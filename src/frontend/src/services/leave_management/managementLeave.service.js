import BaseService from "../base";

class ManagementLeaveService extends BaseService {
  get entity() {
    return "workday/request";
  }

  async getManagementRequestOff(
    page = 1,
    pageSize = 12,
    year = "",
    month = "",
    day = "",
    status = "",
    search = ""
  ) {
    try {
      const request = this.request().get(
        `/${this.entity}/management/get_request_detail`,
        {
          params: {
            year: year,
            month: month,
            day: day,
            status: status,
            search: search,
            page: page,
            page_size: pageSize,
          },
        }
      );
      return request;
    } catch (error) {
      return [];
    }
  }

  async actionRequest(data) {
    try {
      const response = await this.request().post(
        `/${this.entity}/management`,
        data
      );
      return response.data;
    } catch (error) {
      return null;
    }
  }
  async deleteLeaveRequest(data) {
    try {
      const response = await this.request().post(
        `/${this.entity}/management/multi`,
        data
      );
      return response.data;
    } catch (error) {
      return null;
    }
  }

  async countRequest() {
    try {
      let response = this.request().get(`/${this.entity}/management/count`);
      if (response && response.status === 200 && response.data) {
        return response.data;
      }
      return 0;
    } catch (error) {
      return 0;
    }
  }
}

export default new ManagementLeaveService();
