<script setup lang="ts">
import { ref, onMounted } from "vue";
import UserTable from "./table/UserTable.vue";
import PageHeadline from "./PageHeadline.vue";
import LanguageSelector from "./LanguageSelector.vue";
import { type UserData } from "../types";
import { useUsers } from "../composables/useUsers";
import { useTranslations } from "../composables/useTranslations";

const { users, loading, fetchUsers } = useUsers();
const { currentLanguage, setLanguage, t: tComputed } = useTranslations();
const t = (key) => tComputed.value(key);

const selectedUsers = ref<UserData[]>([]);

const handleSelectedUsers = (selected: UserData[]) => {
  selectedUsers.value = selected;
  console.log("Selected users:", selected);
};

const handleLanguageChange = (lang: string) => {
  setLanguage(lang);
};

onMounted(fetchUsers);
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
      :users="users"
      :loading="loading"
      :page-size="12"
      @select-users="handleSelectedUsers"
      :language="currentLanguage"
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
