<template>
  <div>
    <Breadcrumb :items="breadcrumb" />
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
              placeholder="Pencarian..."
              @input="getRiwayat"
            ></b-form-input>
            <span class="input-group-append">
              <div
                class="input-group-text bg-transparent"
                type="button"
                @click="getRiwayat"
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
            :dark="this.$store.state.darkMode"
            :items="riwayatRows"
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
              <b-dropdown text="Opsi" size="sm" variant="warning">
                <b-dropdown-item :to="`riwayat/` + row.item._id"
                  ><b-icon-arrow-up-right
                    font-scale="1"
                  ></b-icon-arrow-up-right>
                  Detail</b-dropdown-item
                >
                <b-dropdown-item
                  variant="danger"
                  @click="hapusData(row.item._id)"
                  ><b-icon-trash font-scale="1"></b-icon-trash>
                  Hapus</b-dropdown-item
                >
              </b-dropdown>
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
                (pagination - 1) * perPage + (riwayatRows.length > 0 ? 1 : 0)
              )
            }}
            sampai
            {{
              numberWithSeparator(
                (pagination - 1) * perPage + riwayatRows.length
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
                (pagination - 1) * perPage + (riwayatRows.length > 0 ? 1 : 0)
              )
            }}
            sampai
            {{
              numberWithSeparator(
                (pagination - 1) * perPage + riwayatRows.length
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
import dateFormat from "dateformat";
export default {
  name: "Riwayat",

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
      riwayatRows: [],
      allFields: [],
      selectedField: [],
      isBusy: true,
      isBusySubmit: false,
      pagination: 1,
      totalRows: 0,
      perPage: 10
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
    this.getRiwayat();
  },
  methods: {
    numberWithSeparator(x) {
      return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    },
    async getRiwayat() {
      this.isBusy = true;
      const data = {
        from: (this.pagination - 1) * this.perPage,
        size: this.perPage,
        _source: ["created_at", "form"],
        sort: [
          {
            created_at: {
              order: "desc",
              format: "strict_date_optional_time_nanos"
            }
          }
        ]
      };
      if (this.searchData) {
        data["query"] = {
          query_string: {
            fields: [
              "form.total_data_latih",
              "form.total_data_uji",
              "form.nilai_k",
              "form.akurasi"
            ],
            query: `*${this.searchData}*`
          }
        };
      }
      await this.$axios
        .post("/api/testing/_search", data)
        .then(resp => {
          this.riwayatRows = [];
          const respData = resp.data;
          const respDataset = respData.hits.hits;
          respDataset.forEach(key => {
            const tanggal_uji = dateFormat(
              key._source.created_at,
              "dd mmm yyyy h:MM"
            );
            const data = {
              tanggal_uji: tanggal_uji,
              data_latih: key._source.form.total_data_latih,
              data_uji: key._source.form.total_data_uji,
              nilai_k: key._source.form.nilai_k,
              akurasi: `${key._source.form.akurasi} %`,
              _id: key._id,
              form: key._source.form
            };
            this.riwayatRows.push(data);
          });
          this.totalRows = respData.hits.total.value;
          return this.riwayatRows;
        })
        .catch(error => {
          this.totalRows = 0;
          this.isBusy = false;
          this.isBusySubmit = false;
        });

      this.isBusy = false;
      this.isBusySubmit = false;
      this.selectedField =
        this.riwayatRows.length > 0
          ? Object.keys(this.riwayatRows[0]).slice(0, 5)
          : [];
      if (this.riwayatRows.length > 0) {
        if (Object.keys(this.riwayatRows[0]).includes("PKT_CLASS")) {
          this.selectedField.push("PKT_CLASS");
        }
      }
      this.allFields =
        this.riwayatRows.length > 0
          ? Object.keys(this.riwayatRows[0]).slice(0, 5)
          : [];
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
            key: key,
            class: "text-center"
          });
        }
      });
      this.fields.push({
        key: "actions",
        label: "Aksi",
        class: "text-center"
      });
      this.isBusy = false;
    },
    async hapusData(id) {
      await this.$confirm({
        title: "⚠ Hapus Data?",
        message: "Yakin, data pengujian akan dihapus permanen",
        button: {
          no: "Tidak",
          yes: "Ya, Hapus"
        },
        callback: confirm => {
          if (confirm) {
            this.$axios.delete(`/api/testing/_doc/${id}`).then(() => {
              setTimeout(() => {
                this.getRiwayat();
              }, 1000);
            });
          }
        }
      });
    }
  },
  watch: {
    pagination: {
      handler: function(value) {
        this.getRiwayat();
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
      title: "Riwayat Pengujian"
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
