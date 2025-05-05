<template>
  <div class="user-table">
    <TableSearch v-model:value="searchQuery" />

    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th
              v-for="header in table.getHeaderGroups()[0].headers"
              :key="header.id"
            >
              <div v-if="header.isPlaceholder" />
              <template v-else>
                {{ header.column.columnDef.header }}
              </template>
            </th>
          </tr>
        </thead>
        <tbody>
          <template v-if="loading">
            <tr>
              <td colspan="4" class="">
                <div class="loading">Loading...</div>
              </td>
            </tr>
          </template>
          <template v-else-if="table.getRowModel().rows.length === 0">
            <tr>
              <td colspan="4" class="">
                <div class="no-results">Keine Ergebnisse gefunden</div>
              </td>
            </tr>
          </template>
          <template v-else>
            <tr
              v-for="row in table.getRowModel().rows"
              :key="row.id"
              :class="{
                selected: selectedRows.some(
                  (selected: UserData) =>
                    selected.username === row.original.username
                ),
              }"
            >
              <td v-for="cell in row.getVisibleCells()" :key="cell.id">
                <template v-if="cell.column.id === 'action'">
                  <SimpleButton
                    label="Action"
                    variant="primary"
                    @click="handleButtonClick(row.original)"
                  />
                </template>

                <template v-else>
                  {{ cell.getValue() }}
                </template>
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>

    <TablePagination
      :current-page="table.getState().pagination.pageIndex + 1"
      :total-pages="table.getPageCount()"
      @page-change="handlePageChange"
    />

    <Modal :isOpen="isModalOpen" @close="closeModal">
      <template #header>
        <h3 class="modal-title">
          Verlorener Token von {{ selectedUser?.firstname }}
          {{ selectedUser?.lastname }}
        </h3>
      </template>
      <div>
        Das Gerät mit dem Zwei-Faktor-Token von {{ selectedUser?.firstname }}
        {{ selectedUser?.lastname }} wird als verloren gemeldet.
      </div>
      <template #footer>
        <div class="modal-buttons">
          <SimpleButton
            label="Abbrechen"
            variant="secondary"
            @click="closeModal"
            :disabled="isTokenResetting"
          />
          <SimpleButton
            label="Token zurücksetzen"
            variant="primary"
            @click="resetToken"
            :loading="isTokenResetting"
          />
        </div>
      </template>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import {
  getCoreRowModel,
  getPaginationRowModel,
  getFilteredRowModel,
  useVueTable,
  type ColumnDef,
} from "@tanstack/vue-table";
import { type UserData } from "../../types";
import TablePagination from "./TablePagination.vue";
import TableSearch from "./TableSearch.vue";
import SimpleButton from "../Button.vue";
import Modal from "../Modal.vue";
import { resetUserToken } from "../../services/reset-user-token";

const props = withDefaults(
  defineProps<{
    title?: string;
    users?: UserData[];
    pageSize?: number;
    loading?: boolean;
  }>(),
  {
    pageSize: 10,
    loading: false,
  }
);

const searchQuery = ref("");

const selectedRows = ref<UserData[]>([]);

const isModalOpen = ref(false);
const selectedUser = ref<UserData | null>(null);
const isTokenResetting = ref(false);

const columns = [
  {
    accessorKey: "username",
    header: "Benutzername",
    cell: (info) => info.getValue(),
  },
  {
    accessorKey: "firstname",
    header: "Vorname",
    cell: (info) => info.getValue(),
  },
  {
    accessorKey: "lastname",
    header: "Nachname",
    cell: (info) => info.getValue(),
  },
  {
    id: "action",
    header: "",
    cell: () => null,
  },
] as ColumnDef<UserData>[];

const table = ref(
  useVueTable({
    get data() {
      return props.users || [];
    },
    columns,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    onGlobalFilterChange: setGlobalFilter,
    state: {
      get globalFilter() {
        return searchQuery.value;
      },
    },
  })
);

function setGlobalFilter(value: string) {
  searchQuery.value = value;
}

function updateTablePageSize() {
  table.value.setPageSize(props.pageSize);
}

const handlePageChange = (page: number) => {
  table.value.setPageIndex(page - 1);
};

onMounted(() => {
  updateTablePageSize();
});

const lastActiveElement = ref<HTMLElement | null>(null);

const handleButtonClick = (user: UserData) => {
  console.log("Button clicked for user:", user);

  lastActiveElement.value = document.activeElement as HTMLElement;
  selectedUser.value = user;
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
  selectedUser.value = null;

  setTimeout(() => {
    if (lastActiveElement.value) {
      lastActiveElement.value.focus();
    }
  }, 10);
};

const resetToken = () => {
  if (!selectedUser.value) return;
  isTokenResetting.value = true;
  resetUserToken(selectedUser.value, () => {
    isTokenResetting.value = false;
    closeModal();
  });
};
</script>

<style scoped>
.user-table {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

.table-wrapper {
  overflow-x: auto;
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
  margin-bottom: 2px;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

thead {
  background-color: var(--table-header-bg);
  border-bottom: 2px solid var(--table-border-color);
}

th {
  padding: 0.75rem 1rem;
  text-align: left;
  font-weight: 600;
  color: var(--table-header-text);
  white-space: nowrap;
}

td {
  padding: 0.75rem 1rem;
  border-bottom: 2px solid var(--table-border-color);
  text-align: left;
  vertical-align: middle;
  overflow: hidden;
  white-space: nowrap;
  box-sizing: border-box;
}

tbody tr:last-child td {
  border-bottom: none;
}

tbody tr:hover {
  background-color: var(--table-row-hover-bg);
}

tr {
  height: 3.75rem;
  max-height: 3.75rem;
  box-sizing: border-box;
  background-color: var(--table-row-bg);
}
tr.selected {
  background-color: var(--table-row-selected-bg);
}

.checkbox-wrapper {
  display: flex;
  align-items: left;
  justify-content: left;
}

input[type="checkbox"] {
  width: 16px;
  height: 16px;
  cursor: pointer;
}

tbody .loading,
tbody .no-results {
  padding: 2rem 0;
  text-align: center;
  color: var(--text-color-muted);
}

tbody tr:has(.loading):hover,
tbody tr:has(.no-results):hover,
.loading:hover,
.no-results:hover {
  background-color: var(--table-row-bg);
}

.select-column {
  width: 40px;
  text-align: center;
}

th:nth-child(2),
td:nth-child(2) {
  /* Firstname column */
  width: 25%;
}

th:nth-child(3),
td:nth-child(3) {
  /* Lastname column */
  width: 25%;
}

th:nth-child(4),
td:nth-child(4) {
  /* Action column */
  width: 15%;
  text-align: center;
}

td:nth-child(4) .button {
  height: 2rem;
  padding: 0.25rem 0.75rem;
  font-size: 0.875rem;
  margin: 0;
}

.modal-buttons {
  display: flex;
  gap: 1rem;
  justify-content: right;
  align-items: center;
  width: 100%;
}

.modal-title {
  color: var(--modal-title-text);
  font-weight: 500;
}
</style>
