export default {
  GET_TYPE_OFF_GROUP(state, data) {
    state.typeOffGroup = data;
  },

  ADD_NEW_TYPE_OFF_GROUP(state, data) {
    state.typeOffGroup.push(data);
  },

  EDIT_TYPE_OFF_GROUP(state, data) {
    let payTypeEdit = state.typeOffGroup.find((item) => item.id === data.id);
    payTypeEdit.title = data.data.title;
    payTypeEdit.is_company_pay = data.data.is_company_pay;
    payTypeEdit.is_insurance_pay = data.data.is_insurance_pay;
  },

  DELETE_TYPE_OFF_GROUP(state, data) {
    const index = state.typeOffGroup.indexOf(
      state.typeOffGroup.find((item) => item.id === data.id)
    );
    state.typeOffGroup = [
      ...state.typeOffGroup.slice(0, index),
      ...state.typeOffGroup.slice(index + 1),
    ];
  },
};
