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
    this.viewSeries();
  },
  methods: {
    async viewSeries() {
      this.series = [];
      const rows = this.chartSeries;
      for (let a in rows) {
        const row = rows[a];
        if (this.trainData && row.type == 1) {
          this.addSeries(this.series, row.pkt_class, [
            row.series.x,
            row.series.y
          ]);
        }
        if (this.testData && row.type == 0) {
          this.addSeries(this.series, row.pkt_class, [
            row.series.x,
            row.series.y
          ]);
        }
      }
    },
    async addSeries(arr, name, data) {
      const found = arr.some(el => el.name === name);
      if (found) {
        for (let i in arr) {
          const el = arr[i];
          if (el.name === name) {
            el.data.push(data);
            break;
          }
        }
      } else {
        arr.push({ name: name, data: [data] });
      }
    }
  },
  watch: {
    chartSeries: {
      handler: function(value) {
        this.viewSeries();
      }
    },
    trainData: {
      handler: function(value) {
        this.viewSeries();
      }
    },
    testData: {
      handler: function(value) {
        this.viewSeries();
      }
    }
  }
};
</script>
