<template>
  <div class="user-table">
    <div class="table-header">
      <TableSearch
        v-model:value="searchQuery"
        :placeholder="t('searchPlaceholder')"
      />
    </div>

    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>{{ t("username") }}</th>
            <th>{{ t("firstname") }}</th>
            <th>{{ t("lastname") }}</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <template v-if="loading">
            <tr>
              <td colspan="4">
                <div class="loading">{{ t("loading") }}</div>
              </td>
            </tr>
          </template>
          <template v-else-if="filteredUsers.length === 0">
            <tr>
              <td colspan="4">
                <div class="no-results">
                  {{ t("noResults") }}
                </div>
              </td>
            </tr>
          </template>
          <template v-else>
            <tr v-for="user in paginatedUsers" :key="user.username">
              <td>{{ user.username }}</td>
              <td>{{ user.firstname }}</td>
              <td>{{ user.lastname }}</td>
              <td>
                <SimpleButton
                  :label="t('actionButtonLabel')"
                  variant="primary"
                  @click="handleButtonClick(user)"
                />
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>

    <TablePagination
      :current-page="currentPage"
      :total-pages="totalPages"
      @page-change="handlePageChange"
    />

    <Modal :isOpen="isModalOpen" @close="closeModal">
      <template #header>
        <h3 class="modal-title">
          {{ t("lostTokenTitle") }}
          {{ selectedUser?.firstname }}
          {{ selectedUser?.lastname }}
        </h3>
      </template>
      <div>
        {{ t("lostTokenMessage") }}
        {{ selectedUser?.firstname }} {{ selectedUser?.lastname }}
        {{ t("willBeReported") }}
      </div>
      <template #footer>
        <div class="modal-buttons">
          <SimpleButton
            :label="t('cancelButton')"
            variant="secondary"
            @click="closeModal"
            :disabled="isTokenResetting"
          />
          <SimpleButton
            :label="t('resetTokenButton')"
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
import { ref, computed, watch } from "vue";
import { type UserData } from "../../types";
import TablePagination from "./TablePagination.vue";
import TableSearch from "./TableSearch.vue";
import SimpleButton from "../Button.vue";
import Modal from "../Modal.vue";
import { resetUserToken } from "../../services/reset-user-token";
import { useTranslations } from "../../composables/useTranslations";

const props = withDefaults(
  defineProps<{
    title?: string;
    users?: UserData[];
    pageSize?: number;
    loading?: boolean;
    language?: string;
  }>(),
  {
    pageSize: 10,
    loading: false,
    language: "de",
  }
);

const { t: tComputed } = useTranslations();
const t = (key) => tComputed.value(key);

const searchQuery = ref("");
const currentPage = ref(1);
const isModalOpen = ref(false);
const selectedUser = ref<UserData | null>(null);
const isTokenResetting = ref(false);

const filteredUsers = computed(() => {
  if (!props.users || !searchQuery.value) {
    return props.users || [];
  }

  const query = searchQuery.value.toLowerCase();
  return props.users.filter((user) => {
    return (
      user.username.toLowerCase().includes(query) ||
      user.firstname.toLowerCase().includes(query) ||
      user.lastname.toLowerCase().includes(query)
    );
  });
});

const totalPages = computed(() => {
  return Math.ceil(filteredUsers.value.length / props.pageSize);
});

const paginatedUsers = computed(() => {
  const startIndex = (currentPage.value - 1) * props.pageSize;
  const endIndex = startIndex + props.pageSize;
  return filteredUsers.value.slice(startIndex, endIndex);
});

watch(searchQuery, () => {
  currentPage.value = 1;
});

const handlePageChange = (page: number) => {
  currentPage.value = page;
};

const handleButtonClick = (user: UserData) => {
  selectedUser.value = user;
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
  selectedUser.value = null;
};

const resetToken = () => {
  if (!selectedUser.value) return;
  isTokenResetting.value = true;

  const successMsg = t("tokenResetSuccess");
  const errorMsg = t("tokenResetError");

  resetUserToken(
    selectedUser.value,
    () => {
      isTokenResetting.value = false;
      closeModal();
    },
    successMsg,
    errorMsg
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

.loading,
.no-results {
  padding: 2rem 0;
  text-align: center;
  color: var(--text-color-muted);
}

th:nth-child(1),
td:nth-child(1) {
  /* Username column */
  width: 30%;
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
