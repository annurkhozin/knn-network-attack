<template>
  <div>
    <Breadcrumb :items="breadcrumb" />
    <b-alert
      show
      variant="success"
      dismissible
      fade
      @dismissed="showDismissibleAlert = false"
      >Halo <strong>{{ this.$store.state.user.fullname }}</strong
      >. Selamat datang kembali 👋.
    </b-alert>
  </div>
</template>

<script>
export default {
  name: "Home",
  transition: "slide-bottom",
  mounted() {
    //KITA LAKUKAN PENGECEK, JIKA BELUM LOGIN
    if (!this.$store.state.loggedIn) {
      //MAKA REDIRECT KE HALAMAN LOGIN
      this.$router.replace("login");
    }
  },
  data() {
    return {
      breadcrumb: [
        {
          text: "Beranda",
          active: true
        }
      ]
    };
  },

  head() {
    return {
      title: "Beranda"
    };
  }
};
</script>

<style></style>
