<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import UserTable from "./table/UserTable.vue";
import PageHeadline from "./PageHeadline.vue";
import LanguageSelector from "./LanguageSelector.vue";
import { type UserData } from "../types";
import { useUsers } from "../composables/useUsers";
import { useTranslations } from "../composables/useTranslations";

const { users, loading, fetchUsers } = useUsers();
const { currentLanguage, setLanguage } = useTranslations();

const selectedUsers = ref<UserData[]>([]);

const adminPageTitle = computed(() => {
  return currentLanguage.value === "en"
    ? "Two-Factor Authentication Administration"
    : "Administration Zwei-Faktor-Authentifizierung";
});

const adminPageDescription = computed(() => {
  return currentLanguage.value === "en"
    ? "Select an entry and click one of the buttons that appear to generate tokens."
    : "Wählen Sie einen Eintrag aus und klicken Sie auf eine der dann erscheinenden Schaltflächen, um Token zu generieren.";
});

const handleSelectedUsers = (selected: UserData[]) => {
  selectedUsers.value = selected;
  console.log("Selected users:", selected);
};

const handleLanguageChange = (lang: string) => {
  setLanguage(lang);
  localStorage.setItem("language", lang);
};

onMounted(fetchUsers);
</script>

<template>
  <div class="users-overview-page">
    <div class="page-header">
      <PageHeadline :text="adminPageTitle" />
      <LanguageSelector @change="handleLanguageChange" />
    </div>
    <p class="description">
      {{ adminPageDescription }}
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

.actions {
  margin-top: 1rem;
  display: flex;
  justify-content: flex-end;
}

.action-button {
  background-color: #42b883;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.action-button:hover {
  background-color: #369e6c;
}
</style>
