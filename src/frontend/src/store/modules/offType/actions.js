export default {
  getListTypeOff({ commit }, data) {
    commit("GET_TYPE_OFF", data);
  },

  addNewTypeOff({ commit, rootState }, data) {
    let payLoad = {
      rootState: rootState,
      dataNew: data,
    };
    commit("ADD_NEW_TYPE_OFF", payLoad);
  },

  editListTypeOff({ commit, rootState }, data) {
    let payLoad = {
      rootState: rootState,
      dataUpdate: data,
    };
    commit("EDIT_TYPE_OFF", payLoad);
  },

  deleteListTypeOff({ commit }, data) {
    commit("DELETE_TYPE_OFF", data);
  },
};
