<!--
 SPDX-License-Identifier: AGPL-3.0-only
 SPDX-FileCopyrightText: 2025 Univention GmbH
-->

<template>
  <div class="language-selector">
    <select
      v-model="selectedLanguage"
      @change="changeLanguage"
      class="language-dropdown"
    >
      <option :value="Locale.DE">Deutsch</option>
      <option :value="Locale.EN">English</option>
    </select>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { Locale } from "../composables/useTranslations";

const emit = defineEmits(["change"]);
const selectedLanguage = ref(Locale.DE);

onMounted(() => {
  const storedLang = localStorage.getItem("language") || Locale.DE;
  selectedLanguage.value = storedLang as Locale;
});

const changeLanguage = () => {
  localStorage.setItem("language", selectedLanguage.value);

  emit("change", selectedLanguage.value);
};
</script>

<style scoped>
.language-selector {
  display: inline-block;
}

.language-dropdown {
  height: var(--control-height);
  padding: 0 var(--control-padding-inline);
  border-radius: var(--control-radius);
  border: 1px solid var(--control-border-color);
  background-color: var(--bgc-inputfield-on-body);
  color: var(--font-color-contrast-high);
  cursor: pointer;
  font-size: var(--control-font-size);
  font-weight: 500;
  transition: border-color 0.2s;
}

.language-dropdown:focus-visible {
  outline: 2px solid var(--color-focus);
}
</style>
