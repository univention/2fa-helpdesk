<script setup lang="ts">
import { ref, onMounted } from "vue";
import UserTable from "./table/UserTable.vue";
import PageHeadline from "./PageHeadline.vue";
import { type UserData } from "../types";

// Sample user data to demonstrate the table
const users = ref<UserData[]>([
  { username: "tante_anna", firstName: "Anna", lastName: "Müller" },
  { username: "sonnenschein", firstName: "Frida", lastName: "Schmidt" },
  { username: "kfz-chef", firstName: "Markus", lastName: "Heinz" },
  { username: "benutzer123", firstName: "Thomas", lastName: "Weber" },
  { username: "tech_guru", firstName: "Laura", lastName: "Fischer" },
  { username: "buchfreund", firstName: "Stefan", lastName: "Meyer" },
  { username: "sportfan", firstName: "Julia", lastName: "Wagner" },
  { username: "naturliebhaber", firstName: "Michael", lastName: "Becker" },
  { username: "filmkenner", firstName: "Sarah", lastName: "Schulz" },
  { username: "musikexperte", firstName: "Daniel", lastName: "Hoffmann" },
  { username: "reisefreund", firstName: "Nicole", lastName: "Koch" },
  { username: "kochlustiger", firstName: "Andreas", lastName: "Richter" },
]);

const loading = ref(true);
const selectedUsers = ref<UserData[]>([]);


const handleSelectedUsers = (selected: UserData[]) => {
  selectedUsers.value = selected;
  console.log("Selected users:", selected);
};

const handleResetToken = () => {

  // console.log("Reset Token from:", selected.username);
};


onMounted(() => {
  setTimeout(() => {
    loading.value = false;
  }, 1000);
});
</script>

<template>
  <div class="users-overview-page">
    <PageHeadline text="Administration Zwei-Faktor-Authentifizierung" />
    <p class="description">
      Wählen Sie einen Eintrag aus und klicken Sie auf eine der dann
      erscheinenden Schaltflächen, um Token zu generieren.
    </p>
    <UserTable
      :users="users"
      :loading="loading"
      :page-size="12"
      @select-users="handleSelectedUsers"
      @handle-reset-token="handleResetToken"
    
    />
  </div>
</template>

<style scoped>
.users-overview-page {
  padding: 1rem;
  max-width: 1200px;
  margin: 0 auto;
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
