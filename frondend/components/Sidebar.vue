<template>
  <aside :class="{ open: this.$store.state.showSidebar, mobile: isMobile }">
    <div class="side-space"></div>
    <div class="d-flex" style="height: 50px">
      <!-- <div class="p-2"><LangToggle /></div> -->
      <div class="ml-auto p-2"><DarkLightMode /></div>
    </div>
    <div class="side-menu-header d-flex align-items-center pl-3 pb-2">
      <span
        class="mx-2 flex-shrink-0 avatar gd-success"
        style="width: 50px; height: 50px"
      >
        <span
          v-if="
            !this.$store.state.user.photo && this.$store.state.user.fullname
          "
        >
          {{ this.$store.state.user.fullname.substring(0, 1).toUpperCase() }}
        </span>
        <img
          v-if="this.$store.state.user.photo"
          :src="this.$store.state.user.photo"
          :alt="this.$store.state.user.fullname"
          class="rounded-circle mx-2 flex-shrink-0"
          style="width: 50px; height: 50px"
        />
      </span>
      <span class="str"
        >{{ this.$store.state.user.fullname }} <br /><span
          style="font-size: 0.7rem"
          >@{{ this.$store.state.user.username }}</span
        ></span
      >
    </div>
    <div class="pt-3 pl-4 pr-3 pb-2">
      <b-input-group size="sm">
        <b-form-input
          v-model="searchMenu"
          placeholder="Search ..."
          class="border-right-0"
        ></b-form-input>
        <span class="input-group-append">
          <div class="input-group-text bg-transparent" type="button">
            <b-icon-search scale="0.9" class="icon"></b-icon-search>
          </div>
        </span>
      </b-input-group>
    </div>
    <div class="side-menu-body mb-5 pb-5">
      <div class="list-group">
        <nuxt-link
          v-for="menu in filterByMenu"
          :key="menu._id"
          :to="{
            path: `/${menu.slug}`
          }"
          :class="isCurrentPage(menu.slug) ? 'active' : ''"
          class="list-group-item d-flex align-items-center"
        >
          <div class="w-100" @click="sidebarMenu">
            <b-icon
              :icon="isCurrentPage(menu.slug) ? menu.active_icon : menu.icon"
              class="icon ml-2 mr-3"
              scale="1.3"
            ></b-icon>
            <span class="str">{{ menu.module_name }}</span>
          </div>
        </nuxt-link>
      </div>
    </div>
  </aside>
</template>

<script>
import { mapMutations } from "vuex";
import DarkLightMode from "~/components/DarkLightMode";
export default {
  name: "Sidebar",
  components: {
    DarkLightMode
  },
  props: {
    menus: Array
  },
  data() {
    return {
      searchMenu: "",
      isMobile: false,
      currentPath: this.$route.name
    };
  },
  computed: {
    filterByMenu() {
      return this.menus.filter(menu => {
        return menu.module_name
          .toLowerCase()
          .includes(this.searchMenu.toLowerCase());
      });
    }
  },
  created() {
    this.currentPath = this.$route.name;
  },
  mounted() {
    this.$nextTick(function() {
      this.onResize();
    });
    window.addEventListener("resize", this.onResize);
  },

  methods: {
    ...mapMutations(["SET_SIDEBAR"]),
    onResize() {
      const widthSize = window.innerWidth;
      if (widthSize > 767) {
        this.isMobile = false;
      } else {
        this.isMobile = true;
      }
    },
    sidebarMenu() {
      const widthSize = window.innerWidth;
      if (widthSize < 767) {
        this.SET_SIDEBAR(false);
      }
    },
    isCurrentPage(page) {
      const path = this.$route.path.split("/");
      if (path.includes(page)) {
        return true;
      } else {
        return false;
      }
    }
  }
};
</script>

<style scoped>
.btn-dark-mode {
  border-left: 1px solid #e3e3e3;
  border-bottom: 1px solid #e3e3e3;
  border-bottom-left-radius: 15px;
  right: 0;
  cursor: pointer;
}
.dark-mode .btn-dark-mode {
  background-color: #1c3c56;
}
.light-mode .btn-dark-mode {
  background-color: aliceblue;
}
.dark-mode aside {
  background-color: #2f495e;
}
.light-mode aside {
  background-color: #fff;
}
aside::-webkit-scrollbar {
  width: 10px;
}

aside::-webkit-scrollbar-track {
  background: transparent;
}
aside::-webkit-scrollbar-corner {
  background: slateblue;
}

aside::-webkit-scrollbar-thumb {
  background: transparent;
}

aside::-webkit-scrollbar-thumb:hover {
  cursor: pointer;
  background: rgb(153, 152, 152);
}

aside .side-menu-body::-webkit-scrollbar {
  width: 8px;
}

aside .side-menu-body::-webkit-scrollbar-thumb {
  height: 56px;
  background: rgba(136, 136, 136, 0.4);
}

.light-mode aside .side-menu-header {
  height: 100px;
  border-bottom: 1px solid #eeeeee;
}

.dark-mode aside .side-menu-header {
  height: 100px;
  bottom: 0;
  border-bottom: 1px solid rgba(136, 136, 136, 0.4);
}

aside .side-menu-body {
  height: calc(100% - 200px);
  overflow-y: auto;
}

aside .side-menu-body::-webkit-scrollbar {
  width: 8px;
}

aside .side-menu-body::-webkit-scrollbar-thumb {
  height: 56px;
  background: rgba(136, 136, 136, 0.4);
}

aside .list-group {
  padding: 12px 0;
}

aside .list-group-item {
  height: 40px;
  font-weight: 400;
  color: #111111;
  padding: 0 24px;
  border: none;
  background-color: inherit;
}

aside .list-group-item {
  height: 40px;
  font-weight: 400;
  padding: 0 0 0 20px;
  border: none;
  background-color: inherit;
}

.dark-mode aside .list-group-item:hover {
  background-color: #283b4d;
}
.light-mode aside .list-group-item:hover {
  background-color: #ebebeb;
}

aside .list-group-item.active {
  color: inherit;
  pointer-events: none;
  font-weight: 700;
}
.dark-mode aside .list-group-item.active {
  background-color: #2b3d4e;
}
.light-mode aside .list-group-item.active {
  background-color: #e2dfdf;
}

aside .list-group-item.active .icon {
  fill: #00c58e;
}

aside.open {
  transform: translate3d(0, 0, 0);
}
.dark-mode aside.open {
  border-right: 1px double #4a6885;
}
.light-mode aside.open {
  border-right: 1px double #e2dfdf;
}
@media (min-width: 767px) {
  .side-space {
    height: 48px;
  }
}
</style>
