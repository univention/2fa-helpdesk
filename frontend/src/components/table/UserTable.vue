<!--
 SPDX-License-Identifier: AGPL-3.0-only
 SPDX-FileCopyrightText: 2025 Univention GmbH
-->

<template>
  <div
    class="user-table"
    :style="{ '--table-header-height': `${tableHeaderHeight}px` }"
  >
    <div class="table-header" ref="tableHeader">
      <div class="search-column">
        <TableSearch
          :value="props.searchQuery ?? ''"
          @update:value="onSearchInput"
          :placeholder="t('searchPlaceholder')"
        />
        <p v-if="searchTooShort" class="search-hint">
          {{ t("searchMinChars") }}
        </p>
      </div>
    </div>

    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>{{ t("username") }}</th>
            <th>{{ t("firstname") }}</th>
            <th>{{ t("lastname") }}</th>
            <th>{{ t("actions") }}</th>
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
          <template v-else-if="users?.length === 0">
            <tr>
              <td colspan="4">
                <div class="no-results">
                  {{ t("noResults") }}
                </div>
              </td>
            </tr>
          </template>
          <template v-else>
            <tr v-for="user in users" :key="user.keycloak_internal_id">
              <td>{{ user.username }}</td>
              <td>{{ user.firstname }}</td>
              <td>{{ user.lastname }}</td>
              <td>
                <SimpleButton
                  :label="t('resetTokenButton')"
                  :variant="user.totp ? 'primary' : 'secondary'"
                  :disabled="!user.totp"
                  :title="!user.totp ? t('noTotpConfigured') : undefined"
                  @click="handleButtonClick(user)"
                  :aria-label="`${user.firstname} ${user.lastname}, ${user.username} : ${
                    user.totp ? t('resetTokenButton') : t('noTotpConfigured')
                  }`"
                />
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>

    <TableLoadMore
      v-if="!loading && !searchTooShort && users?.length"
      :has-next-page="hasNextPage ?? false"
      :loading-more="loadingMore"
      @load-more="emit('load-more')"
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
import { onBeforeUnmount, onMounted, ref } from "vue";
import { type UserData } from "../../types";
import TableLoadMore from "./TableLoadMore.vue";
import TableSearch from "./TableSearch.vue";
import SimpleButton from "../Button.vue";
import Modal from "../Modal.vue";
import { resetUserToken } from "../../services/reset-user-token";
import {
  Locale,
  Translations,
  useTranslations,
} from "../../composables/useTranslations";

const props = withDefaults(
  defineProps<{
    title?: string;
    users?: UserData[];
    searchQuery?: string;
    searchTooShort?: boolean;
    loading?: boolean;
    loadingMore?: boolean;
    language?: string;
    hasNextPage?: boolean;
  }>(),
  {
    loading: false,
    loadingMore: false,
    searchTooShort: false,
    language: Locale.DE,
  }
);

const { t: tComputed } = useTranslations();

const t = (key: keyof Translations[Locale]) => tComputed.value(key);

const emit = defineEmits<{
  (e: "update:searchQuery", val: string): void;
  (e: "load-more"): void;
}>();

function onSearchInput(val: string) {
  emit("update:searchQuery", val);
}
// The column row sticks directly below the search header, whose height
// changes when the "minimum characters" hint appears. Measuring it keeps the
// two from overlapping or leaving a gap between them.
const tableHeader = ref<HTMLElement | null>(null);
const tableHeaderHeight = ref(0);
let headerResizeObserver: ResizeObserver | null = null;

onMounted(() => {
  if (!tableHeader.value) return;
  headerResizeObserver = new ResizeObserver(([entry]) => {
    tableHeaderHeight.value = (entry.target as HTMLElement).offsetHeight;
  });
  headerResizeObserver.observe(tableHeader.value);
});

onBeforeUnmount(() => {
  headerResizeObserver?.disconnect();
  headerResizeObserver = null;
});

const isModalOpen = ref(false);
const selectedUser = ref<UserData | null>(null);
const isTokenResetting = ref(false);

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
  padding-bottom: 1rem;
  position: sticky;
  top: var(--module-header-height, 0px);
  z-index: 2;
  background-color: var(--bgc-content-body);
}

.search-column {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.search-hint {
  margin: 0;
  font-size: 0.8125rem;
  font-style: italic;
  color: var(--font-color-contrast-middle);
}

.table-wrapper {
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
  margin-bottom: 2px;
}

@media (max-width: 768px) {
  .table-wrapper {
    overflow-x: auto;
  }
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

thead {
  background-color: var(--bgc-table-row-bg);
}

th {
  padding: 0.75rem 1rem;
  text-align: left;
  font-weight: 600;
  color: var(--font-color-contrast-high);
  white-space: nowrap;
  background-color: var(--bgc-table-row-bg);
  position: sticky;
  top: calc(
    var(--module-header-height, 0px) + var(--table-header-height, 0px)
  );
  z-index: 1;
  box-shadow: inset 0 -2px 0 var(--bgc-table-seperator);
}

td {
  padding: 0.75rem 1rem;
  border-bottom: 2px solid var(--bgc-table-seperator);
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
  background-color: color-mix(
    in srgb,
    var(--bgc-content-container) 80%,
    var(--font-color-contrast-high) 5%
  );
}

tr {
  height: 3.75rem;
  max-height: 3.75rem;
  box-sizing: border-box;
  background-color: var(--bgc-content-container);
}

.loading,
.no-results {
  padding: 2rem 0;
  text-align: center;
  color: var(--font-color-contrast-middle);
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
  color: var(--font-color-contrast-high);
  font-weight: 500;
}
</style>
