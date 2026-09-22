<!--
 SPDX-License-Identifier: AGPL-3.0-only
 SPDX-FileCopyrightText: 2025 Univention GmbH
-->

<script setup lang="ts">
import { computed, onBeforeUnmount } from "vue";
import {
  Locale,
  Translations,
  useTranslations,
} from "../../composables/useTranslations";
import { debounce } from "lodash-es";

const props = defineProps<{
  value: string;
  placeholder?: string;
}>();

const emit = defineEmits<{
  (e: "update:value", value: string): void;
}>();

const { t: tComputed } = useTranslations();
const t = (key: keyof Translations[Locale]) => tComputed.value(key);

const translatedPlaceholder = computed(() => {
  return props.placeholder || t("searchPlaceholder");
});
// Trailing debounce on purpose: the search runs against LDAP, so a query
// should only be issued once typing comes to rest, never on the prefixes
// passed through on the way there.
const debouncedEmit = debounce((val: string) => {
  emit("update:value", val);
}, 400);

// Emit updates on user input with debounce
function onInput(event: Event) {
  const target = event.target as HTMLInputElement;
  debouncedEmit(target.value);
}

onBeforeUnmount(() => {
  debouncedEmit.cancel();
});
</script>

<template>
  <div class="search-container">
    <input
      type="search"
      :value="value"
      @input="onInput"
      :placeholder="translatedPlaceholder"
      class="search-input"
    />

    <span class="search-icon">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="16"
        height="16"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
      >
        <circle cx="11" cy="11" r="8"></circle>
        <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
      </svg>
    </span>
  </div>
</template>

<style scoped>
.search-container {
  position: relative;
  width: 100%;
  max-width: 22rem;
}

.search-input {
  width: 100%;
  display: block;
  height: var(--control-height);
  padding: 0 var(--control-padding-inline);
  /* Room for the magnifier sitting inside the field. */
  padding-right: 2rem;
  border: 1px solid var(--control-border-color);
  background-color: var(--bgc-inputfield-on-body);
  border-radius: var(--control-radius);
  font-size: var(--control-font-size);
  font-weight: 500;
  outline: none;
  transition: border-color 0.2s;
  color: var(--font-color-contrast-high);
}

.search-input:focus-visible {
  outline: 2px solid var(--color-focus);
}

.search-input::placeholder {
  color: var(--font-color-contrast-middle);
}
.search-icon {
  display: block;
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--font-color-contrast-high);
}
</style>
