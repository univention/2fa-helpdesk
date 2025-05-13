<script setup lang="ts">
import { ref, onMounted } from "vue";
import UserTable from "./table/UserTable.vue";
import PageHeadline from "./PageHeadline.vue";
import LanguageSelector from "./LanguageSelector.vue";
import { type UserData } from "../types";
import { useUsers } from "../composables/useUsers";
import { Translations, useTranslations } from "../composables/useTranslations";

const { users, searchQuery, loading, currentPage, totalPages, fetchUsers } =
  useUsers();

const { currentLanguage, setLanguage, t: tComputed } = useTranslations();
const t = (key: keyof Translations["de"]) => tComputed.value(key);

const selectedUsers = ref<UserData[]>([]);

const handleSelectedUsers = (selected: UserData[]) => {
  selectedUsers.value = selected;
};

const handleLanguageChange = (lang: string) => {
  setLanguage(lang);
};

onMounted(() => {
  fetchUsers(0);
});
</script>

<template>
  <div class="users-overview-page">
    <div class="page-header">
      <PageHeadline :text="t('adminPageTitle')" />
      <LanguageSelector @change="handleLanguageChange" />
    </div>
    <p class="description">
      {{ t("adminPageDescription") }}
    </p>
    <UserTable
      v-model:search-query="searchQuery"
      :users="users"
      :loading="loading"
      :current-page="currentPage"
      :total-pages="totalPages"
      @select-users="handleSelectedUsers"
      :language="currentLanguage"
      :fetchUsers="fetchUsers"
    />
  </div>
</template>

<style scoped>
.users-overview-page {
  padding: 1rem;
  max-width: 1200px;
  margin: 0 auto;
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
  margin-bottom: 2.5rem;
}
</style>
