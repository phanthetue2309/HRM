import BaseService from "../base";
import { accessToken } from "@/helper/accessToken";
import { decodeToken } from "@/utils/decodeToken";

export class ScopeService extends BaseService {
  get entity() {
    return `oauth2/applications/retrieve_all_scopes`;
  }

  getScopes() {
    try {
      return this.request().get(`${this.entity}`);
    } catch (e) {
      console.log(e);
    }
  }

  getScopesFromStorage() {
    try {
      if (accessToken()) {
        return decodeToken(accessToken());
      } else return null;
    } catch (e) {
      console.log(e);
    }
  }
}

export default new ScopeService();
