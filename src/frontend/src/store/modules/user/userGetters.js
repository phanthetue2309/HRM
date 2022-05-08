export default {
  isAdmin: (state) => state.currentUser.role === 1,
  allUsers: (state) => state.allUsers
};
