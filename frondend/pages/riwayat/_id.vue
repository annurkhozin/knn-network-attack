<template>
  <div>
    <Breadcrumb :items="breadcrumb" />
    <b-card :class="this.$store.state.darkMode ? 'bg-dark' : ''" class="mb-3">
      <b-row align-h="center">
        <b-tooltip
          :show.sync="tooltipsShow"
          target="tooltip-steps"
          placement="left"
        >
          Klik, untuk melihat hasil dari setiap tahap.
        </b-tooltip>
        <div
          class="breadcrumbs msg-tooltip"
          data-toggle="tooltip"
          data-placement="left"
          id="tooltip-steps"
        >
          <span
            class="breadcrumb__step step-1 str "
            v-for="(step, index) in processedSteps"
            :key="index"
            role="button"
            @click="showStep(index)"
            >{{ step }}</span
          >
        </div>
      </b-row>

      <b-row align-h="center" class="mt-4" v-show="activeStep == 0">
        <b-col class="col-md-12">
          <b-tabs content-class="mt-3" card align="center">
            <b-tab title="Data Latih" active>
              <Table :items="dataset.latih" v-if="dataset.latih.length > 0" />
            </b-tab>
            <b-tab title="Data Uji">
              <Table :items="dataset.uji" v-if="dataset.uji.length > 0" />
            </b-tab>
          </b-tabs>
        </b-col>
      </b-row>
      <b-row align-h="center" class="mt-4" v-show="activeStep == 1">
        <b-col class="col-md-12">
          <b-tabs content-class="mt-3" card align="center">
            <b-tab title="Normalisasi Data Latih" active>
              <Table
                :items="dataset.normalisasi_latih"
                v-if="dataset.normalisasi_latih.length > 0"
              />
            </b-tab>
            <b-tab title="Normalisasi Data Uji">
              <Table
                :items="dataset.normalisasi_uji"
                v-if="dataset.normalisasi_uji.length > 0"
              />
            </b-tab>
          </b-tabs>
        </b-col>
      </b-row>
      <b-row align-h="center" class="mt-4" v-show="activeStep == 2">
        <b-col class="col-md-12">
          <TableK
            :items="dataset.hasil_uji"
            :k="form.nilai_k"
            v-if="dataset.hasil_uji.length > 0"
          />
        </b-col>
      </b-row>
      <b-row align-h="center" class="mt-4" v-show="activeStep == 3">
        <b-col class="col-md-12">
          <Visualisasi
            v-if="form.akurasi > 0"
            :data="form"
            :chartSeries="chartSeries"
          />
        </b-col>
      </b-row>
      <b-row class="mt-3 mb-3" v-if="isBusy">
        <b-col align-h="center" class="text-center">
          <div class="text-success my-2">
            <b-spinner class="align-middle"></b-spinner>
            <strong>Loading...</strong>
          </div>
        </b-col>
      </b-row>
    </b-card>
  </div>
</template>

