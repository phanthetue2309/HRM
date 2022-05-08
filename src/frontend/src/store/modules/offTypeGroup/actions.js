export default {
  getListTypeOffGroup({ commit }, data) {
    commit("GET_TYPE_OFF_GROUP", data);
  },

  addNewTypeOffGroup({ commit }, data) {
    commit("ADD_NEW_TYPE_OFF_GROUP", data);
  },

  editListTypeOffGroup({ commit }, data) {
    commit("EDIT_TYPE_OFF_GROUP", data);
  },

  deleteListTypeOffGroup({ commit }, data) {
    commit("DELETE_TYPE_OFF_GROUP", data);
  },
};
