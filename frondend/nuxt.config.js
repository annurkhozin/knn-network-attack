export default {
  ssr: false,
  globalName: "myApp",
  globals: {
    id: globalName => `${globalName}`,
    nuxt: globalName => `$${globalName}`
  },
  server: {
    host: "0.0.0.0", // default: localhost
    port: 3000 // default: 3000
  },

  loading: {
    color: "#00ab6b"
  },
  loadingIndicator: {
    name: "circle",
    color: "#00ab6b",
    background: "white"
  },

  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    title: "k-NN Network Attack",
    meta: [
      { charset: "utf-8" },
      { name: "viewport", content: "width=device-width, initial-scale=1" },
      { name: "theme-color", content: "#317EFB" },
      { hid: "author", name: "author", content: "Nur Khozin" },
      { hid: "author", name: "author", content: "annurkhozin@gmail.com" }
    ],
    link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }]
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: ["@/static/css/main.css"],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
    {
      src: "~/plugins/confirm-dialog.js",
      mode: "client"
    },
    { src: "~/plugins/vue-apexchart.js", ssr: false }
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    // https://go.nuxtjs.dev/bootstrap
    "bootstrap-vue/nuxt",
    // https://go.nuxtjs.dev/axios
    "@nuxtjs/axios",
    "@nuxtjs/proxy",
    // https://go.nuxtjs.dev/pwa
    "@nuxtjs/pwa"
  ],

  bootstrapVue: {
    icons: true
  },

  // Axios module configuration: https://go.nuxtjs.dev/config-axios
  // axios: {
  //   baseURL: "http://127.0.0.1:9200/"
  // },
  axios: {
    proxy: true
  },

  proxy: {
    "/api/": {
      target: "http://127.0.0.1:9200/",
      pathRewrite: { "^/api/": "/" },
      changeOrigin: true
    }
  },

  //Middleware untuk mengecek sudah login atau belum, set global
  router: {},

  // PWA module configuration: https://go.nuxtjs.dev/pwa
  pwa: {
    meta: {
      title: "Network Attack",
      author: "annurkhozin@gmail.com"
    },
    manifest: {
      name: "k-NN Network Attack",
      short_name: "Network Attack",
      lang: "en",
      theme_color: "#317EFB"
    }
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
    publicPath: "/script/",
    babel: {
      compact: true
    },
    vendor: ["vue-apexchart"]
  }
};
