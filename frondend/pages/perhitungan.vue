<template>
  <div>
    <Breadcrumb :items="breadcrumb" />
    <b-card :class="this.$store.state.darkMode ? 'bg-dark' : ''" class="mb-3">
      <b-row align-h="center">
        <b-col class="col-md-4 col-sm-8">
          <b-form-group class="str text-center" label="Perbandingan Dataset">
            <b-row>
              <b-col class="col-md-6">
                <b-input-group class="mb-2" size="sm">
                  <b-input-group-append is-text>
                    <span class="str">Latih</span>
                  </b-input-group-append>
                  <b-form-input
                    ref="data_latih"
                    type="number"
                    v-model="form.persen_data_latih"
                    :max="99"
                    placeholder="Data Latih"
                  ></b-form-input>
                  <span class="input-group-append">
                    <div class="input-group-text bg-transparent str">
                      %
                    </div>
                  </span>
                </b-input-group>
              </b-col>
              <b-col class="col-md-6">
                <b-input-group class="mb-2" size="sm">
                  <b-input-group-append is-text class="str">
                    <span class="str">Uji</span>
                  </b-input-group-append>
                  <b-form-input
                    ref="data_uji"
                    type="number"
                    v-model="form.persen_data_uji"
                    disabled
                    placeholder="Data Uji"
                  ></b-form-input>
                  <span class="input-group-append">
                    <div class="input-group-text bg-transparent str">
                      %
                    </div>
                  </span>
                </b-input-group>
              </b-col>
            </b-row>
          </b-form-group>
          <b-form-group>
            <b-row>
              <b-col class="col-md-6">
                <b-input-group size="sm">
                  <b-input-group-append is-text class="str">
                    <span class="str">Nilai K</span>
                  </b-input-group-append>
                  <b-form-select
                    v-model="form.nilai_k"
                    :options="[3, 5, 7, 9]"
                  ></b-form-select>
                </b-input-group>
              </b-col>
              <b-col class="col-md-6">
                <b-dropdown
                  text="Seleksi fitur"
                  block
                  :variant="
                    this.$store.state.darkMode
                      ? 'secondary'
                      : 'outline-secondary'
                  "
                  size="sm"
                  class="filter-field"
                  menu-class="w-100"
                >
                  <b-form-checkbox-group
                    v-model="feature.selected"
                    :options="feature.all"
                    role="button"
                    class="ml-2 mr-2 str"
                  ></b-form-checkbox-group>
                </b-dropdown>
              </b-col>
            </b-row>
          </b-form-group>
          <div class="text-center mt-4">
            <b-overlay
              :show="prosesHitung"
              rounded
              opacity="0.6"
              spinner-small
              spinner-variant="primary"
              block
            >
              <b-button
                variant="success"
                block
                @click="mulaiHitung"
                :disabled="prosesHitung"
                >Mulai Perhitungan k-NN</b-button
              >
              <b-button
                variant="primary"
                block
                v-show="stepStatus.every(v => v === true)"
                @click="simpanPengujian"
                :disabled="prosesHitung"
                >Simpan Pengujian</b-button
              >
            </b-overlay>
          </div>
        </b-col>
      </b-row></b-card
    >
    <b-card
      :class="this.$store.state.darkMode ? 'bg-dark' : ''"
      class="mb-3"
      v-if="tampilkanData"
    >
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
          <span
            class="breadcrumb__step str breadcrumb__step--active"
            role="button"
            v-if="!stepStatus.every(v => v === true)"
            @click="showStep(activeStep)"
            ><div class="spinner-border spinner-border-sm" role="status">
              <span class="sr-only">Loading...</span>
            </div>
            <span>{{ processName }}</span></span
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
    </b-card>
  </div>
</template>

