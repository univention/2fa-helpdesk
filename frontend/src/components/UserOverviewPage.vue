<!--
 SPDX-License-Identifier: AGPL-3.0-only
 SPDX-FileCopyrightText: 2026 Univention GmbH
-->

<script setup lang="ts">
import { ref, onBeforeUnmount, onMounted } from "vue";
import UserTable from "./table/UserTable.vue";
import PageHeadline from "./PageHeadline.vue";
import LanguageSelector from "./LanguageSelector.vue";
import { type UserData } from "../types";
import { useUsers } from "../composables/useUsers";
import { Translations, useTranslations } from "../composables/useTranslations";

const {
  users,
  searchQuery,
  searchTooShort,
  loading,
  loadingMore,
  hasNextPage,
  fetchUsers,
  loadMore,
} = useUsers();

const { currentLanguage, setLanguage, t: tComputed } = useTranslations();
const t = (key: keyof Translations["de"]) => tComputed.value(key);

// Everything above the rows stays put while they are scrolled. The search
// field and the column row stack below this block, so they need to know how
// tall it is. Publishing it as a custom property lets them read it without
// the table knowing anything about the page around it.
const moduleHeader = ref<HTMLElement | null>(null);
const moduleHeaderHeight = ref(0);
let moduleHeaderResizeObserver: ResizeObserver | null = null;

onMounted(() => {
  if (!moduleHeader.value) return;
  moduleHeaderResizeObserver = new ResizeObserver(([entry]) => {
    moduleHeaderHeight.value = (entry.target as HTMLElement).offsetHeight;
  });
  moduleHeaderResizeObserver.observe(moduleHeader.value);
});

onBeforeUnmount(() => {
  moduleHeaderResizeObserver?.disconnect();
  moduleHeaderResizeObserver = null;
});

const selectedUsers = ref<UserData[]>([]);

const handleSelectedUsers = (selected: UserData[]) => {
  selectedUsers.value = selected;
};

const handleLanguageChange = (lang: string) => {
  setLanguage(lang);
};

onMounted(() => {
  fetchUsers();
});
</script>

<template>
  <div
    class="users-overview-page"
    :style="{ '--module-header-height': `${moduleHeaderHeight}px` }"
  >
    <div class="module-header" ref="moduleHeader">
      <div class="page-header">
        <PageHeadline :text="t('adminPageTitle')" />
        <LanguageSelector @change="handleLanguageChange" />
      </div>
      <p class="description">
        {{ t("adminPageDescription") }}
      </p>
    </div>
    <UserTable
      v-model:search-query="searchQuery"
      :users="users"
      :loading="loading"
      :loading-more="loadingMore"
      :search-too-short="searchTooShort"
      :has-next-page="hasNextPage"
      @select-users="handleSelectedUsers"
      @load-more="loadMore"
      :language="currentLanguage"
    />
  </div>
</template>

<style scoped>
.users-overview-page {
  /* The top spacing belongs to .module-header, which keeps it while stuck. */
  padding: 0 1rem 1rem;
  max-width: 1200px;
  margin: 0 auto;
}

.module-header {
  position: sticky;
  top: 0;
  z-index: 3;
  padding-top: 1rem;
  padding-bottom: 0.5rem;
  background-color: var(--bgc-content-body);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.description {
  text-align: left;
  font-weight: 600;
  margin-bottom: 0;
}
</style>