<script>
export default {
  name: "DetailRiwayat",
  transition: "slide-bottom",
  mounted() {
    //KITA LAKUKAN PENGECEK, JIKA BELUM LOGIN
    if (!this.$store.state.loggedIn) {
      //MAKA REDIRECT KE HALAMAN LOGIN
      this.$router.replace("/login");
    }
  },
  data() {
    return {
      breadcrumb: [
        {
          text: "Beranda",
          to: "home"
        },
        {
          text: "Riwayat",
          to: "riwayat"
        },
        {
          text: "Detail",
          active: true
        }
      ],
      form: {
        persen_data_latih: 0,
        persen_data_uji: 0,
        nilai_k: 0,
        total_data_latih: 0,
        total_data_uji: 0,
        akurasi: 0
      },
      feature: {
        all: [],
        selected: [],
        info: []
      },
      chartSeries: [],
      tooltipsShow: true,
      tampilkanData: false,
      prosesHitung: false,
      dataset: {
        raw: [],
        latih: [],
        uji: [],
        normalisasi_latih: [],
        normalisasi_uji: [],
        hasil_uji: []
      },
      totalRows: 0,
      processedSteps: [
        "Dataset",
        "Normalisasi",
        "Klasifikasi k-NN",
        "Visualisasi"
      ],
      activeStep: 3,
      isBusy: true
    };
  },
  created() {
    this.getDataTesting();
  },
  methods: {
    async getDataTesting() {
      this.dataset.raw = [];

      const respDataset = await this.$axios
        .get(`/api/testing/_doc/${this.$route.params.id}`)
        .then(resp => {
          const respData = resp.data;
          this.form = respData._source.form;
          this.feature = JSON.parse(respData._source.feature);
          this.dataset = JSON.parse(respData._source.dataset);
          this.chartSeries = JSON.parse(respData._source.chartSeries);
          this.isBusy = false;
        })
        .catch(error => {
          this.totalRows = 0;
          this.isBusy = false;
        });
    },
    async showStep(index) {
      this.activeStep = index;
    }
  },

  head() {
    return {
      title: "Detail Riwayat Pengujian"
    };
  }
};
</script>

<style scoped>
.breadcrumbs {
  text-align: center;
  display: inline-block;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.25);
  overflow: hidden;
  border-radius: 5px;
  counter-reset: flag;
}
.breadcrumb__step {
  text-decoration: none;
  outline: none;
  display: block;
  float: left;
  font-size: 12px;
  line-height: 36px;
  padding: 0 10px 0 60px;
  position: relative;
  background: transparent;
  transition: background 0.5s;
}
.dark-mode .breadcrumb__step {
  background: white;
}
.dark-mode .breadcrumb__step {
  background: #2f495e;
}
.breadcrumb__step:first-child {
  padding-left: 46px;
  border-radius: 5px 0 0 5px;
}
.breadcrumb__step:first-child::before {
  left: 14px;
}
.breadcrumb__step:last-child {
  border-radius: 0 5px 5px 0;
  padding-right: 20px;
}
.breadcrumb__step:last-child::after {
  content: none;
}
.breadcrumb__step::before {
  content: counter(flag);
  counter-increment: flag;
  border-radius: 100%;
  width: 20px;
  height: 20px;
  line-height: 20px;
  margin: 8px 0;
  position: absolute;
  top: 0;
  left: 30px;
  font-weight: bold;
  background: #fff;
  box-shadow: 0 0 0 1px #00ab6b;
}
.light-mode .breadcrumb__step::before {
  background: #fff;
}
.dark-mode .breadcrumb__step::before {
  background: #2f495e;
}
.breadcrumb__step::after {
  content: "";
  position: absolute;
  top: 0;
  right: -18px;
  width: 36px;
  height: 36px;
  transform: scale(0.707) rotate(45deg);
  z-index: 1;
  border-radius: 0 5px 0 50px;
  transition: background 0.5s;
  box-shadow: 2px -2px 0 0 #c9b9be;
}
.light-mode .breadcrumb__step::after {
  background: #fff;
}
.dark-mode .breadcrumb__step::after {
  background: #2f495e;
}
.light-mode .breadcrumb__step--active {
  color: #fff;
  background: #00ab6b;
}
.dark-mode .breadcrumb__step--active {
  color: #fff;
  background: #00ab6b;
}
.breadcrumb__step--active::before {
  color: #00ab6b;
}
.breadcrumb__step--active::after {
  background: #00ab6b;
}
.breadcrumb__step--active > span:hover {
  color: white;
}
.breadcrumb__step:hover {
  color: black;
  text-decoration: none;
}
.breadcrumb__step--active:hover {
  color: #00ab6b;
}
.filter-field /deep/ .dropdown-menu {
  max-height: 200px;
  overflow-y: auto;
}
</style>
