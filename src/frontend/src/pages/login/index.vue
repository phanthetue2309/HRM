<template>
  <div class="background">
    <div class="row justify-content-center m-0">
      <div class="col-10 col-xl-4 col-lg-4 text-center">
        <img class="icon" src="@/static/images/logo-paradox-white-01.png" />
      </div>
    </div>

    <div class="hero-content text-info">
      <div id="loginform" class="container" v-show="checkForgotPassword === false">
        <!-- Outer Row -->
        <div class="row justify-content-center">
          <div class="col-xl-5 col-lg-5 col-md-8 col-sm-12 col-12">
            <div class="my-5">
              <el-card class="box-card py-4" shadow="always">
                <div class="text-center">
                  <h1 class="h4 text-info mb-3 font-weight-bold">Welcome Back!</h1>
                </div>
                <div class="form-controler">
                  <el-form
                    id="login"
                    class="login-form"
                    method="POST"
                    ref="form"
                    @submit.native.prevent="login"
                    @keyup.enter="login"
                    label-width="120px"
                  >
                    <div v-if="error !== ''" class="text-danger">{{ error }}</div>
                    <br />
                    <el-form-item label-width="0px" prop="email">
                      <el-input
                        id="email"
                        v-model="loginFormData.email"
                        aria-describedby="emailHelp"
                        type="email"
                        class="form-control form-control-user"
                        placeholder="Email Address"
                      ></el-input>
                    </el-form-item>
                    <el-form-item label-width="0px" prop="password">
                      <el-input
                        id="password"
                        v-model="loginFormData.password"
                        type="password"
                        class="form-control form-control-user"
                        placeholder="Password"
                      ></el-input>
                    </el-form-item>
                    <hr />
                    <el-form-item label-width="0px">
                      <el-button
                        :loading="loading"
                        class="login-button"
                        type="primary"
                        native-type="submit"
                        block
                      >Login</el-button>
                    </el-form-item>
                    <el-form-item label-width="0px">
                      <el-button
                        size="medium"
                        round
                        @click.prevent="loginWithGoogle"
                        class="google-button"
                      >
                        <span>
                          <img alt="Google login" src="../../static/images/googleIcon.svg" />
                          <span class="text-login">Login with Google</span>
                        </span>
                      </el-button>
                    </el-form-item>
                  </el-form>
                </div>
                <div class="text-center mt-3">
                  <a
                    class="no-underline pointer"
                    title="Click to find your password"
                    @click="displayForgotPassBox"
                  >Forgot password?</a>
                </div>
                <div class="text-center mt-3">
                  <a class="no-underline pointer" href="terms-of-use/">Term of use</a>
                  <a class="no-underline pointer">|</a>
                  <a class="no-underline pointer" href="privacy-policy/">Privacy policy</a>
                </div>
              </el-card>
            </div>
          </div>
        </div>
      </div>
      <div class="container" v-show="checkForgotPassword === true">
        <div class="row justify-content-center">
          <div class="col-xl-6 col-lg-6 col-md-8 col-sm-12 col-12">
            <div class="card o-hidden border-0 shadow-lg my-5" v-if="!success">
              <el-card class="box-card">
                <div slot="header" class="clearfix">
                  <div class="text-center">
                    <h1 class="h4 text-info mt-3 font-weight-bold">Find your account</h1>
                  </div>
                </div>
                <div class="form-controler">
                  <div class="row">
                    <div
                      class="col-12 alert color-danger mt-2"
                      v-show="forgotPassError.title !== ''"
                    >
                      <el-alert title type="error">
                        <strong>{{ forgotPassError.title }}</strong>
                        <br />
                        {{ forgotPassError.content }}
                      </el-alert>
                    </div>
                    <div
                      class="col-12 mx-auto text-dark my-2 text-center"
                    >Please enter your email address:</div>
                    <div class="col-12">
                      <el-form
                        id="find"
                        class="login-form"
                        method="POST"
                        ref="form"
                        @submit.native.prevent="submitForgotPassBox"
                        @keyup.enter="submitForgotPassBox"
                      >
                        <el-form-item label-width="0px">
                          <el-input
                            type="text"
                            id="identify_email"
                            class="w-100 p-1 form-control"
                            v-model="emailToGetPassword"
                            name="email"
                            placeholder="Email address"
                            autofocus="1"
                            aria-label="email address"
                          ></el-input>
                        </el-form-item>
                        <el-form-item class="text-right">
                          <el-button type="info" @click="displayForgotPassBox">Cancel</el-button>
                          <el-button
                            type="primary"
                            @click="submitForgotPassBox"
                          >Send reset password email</el-button>
                        </el-form-item>
                      </el-form>
                    </div>
                  </div>
                </div>
              </el-card>
            </div>
            <div class="card o-hidden border-0 shadow-lg my-5" v-else>
              <el-card class="box-card">
                <div slot="header" class="clearfix">
                  <div class="text-center">
                    <h1 class="h4 text-info mt-3 font-weight-bold">Success</h1>
                  </div>
                </div>
                <div class="card-body mb-3">
                  <div class="row">
                    <el-alert title type="success">
                      Reset password link had been sent to email
                      {{ emailToGetPassword }}.
                    </el-alert>
                  </div>
                </div>
                <div class="card-footer text-right">
                  <div class="justify-content-end d-flex">
                    <el-button type="primary" @click="displayForgotPassBox">Return to login</el-button>
                  </div>
                </div>
              </el-card>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import authenticationServices from "@/services/authentication/authentication.services.js";
import Oauth2Service from "@/services/authentication/oauth2.services.js";
import GetUserService from "@/services/user/getUser";
import messageRespone from "@/services/authentication/responseMessage";
import { mapActions } from "vuex";
import UserService from "@/services/user/getUser";

