<template>
  <Loading />
</template>

<script>
export default {
  name: "Index",
  auth: false,
  head() {
    return {
      title: "Beranda"
    };
  },
  mounted() {
    this.page();
  },
  methods: {
    async page() {
      setTimeout(() => {
        var token = this.$store.state.token_id;
        if (token) {
          this.$router.replace("/beranda");
        } else {
          this.$router.replace("/login");
        }
      }, 2000);
    }
  }
};
</script>
