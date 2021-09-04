<template>
  <div>
    <b-navbar
      toggleable="md"
      class="navbar-top fixed-top py-0 py-md-1 d-none d-md-block"
    >
      <b-container>
        <b-navbar-brand to="/" class="d-none d-md-block"
          ><span class="str"
            ><strong>Network Attack</strong></span
          ></b-navbar-brand
        >
        <b-collapse id="nav-collapse" is-nav class="d-none d-md-block">
          <b-navbar-nav v-if="this.$store.state.loggedIn">
            <b-nav-item class="menu" @click="sidebarMenu"
              ><b-icon-list class="icon"></b-icon-list>
              <span class="str">Menu</span>
            </b-nav-item>
            <b-nav-item-dropdown
              class="str toCapitalFirst"
              :text="this.$route.name"
            >
              <b-dropdown-item
                v-for="menu in menus"
                :key="menu._id"
                :to="{
                  path: `/${menu.slug}`
                }"
                class="toCapitalFirst"
              >
                <b-icon :icon="menu.icon" scale="0.8"></b-icon>
                {{ menu.slug }}</b-dropdown-item
              >
            </b-nav-item-dropdown>
          </b-navbar-nav>
          <b-navbar-nav class="ml-auto">
            <b-nav-item-dropdown
              v-if="this.$store.state.loggedIn"
              right
              no-caret
            >
              <template #button-content>
                <div class="d-flex">
                  <div
                    class="avatar gd-success"
                    style="width: 24px; height: 24px; font-size: 16px"
                  >
                    <span
                      v-if="
                        !$store.state.user.photo && $store.state.user.fullname
                      "
                      style="color: #fff"
                    >
                      {{
                        $store.state.user.fullname.substring(0, 1).toUpperCase()
                      }}
                    </span>
                    <img
                      v-if="$store.state.user.photo"
                      :src="$store.state.user.photo"
                      :alt="$store.state.user.fullname"
                      class="rounded-circle mx-2 flex-shrink-0"
                      style="width: 32px; height: 32px"
                    />
                  </div>
                  <div class="str align-self-center">
                    &nbsp;&nbsp;{{ $store.state.user.fullname }}
                  </div>
                </div>
              </template>

              <b-dropdown-item @click="updateProfile"
                ><b-icon-person scale="0.8"></b-icon-person>
                Profile</b-dropdown-item
              >
              <b-dropdown-divider></b-dropdown-divider>
              <b-dropdown-item @click="logout"
                ><b-icon-power scale="0.8"></b-icon-power>
                Logout</b-dropdown-item
              >
            </b-nav-item-dropdown>
          </b-navbar-nav>
        </b-collapse>
      </b-container>
    </b-navbar>
    <b-navbar
      :class="showNavbar ? 'scrolled-down' : 'scrolled-up'"
      class="
        fixed-bottom
        shadow
        py-1 py-md-1
        d-block d-md-none d-lg-none d-xl-none
        navbar-bottom
      "
    >
      <b-navbar-nav class="nav-justified">
        <b-nav-item to="home">
          <b-icon-house class="white"></b-icon-house>
        </b-nav-item>
        <b-nav-item
          ><b-icon-grid class="white" @click="sidebarMenu"></b-icon-grid>
        </b-nav-item>

        <b-nav-item-dropdown
          v-if="this.$store.state.loggedIn"
          right
          dropup
          no-caret
          variant="link"
        >
          <template #button-content>
            <b-icon-three-dots-vertical
              class="white"
            ></b-icon-three-dots-vertical>
          </template>

          <b-dropdown-item to="profile"
            ><b-icon-person scale="0.8"></b-icon-person>
            Profile</b-dropdown-item
          >
          <b-dropdown-divider></b-dropdown-divider>
          <b-dropdown-item @click="logout"
            ><b-icon-power scale="0.8"></b-icon-power> Logout</b-dropdown-item
          >
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-navbar>
    <b-modal
      id="modal-prevent-closing"
      ref="modal"
      size="sm"
      title="Data Pengguna"
      @hidden="resetModal"
      @ok="handleOk"
    >
      <form ref="form" @submit.stop.prevent="handleSubmit">
        <b-alert :show="error === '' ? false : true" variant="danger" fade>{{
          error
        }}</b-alert>
        <b-input-group class="mb-4" size="sm">
          <b-input-group-append is-text>
            <b-icon-person class="icon"></b-icon-person>
          </b-input-group-append>
          <b-form-input
            ref="fullname"
            v-model="form.fullname"
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
            v-model="form.username"
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
            v-model="form.password"
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
      </form>
    </b-modal>
  </div>
</template>

<script>
import { mapMutations } from "vuex";
const OFFSET = 5;

