<template>
  <b-container fluid>
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
          :options="pageOptions"
        ></b-form-select>
      </b-col>
      <b-col class="d-flex justify-content-end">
        <b-input-group size="sm" class="col-12 col-md-8">
          <b-form-input
            v-model="searchInput"
            type="search"
            placeholder="Pencarian..."
          ></b-form-input>
          <span class="input-group-append">
            <div
              class="input-group-text bg-transparent"
              type="button"
              @click="refreshTable"
            >
              <b-icon-arrow-repeat class="icon"></b-icon-arrow-repeat>
            </div>
          </span>
        </b-input-group>
      </b-col>
    </b-row>
    <b-row class="mt-3 mb-3" v-if="showSpinner">
      <b-col align-h="center" class="text-center">
        <div class="text-success my-2">
          <b-spinner class="align-middle"></b-spinner>
          <strong>Loading...</strong>
        </div>
      </b-col>
    </b-row>
    <!-- Main table element -->
    <b-row class="mt-3 mb-3">
      <b-col align-self="start">
        <b-table
          ref="table"
          :items="items"
          :fields="fields"
          :bordered="true"
          :current-page="currentPage"
          :per-page="perPage"
          :filter="filter"
          :filter-included-fields="selectedField"
          :dark="this.$store.state.darkMode"
          stacked="md"
          show-empty
          responsive
          hover
          outlined
          small
          :busy="isBusy"
          @filtered="onFiltered"
        >
          <template #table-busy>
            <div class="text-center text-success my-2">
              <b-spinner class="align-middle"></b-spinner>
              <strong>Loading...</strong>
            </div>
          </template>
          <template slot="thead-top">
            <tr>
              <th rowspan="2" style="vertical-align: top" class="text-center">
                #
              </th>
              <th rowspan="2" style="vertical-align: top" class="text-center">
                Actual
              </th>
              <th rowspan="2" style="vertical-align: top" class="text-center">
                Predict
              </th>
              <th :colspan="k * 2" class="text-center">
                Nilai K
              </th>
            </tr>
          </template>
          <template #cell(index)="data">
            {{
              numberWithSeparator(data.index + 1 + (currentPage - 1) * perPage)
            }}
          </template>
        </b-table>
      </b-col>
    </b-row>

    <b-row>
      <b-col align-self="start">
        <label
          class="mr-sm-2 d-none d-md-block str"
          for="inline-form-custom-select-pref"
          >Ditampilkan
          {{
            numberWithSeparator(
              (currentPage - 1) * perPage + (items.length > 0 ? 1 : 0)
            )
          }}
          sampai
          {{ numberWithSeparator((currentPage - 1) * perPage + perPage) }}
          dari {{ numberWithSeparator(totalRows) }} data
        </label>
        <label
          class="mr-sm-2 d-block d-md-none str"
          for="inline-form-custom-select-pref"
          >Data
          {{
            numberWithSeparator(
              (currentPage - 1) * perPage + (items.length > 0 ? 1 : 0)
            )
          }}
          sampai
          {{ numberWithSeparator((currentPage - 1) * perPage + items.length) }}
        </label>
      </b-col>
      <b-col class="d-flex justify-content-end">
        <b-pagination
          v-model="currentPage"
          :total-rows="totalRows"
          :per-page="perPage"
          align="fill"
          size="sm"
          class="my-0"
        ></b-pagination>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  props: {
    items: {
      type: Array
    },
    k: {
      type: Number
    }
  },
  data() {
    return {
      fields: [],
      allFields: [],
      selectedField: [],
      totalRows: 1,
      currentPage: 1,
      perPage: 5,
      pageOptions: [5, 10, 50, 100],
      filter: "",
      searchInput: "",
      isBusy: true,
      showSpinner: false
    };
  },
  created() {
    this.$_debounceTimeoutId = null;
    this.selectedField =
      this.items.length > 0 ? Object.keys(this.items[0]) : [];
    if (this.items.length > 0) {
      if (Object.keys(this.items[0]).includes("PKT_CLASS")) {
        this.selectedField.push("PKT_CLASS");
      }
    }
    this.columnView();
  },
  beforeDestroy() {
    clearTimeout(this.$_debounceTimeoutId);
    this.$_debounceTimeoutId = null;
  },
  mounted() {
    // Set the initial number of items
    this.totalRows = this.items.length;
    this.allFields = this.items.length > 0 ? Object.keys(this.items[0]) : [];
  },
  methods: {
    async columnView() {
      const value = this.selectedField;
      this.fields = [
        {
          key: "index",
          label: "#",
          thClass: "d-none",
          class: "text-center"
        },
        {
          key: "actual",
          thClass: "d-none",
          class: "text-center"
        },
        {
          key: "predict",
          thClass: "d-none",
          class: "text-center"
        }
      ];
      const hide = ["actual", "predict"];
      this.allFields.forEach(key => {
        if (value.includes(key) && !hide.includes(key)) {
          this.fields.push({
            key: key,
            class: "text-center"
          });
        }
      });
      this.isBusy = false;
    },
    async refreshTable() {
      this.$refs.table.refresh();
    },
    numberWithSeparator(x) {
      return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    },
    async onFiltered(filteredItems) {
      this.totalRows = filteredItems.length;
      this.currentPage = 1;
    }
  },
  watch: {
    selectedField: {
      handler: function(value) {
        this.columnView();
      }
    },
    searchInput(newVal, oldVal) {
      clearTimeout(this.$_debounceTimeoutId);
      this.$_debounceTimeoutId = null;
      if (!newVal) {
        this.filter = "";
        this.showSpinner = false;
      } else {
        this.showSpinner = true;
        this.$_debounceTimeoutId = setTimeout(() => {
          this.filter = this.searchInput;
          this.showSpinner = false;
        }, 1000);
      }
    }
  }
};
</script>
<style scoped>
.filter-field /deep/ .dropdown-menu {
  max-height: 200px;
  overflow-y: auto;
}
</style>
