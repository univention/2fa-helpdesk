<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import {
  getCoreRowModel,
  getPaginationRowModel,
  getFilteredRowModel,
  useVueTable,
  type ColumnDef,
} from "@tanstack/vue-table";
import { type UserData } from "../types";
import TablePagination from "./TablePagination.vue";
import TableSearch from "./TableSearch.vue";
import PageHeadline from "./PageHeadline.vue";

// Props for the component
const props = withDefaults(
  defineProps<{
    title?: string;
    users?: UserData[];
    pageSize?: number;
    loading?: boolean;
  }>(),
  {
    title: "Administration Zwei-Faktor-Authentifizierung",
    pageSize: 10,
    loading: false,
  }
);

// Emits for handling selections and other events
const emit = defineEmits<{
  (e: "select-users", users: UserData[]): void;
}>();

// Search state
const searchQuery = ref("");

// Selected rows state
const selectedRows = ref<UserData[]>([]);

// Toggle selection for a specific row
const toggleRowSelection = (user: UserData) => {
  const isSelected = selectedRows.value.some(
    (selected) => selected.username === user.username
  );

  if (isSelected) {
    selectedRows.value = selectedRows.value.filter(
      (selected) => selected.username !== user.username
    );
  } else {
    selectedRows.value.push(user);
  }

  emit("select-users", selectedRows.value);
};

// Toggle selection for all rows on the current page
const toggleSelectAll = (selected: boolean) => {
  if (selected) {
    // Add all page rows that aren't already selected
    table.value.getRowModel().rows.forEach((row) => {
      if (
        !selectedRows.value.some(
          (selected) => selected.username === row.original.username
        )
      ) {
        selectedRows.value.push(row.original);
      }
    });
  } else {
    // Remove all page rows from selection
    selectedRows.value = selectedRows.value.filter((selected) => {
      return !table.value
        .getRowModel()
        .rows.some((row) => row.original.username === selected.username);
    });
  }

  emit("select-users", selectedRows.value);
};

// Check if all rows on the current page are selected
const areAllRowsSelected = computed(() => {
  if (!table.value?.getRowModel().rows.length) return false;

  return table.value.getRowModel().rows.every((row) => {
    return selectedRows.value.some(
      (selected) => selected.username === row.original.username
    );
  });
});

const columns = [
  {
    id: "select",
    header: () => "Select",
    cell: ({ row }) => row.original,
    enableSorting: false,
  },

  {
    accessorKey: "username",
    header: "Benutzername",
    cell: (info) => info.getValue(),
  },

  {
    accessorKey: "firstName",
    header: "Vorname",
    cell: (info) => info.getValue(),
  },

  {
    accessorKey: "lastName",
    header: "Nachname",
    cell: (info) => info.getValue(),
  },
] as ColumnDef<UserData>[];

// Create the table instance
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

// Set the global filter value
function setGlobalFilter(value: string) {
  searchQuery.value = value;
}

// Set the page size when pageSize prop changes
function updateTablePageSize() {
  table.value.setPageSize(props.pageSize);
}

// Handle page change from pagination component
const handlePageChange = (page: number) => {
  table.value.setPageIndex(page - 1); // TanStack uses 0-based index
};

// Initialize and update the table when props change
onMounted(() => {
  updateTablePageSize();
});
</script>

<template>
  <div class="user-table">
    <!-- Table title -->
    <PageHeadline :text="title" :level="2" />

    <p>
      Wählen Sie einen Eintrag aus und klicken Sie auf eine der dann
      erscheinenden Schaltflächen, um Token zu generieren.
    </p>

    <!-- Search input -->
    <TableSearch v-model:value="searchQuery" />

    <!-- Table wrapper -->
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <!-- Custom checkbox header column -->
            <th class="select-column">
              <div class="checkbox-wrapper">
                <input
                  type="checkbox"
                  :checked="areAllRowsSelected"
                  @change="(e) => toggleSelectAll(e?.target?.checked)"
                />
              </div>
            </th>
            <!-- Regular column headers -->
            <th
              v-for="header in table.getHeaderGroups()[0].headers.slice(1)"
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
              <td colspan="4" class="text-center">
                <div class="loading">Loading...</div>
              </td>
            </tr>
          </template>
          <template v-else-if="table.getRowModel().rows.length === 0">
            <tr>
              <td colspan="4" class="text-center">
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
                  (selected) => selected.username === row.original.username
                ),
              }"
            >
              <!-- Custom checkbox cell -->
              <td class="select-column">
                <div class="checkbox-wrapper">
                  <input
                    type="checkbox"
                    :checked="
                      selectedRows.some(
                        (selected) =>
                          selected.username === row.original.username
                      )
                    "
                    @change="() => toggleRowSelection(row.original)"
                  />
                </div>
              </td>
              <!-- Regular data cells -->
              <td v-for="cell in row.getVisibleCells().slice(1)" :key="cell.id">
                {{ cell.getValue() }}
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>

    <!-- Pagination -->
    <TablePagination
      :current-page="table.getState().pagination.pageIndex + 1"
      :total-pages="table.getPageCount()"
      @page-change="handlePageChange"
    />
  </div>
</template>

<style scoped>
.user-table {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

.table-wrapper {
  overflow-x: auto;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  margin-bottom: 1rem;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

thead {
  background-color: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

th {
  padding: 0.75rem 1rem;
  text-align: left;
  font-weight: 600;
  color: #475569;
  white-space: nowrap;
}

td {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #e2e8f0;
}

tbody tr:last-child td {
  border-bottom: none;
}

tr:hover {
  background-color: #f1f5f9;
}

tr.selected {
  background-color: rgba(66, 184, 131, 0.1);
}

.checkbox-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
}

input[type="checkbox"] {
  width: 16px;
  height: 16px;
  cursor: pointer;
}

.loading,
.no-results {
  padding: 2rem 0;
  text-align: center;
  color: #64748b;
}

.text-center {
  text-align: center;
}

.select-column {
  width: 40px;
  text-align: center;
}
</style>
