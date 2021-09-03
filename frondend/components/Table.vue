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
          <template #cell(index)="data">
            {{
              numberWithSeparator(data.index + 1 + (currentPage - 1) * perPage)
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
            <b-card>
              <b-row align-h="center">
                <table>
                  <tr v-for="(value, key) in row.item" :key="key">
                    <td>{{ key }}</td>
                    <td>{{ value }}</td>
                  </tr>
                </table>
              </b-row>
            </b-card>
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
    this.selectedField =
      this.items.length > 0 ? Object.keys(this.items[0]).slice(0, 3) : [];
    if (this.items.length > 0) {
      if (Object.keys(this.items[0]).includes("PKT_CLASS")) {
        this.selectedField.push("PKT_CLASS");
      }
    }
    this.$_debounceTimeoutId = null;
    this.columnView();
  },
  beforeDestroy() {
    clearTimeout(this.$_debounceTimeoutId);
    this.$_debounceTimeoutId = null;
  },
  mounted() {
    this.allFields = this.items.length > 0 ? Object.keys(this.items[0]) : [];

    // Set the initial number of items
    this.totalRows = this.items.length;
    if (this.items.length > 0) {
      if (Object.keys(this.items[0]).includes("PKT_CLASS")) {
        this.selectedField.push("PKT_CLASS");
      }
    }
  },
  methods: {
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
    items: {
      handler: function(value) {
        this.selectedField =
          this.items.length > 0 ? Object.keys(this.items[0]).slice(0, 3) : [];
        if (this.items.length > 0) {
          if (Object.keys(this.items[0]).includes("PKT_CLASS")) {
            this.selectedField.push("PKT_CLASS");
          }
        }
      }
    },
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
