<template>
  <div class="switches p-2 pr-3">
    <input
      id="darktoggle"
      type="checkbox"
      :checked="this.$store.state.darkMode"
      @click="setBgMode"
    />
    <label for="darktoggle">
      <span></span>
    </label>
  </div>
</template>

<script>
import { mapMutations } from "vuex";

export default {
  methods: {
    ...mapMutations(["SET_BG_MODE"]),
    setBgMode() {
      this.SET_BG_MODE(!this.$store.state.darkMode);
    }
  }
};
</script>

<style scoped>
.switches [type="checkbox"] {
  position: absolute;
  left: -9999px;
}

.switches {
  border-radius: 50px;
}

.switches label {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.switches span:last-child {
  position: relative;
  width: 53px;
  height: 28px;
  border-radius: 15px;
  transition: all 0.3s;
}

.dark-mode .switches span:last-child {
  border: 1px double #739bbb;
}
.light-mode .switches span:last-child {
  border: 1px double #8a9dad;
}

.switches span:last-child::before,
.switches span:last-child::after {
  content: "";
  position: absolute;
}

.switches span:last-child::before {
  left: 1px;
  top: 1px;
  width: 24px;
  height: 24px;
  background: #556e84;
  border: 1px double rgb(243, 228, 23);
  border-radius: 50%;
  z-index: 1;
  transition: transform 0.3s;
}

.switches span:last-child::after {
  top: 50%;
  right: 3px;
  width: 20px;
  height: 20px;
  transform: translateY(-50%);
  background: url("data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%221em%22 font-size=%2280%22>🌞</text></svg>");
  background-size: 20px 20px;
  background-repeat: no-repeat;
  cursor: pointer;
}

.switches [type="checkbox"] + label span:last-child {
  background: aliceblue;
}
.switches [type="checkbox"]:checked + label span:last-child {
  background: #2f495e;
}

.switches [type="checkbox"]:checked + label span:last-child::before {
  transform: translateX(24px);
  background: #cfd7de;
}

.switches [type="checkbox"]:checked + label span:last-child::after {
  width: 20px;
  height: 20px;
  left: 3px;
  background: url("data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%221em%22 font-size=%2280%22>🌜</text></svg>");
  background-size: 20px 20px;
  background-repeat: no-repeat;
  cursor: pointer;
}
</style>
