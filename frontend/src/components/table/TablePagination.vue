<script setup lang="ts">
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

const getVisiblePageNumbers = () => {
  const maxButtons = props.maxPageButtons || 5;
  const halfMaxButtons = Math.floor(maxButtons / 2);

  let startPage = Math.max(props.currentPage - halfMaxButtons, 1);
  let endPage = Math.min(startPage + maxButtons - 1, props.totalPages);

  if (endPage - startPage + 1 < maxButtons) {
    startPage = Math.max(endPage - maxButtons + 1, 1);
  }

  const pages = [];
  for (let i = startPage; i <= endPage; i++) {
    pages.push(i);
  }

  return pages;
};
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
      <template v-if="totalPages <= 7">
        <button
          v-for="page in totalPages"
          :key="page"
          :class="[
            'pagination-button',
            'page-number',
            { active: page === currentPage },
          ]"
          @click="goToPage(page)"
        >
          {{ page }}
        </button>
      </template>

      <template v-else>
        <template v-if="currentPage > 3">
          <button class="pagination-button page-number" @click="goToPage(1)">
            1
          </button>
          <span v-if="currentPage > 4" class="pagination-ellipsis">...</span>
        </template>

        <button
          v-for="page in getVisiblePageNumbers()"
          :key="page"
          :class="[
            'pagination-button',
            'page-number',
            { active: page === currentPage },
          ]"
          @click="goToPage(page)"
        >
          {{ page }}
        </button>

        <template v-if="currentPage < totalPages - 2">
          <span v-if="currentPage < totalPages - 3" class="pagination-ellipsis"
            >...</span
          >
          <button
            class="pagination-button page-number"
            @click="goToPage(totalPages)"
          >
            {{ totalPages }}
          </button>
        </template>
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
</style>