export default {
  name: "Navbar",
  props: {
    menus: Array
  },
  data() {
    return {
      showNavbar: true,
      lastScrollPosition: 0,
      scrollValue: 0,
      form: {},
      error: "",
      showPassword: false,
      passwordFieldType: "password"
    };
  },

  mounted() {
    this.lastScrollPosition = window.pageYOffset;
    window.addEventListener("scroll", this.onScroll);
    const viewportMeta = document.createElement("meta");
    viewportMeta.name = "viewport";
    viewportMeta.content = "width=device-width, initial-scale=1";
    document.head.appendChild(viewportMeta);
  },

  beforeDestroy() {
    window.removeEventListener("scroll", this.onScroll);
  },

  methods: {
    ...mapMutations([
      "SET_SIDEBAR",
      "SET_TOKEN_ID",
      "SET_lOGGED_IN",
      "SET_USER"
    ]),
    async logout() {
      await this.$confirm({
        title: "⚠ Keluar Akun!",
        message: "Yakin, ingin keluar dari akun Anda",
        button: {
          no: "Tidak",
          yes: "Ya, Keluar"
        },
        callback: confirm => {
          if (confirm) {
            this.SET_lOGGED_IN(false);
            this.SET_TOKEN_ID(null);
            this.SET_USER({});
            this.$router.push("login");
          }
        }
      });
    },
    sidebarMenu() {
      this.SET_SIDEBAR(!this.$store.state.showSidebar);
    },
    onScroll() {
      if (window.pageYOffset < 0) {
        return;
      }
      if (Math.abs(window.pageYOffset - this.lastScrollPosition) < OFFSET) {
        return;
      }
      this.showNavbar = window.pageYOffset < this.lastScrollPosition;
      this.lastScrollPosition = window.pageYOffset;
    },
    async updateProfile() {
      this.form = {
        _id: this.$store.state.token_id,
        fullname: this.$store.state.user.fullname,
        username: this.$store.state.user.username
      };
      this.$bvModal.show("modal-prevent-closing");
    },
    resetModal() {
      this.form = {};
      this.error = "";
    },
    handleOk(bvModalEvt) {
      bvModalEvt.preventDefault();
      this.handleSubmit();
    },
    async handleSubmit() {
      if (!this.form.fullname) {
        this.$refs.fullname.$el.focus();
        this.error = "Nama lengkap wajid diisi";
      } else if (!this.form.username) {
        this.$refs.username.$el.focus();
        this.error = "Username wajid diisi";
      } else if (!this.form.password && !this.form._id) {
        this.$refs.password.$el.focus();
        this.error = "Password wajid diisi";
      } else if (!this.form.photo && !this.form._id) {
        this.$refs.photo.$el.focus();
        this.error = "Photo wajid diisi";
      } else {
        this.isBusySubmit = true;
        const data = {
          fullname: this.form.fullname,
          username: this.form.username
        };
        if (this.form.password) {
          data.password = md5(this.form.password);
        }
        if (this.form.photo) {
          data.photo = this.form.photo;
        }
        const headers = {
          "Content-Type": "application/json"
        };
        const _id = this.form._id;
        if (_id) {
          const doc = {
            doc: data
          };
          await this.$axios
            .post(`/api/users/_update/${_id}`, doc, {
              headers: headers
            })
            .then(resp => {
              this.isBusySubmit = false;
              this.$confirm({
                title: "⚠ Success",
                message: "Pengguna berhasil diperbarui",
                button: {
                  yes: "Ok"
                },
                callback: confirm => {
                  this.$bvModal.hide("modal-prevent-closing");
                  this.getProfile();
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
      }
    },
    base64File: function() {
      const file = document.querySelector("input[type=file]").files[0];
      const reader = new FileReader();

      reader.onloadend = () => {
        this.form.photo = reader.result;
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
    async getProfile() {
      var token = this.$store.state.token_id;
      if (token) {
        await this.$axios
          .get(`/api/users/_doc/${token}`)
          .then(resp => {
            const found = resp.data.found;
            this.busy = false;
            if (found) {
              this.SET_lOGGED_IN(true);
              this.SET_TOKEN_ID(resp.data._id);
              this.SET_USER(resp.data._source);
            } else {
              this.SET_TOKEN_ID(null);
            }
          })
          .catch(error => {
            this.SET_lOGGED_IN(false);
            this.SET_TOKEN_ID(null);
          });
      }
    }
  }
};
</script>

<style scoped>
.toCapitalFirst {
  text-transform: capitalize;
}
.navbar {
  z-index: 1030;
}
.dark-mode .navbar {
  background-color: #375268;
}
.light-mode .navbar {
  background-color: white;
  border-bottom: 1px solid #eee;
}
.navbar-bottom {
  margin-bottom: 10px;
  margin-left: 20%;
  margin-right: 20%;
  border-radius: 50px;
  font-size: 1rem;
}
.light-mode .navbar-bottom,
.light-mode .navbar-bottom::before {
  background: linear-gradient(to right, #50c088 0%, #51c48a 80%, #4eb883 100%);
}
.dark-mode .navbar-bottom,
.dark-mode .navbar-bottom::before {
  background: linear-gradient(to right, #328059 0%, #30845a 80%, #369465 100%);
}

.navbar-bottom:before {
  content: "";
  display: inline-block;
  height: 40px;
  position: absolute;
  bottom: -3px;
  left: 10%;
  right: 10%;
  z-index: -1;
  border-radius: 50px;
  filter: blur(10px) brightness(0.95);
  transform-style: preserve-3d;
  transition: all 0.3s ease-out;
}

.scrolled-down {
  transform: translateY(0);
  transition: all 0.7s ease-in-out;
}
.scrolled-up {
  margin-bottom: -10px;
  transform: translateY(100%);
  transition: all 0.7s ease-in-out;
}

span.notification-badge {
  position: relative;
  top: -10px;
  right: 13px;
  border-radius: 50%;
}

.navbar-bottom .navbar-nav .nuxt-link-exact-active:hover,
.navbar-bottom .navbar-nav .nuxt-link-exact-active:focus {
  color: white;
}
</style>
