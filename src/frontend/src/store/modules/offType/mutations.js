export default {
  GET_TYPE_OFF(state, data) {
    state.typeOff = data;
  },

  ADD_NEW_TYPE_OFF(state, payLoad) {
    const index = payLoad.rootState.offTypeGroup.typeOffGroup.indexOf(
      payLoad.rootState.offTypeGroup.typeOffGroup.find(
        (item) => item.id === payLoad.dataNew.leave_type_group
      )
    );
    let dataAdd = {
      id: payLoad.dataNew.id,
      name: payLoad.dataNew.name,
      leave_type_group: payLoad.dataNew.leave_type_group,
      days: payLoad.dataNew.days,
      is_count: payLoad.dataNew.is_count,
      descriptions: payLoad.dataNew.descriptions,
      is_active: payLoad.dataNew.is_active,
      name_type: payLoad.rootState.offTypeGroup.typeOffGroup[index].name,
    };
    state.typeOff.push(dataAdd);
  },

  EDIT_TYPE_OFF(state, payLoad) {
    let offTypeEdit = state.typeOff.find(
      (item) => item.id === payLoad.dataUpdate.id
    );
    offTypeEdit.name = payLoad.dataUpdate.data.name;
    offTypeEdit.is_count = payLoad.dataUpdate.data.is_count;
    offTypeEdit.days = payLoad.dataUpdate.data.days;
    const index = payLoad.rootState.offTypeGroup.typeOffGroup.find(
      (item) => item.id === payLoad.dataUpdate.data.leave_type_group
    );
    offTypeEdit.name_type = index.name;
    offTypeEdit.leave_type_group = payLoad.dataUpdate.data.leave_type_group;
    offTypeEdit.descriptions = payLoad.dataUpdate.data.descriptions;
  },

  DELETE_TYPE_OFF(state, data) {
    const index = state.typeOff.indexOf(
      state.typeOff.find((item) => item.id === data.id)
    );
    state.typeOff = [
      ...state.typeOff.slice(0, index),
      ...state.typeOff.slice(index + 1),
    ];
  },
};