export default {
  name: "login",
  middleware: "afterlogin",
  data() {
    return {
      emailToGetPassword: "",
      error: "",
      loginFormData: {
        email: "",
        password: "",
      },
      checkForgotPassword: false,
      forgotPassError: {
        title: "",
        content: "",
      },
      success: false,
      loading: false,
    };
  },
  head() {
    return {
      title: "Login",
    };
  },
  methods: {
    ...mapActions("user", ["setCurrentUser"]),
    async fetchUser(errMess) {
      const result = await UserService.getCurrentUser();
      if (result) {
        this.setCurrentUser(result);
      } else {
        this.error = errMess;
      }
    },
    submitForgotPassBox: async function () {
      if (this.emailToGetPassword === "") {
        this.forgotPassError.title = messageRespone.VALIDATION.EMPTY_INPUT;
        this.forgotPassError.content =
          messageRespone.VALIDATION.EMPTY_INPUT_DETAIL;
      } else if (this.validEmail(this.emailToGetPassword) !== true) {
        this.emailToGetPassword = "";
        this.forgotPassError.title = messageRespone.VALIDATION.EMAIL;
        this.forgotPassError.content = messageRespone.VALIDATION.EMAIL_DETAIL;
      } else {
        this.forgotPassError = {
          title: "",
          content: "",
        };
        const formdata = new FormData();
        formdata.append("email", this.emailToGetPassword);

        const responseResult = await authenticationServices.forgotPassword(
          formdata
        );
        if (responseResult) {
          this.displayForgotPassBox;
          this.forgotPassError = {
            title: "",
            content: "",
          };
          this.success = true;
        } else {
          this.forgotPassError.title = messageRespone.SEARCH_RESULT.TITLE;
          this.forgotPassError.content = messageRespone.SEARCH_RESULT.CONTENT;
        }
      }
    },
    displayForgotPassBox: function () {
      this.checkForgotPassword = !this.checkForgotPassword;
      this.forgotPassError = {
        title: "",
        content: "",
      };
      this.emailToGetPassword = "";
      this.success = false;
    },
    login: async function () {
      if ((await this.validation()) === true) {
        this.loading = true;
        const token = await Oauth2Service.login(this.loginFormData);
        if (token) {
          const user = await GetUserService.getCurrentUser(token.sub);
          if (user) {
            const { id, email, profile, active, admin } = user.data;
            if (!active) {
              this.error = messageRespone.AUTHENTICATION.USER_DEACTIVATED;
              this.loginFormData.password = "";
              return;
            }
            const userData = {
              user: id,
              email: email,
              name: profile.name,
              profile_id: profile.id,
              is_admin: admin,
            };
            this.$store.commit("user/SET_CURRENT_USER", userData);
            localStorage.setItem("email", email);
            localStorage.setItem("user_id", id);
            localStorage.setItem("profile_id", profile.id);
            localStorage.setItem("is_admin", admin);
            localStorage.setItem("imageUrl", profile.image);
            localStorage.setItem("name", profile.name);
            this.loading = false;
            if (this.$router.currentRoute.name == "Login") {
              this.$router.push("/");
              this.$router.go(0);
            }
          } else {
            this.error = messageRespone.AUTHENTICATION.INCORRECT_ACCOUNT;
            this.loginFormData.email = "";
            this.loginFormData.password = "";
          }
        } else {
          this.error = "invalid password";
          this.loading = false;
        }
      }
    },
    loginWithGoogle: async function () {
      const googleUser = await this.$gAuth.signIn();
      const id_token = googleUser.wc.id_token;
      const token = await Oauth2Service.loginWithGoogle(id_token);
      if (token) {
        const user = await GetUserService.getCurrentUser(token.sub);
        if (user) {
          const { id, email, profile, active, admin } = user.data;
          if (!active) {
            this.error = messageRespone.AUTHENTICATION.USER_DEACTIVATED;
            this.loginFormData.password = "";
            return;
          }
          const userData = {
            user: id,
            email: email,
            name: profile.name,
            profile_id: profile.id,
            is_admin: admin,
          };
          this.$store.commit("user/SET_CURRENT_USER", userData);
          localStorage.setItem("email", email);
          localStorage.setItem("user_id", id);
          localStorage.setItem("profile_id", profile.id);
          localStorage.setItem("is_admin", admin);
          localStorage.setItem("imageUrl", profile.image);
          localStorage.setItem("name", profile.name);
          if (this.$router.currentRoute.name == "Login") {
            this.$router.push("/");
            this.$router.go(0);
          }
        } else {
          this.error = messageRespone.AUTHENTICATION.INCORRECT_ACCOUNT;
          this.loginFormData.email = "";
          this.loginFormData.password = "";
        }
      } else this.error = messageRespone.AUTHENTICATION.ACCOUNT_NOT_EXIST;
    },
    validation: async function () {
      this.error = "";
      if (!this.loginFormData.email) {
        this.error = messageRespone.VALIDATION.EMPTY_EMAIL;
        return false;
      } else if (!this.validEmail(this.loginFormData.email)) {
        this.error = messageRespone.EMAIL;
        return false;
      } else if (
        !this.loginFormData.password ||
        this.loginFormData.password.length < 6
      ) {
        this.error = messageRespone.VALIDATION.PASSWORD;
        return false;
      }

      return true;
    },
    validEmail: function (email) {
      const re =
        /^(([^<>()\]\\.,;:\s@"]+(\.[^<>()\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return re.test(email);
    },
  },
};
</script>

<style lang="scss" scoped>
@import "index.scss";
</style>
