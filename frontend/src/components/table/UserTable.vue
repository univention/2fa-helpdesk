<template>
  <div class="user-table">
    <div class="table-header">
      <TableSearch v-model:value="searchQuery" />
      <LanguageSelector @change="handleLanguageChange" />
    </div>

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
                <div class="loading">{{ loadingText }}</div>
              </td>
            </tr>
          </template>
          <template v-else-if="table.getRowModel().rows.length === 0">
            <tr>
              <td colspan="4" class="">
                <div class="no-results">{{ noResultsText }}</div>
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
                    :label="actionButtonText"
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
          {{ lostTokenTitleText }} {{ selectedUser?.firstname }}
          {{ selectedUser?.lastname }}
        </h3>
      </template>
      <div>
        {{ lostTokenMessageText }} {{ selectedUser?.firstname }}
        {{ selectedUser?.lastname }} {{ willBeReportedText }}
      </div>
      <template #footer>
        <div class="modal-buttons">
          <SimpleButton
            :label="cancelButtonText"
            variant="secondary"
            @click="closeModal"
            :disabled="isTokenResetting"
          />
          <SimpleButton
            :label="resetTokenButtonText"
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
import { ref, onMounted, computed } from "vue";
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
import LanguageSelector from "../LanguageSelector.vue";
import { resetUserToken } from "../../services/reset-user-token";

const currentLanguage = ref(localStorage.getItem("language") || "de");

const translations = {
  de: {
    username: "Benutzername",
    firstname: "Vorname",
    lastname: "Nachname",
    loading: "Lädt...",
    noResults: "Keine Ergebnisse gefunden",
    actionButton: "Aktion",
    lostTokenTitle: "Verlorener Token von",
    lostTokenMessage: "Das Gerät mit dem Zwei-Faktor-Token von",
    willBeReported: "wird als verloren gemeldet.",
    cancelButton: "Abbrechen",
    resetTokenButton: "Token zurücksetzen",
  },
  en: {
    username: "Username",
    firstname: "First Name",
    lastname: "Last Name",
    loading: "Loading...",
    noResults: "No results found",
    actionButton: "Action",
    lostTokenTitle: "Lost token of",
    lostTokenMessage: "The device with the two-factor token of",
    willBeReported: "will be reported as lost.",
    cancelButton: "Cancel",
    resetTokenButton: "Reset Token",
  },
};

const usernameText = computed(
  () => translations[currentLanguage.value as "de" | "en"].username
);
const firstnameText = computed(
  () => translations[currentLanguage.value as "de" | "en"].firstname
);
const lastnameText = computed(
  () => translations[currentLanguage.value as "de" | "en"].lastname
);
const loadingText = computed(
  () => translations[currentLanguage.value as "de" | "en"].loading
);
const noResultsText = computed(
  () => translations[currentLanguage.value as "de" | "en"].noResults
);
const actionButtonText = computed(
  () => translations[currentLanguage.value as "de" | "en"].actionButton
);
const lostTokenTitleText = computed(
  () => translations[currentLanguage.value as "de" | "en"].lostTokenTitle
);
const lostTokenMessageText = computed(
  () => translations[currentLanguage.value as "de" | "en"].lostTokenMessage
);
const willBeReportedText = computed(
  () => translations[currentLanguage.value as "de" | "en"].willBeReported
);
const cancelButtonText = computed(
  () => translations[currentLanguage.value as "de" | "en"].cancelButton
);
const resetTokenButtonText = computed(
  () => translations[currentLanguage.value as "de" | "en"].resetTokenButton
);

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

const handleLanguageChange = (lang: string) => {
  currentLanguage.value = lang;
  localStorage.setItem("language", lang);

  updateColumns();
};

const getColumns = computed(
  () =>
    [
      {
        accessorKey: "username",
        header: usernameText.value,
        cell: (info) => info.getValue(),
      },
      {
        accessorKey: "firstname",
        header: firstnameText.value,
        cell: (info) => info.getValue(),
      },
      {
        accessorKey: "lastname",
        header: lastnameText.value,
        cell: (info) => info.getValue(),
      },
      {
        id: "action",
        header: "",
        cell: () => null,
      },
    ] as ColumnDef<UserData>[]
);

const columns = ref(getColumns.value);

const updateColumns = () => {
  columns.value = getColumns.value;

  table.value = useVueTable({
    data: props.users || [],
    columns: columns.value,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    onGlobalFilterChange: setGlobalFilter,
    state: {
      globalFilter: searchQuery.value,
    },
  });
};

const table = ref(
  useVueTable({
    get data() {
      return props.users || [];
    },
    get columns() {
      return columns.value;
    },
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

  const successMessage =
    currentLanguage.value === "en"
      ? "Token has been successfully reset."
      : "Token wurde erfolgreich zurückgesetzt.";

  const errorMessage =
    currentLanguage.value === "en"
      ? "Error resetting token. Please try again."
      : "Fehler beim Zurücksetzen des Tokens. Bitte versuchen Sie es erneut.";

  resetUserToken(
    selectedUser.value,
    () => {
      isTokenResetting.value = false;
      closeModal();
    },
    successMessage,
    errorMessage
  );
};
</script>

<style scoped>
.user-table {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
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
