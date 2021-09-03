<template>
  <div>
    <noscript>
      <strong
        >We're sorry but this site doesn't work properly without JavaScript
        enabled. Please enable it to continue.</strong
      >
    </noscript>

    <div :class="this.$store.state.darkMode ? 'dark-mode' : 'light-mode'">
      <Navbar v-if="this.$store.state.loggedIn" :menus="menus" />
      <div class="d-flex pt-2">
        <Sidebar v-if="this.$store.state.loggedIn" :menus="menus" />
        <main class="content w-100">
          <div class="container">
            <Nuxt />
          </div>
        </main>
        <div class="side-menu-backdrop" @click="sidebarMenu"></div>
      </div>
      <vue-confirm-dialog />
    </div>
  </div>
</template>

<script>
import { mapMutations } from "vuex";
export default {
  name: "App",
  data() {
    return {
      menus: [
        {
          module_name: "Beranda",
          slug: "beranda",
          icon: "house",
          active_icon: "house-fill"
        },
        {
          module_name: "Pengguna",
          slug: "pengguna",
          icon: "people",
          active_icon: "people-fill"
        },
        {
          module_name: "Dataset",
          slug: "dataset",
          icon: "menu-button-wide",
          active_icon: "menu-button-wide-fill"
        },
        {
          module_name: "Perhitungan",
          slug: "perhitungan",
          icon: "calculator",
          active_icon: "calculator-fill"
        },
        {
          module_name: "Riwayat Pengujian",
          slug: "riwayat",
          icon: "bootstrap-reboot",
          active_icon: "bootstrap-reboot"
        }
      ]
    };
  },
  created() {
    this.getUser();
  },
  methods: {
    ...mapMutations([
      "SET_SIDEBAR",
      "SET_TOKEN_ID",
      "SET_lOGGED_IN",
      "SET_USER"
    ]),
    sidebarMenu() {
      this.SET_SIDEBAR(!this.$store.state.showSidebar);
    },
    async getUser() {
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
