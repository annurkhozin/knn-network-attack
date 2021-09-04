<template>
  <div>
    <Breadcrumb :items="breadcrumb" />
    <b-card :class="this.$store.state.darkMode ? 'bg-dark' : ''" class="mb-3">
      <b-row align-h="center">
        <b-col class="col-md-4 col-sm-8">
          <b-input-group size="sm">
            <b-input-group-append is-text>
              <b-icon-diagram3 class="icon"></b-icon-diagram3>
            </b-input-group-append>
            <b-form-file
              ref="dataset-file"
              size="sm"
              accept=".csv"
              :disabled="isBusySubmit"
              @change="selectFile"
              placeholder="Pilih dataset (csv)"
              style="border-left: 0"
              required
            ></b-form-file>
          </b-input-group>
          <b-form-checkbox class="str mt-2" v-model="hapusDataset"
            >Hapus dataset lama</b-form-checkbox
          >
        </b-col>
        <b-col class="col-auto">
          <b-overlay
            :show="isBusySubmit"
            rounded
            opacity="0.6"
            spinner-small
            spinner-variant="primary"
            class="d-inline-block"
          >
            <b-button
              variant="success shadow"
              size="sm"
              :disabled="isBusySubmit"
              @click="uploadData"
              ><b-icon-file-earmark-arrow-up
                scale="1.3"
              ></b-icon-file-earmark-arrow-up>
              &nbsp;Unggah {{ proses > 0 ? `(${proses}) data` : "" }}</b-button
            >
          </b-overlay>
        </b-col>
      </b-row>
    </b-card>
    <b-card :class="this.$store.state.darkMode ? 'bg-dark' : ''">
      <b-row>
        <b-col align-self="start">
          <label class="mr-sm-2 str" for="inline-form-custom-select-pref"
            >Tampilkan&nbsp;
          </label>
          <b-form-select
            id="inline-form-custom-select-pref"
            v-model="perPage"
            size="sm"
            class="mr-sm-2 mb-sm-0 col-5 col-sm-6 col-md-3"
            :options="[10, 50, 100, 500]"
          ></b-form-select>
          <b-dropdown
            text="Kolom"
            size="sm"
            :variant="
              this.$store.state.darkMode ? 'secondary' : 'outline-secondary'
            "
            class="col-2 pl-0 pr-0 str filter-field"
          >
            <b-form-checkbox-group
              v-model="selectedField"
              :options="allFields"
              class="ml-2 mr-2 str"
            ></b-form-checkbox-group>
            <b-dropdown-divider></b-dropdown-divider>
          </b-dropdown>
        </b-col>
        <b-col class="d-flex justify-content-end">
          <b-input-group size="sm" class="col-12 col-md-8">
            <b-form-input
              v-model="searchData"
              placeholder="Cari berdasarkan kelas..."
              @input="getDataset"
            ></b-form-input>
            <span class="input-group-append">
              <div
                class="input-group-text bg-transparent"
                type="button"
                @click="getDataset"
              >
                <b-icon-arrow-repeat class="icon"></b-icon-arrow-repeat>
              </div>
            </span>
          </b-input-group>
        </b-col>
      </b-row>
      <b-row class="mt-3 list-row block">
        <b-col>
          <b-table
            responsive
            hover
            outlined
            small
            :dark="this.$store.state.darkMode"
            :items="datasetRows"
            :fields="fields"
            :busy="isBusy"
          >
            <template #table-busy>
              <div class="text-center text-success my-2">
                <b-spinner class="align-middle"></b-spinner>
                <strong>Loading...</strong>
              </div>
            </template>
            <template #cell(index)="data">
              {{
                numberWithSeparator(data.index + 1 + (pagination - 1) * perPage)
              }}
            </template>
            <template #cell(actions)="row">
              <b-button size="sm" @click="row.toggleDetails" variant="warning">
                <div class="d-none d-md-block">
                  {{ row.detailsShowing ? "Hide" : "Show" }}
                  <b-icon-chevron-down></b-icon-chevron-down>
                </div>
                <b-icon-chevron-down
                  class="d-block d-md-none"
                ></b-icon-chevron-down>
              </b-button>
            </template>
            <template #row-details="row">
              <b-row align-h="center">
                <table>
                  <tr v-for="(value, key) in row.item" :key="key">
                    <td>{{ key }}</td>
                    <td>{{ value }}</td>
                  </tr>
                </table>
              </b-row>
            </template>
          </b-table></b-col
        ></b-row
      >
      <b-row>
        <b-col align-self="start">
          <label
            class="mr-sm-2 d-none d-md-block str"
            for="inline-form-custom-select-pref"
            >Ditampilkan
            {{
              numberWithSeparator(
                (pagination - 1) * perPage + (datasetRows.length > 0 ? 1 : 0)
              )
            }}
            sampai
            {{
              numberWithSeparator(
                (pagination - 1) * perPage + datasetRows.length
              )
            }}
            dari {{ numberWithSeparator(totalRows) }} data
          </label>
          <label
            class="mr-sm-2 d-block d-md-none str"
            for="inline-form-custom-select-pref"
            >Data
            {{
              numberWithSeparator(
                (pagination - 1) * perPage + (datasetRows.length > 0 ? 1 : 0)
              )
            }}
            sampai
            {{
              numberWithSeparator(
                (pagination - 1) * perPage + datasetRows.length
              )
            }}
          </label>
        </b-col>
        <b-col class="d-flex justify-content-end">
          <b-pagination
            v-model="pagination"
            :total-rows="totalRows"
            :per-page="perPage"
            align="fill"
            size="sm"
            class="my-0"
          ></b-pagination>
        </b-col>
      </b-row>
    </b-card>
  </div>
