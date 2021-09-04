<template>
  <div>
    <div
      class="d-flex justify-content-end"
      style="position: absolute; right: 10%"
    >
      <DarkLightMode />
    </div>
    <div class="container-login100">
      <div class="wrap-login100">
        <b-col class="col-7 d-none d-md-block d-md-block">
          <LoginVector class="login-vector" />
        </b-col>
        <b-col class="col-12 col-sm-8 col-md-5 offset-sm-2 offset-md-0">
          <div
            class="box-login shadow justify-content-center align-items-center"
          >
            <b-form method="post" @submit.prevent="sendAuth">
              <div class="text-center m-4">
                <Logo class="logo mb-2" />
                <p>
                  <strong>Halo sobat 👋</strong>
                </p>
                <p>
                  Lakukan autentikasi akun Anda terlebih dahulu ya.
                </p>
              </div>
              <b-alert
                :show="error === '' ? false : true"
                variant="danger"
                fade
                >{{ error }}</b-alert
              >
              <b-input-group class="mb-4" size="sm">
                <b-input-group-append is-text>
                  <b-icon-key class="icon"></b-icon-key>
                </b-input-group-append>
                <b-form-input
                  ref="username"
                  v-model="auth.username"
                  placeholder="Username"
                  style="border-left: 0"
                  required
                ></b-form-input>
              </b-input-group>
              <b-input-group class="mb-2" size="sm">
                <b-input-group-append is-text>
                  <b-icon-lock class="icon"></b-icon-lock>
                </b-input-group-append>
                <b-form-input
                  ref="password"
                  v-model="auth.password"
                  :type="passwordFieldType"
                  placeholder="Password"
                  style="border-left: 0"
                  class="border-right-0"
                  required
                ></b-form-input>
                <span class="input-group-append">
                  <div
                    class="input-group-text bg-transparent"
                    type="button"
                    @click="btnPassword"
                  >
                    <b-icon-eye-slash
                      v-if="!showPassword"
                      scale="0.9"
                      class="icon"
                    ></b-icon-eye-slash>
                    <b-icon-eye
                      v-if="showPassword"
                      scale="0.9"
                      class="icon"
                    ></b-icon-eye>
                  </div>
                </span>
              </b-input-group>
              <div class="text-center mt-4">
                <b-overlay
                  :show="busy"
                  rounded
                  opacity="0.6"
                  spinner-small
                  spinner-variant="primary"
                  class="d-inline-block"
                >
                  <b-button :disabled="busy" variant="success" type="submit">
                    Login
                  </b-button>
                </b-overlay>
              </div>
            </b-form>
            <p class="line">&nbsp;</p>
            <div class="text-center" v-if="allowRegister">
              <nuxt-link to="register">Registrasi Akun</nuxt-link>
            </div>
          </div>
        </b-col>
      </div>
    </div>
  </div>
</template>

<script>
import Logo from "~/components/NuxtLogo";
import LoginVector from "~/components/LoginVector";
import DarkLightMode from "~/components/DarkLightMode";
import { mapMutations } from "vuex";
import md5 from "md5";
export default {
  name: "Login",
  components: {
    Logo,
    LoginVector,
    DarkLightMode
  },
  data() {
    return {
      showPassword: false,
      passwordFieldType: "password",
      auth: {},
      time: "",
      busy: false,
      error: "",
      allowRegister: false
    };
  },
  head() {
    return {
      title: "Login"
    };
  },
  mounted() {
    //KITA LAKUKAN PENGECEK, JIKA SUDAH LOGIN
    if (this.$store.state.loggedIn) {
      //MAKA REDIRECT KE HALAMAN UTAMA
      this.$router.replace("beranda");
    }
  },
  created() {
    this.checkUsers();
  },
  methods: {
    ...mapMutations(["SET_TOKEN_ID", "SET_lOGGED_IN", "SET_USER"]),
    async checkUsers() {
      await this.$axios
        .get("/api/users/_search")
        .then(resp => {
          const count = resp.data.hits.total.value;
          this.busy = false;
          if (count > 0) {
            this.allowRegister = false;
          } else {
            this.allowRegister = true;
          }
        })
        .catch(error => {
          this.allowRegister = true;
        });
    },
    btnPassword() {
      if (this.showPassword === true) {
        this.showPassword = false;
        this.passwordFieldType = "password";
      } else {
        this.showPassword = true;
        this.passwordFieldType = "text";
      }
    },
    //JIKA TOMBOL LOGIN DITEKAN, MAKA METHOD INI AKAN DIJALANKAN
    async sendAuth() {
      this.busy = true;
      if (!this.auth.username) {
        this.$refs.username.$el.focus();
        this.error = "Username / email wajid diisi";
      } else if (!this.auth.password) {
        this.$refs.password.$el.focus();
        this.error = "Password wajid diisi";
      } else {
        try {
          //MELAKUKAN PROSES LOGIN, DENGAN MENGGUNAKAN STRATEGIES LOCAL YANG ADA DI NUXT CONFIG
          //DAN MENGIRIMKAN DATA BERUPA EMAIL DAN PASSWORD
          const data = {
            query: {
              bool: {
                must: [
                  {
                    match: {
                      username: this.auth.username
                    }
                  },
                  {
                    match: {
                      password: md5(this.auth.password)
                    }
                  }
                ]
              }
            }
          };
          await this.$axios
            .post("/api/users/_search", data)
            .then(resp => {
              const count = resp.data.hits.total.value;
              this.busy = false;
              if (count > 0) {
                this.SET_lOGGED_IN(true);
                this.SET_TOKEN_ID(resp.data.hits.hits[0]._id);
                this.SET_USER(resp.data.hits.hits[0]._source);
                this.$router.replace("beranda");
              } else {
                this.busy = false;
                this.error = "Username / password tidak sesuai";
              }
            })
            .catch(() => {
              this.busy = false;
            });
        } catch (e) {
          console.log(e);
          this.busy = false;
          this.error = "Username / password tidak sesuai";
        }
      }
    }
  }
};
</script>

<style scoped>
.btn-dark-mode {
  position: absolute;
  border: 1px solid #e3e3e3;
  border-radius: 15px;
  cursor: pointer;
  z-index: 99;
}
.dark-mode .btn-dark-mode {
  background-color: #1c3c56;
}
.light-mode .btn-dark-mode {
  background-color: aliceblue;
}

.login-vector {
  position: absolute;
  bottom: 0;
}
.logo {
  width: 30%;
}
.box-login {
  top: 50vh;
  min-width: 80%;
  min-height: 100%;
  padding: 15px;
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.18);
}

.container-login100 {
  width: 100%;
  min-height: 100vh;
  display: -webkit-box;
  display: -webkit-flex;
  display: -moz-box;
  display: -ms-flexbox;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  padding: 15px;
}
.wrap-login100 {
  width: 960px;
  min-height: 70vh;
  background: #fff;
  overflow: hidden;
  display: -webkit-box;
  display: -webkit-flex;
  display: -moz-box;
  display: -ms-flexbox;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  padding: 50px 10px 40px 10px;
}

.dark-mode .wrap-login100 {
  background-color: #2f495e;
}
.light-mode .wrap-login100 {
  background-color: #fff;
}

.div-menu {
  position: absolute;
  bottom: 0;
  width: 100%;
}
.link-menu {
  padding: 5px;
}
@media (max-width: 480px) {
  .container-login100 {
    padding: 0;
  }
}
</style>
