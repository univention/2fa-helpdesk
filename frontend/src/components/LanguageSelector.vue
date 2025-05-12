<template>
  <div class="language-selector">
    <select
      v-model="selectedLanguage"
      @change="changeLanguage"
      class="language-dropdown"
    >
      <option value="de">Deutsch</option>
      <option value="en">English</option>
    </select>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";

const emit = defineEmits(["change"]);
const selectedLanguage = ref("de");

onMounted(() => {
  const storedLang = localStorage.getItem("language") || "de";
  selectedLanguage.value = storedLang;
});

const changeLanguage = () => {
  localStorage.setItem("language", selectedLanguage.value);

  emit("change", selectedLanguage.value);
};
</script>

<style scoped>
.language-selector {
  display: inline-block;
  margin-left: 1rem;
}

.language-dropdown {
  padding: 0.5rem;
  border-radius: 4px;
  border: 1px solid var(--font-color-contrast-low);
  background-color: var(--bgc-inputfield-on-body);
  color: var(--font-color-contrast-high);
  cursor: pointer;
  font-size: 0.9rem;
}

.language-dropdown:focus {
  outline: none;
  border-color: var(--color-focus);
}
</style>
