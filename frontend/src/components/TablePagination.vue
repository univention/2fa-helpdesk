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
  justify-content: center;
  margin: 1rem 0;
}

.pagination-button {
  background: transparent;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 0.25rem 0.75rem;
  margin: 0 0.25rem;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.875rem;
}

.pagination-button:hover:not(:disabled) {
  background-color: #f0f0f0;
}

.pagination-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-number.active {
  background-color: #42b883;
  color: white;
  border-color: #42b883;
}

.pagination-ellipsis {
  margin: 0 0.25rem;
}
</style>
