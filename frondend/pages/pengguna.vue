<template>
  <div>
    <Breadcrumb :items="breadcrumb" />
    <b-card :class="this.$store.state.darkMode ? 'bg-dark' : ''">
      <b-row class="mb-4 ml-1">
        <b-button v-b-modal.modal-pengguna variant="success shadow" size="sm"
          ><b-icon-plus scale="1.3"></b-icon-plus> &nbsp;Tambah baru</b-button
        >
      </b-row>
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
        </b-col>
        <b-col class="d-flex justify-content-end">
          <b-input-group size="sm" class="col-12 col-md-8">
            <b-form-input
              v-model="searchData"
              placeholder="Cari berdasarkan nama..."
              @input="getUsers"
            ></b-form-input>
            <span class="input-group-append">
              <div
                class="input-group-text bg-transparent"
                type="button"
                @click="getUsers"
              >
                <b-icon-arrow-repeat class="icon"></b-icon-arrow-repeat>
              </div>
            </span>
          </b-input-group>
        </b-col>
      </b-row>
      <b-row class="mt-3 list-row block">
        <b-col
          v-for="(user, index) in userRows"
          :key="index"
          cols="12"
          sm="6"
          md="3"
          class="pr-2 pl-2"
        >
          <div class="list-item">
            <div>
              <a href="javascript:void();"
                ><span class="w-48 avatar" :class="bgAvatar()">
                  <span v-if="!user.photo && user.fullname">
                    {{ user.fullname.substring(0, 1).toUpperCase() }}
                  </span>
                  <img
                    v-if="user.photo"
                    :src="user.photo"
                    :alt="user.fullname"
                    class="rounded-circle mx-2 flex-shrink-0"
                    style="width: 48px; height: 48px"/></span
              ></a>
            </div>
            <div class="flex">
              <a
                href="javascript:void();"
                class="item-author str font-weight-bold"
                >{{ user.fullname }}</a
              >
              <div class="item-except text-sm h-1x str">
                @{{ user.username }}
              </div>
            </div>
            <b-col
              v-if="$store.state.token_id != user._id"
              class="text-right"
              style="position: absolute"
            >
              <b-button
                size="sm"
                variant="danger"
                class="btn-action"
                @click="hapusData(user._id, user.fullname)"
              >
                <b-icon-trash></b-icon-trash>
              </b-button>
              <b-button
                size="sm"
                variant="success"
                class="btn-action"
                @click="updateData(user)"
              >
                <b-icon-person-badge></b-icon-person-badge>
              </b-button>
              <span class="d-inline d-sm-none d-md-none d-lg-none d-xl-none">
                <b-icon-three-dots-vertical
                  class="icon"
                  scale="1.3"
                ></b-icon-three-dots-vertical>
              </span>
            </b-col>
          </div>
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
                (pagination - 1) * perPage + (userRows.length > 0 ? 1 : 0)
              )
            }}
            sampai
            {{
              numberWithSeparator((pagination - 1) * perPage + userRows.length)
            }}
            dari {{ numberWithSeparator(totalRows) }} data
          </label>
          <label
            class="mr-sm-2 d-block d-md-none str"
            for="inline-form-custom-select-pref"
            >Data
            {{
              numberWithSeparator(
                (pagination - 1) * perPage + (userRows.length > 0 ? 1 : 0)
              )
            }}
            sampai
            {{
              numberWithSeparator((pagination - 1) * perPage + userRows.length)
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

    <b-modal
      id="modal-pengguna"
      ref="modal"
      size="sm"
      title="Data Pengguna"
      @hidden="resetModal"
      @ok="handleOk"
    >
      <form ref="form" @submit.stop.prevent="handleSubmit">
        <b-alert :show="error === '' ? false : true" variant="danger" fade>{{
          error
        }}</b-alert>
        <b-input-group class="mb-4" size="sm">
          <b-input-group-append is-text>
            <b-icon-person class="icon"></b-icon-person>
          </b-input-group-append>
          <b-form-input
            ref="fullname"
            v-model="form.fullname"
            placeholder="Nama lengkap"
            style="border-left: 0"
            required
          ></b-form-input>
        </b-input-group>
        <b-input-group class="mb-4" size="sm">
          <b-input-group-append is-text>
            <b-icon-key class="icon"></b-icon-key>
          </b-input-group-append>
          <b-form-input
            ref="username"
            v-model="form.username"
            placeholder="Username"
            style="border-left: 0"
            required
          ></b-form-input>
        </b-input-group>
        <b-input-group class="mb-4" size="sm">
          <b-input-group-append is-text>
            <b-icon-lock class="icon"></b-icon-lock>
          </b-input-group-append>
          <b-form-input
            ref="password"
            v-model="form.password"
            :type="passwordFieldType"
            placeholder="Password"
            style="border-left: 0"
            class="border-right-0"
            required
          ></b-form-input>
          <span class="input-group-append">
            <div
              class="input-group-text bg-transparent"
              type="button"
              @click="btnPassword"
            >
              <b-icon-eye-slash
                v-if="!showPassword"
                scale="0.9"
                class="icon"
              ></b-icon-eye-slash>
              <b-icon-eye
                v-if="showPassword"
                scale="0.9"
                class="icon"
              ></b-icon-eye>
            </div>
          </span>
        </b-input-group>
        <b-input-group class="mb-4" size="sm">
          <b-input-group-append is-text>
            <b-icon-image class="icon"></b-icon-image>
          </b-input-group-append>
          <b-form-file
            ref="photo"
            size="sm"
            accept="image/jpeg, image/png, image/jpg"
            placeholder="Photo"
            @change="base64File"
            style="border-left: 0"
            required
          ></b-form-file>
        </b-input-group>
      </form>
    </b-modal>
  </div>
</template>

<script>
import md5 from "md5";
export default {
  name: "Pengguna",
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
          to: "home"
        },
        {
          text: "Pengguna",
          active: true
        }
      ],
      form: {},
      error: "",
      showPassword: false,
      passwordFieldType: "password",
      searchData: "",
      userRows: [],
      colorAvatar: ["gd-primary", "gd-success", "gd-info", "gd-warning"],
      isBusy: true,
      isBusySubmit: false,
      pagination: 1,
      totalRows: 0,
      perPage: 10
    };
  },
  created() {
    this.getUsers();
  },
  methods: {
    numberWithSeparator(x) {
      return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    },
    resetModal() {
      this.form = {};
      this.error = "";
    },
    handleOk(bvModalEvt) {
      bvModalEvt.preventDefault();
      this.handleSubmit();
    },
    async handleSubmit() {
      if (!this.form.fullname) {
        this.$refs.fullname.$el.focus();
        this.error = "Nama lengkap wajid diisi";
      } else if (!this.form.username) {
        this.$refs.username.$el.focus();
        this.error = "Username wajid diisi";
      } else if (!this.form.password && !this.form._id) {
        this.$refs.password.$el.focus();
        this.error = "Password wajid diisi";
      } else if (!this.form.photo && !this.form._id) {
        this.$refs.photo.$el.focus();
        this.error = "Photo wajid diisi";
      } else {
        this.isBusySubmit = true;
        const data = {
          fullname: this.form.fullname,
          username: this.form.username
        };
        if (this.form.password) {
          data.password = md5(this.form.password);
        }
        if (this.form.photo) {
          data.photo = this.form.photo;
        }
        const headers = {
          "Content-Type": "application/json"
        };
        const _id = this.form._id;
        if (_id) {
          const doc = {
            doc: data
          };
          await this.$axios
            .post(`/api/users/_update/${_id}`, doc, {
              headers: headers
            })
            .then(resp => {
              this.isBusySubmit = false;
              this.$confirm({
                title: "⚠ Success",
                message: "Pengguna berhasil diperbarui",
                button: {
                  yes: "Ok"
                },
                callback: confirm => {
                  this.$bvModal.hide("modal-pengguna");
                  this.getUsers();
                }
              });
            })
            .catch(error => {
              if (error.response) {
                this.isBusySubmit = false;
                this.$confirm({
                  title: "⛔ Error",
                  message: "Gagal menyimpan data",
                  button: {
                    yes: "Ok"
                  }
                });
              }
            });
        } else {
          await this.$axios
            .post(`/api/users/_doc/`, data, {
              headers: headers
            })
            .then(resp => {
              this.isBusySubmit = false;
              this.$confirm({
                title: "⚠ Success",
                message: "Pengguna berhasil ditambahkan",
                button: {
                  yes: "Ok"
                },
                callback: confirm => {
                  this.$bvModal.hide("modal-pengguna");
                  this.getUsers();
                }
              });
            })
            .catch(error => {
              if (error.response) {
                this.isBusySubmit = false;
                this.$confirm({
                  title: "⛔ Error",
                  message: "Gagal menyimpan data",
                  button: {
                    yes: "Ok"
                  }
                });
              }
            });
        }
      }
    },
    base64File: function() {
      const file = document.querySelector("input[type=file]").files[0];
      console.log(file);
      const reader = new FileReader();

      reader.onloadend = () => {
        this.form.photo = reader.result;
      };
      reader.readAsDataURL(file);
      // console.log(file);
    },
    btnPassword() {
      if (this.showPassword === true) {
        this.showPassword = false;
        this.passwordFieldType = "password";
      } else {
        this.showPassword = true;
        this.passwordFieldType = "text";
      }
    },
    async getUsers() {
      this.isBusy = true;
      const data = {
        from: (this.pagination - 1) * this.perPage,
        size: this.perPage
      };
      if (this.searchData) {
        data["query"] = {
          query_string: {
            fields: ["fullname", "username"],
            query: `*${this.searchData}*`
          }
        };
      }
      await this.$axios
        .post("/api/users/_search", data)
        .then(resp => {
          this.userRows = [];
          const respData = resp.data;
          const respDataset = respData.hits.hits;
          respDataset.forEach(key => {
            const data = key._source;
            data["_id"] = key._id;
            this.userRows.push(data);
          });
          this.totalRows = respData.hits.total.value;
          return this.userRows;
        })
        .catch(error => {
          this.totalRows = 0;
          this.isBusy = false;
          this.isBusySubmit = false;
        });

      this.isBusy = false;
      this.isBusySubmit = false;
    },
    async updateData(user) {
      this.form = {
        _id: user._id,
        fullname: user.fullname,
        username: user.username
      };
      this.$bvModal.show("modal-pengguna");
    },
    async hapusData(id, name) {
      await this.$confirm({
        title: `⚠ Hapus akun ${name}?`,
        message: "Yakin, data akun akan dihapus permanen",
        button: {
          no: "Tidak",
          yes: "Ya, Hapus"
        },
        callback: confirm => {
          if (confirm) {
            this.$axios.delete(`/api/users/_doc/${id}`).then(() => {
              setTimeout(() => {
                this.getUsers();
              }, 1000);
            });
          }
        }
      });
    },
    bgAvatar() {
      return this.colorAvatar[
        Math.floor(Math.random() * this.colorAvatar.length)
      ];
    }
  },

  head() {
    return {
      title: "Pengguna"
    };
  }
};
</script>

