<template>
  <div class="user-table">
    <!-- Search input -->
    <TableSearch v-model:value="searchQuery" />

    <!-- Table wrapper -->
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <!-- Custom checkbox header column -->
            <th class="select-column"></th>
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
             
              <td v-for="cell in row.getVisibleCells().slice(1)" :key="cell.id">
                {{ cell.getValue() }}
              </td>
              <td v-if="selectedRows.some(selected => selected.username === row.original.username)">
                <SimpleButton
                  label="Action"
                  variant="primary"
                  @click="handleButtonClick(row.original)"
                />
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

// Props for the component
const props = withDefaults(
  defineProps<{
    title?: string;
    users?: UserData[];
    pageSize?: number;
    loading?: boolean;
    handleSelectedUsers?: (selected: UserData[]) => void;
    handleResetToken?: (selected: UserData[]) => void;
  }>(),
  {
    pageSize: 10,
    loading: false,
  }
);


const emit = defineEmits<{
  (e: "select-users", users: UserData[]): void;
}>();

const searchQuery = ref("");

const selectedRows = ref<UserData[]>([]);

  const toggleRowSelection = (user: UserData) => {
  const isSelected = selectedRows.value.some(
    (selected) => selected.username === user.username
  );

  if (isSelected) {
    // If the user is already selected, deselect them
    selectedRows.value = [];
  } else {
    // Clear previous selection and add the new user
    selectedRows.value = [user];
  }

  console.log("Selected Rows:", selectedRows.value); // Debugging
  emit("select-users", selectedRows.value);
};

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
  // {
  //   accessorKey: "action",
  //   header: "",
  //   cell: null,
  // },
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

// Set the global filter value
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

const handleButtonClick = (user: UserData) => {
  console.log("Button clicked for user:", user);
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
  background-color: #ffffff;
  border-bottom: 2px solid #eeeff2;
}

th {
  padding: 0.75rem 1rem;
  text-align: left;
  font-weight: 600;
  color: #203257;
  white-space: nowrap;
}

td {
  padding: 0.75rem 1rem;
  border-bottom: 2px solid #eeeff2;
  text-align: left;
}

tbody tr:last-child td {
  border-bottom: none;
}

tbody tr:hover {
  background-color: #f1eeff;
}

tr {
  background-color: #ffffff;
}
tr.selected {
  background-color: #f1eeff;
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

.loading,
.no-results {
  padding: 2rem 0;
  text-align: center;
  color: #64748b;
}

tbody tr:has(.loading):hover,
tbody tr:has(.no-results):hover,
.loading:hover,
.no-results:hover {
  background-color: #ffffff;
}

.select-column {
  width: 40px;
  text-align: center;
}
</style>
