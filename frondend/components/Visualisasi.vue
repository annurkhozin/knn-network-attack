<template>
  <b-row>
    <b-col class="col-xl-3 col-sm-6 col-12">
      <b-card :class="this.$store.state.darkMode ? 'bg-dark' : ''">
        <div class="media d-flex">
          <div class="media-body text-left">
            <h3>{{ data.total_data_latih }}</h3>
            <span class="str">Data latih</span>
          </div>
          <div class="align-self-center">
            <b-icon-menu-app
              font-scale="4"
              variant="primary"
              class="float-right"
            ></b-icon-menu-app>
          </div>
        </div>
      </b-card>
    </b-col>
    <b-col class="col-xl-3 col-sm-6 col-12">
      <b-card :class="this.$store.state.darkMode ? 'bg-dark' : ''">
        <div class="media d-flex">
          <div class="media-body text-left">
            <h3>{{ data.total_data_uji }}</h3>
            <span class="str">Data Uji</span>
          </div>
          <div class="align-self-center">
            <b-icon-hdd-network
              font-scale="4"
              variant="success"
              class="float-right"
            ></b-icon-hdd-network>
          </div>
        </div>
      </b-card>
    </b-col>
    <b-col class="col-xl-3 col-sm-6 col-12">
      <b-card :class="this.$store.state.darkMode ? 'bg-dark' : ''">
        <div class="media d-flex">
          <div class="media-body text-left">
            <h3>{{ data.nilai_k }}</h3>
            <span class="str">Nilai K</span>
          </div>
          <div class="align-self-center">
            <b-icon-bezier
              font-scale="4"
              variant="warning"
              class="float-right"
            ></b-icon-bezier>
          </div>
        </div>
      </b-card>
    </b-col>
    <b-col class="col-xl-3 col-sm-6 col-12">
      <b-card :class="this.$store.state.darkMode ? 'bg-dark' : ''">
        <div class="media d-flex">
          <div class="media-body text-left">
            <h3>{{ data.akurasi }} %</h3>
            <span class="str">Akurasi</span>
          </div>
          <div class="align-self-center">
            <b-icon-pie-chart
              font-scale="4"
              variant="danger"
              class="float-right"
            ></b-icon-pie-chart>
          </div>
        </div>
      </b-card>
    </b-col>
    <b-col class="col-12 mt-3">
      <b-card :class="this.$store.state.darkMode ? 'bg-dark' : ''">
        <b-row align-h="center">
          <b-form-checkbox v-model="trainData" class="mr-3">
            Data Latih
          </b-form-checkbox>
          <b-form-checkbox v-model="testData" class="ml-3">
            Data Uji
          </b-form-checkbox>
        </b-row>
        <VueApexCharts
          max-width="300"
          :options="chartOptions"
          :series="series"
        ></VueApexCharts>
      </b-card>
    </b-col>
  </b-row>
</template>

<script>
export default {
  props: {
    data: {
      type: Object
    },
    chartSeries: {
      type: Array
    }
  },
  data() {
    return {
      series: [],
      trainData: true,
      testData: true,
      chartOptions: {
        chart: {
          type: "scatter",
          zoom: {
            enabled: false,
            type: "xy"
          }
        },
        xaxis: {
          labels: {
            show: false
          }
        },
        yaxis: {
          labels: {
            show: false
          }
        }
      }
    };
  },
  created() {
    this.addSeries();
  },
  methods: {
    async addSeries() {
      this.series = [];
      const rows = [...this.chartSeries];
      for (let a in rows) {
        const data = [];
        const row = rows[a];
        for (let b in row.data) {
          if (this.trainData && row.type[b] == 1) {
            data.push(row.data[b]);
          }
          if (this.testData && row.type[b] == 0) {
            data.push(row.data[b]);
          }
        }
        this.series.push({ name: row.name, data: data });
      }
    }
  },
  watch: {
    chartSeries: {
      handler: function(value) {
        this.addSeries();
      }
    },
    trainData: {
      handler: function(value) {
        this.addSeries();
      }
    },
    testData: {
      handler: function(value) {
        this.addSeries();
      }
    }
  }
};
</script>
