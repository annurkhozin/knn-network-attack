<template>
  <div>
    <div class="d-flex mb-4">
      <b-breadcrumb class="bg-transparent" :items="items"> </b-breadcrumb>
      <div class="ml-auto d-block d-md-none d-lg-none d-xl-none">
        <b-dropdown variant="link" right no-caret class="flex" size="sm">
          <template #button-content>
            <b-icon-bell class="icon"></b-icon-bell>
            <span class="notification-badge badge badge-danger">3</span>
          </template>
          <b-dropdown-item
            v-for="(n, index) in 10"
            :key="index"
            v-b-tooltip.hover.leftbottom="n"
            to="profile"
          >
            <span class="h-1x">
              Contoh berikut adalah menunjukkan notifikasi dalam bentuk text
            </span>
          </b-dropdown-item>
          <b-dropdown-divider></b-dropdown-divider>
          <b-dropdown-item>Lainnya...</b-dropdown-item>
        </b-dropdown>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    items: {
      type: Array,
      required: true
    }
  },
  methods: {
    refreshPage() {
      window.location.reload();
    }
  }
};
</script>

<style scoped>
.breadcrumb {
  padding: 0.75rem 0;
  margin-bottom: 0;
}
span.notification-badge {
  position: absolute;
  top: 1px;
  left: 16px;
  border-radius: 50%;
}
.badge {
  padding: 0.1rem 0.2rem;
}
</style>
