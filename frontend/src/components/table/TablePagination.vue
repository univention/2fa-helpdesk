<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{
  currentPage: number;
  totalPages: number;
  maxPageButtons?: number;
}>();

const emit = defineEmits<{
  (e: "page-change", page: number): void;
}>();

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
console.log(getVisiblePageNumbers());
</script>

<template>
  <div class="pagination">
    <button
      class="pagination-button"
      @click="goToPage(currentPage - 1)"
      :disabled="currentPage <= 1"
    >
      Zurück
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
      <template v-else>
        <!-- first page + left ellipsis -->
        <button
          v-if="getVisiblePageNumbers()[0] > 1"
          class="pagination-button page-number"
          @click="goToPage(1)"
        >
          1
        </button>
        <span v-if="getVisiblePageNumbers()[0] > 2" class="pagination-ellipsis"
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
          v-if="getVisiblePageNumbers().at(-1)! < props.totalPages - 1"
          class="pagination-ellipsis"
          >…</span
        >
        <button
          v-if="getVisiblePageNumbers().at(-1)! < props.totalPages"
          class="pagination-button page-number"
          @click="goToPage(props.totalPages)"
        >
          {{ props.totalPages }}
        </button>
      </template>
    </div>

    <button
      class="pagination-button"
      @click="goToPage(currentPage + 1)"
      :disabled="currentPage >= totalPages"
    >
      Vor
    </button>
  </div>
</template>

<style scoped>
.pagination {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: var(--pagination-bg);
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
  color: var(--pagination-text);
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
  color: var(--pagination-text);
}
.page-number.active {
  background-color: var(--pagination-active-bg);
  color: var(--pagination-active-text);
  border-color: var(--pagination-active-border);
}

.pagination-ellipsis {
  margin: 0 0.25rem;
}
</style>
