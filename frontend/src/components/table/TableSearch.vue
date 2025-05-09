<script setup lang="ts">
import { computed } from "vue";
import { useTranslations } from "../../composables/useTranslations";
import { debounce } from "lodash-es";
// Props and emits for v-model:value API
const props = defineProps<{
  value: string;
  placeholder?: string;
}>();

const emit = defineEmits<{
  (e: "update:value", value: string): void;
}>();

const { currentLanguage } = useTranslations();

const translatedPlaceholder = computed(() => {
  const translations = {
    de: "Nach Benutzer suchen",
    en: "Search for user",
  };
  return (
    props.placeholder || translations[currentLanguage.value as "de" | "en"]
  );
});
const debouncedEmit = debounce((val: string) => {
  emit("update:value", val);
}, 300);

// Emit updates on user input with debounce
function onInput(event: Event) {
  const target = event.target as HTMLInputElement;
  debouncedEmit(target.value);
}
</script>

<template>
  <div class="search-container">
    <input
      type="text"
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
  max-width: 354px;
  margin-bottom: 1rem;
}

.search-input {
  width: 100%;
  box-sizing: border-box;
  display: block;
  padding: 0.5rem 0.75rem;
  padding-right: 2rem;
  border: 1px solid var(--font-color-contrast-low);
  background-color: var(--bgc-inputfield-on-body);
  border-radius: 8px;
  font-weight: 500;
  outline: none;
  transition: border-color 0.2s;
  color: var(--font-color-contrast-high);
}

.search-input:focus {
  outline: 2px solid var(--color-focus);
}

.search-input::placeholder {
  color: var(---font-color-contrast-medium);
}
.search-icon {
  display: block;
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(-font-color-contrast-high);
}
</style>
