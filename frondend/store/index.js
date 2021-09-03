export const state = () => ({
  darkMode: process.server
    ? false
    : localStorage.getItem("darkMode") == "true"
    ? Boolean(true)
    : Boolean(false),
  showSidebar: process.server
    ? false
    : localStorage.getItem("showSidebar") == "true"
    ? Boolean(true)
    : Boolean(false),
  token_id: process.server ? null : localStorage.getItem("token_id"),
  loggedIn: process.server ? false : localStorage.getItem("loggedIn"),
  user: process.server ? {} : localStorage.getItem("user")
});

export const mutations = {
  //mutations untuk mengubah state di atas
  SET_BG_MODE(state, payload) {
    localStorage.setItem("darkMode", payload);
    state.darkMode = payload;
  },
  SET_SIDEBAR(state, payload) {
    localStorage.setItem("showSidebar", payload);
    state.showSidebar = payload;
  },
  SET_TOKEN_ID(state, payload) {
    localStorage.setItem("token_id", payload);
    state.token_id = payload;
  },
  SET_lOGGED_IN(state, payload) {
    state.loggedIn = payload;
  },
  SET_USER(state, payload) {
    state.user = payload;
  }
};
