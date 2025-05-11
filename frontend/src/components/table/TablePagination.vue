<script setup lang="ts">
import { computed, ref } from "vue";
import {
  Locale,
  Translations,
  useTranslations,
} from "../../composables/useTranslations";

const props = defineProps<{
  currentPage: number;
  totalPages: number;
  maxPageButtons?: number;
}>();

const emit = defineEmits<{
  (e: "page-change", page: number): void;
}>();

const { t: tComputed } = useTranslations();
const t = (key: keyof Translations[Locale]) => tComputed.value(key);

const pageInput = ref<number | null>(null);

const goToPage = (page: number) => {
  if (page < 1 || page > props.totalPages) return;
  emit("page-change", page);
};

const pageNumbers = computed(() =>
  Array.from({ length: props.totalPages }, (_, i) => i + 1)
);

const getVisiblePageNumbers = () => {
  const maxButtons = props.maxPageButtons ?? 5;
  const half = Math.floor(maxButtons / 2);

  let start = Math.max(props.currentPage - half, 1);
  let end = Math.min(start + maxButtons - 1, props.totalPages);

  if (end - start + 1 < maxButtons) {
    start = Math.max(end - maxButtons + 1, 1);
  }

  return Array.from({ length: end - start + 1 }, (_, i) => start + i);
};

const onGo = () => {
  if (pageInput.value != null) {
    goToPage(Math.floor(pageInput.value));
    pageInput.value = null;
  }
};
</script>

<template>
  <div class="pagination">
    <button
      class="pagination-button"
      @click="goToPage(currentPage - 1)"
      :disabled="currentPage <= 1"
    >
      {{ t("previous") }}
    </button>
    <div>
      <!-- simple mode when few pages -->
      <template v-if="props.totalPages <= (props.maxPageButtons ?? 7)">
        <button
          v-for="page in pageNumbers"
          :key="page"
          :class="[
            'pagination-button',
            'page-number',
            { active: page === props.currentPage },
          ]"
          @click="goToPage(page)"
        >
          {{ page }}
        </button>
      </template>

      <!-- sliding window + ellipses when many pages -->
      <div v-else class="pagination--button-wrapper">
        <div>
          <!-- first page + left ellipsis -->
          <button
            v-if="getVisiblePageNumbers()[0] > 1"
            class="pagination-button page-number"
            @click="goToPage(1)"
          >
            1
          </button>
          <span
            v-if="getVisiblePageNumbers()[0] > 2"
            class="pagination-ellipsis"
            >…</span
          >

          <!-- middle pages -->
          <button
            v-for="page in getVisiblePageNumbers()"
            :key="page"
            :class="[
              'pagination-button',
              'page-number',
              { active: page === props.currentPage },
            ]"
            @click="goToPage(page)"
          >
            {{ page }}
          </button>

          <!-- right ellipsis + last page -->
          <span
            v-if="
              getVisiblePageNumbers()[getVisiblePageNumbers().length - 1] <
              props.totalPages - 1
            "
            class="pagination-ellipsis"
            >…</span
          >
          <button
            v-if="
              getVisiblePageNumbers()[getVisiblePageNumbers().length - 1] <
              props.totalPages
            "
            class="pagination-button page-number"
            @click="goToPage(props.totalPages)"
          >
            {{ props.totalPages }}
          </button>
        </div>
        <div class="pagination--input">
          <input
            type="number"
            v-model.number="pageInput"
            @keyup.enter="onGo"
            :min="1"
            :max="props.totalPages"
            placeholder="…"
            class="pagination-input-field"
          />
          <button
            class="pagination-button"
            @click="onGo"
            :disabled="
              !pageInput || pageInput < 1 || pageInput > props.totalPages
            "
          >
            {{ t("go") }}
          </button>
        </div>
      </div>
    </div>

    <button
      class="pagination-button"
      @click="goToPage(currentPage + 1)"
      :disabled="currentPage >= totalPages"
    >
      {{ t("next") }}
    </button>
  </div>
</template>

<style scoped>
.pagination {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: var(--bgc-table-row-bg);
  padding: 0.75rem 1.5rem;
  border-bottom-left-radius: 8px;
  border-bottom-right-radius: 8px;
}

.pagination-button {
  background: transparent;
  border-radius: 4px;
  padding: 0.25rem 0.75rem;
  margin: 0 0.25rem;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.875rem;
  color: var(--font-color-contrast-high);
}
.pagination-button:hover:not(.page-number) {
  text-decoration: underline;
}

.pagination-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-number {
  border: 1px solid transparent;
  color: var(--font-color-contrast-high);
}
.page-number.active {
  background-color: var(--pagination-active-bg);
  background-color: color-mix(
    in srgb,
    var(--bgc-pagination-button-bg) 80%,
    var(--font-color-contrast-high) 20%
  );
  color: var(--font-color-contrast-high);
  border-color: color-mix(
    in srgb,
    var(--bgc-pagination-button-bg) 80%,
    var(--font-color-contrast-high) 50%
  );
}
.page-number:focus {
  border: 1px solid var(--color-focus);
  outline: 1px solid var(--color-focus);
}
.page-number:hover {
  background-color: color-mix(
    in srgb,
    var(--bgc-pagination-button-bg) 80%,
    var(--font-color-contrast-high) 10%
  );
}

.pagination-ellipsis {
  margin: 0 0.25rem;
}

.pagination--button-wrapper {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 1rem;
}
.pagination {
  &--button-wrapper {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 1rem;
  }
  &--input {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-left: auto;
  }
}
</style>
