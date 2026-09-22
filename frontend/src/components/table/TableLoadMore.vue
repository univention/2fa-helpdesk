<!--
 SPDX-License-Identifier: AGPL-3.0-only
 SPDX-FileCopyrightText: 2026 Univention GmbH
-->

<script setup lang="ts">
import {
  Locale,
  Translations,
  useTranslations,
} from "../../composables/useTranslations";

defineProps<{
  hasNextPage: boolean;
  loadingMore?: boolean;
}>();

const emit = defineEmits<{
  (e: "load-more"): void;
}>();

const { t: tComputed } = useTranslations();
const t = (key: keyof Translations[Locale]) => tComputed.value(key);
</script>

<template>
  <div class="table-footer">
    <template v-if="hasNextPage">
      <button
        class="load-more-button"
        @click="emit('load-more')"
        :disabled="loadingMore"
      >
        {{ loadingMore ? t("loading") : t("loadMore") }}
      </button>
      <p class="load-more-hint">{{ t("loadMoreHint") }}</p>
    </template>
    <p v-else class="load-more-hint">{{ t("noMoreResults") }}</p>
  </div>
</template>

<style scoped>
.table-footer {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.125rem;
  background-color: var(--bgc-table-row-bg);
  padding: 0.75rem 1.5rem;
  border-bottom-left-radius: 8px;
  border-bottom-right-radius: 8px;
}

.load-more-button {
  background: transparent;
  border: none;
  border-radius: 4px;
  padding: 0.25rem 0.75rem;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 1rem;
  font-weight: 600;
  color: var(--font-color-contrast-high);
}

.load-more-button:hover:not(:disabled) {
  text-decoration: underline;
}

.load-more-button:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}

.load-more-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.load-more-hint {
  margin: 0;
  font-size: 0.8125rem;
  font-style: italic;
  color: var(--font-color-contrast-middle);
  text-align: center;
}
</style>
