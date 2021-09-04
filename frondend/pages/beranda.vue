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
    <b-row>
      <b-col class="col-xl-3 col-sm-6 col-12">
        <b-card :class="this.$store.state.darkMode ? 'bg-dark' : ''">
          <div class="media d-flex">
            <div class="media-body text-left">
              <h3>{{ total_pengguna }}</h3>
              <b-link to="/pengguna" class="card-link str">Pengguna</b-link>
            </div>
            <div class="align-self-center">
              <b-icon-people
                font-scale="4"
                variant="primary"
                class="float-right"
              ></b-icon-people>
            </div>
          </div>
        </b-card>
      </b-col>
      <b-col class="col-xl-3 col-sm-6 col-12">
        <b-card :class="this.$store.state.darkMode ? 'bg-dark' : ''">
          <div class="media d-flex">
            <div class="media-body text-left">
              <h3>{{ total_dataset }}</h3>
              <b-link to="/dataset" class="card-link str">Dataset</b-link>
            </div>
            <div class="align-self-center">
              <b-icon-menu-button-wide
                font-scale="4"
                variant="success"
                class="float-right"
              ></b-icon-menu-button-wide>
            </div>
          </div>
        </b-card>
      </b-col>
      <b-col class="col-xl-3 col-sm-6 col-12">
        <b-card :class="this.$store.state.darkMode ? 'bg-dark' : ''">
          <div class="media d-flex">
            <div class="media-body text-left">
              <h3>{{ total_pengujian }}</h3>
              <b-link to="/pengujian" class="card-link str">Pengujian</b-link>
            </div>
            <div class="align-self-center">
              <b-icon-calculator
                font-scale="4"
                variant="warning"
                class="float-right"
              ></b-icon-calculator>
            </div>
          </div>
        </b-card>
      </b-col>
      <b-col class="col-xl-3 col-sm-6 col-12">
        <b-card :class="this.$store.state.darkMode ? 'bg-dark' : ''">
          <div class="media d-flex">
            <div class="media-body text-left">
              <h3>{{ pengujian_tertinggi }} %</h3>
              <b-link
                :to="
                  pengujian_tertinggi > 0
                    ? `/riwayat/${id_pengujian_tertinggi}`
                    : '#'
                "
                class="card-link str"
                >Pengujian Tertinggi</b-link
              >
            </div>
            <div class="align-self-center">
              <b-icon-bezier
                font-scale="4"
                variant="danger"
                class="float-right"
              ></b-icon-bezier>
            </div>
          </div>
        </b-card>
      </b-col>
    </b-row>
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
      ],
      total_pengguna: 0,
      total_dataset: 0,
      total_pengujian: 0,
      pengujian_tertinggi: 0,
      id_pengujian_tertinggi: ""
    };
  },

  created() {
    this.getData();
  },
  methods: {
    async getData() {
      this.total_pengguna = await this.$axios
        .get(`/api/users/_count`)
        .then(resp => {
          return resp.data.count;
        });

      this.total_dataset = await this.$axios
        .get(`/api/dataset/_count`)
        .then(resp => {
          return resp.data.count;
        });

      this.total_pengujian = await this.$axios
        .get(`/api/testing/_count`)
        .then(resp => {
          return resp.data.count;
        });

      const data = {
        size: 1,
        _source: ["form"],
        sort: [
          {
            "form.akurasi": {
              order: "desc"
            }
          }
        ],
        aggs: {
          akurasi_tertinggi: { max: { field: "form.akurasi" } }
        }
      };
      await this.$axios.post("/api/testing/_search", data).then(resp => {
        const respData = resp.data.hits.hits;
        return respData.map(key => {
          this.pengujian_tertinggi = key._source.form.akurasi;
          this.id_pengujian_tertinggi = key._id;
          return key._id;
        });
      });
    }
  },

  head() {
    return {
      title: "Beranda"
    };
  }
};
</script>

<style></style>
