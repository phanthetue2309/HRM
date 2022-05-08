<template>
  <div class="bg-light">
    <div>
      <el-form class="mt-3" label-width="180px">
        <el-form-item label="Current Password *">
          <el-input v-model="currentPassword" type="password" style="width: 40%"/>
        </el-form-item>
        <el-form-item label="New Password *">
          <el-input v-model="newPassword" type="password" style="width: 40%"/>
        </el-form-item>
        <el-form-item label="Confirm Password *">
          <el-input v-model="repeatedNewPassword" type="password" style="width: 40%"/>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submit">Save</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>
<script>
import UserService from '@/services/user/user'

export default {
  name: 'id_change_password',
  middleware: 'authentication',
  data() {
    return {
      currentPassword: '',
      newPassword: '',
      repeatedNewPassword: '',
    };
  },
  methods: {
    submit: function () {
      if (this.check_form()) {
        const formData = new FormData();
        const id = localStorage.getItem('user_id');
        formData.append('current_password', this.currentPassword);
        formData.append('new_password', this.newPassword);
        UserService.changePassword(id, formData)
          .then(() => {
            this.$toast.success('Your password is changed successfully')
          })
          .catch((e) => {
            this.$toast.error('Your current password is not correct')
          });
      }
    },
    check_form() {
      if (this.currentPassword.length < 6) {
        this.$toast.error('Current password need more than 6 characters');
        return false;
      }
      if (this.newPassword.length < 6) {
        this.$toast.error('New Password need more than 6 characters');
        return false;
      }
      if (this.repeatedNewPassword < 6) {
        this.$toast.error('Repeated New Password need more than 6 characters');
        return false;
      }
      if (this.newPassword !== this.repeatedNewPassword) {
        this.$toast.error("New Password and Repeated New Password don't match");
        return false;
      }
      return true;
    },
  },
};
</script>
<style lang="scss" scoped>
</style>