<script>
import trainTestSplit from "train-test-split";
export default {
  name: "Training",
  head() {
    return {
      title: "Training Dataset"
    };
  },
  data() {
    return {
      breadcrumb: [
        {
          text: "Beranda",
          to: "home"
        },
        {
          text: "Training",
          active: true
        }
      ],
      form: {
        persen_data_latih: 90,
        persen_data_uji: 10,
        nilai_k: 3,
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
      steps: ["Dataset", "Normalisasi", "Klasifikasi k-NN", "Visualisasi"],
      stepStatus: [false, false, false, false],
      processedSteps: [],
      processName: null,
      activeStep: 0
    };
  },
  mounted() {
    //KITA LAKUKAN PENGECEKAN, JIKA BELUM LOGIN
    if (!this.$store.state.loggedIn) {
      //MAKA REDIRECT KE HALAMAN LOGIN
      this.$router.replace("login");
    }
  },
  created() {
    this.getMapping();
  },
  methods: {
    async getMapping() {
      var mapping = await this.$axios
        .get("/api/dataset/_mapping")
        .then(resp => {
          return resp.data.dataset.mappings.properties;
        });
      this.feature.all = [];
      var mapping = mapping ? Object.keys(mapping) : [];
      mapping.forEach(key => {
        if (key == "PKT_CLASS") {
          this.feature.all.push({ text: key, value: key, disabled: true });
        } else {
          this.feature.all.push(key);
        }
        this.feature.selected.push(key);
      });
    },
    async processedStep() {
      this.processedSteps = this.steps.filter((key, index) => {
        return this.stepStatus[index] ? key : null;
      });
    },
    async mulaiHitung() {
      this.stepStatus = [false, false, false, false];
      this.processedSteps = [];
      this.tampilkanData = true;
      this.prosesHitung = true;
      this.processName = "Memuat Dataset";
      this.activeStep = 0;
      this.getDataset();
    },
    async getDataset() {
      this.dataset.raw = [];
      const data = {
        from: 0,
        size: 5000,
        query: {
          match_all: {}
        }
      };

      const respDataset = await this.$axios
        .post("/api/dataset/_search", data)
        .then(resp => {
          const respData = resp.data;
          const respHits = respData.hits.hits;
          respHits.forEach(key => {
            const data = key._source;
            this.dataset.raw.push(data);
          });
          this.totalRows = respData.hits.total.value;
          return this.dataset.raw;
        })
        .catch(error => {
          this.totalRows = 0;
        });
      setTimeout(() => {
        this.splitDataset(respDataset, this.form.persen_data_latih);
      }, 100);
    },

    async splitDataset(dataset, persen_data_latih) {
      this.processName = "Membagi data Latih dan data Uji";

      // fungsi untuk mengambil acak index dataset (dimulai dari 0, sampai banyak dataset)
      function randomIndex(min, max) {
        var random = Math.floor(Math.random() * (max - min) + min);
        return random;
      }

      const l = new Set(this.feature.selected);

      for (let obj of dataset) {
        for (let prop of Object.keys(obj)) {
          if (!l.has(prop)) {
            delete obj[prop];
          }
        }
      }

      // // kumpulkan berdasarkan jenis kelas
      var groupBy = function(rows, key) {
        return rows.reduce(function(rv, x) {
          (rv[x[key]] = rv[x[key]] || []).push(x);
          return rv;
        }, {});
      };
      const groupByClass = groupBy(dataset, "PKT_CLASS");
      var data_latih = [];
      var data_uji = [];
      for (var key in groupByClass) {
        const [train, test] = await trainTestSplit(
          groupByClass[key],
          persen_data_latih / 100
        );
        data_latih = data_latih.concat(train);
        data_uji = data_uji.concat(test);
      }

      // acak kembali dataset / agar dataset setiap kelas tersebar
      this.dataset.latih = [];
      var indexArray = [];
      for (let i = 0; i < data_latih.length; i++) {
        var loop = true;
        while (loop) {
          var index = randomIndex(0, data_latih.length);
          if (!indexArray.includes(index)) {
            indexArray.push(index);
            this.dataset.latih.push(data_latih[index]);
            loop = false;
          }
        }
      }
      this.dataset.uji = [];
      var indexArray = [];
      for (let i = 0; i < data_uji.length; i++) {
        var loop = true;
        while (loop) {
          var index = randomIndex(0, data_uji.length);
          if (!indexArray.includes(index)) {
            indexArray.push(index);
            this.dataset.uji.push(data_uji[index]);
            loop = false;
          }
        }
      }

      this.stepStatus[0] = true;
      this.processedStep();

      this.processName = "Normalisasi Dataset";
      this.activeStep = 1;
      setTimeout(() => {
        this.normalisasiData();
      }, 100);
    },

    async normalisasiData() {
      this.chartSeries = [];
      // get koleksi data, min & max
      this.feature.info = await this.infoDataset(
        this.dataset.latih,
        this.feature.selected
      );
      // scale & normalisasi dataset berdasarkan info data
      this.dataset.normalisasi_latih = await this.prosesNormalisasi(
        this.dataset.latih,
        this.feature.selected,
        1
      );
      this.dataset.normalisasi_uji = await this.prosesNormalisasi(
        this.dataset.uji,
        this.feature.selected,
        0
      );
      this.stepStatus[1] = true;
      this.processedStep();
      this.processName = "Klasifikasi k-NN";
      this.activeStep = 2;
      setTimeout(() => {
        this.klasifikasikNN();
      }, 100);
    },

    async infoDataset(dataset, dataKeys) {
      const datasetInfo = [];
      for (let i in dataKeys) {
        const dataKey = dataKeys[i];

        var info = await dataset.map(key => {
          return key[dataKey];
        });
        if (isNaN(info[0])) {
          const type = "string";
          const options = new Set(info);
          let len = [...options].length;
          const min = 0;
          const max = len > 1 ? len - 1 : len;
          datasetInfo.push({
            key: dataKey,
            type: type,
            min: min,
            max: max,
            options: [...options]
          });
        } else {
          const type = "number";
          const min = Math.min(...info);
          const max = Math.max(...info);
          datasetInfo.push({ key: dataKey, type: type, min: min, max: max });
        }
      }
      return datasetInfo;
    },

    async prosesNormalisasi(dataset, keys, type) {
      const datasetRows = [];
      for (let i in dataset) {
        const row = dataset[i];
        const datasetRow = {};
        var datasetRowTest = [0, 0];
        for (let key in row) {
          if (keys.includes(key)) {
            const getIndexKey = keys.indexOf(key);
            const koleksiData = this.feature.info[getIndexKey];
            let v = row[key];
            let min = koleksiData.min;
            let max = koleksiData.max;
            let new_min = 0;
            let new_max = 1;
            if (koleksiData.type == "string") {
              v = koleksiData.options.indexOf(v);
              if (key == "PKT_CLASS") {
                datasetRow[key] = v;
                break;
              }
            }
            v = ((v - min) / (max - min)) * (new_max - new_min) + new_min;
            datasetRow[key] = v;
            if (getIndexKey % 2 !== 0) {
              datasetRowTest[0] += datasetRowTest[0] + v;
            } else {
              datasetRowTest[1] += datasetRowTest[1] + v;
            }
          }
        }
        datasetRowTest[0] = datasetRowTest[0];
        datasetRowTest[1] = datasetRowTest[1];

        this.addSeries(this.chartSeries, row.PKT_CLASS, datasetRowTest, type);
        datasetRows.push(datasetRow);
      }

      return datasetRows;
    },

    async addSeries(arr, name, data, type) {
      const found = arr.some(el => el.name === name);
      if (found) {
        for (let i in arr) {
          const el = arr[i];
          if (el.name === name) {
            el.data.push(data);
            el.type.push(type);
            break;
          }
        }
      } else {
        arr.push({ name: name, data: [data], type: [type] });
      }
      return arr;
    },

    async klasifikasikNN() {
      var daftar_kelas = [];
      const koleksiData = this.feature.info;
      for (let i in koleksiData) {
        const row = koleksiData[i];
        if (row.key == "PKT_CLASS") {
          daftar_kelas = row.options;
        }
      }

      const hasil_uji = [];
      const data_uji = this.dataset.normalisasi_uji;
      let prediksi_benar = 0;
      for (let i in data_uji) {
        const row_data_uji = data_uji[i];
        const predict = await this.hitungJarakKNN(
          daftar_kelas,
          this.feature.selected,
          this.dataset.normalisasi_latih,
          row_data_uji,
          this.form.nilai_k
        );

        const data = {
          actual: daftar_kelas[row_data_uji.PKT_CLASS]
        };

        const orderKelas = [];
        const countKelas = [];
        var maks = 0;
        for (let i in daftar_kelas) {
          const count = (arr, val) =>
            arr.reduce((a, v) => (v.kelas === val ? a + 1 : a), 0);
          const getCount = count(predict, daftar_kelas[i]);
          if (maks <= getCount) {
            orderKelas.push(daftar_kelas[i]);
            countKelas.push(countKelas);
            if (maks < getCount) {
              orderKelas = [daftar_kelas[i]];
              countKelas = [countKelas];
            }

            maks = getCount;
          }
        }

        if (orderKelas.length == 1) {
          data["predict"] = orderKelas[0];
        } else {
          let avg = 0;
          for (let a in orderKelas) {
            const sumData = (arr, val) =>
              arr.reduce((a, v) => (v.kelas === val ? a + v.jarak : a), 0);
            const getAvg = sumData(predict, orderKelas[a]);
            if (avg < getAvg) {
              data["predict"] = orderKelas[a];
              avg = getAvg;
            }
          }
        }
        for (let i in predict) {
          let k = 1 + parseInt(i);
          data[`k-${k}`] = predict[i].kelas;
          data[`jarak_k-${k}`] = predict[i].jarak;
        }
        if (data["actual"] == data["predict"]) {
          prediksi_benar += 1;
        }
        // console.log(data);
        hasil_uji.push(data);
      }
      let akurasi = (prediksi_benar / data_uji.length) * 100;
      this.form.akurasi = Math.round(akurasi * 100) / 100;
      this.stepStatus[2] = true;
      this.processedStep();

      this.processName = "Visualisasi data";
      this.activeStep = 3;
      this.dataset.hasil_uji = hasil_uji;
      setTimeout(() => {
        this.visualisasi();
      }, 100);
    },

    async hitungJarakKNN(daftar_kelas, fitur, data_latih, uji, nilai_k) {
      const jarak = [];
      for (let a in data_latih) {
        const row = data_latih[a];
        let jarak_i = 0;
        for (let b in row) {
          if (fitur.includes(b) && b != "PKT_CLASS") {
            let kuadrat = Math.pow(row[b] - uji[b], 2);
            jarak_i += kuadrat;
          }
        }
        jarak_i = Math.sqrt(jarak_i);
        jarak.push(jarak_i);
      }
      var urutan = [...jarak];
      urutan = urutan.sort((a, b) => {
        return a - b;
      });

      const jarak_terdekat = [];
      const jarak_k = urutan.slice(0, nilai_k);

      for (let k in jarak_k) {
        let getIndexK = jarak.indexOf(jarak_k[k]);
        let nomor_kelas = data_latih[getIndexK].PKT_CLASS;
        let label_kelas = daftar_kelas[nomor_kelas];
        const data = {
          index: getIndexK,
          nomor_kelas: nomor_kelas,
          kelas: label_kelas,
          jarak: jarak_k[k]
        };
        jarak_terdekat.push(data);
      }
      return jarak_terdekat;
    },

    async visualisasi() {
      this.form.total_data_latih = this.dataset.latih.length;
      this.form.total_data_uji = this.dataset.uji.length;
      this.stepStatus[3] = true;
      this.processedStep();
      this.activeStep = 3;
      this.prosesHitung = false;
    },

    async showStep(index) {
      this.activeStep = index;
    },

    async simpanPengujian() {
      await this.$confirm({
        title: "⚠ Simpan Hasil Pengujian",
        message: "Pengujian akan disimpan",
        button: {
          no: "Tidak",
          yes: "Ya, Simpan"
        },
        callback: async confirm => {
          if (confirm) {
            this.isBusySubmit = true;
            this.isBusy = true;
            const data = [
              {
                form: this.form,
                chartSeries: JSON.stringify(this.chartSeries),
                dataset: JSON.stringify(this.dataset),
                feature: JSON.stringify(this.feature),
                created_at: new Date()
              }
            ];

            const json_data = data.flatMap(doc => [
              { index: { _index: "testing" } },
              doc
            ]);
            var bulk_data = Object.keys(json_data)
              .map(function(k) {
                return JSON.stringify(json_data[k]);
              })
              .join("\n");

            await this.$axios
              .post(`/api/_bulk`, `${bulk_data}\n`, {
                headers: {
                  "Content-type": "application/json"
                }
              })
              .then(() => {
                this.$confirm({
                  title: "🥳 Sukses",
                  message: "Pengujian berhasil disimpan",
                  button: {
                    yes: "Ok"
                  }
                });
                this.stepStatus = [false, false, false, false];
                this.processedSteps = [];
                this.tampilkanData = false;
                this.prosesHitung = false;
              });

            // const id = new Date().getTime();
            // var data = {
            //   doc: {
            //     form: this.form,
            //     created_at: new Date()
            //   }
            // };
            // await this.$axios.post(`/api/testing/_doc/${id}`, data, {
            //   headers: {
            //     "Content-type": "application/json"
            //   }
            // });
            // data = {
            //   doc: {
            //     feature: JSON.stringify(this.feature)
            //   }
            // };
            // await this.$axios.post(`/api/testing/_update/${id}`, data, {
            //   headers: {
            //     "Content-type": "application/json"
            //   }
            // });
            // data = {
            //   doc: {
            //     dataset: JSON.stringify(this.dataset.raw)
            //   }
            // };
            // await this.$axios.post(`/api/testing/_update/${id}`, data, {
            //   headers: {
            //     "Content-type": "application/json"
            //   }
            // });
            // data = {
            //   doc: {
            //     dataset: {
            //       latih: JSON.stringify(this.dataset.latih)
            //     }
            //   }
            // };
            // console.log(data);
            // await this.$axios.post(`/api/testing/_update/${id}`, data);
            // data = {
            //   doc: {
            //     dataset: {
            //       uji: JSON.stringify(this.dataset.uji)
            //     }
            //   }
            // };
            // console.log(data);
            // await this.$axios.post(`/api/testing/_update/${id}`, data);
            // await this.$confirm({
            //   title: "🥳 Sukses",
            //   message: "Pengujian berhasil disimpan",
            //   button: {
            //     yes: "Ok"
            //   }
            // });
            // this.stepStatus = [false, false, false, false];
            // this.processedSteps = [];
            // this.tampilkanData = false;
            // this.prosesHitung = false;
          }
        }
      });
    }
  },
  watch: {
    "form.persen_data_latih"(value) {
      this.form.persen_data_uji = 100 - value;
    }
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