<style scoped>
.btn-action {
  visibility: hidden;
}

.list-item:hover {
  background: rgba(255, 255, 255, 0.25);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
}
.list-item:hover .btn-action {
  position: relative;
  visibility: visible;
  transition: all 0.2s linear;
}

.list-item {
  cursor: pointer;
  position: relative;
  display: -ms-flexbox;
  display: flex;
  -ms-flex-direction: column;
  flex-direction: column;
  min-width: 0;
  word-wrap: break-word;
  margin-bottom: 1rem;
}

.list-row .list-item {
  -ms-flex-direction: row;
  flex-direction: row;
  -ms-flex-align: center;
  align-items: center;
}

.list-row .list-item > * {
  padding: 0.5rem;
}

.no-wrap {
  white-space: nowrap;
}

.text-gd {
  -webkit-background-clip: text;
  -moz-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  -moz-text-fill-color: transparent;
}

.text-sm {
  font-size: 0.825rem;
}

.w-48 {
  width: 48px !important;
  height: 48px !important;
}
.custom-select {
  background: transparent;
  padding: 0.375rem;
  text-align: center;
  width: 50px;
}

.dark-mode .btn-filter {
  border: #eee;
}

@media (max-width: 575px) {
  .dark-mode .list-item {
    border-bottom: 1px solid rgba(136, 136, 136, 0.4);
  }
  .light-mode .list-item {
    border-bottom: 1px solid #eeeeee;
  }
  .custom-select {
    width: 40px;
  }
}
</style>
