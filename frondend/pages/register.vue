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
            <b-form method="post" @submit.prevent="postData">
              <div class="text-center mb-4">
                <p>
                  <strong>ADMINISTRATOR</strong>
                </p>
                <p>
                  Lakukan registrasi akun Admin sistem.
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
                  <b-icon-person class="icon"></b-icon-person>
                </b-input-group-append>
                <b-form-input
                  ref="fullname"
                  v-model="auth.fullname"
                  placeholder="Nama lengkap"
                  style="border-left: 0"
                  required
                ></b-form-input>
              </b-input-group>
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
              <b-input-group class="mb-4" size="sm">
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
              <b-input-group class="mb-4" size="sm">
                <b-input-group-append is-text>
                  <b-icon-image class="icon"></b-icon-image>
                </b-input-group-append>
                <b-form-file
                  ref="photo"
                  size="sm"
                  accept="image/jpeg, image/png, image/jpg"
                  placeholder="Photo"
                  @change="base64File"
                  style="border-left: 0"
                  required
                ></b-form-file>
              </b-input-group>
              <div class="text-center mt-4">
                <b-overlay
                  :show="isBusySubmit"
                  rounded
                  opacity="0.6"
                  spinner-small
                  spinner-variant="primary"
                  class="d-inline-block"
                >
                  <b-button
                    :disabled="isBusySubmit"
                    variant="success"
                    type="submit"
                  >
                    Daftar
                  </b-button>
                </b-overlay>
              </div>
            </b-form>
            <p class="line">&nbsp;</p>
            <div class="text-center str">
              Sudah punya akun? <nuxt-link to="login">Login saja</nuxt-link>
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
import md5 from "md5";
export default {
  name: "Registrasi",
  auth: false,
  components: {
    Logo,
    LoginVector,
    DarkLightMode
  },
  data() {
    return {
      showPassword: false,
      passwordFieldType: "password",
      auth: {
        photo: null
      },
      time: "",
      isBusySubmit: false,
      error: ""
    };
  },
  head() {
    return {
      title: "Registrasi",
      meta: [
        {
          hid: "register",
          name: "register",
          content: "Halaman registrasi akun"
        }
      ]
    };
  },
  mounted() {
    //KITA LAKUKAN PENGECEK, JIKA SUDAH LOGIN
    if (this.$store.state.loggedIn) {
      //MAKA REDIRECT KE HALAMAN UTAMA
      this.$router.replace("home");
    }
  },
  created() {
    this.showMessage();
  },
  methods: {
    base64File: function() {
      const file = document.querySelector("input[type=file]").files[0];
      const reader = new FileReader();

      reader.onloadend = () => {
        this.auth.photo = reader.result;
      };
      reader.readAsDataURL(file);
      // console.log(file);
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
    async postData() {
      if (!this.auth.fullname) {
        this.$refs.fullname.$el.focus();
        this.error = "Nama lengkap wajid diisi";
      } else if (!this.auth.username) {
        this.$refs.username.$el.focus();
        this.error = "Username wajid diisi";
      } else if (!this.auth.password) {
        this.$refs.password.$el.focus();
        this.error = "Password wajid diisi";
      } else if (!this.auth.photo) {
        this.$refs.photo.$el.focus();
        this.error = "Photo wajid diisi";
      } else {
        this.isBusySubmit = true;
        const data = {
          fullname: this.auth.fullname,
          username: this.auth.username,
          password: md5(this.auth.password),
          photo: this.auth.photo
        };
        const headers = {
          "Content-Type": "application/json"
        };
        await this.$axios
          .post(`/api/users/_doc/`, data, {
            headers: headers
          })
          .then(resp => {
            this.isBusySubmit = false;
            this.$confirm({
              title: "⚠ Success",
              message: "Berhasil mendaftar sebagai Adminstrator",
              button: {
                yes: "Login sekarang"
              },
              callback: confirm => {
                if (confirm) {
                  this.$router.push("login");
                }
              }
            });
          })
          .catch(error => {
            if (error.response) {
              this.isBusySubmit = false;
              this.$confirm({
                title: "⛔ Error",
                message: "Gagal menyimpan data",
                button: {
                  yes: "Ok"
                }
              });
            }
          });
      }
    },
    async showMessage() {
      this.$confirm({
        title: "⚠ Info",
        message:
          "Pastikan mengingat username & password yang akan Anda daftarkan.",
        button: {
          yes: "Ya, mengerti"
        }
      });
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