</template>

<script>
export default {
  name: "Dataset",
  data() {
    return {
      breadcrumb: [
        {
          text: "Beranda",
          to: "home"
        },
        {
          text: "Dataset",
          active: true
        }
      ],
      fields: [],
      searchData: "",
      hapusDataset: false,
      datasetRows: [],
      allFields: [],
      selectedField: [],
      isBusy: true,
      isBusySubmit: false,
      pagination: 1,
      totalRows: 0,
      perPage: 10,
      proses: 0
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
    this.getDataset();
  },
  methods: {
    async selectFile() {
      this.proses = 0;
    },
    async uploadData() {
      await this.$confirm({
        title: "⚠ Import Dataset",
        message: this.hapusDataset
          ? "Dataset sebelumnya akan ditimpa dengan dataset baru"
          : "Tambahkan dataset baru",
        button: {
          no: "Tidak",
          yes: "Ya, Lakukan"
        },
        callback: confirm => {
          if (confirm) {
            this.isBusySubmit = true;
            this.isBusy = true;
            const file = document.querySelector("input[type=file]").files[0];
            const reader = new FileReader();
            var rowData = [];
            reader.onloadend = async () => {
              rowData = await this.csvJSON(reader.result);
              try {
                if (this.hapusDataset) {
                  await this.$axios.delete(`/api/dataset`);
                }

                var i,
                  j,
                  temporary,
                  chunk = 200;
                for (i = 0, j = rowData.length; i < j; i += chunk) {
                  this.proses = i;
                  temporary = rowData.slice(i, i + chunk);
                  const json_data = temporary.flatMap(doc => [
                    { index: { _index: "dataset" } },
                    doc
                  ]);
                  var bulk_data = Object.keys(json_data)
                    .map(function(k) {
                      return JSON.stringify(json_data[k]);
                    })
                    .join("\n");

                  await this.$axios.post(`/api/_bulk`, `${bulk_data}\n`, {
                    headers: {
                      "Content-type": "application/json"
                    }
                  });
                  this.proses = j;
                }

                this.getDataset();
              } catch (error) {
                console.log(error);
              }
            };
            reader.readAsBinaryString(file);
          }
        }
      });
    },
    async csvJSON(csv) {
      var lines = csv.split("\n");
      var result = [];
      var headers = lines[0].replace(/\s/g, "").split(",");
      for (var i = 1; i < lines.length; i++) {
        var obj = {};
        var currentline = lines[i].split(",");
        if (currentline.length > 1) {
          for (var j = 0; j < headers.length; j++) {
            obj[headers[j]] =
              currentline.length == j + 1
                ? currentline[j].replace(/\s/g, "")
                : isNaN(currentline[j])
                ? currentline[j]
                : Number(currentline[j]);
          }
          result.push(obj);
        }
      }
      return result;
    },
    numberWithSeparator(x) {
      return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    },
    async getDataset() {
      this.isBusy = true;
      const data = {
        from: (this.pagination - 1) * this.perPage,
        size: this.perPage
      };
      if (this.searchData) {
        data["query"] = {
          wildcard: {
            PKT_CLASS: `*${this.searchData}*`
          }
        };
      }
      await this.$axios
        .post("/api/dataset/_search", data)
        .then(resp => {
          this.datasetRows = [];
          const respData = resp.data;
          const respDataset = respData.hits.hits;
          respDataset.forEach(key => {
            const data = key._source;
            data["_id"] = key._id;
            this.datasetRows.push(data);
          });
          this.totalRows = respData.hits.total.value;
          return this.datasetRows;
        })
        .catch(error => {
          this.totalRows = 0;
          this.isBusy = false;
          this.isBusySubmit = false;
        });

      this.isBusy = false;
      this.isBusySubmit = false;
      this.selectedField =
        this.datasetRows.length > 0
          ? Object.keys(this.datasetRows[0]).slice(0, 3)
          : [];
      if (this.datasetRows.length > 0) {
        if (Object.keys(this.datasetRows[0]).includes("PKT_CLASS")) {
          this.selectedField.push("PKT_CLASS");
        }
      }
      this.allFields =
        this.datasetRows.length > 0 ? Object.keys(this.datasetRows[0]) : [];
      this.columnView(this.selectedField);
    },
    async columnView() {
      const value = this.selectedField;
      this.fields = [
        {
          key: "index",
          label: "#",
          class: "text-center"
        }
      ];
      this.allFields.forEach(key => {
        if (value.includes(key)) {
          this.fields.push({
            key: key
          });
        }
      });
      this.fields.push({
        key: "actions",
        label: "Aksi",
        class: "text-center"
      });
      this.isBusy = false;
    }
  },
  watch: {
    pagination: {
      handler: function(value) {
        this.getDataset();
      }
    },
    selectedField: {
      handler: function(value) {
        this.columnView();
      }
    }
  },
  head() {
    return {
      title: "Dataset"
    };
  }
};
</script>
<style scoped>
.filter-field /deep/ .dropdown-menu {
  max-height: 200px;
  overflow-y: auto;
}
</style>
