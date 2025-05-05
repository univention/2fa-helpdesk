<template>
  <div class="self-service-page">
    <h1>Self Service</h1>

    <div class="token-reset-container">
      <div class="token-reset-text">
        Wollen Sie ihren eigenen Token zurücksetzen?
      </div>

      <div class="checkbox-container">
        <input
          type="checkbox"
          id="confirm-reset"
          v-model="confirmReset"
          class="reset-checkbox"
        />
        <label for="confirm-reset"
          >Ja, ich möchte meinen Token zurücksetzen.</label
        >
      </div>

      <SimpleButton
        label="Token zurücksetzen"
        variant="primary"
        :disabled="!confirmReset"
        :loading="isResetting"
        @click="resetOwnToken"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import SimpleButton from "../components/Button.vue";

const confirmReset = ref(false);
const isResetting = ref(false);

const resetOwnToken = () => {
  if (isResetting.value || !confirmReset.value) {
    return;
  }

  isResetting.value = true;

  fetch("/backend/token/reset/own/", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token") || ""}`,
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.json();
    })
    .then((result) => {
      console.log("Token reset successful:", result);
      alert("Ihr Token wurde erfolgreich zurückgesetzt.");
      confirmReset.value = false;
    })
    .catch((error) => {
      console.error("Error resetting token:", error);
      alert(
        "Fehler beim Zurücksetzen des Tokens. Bitte versuchen Sie es erneut."
      );
    })
    .finally(() => {
      isResetting.value = false;
    });
};
</script>

<style scoped>
.self-service-page {
  text-align: center;
  margin-top: 2rem;
}

.token-reset-container {
  max-width: 500px;
  margin: 2rem auto;
  text-align: left;
  padding: 1.5rem;
  border-radius: 8px;
  background-color: var(--modal-content-bg);
  box-shadow: 0 2px 4px var(--modal-content-shadow);
}

.token-reset-text {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: var(--text-color-default);
}

.checkbox-container {
  display: flex;
  align-items: center;
  margin-bottom: 1.5rem;
}

.reset-checkbox {
  width: 18px;
  height: 18px;
  margin-right: 0.75rem;
  cursor: pointer;
}

label {
  cursor: pointer;
  color: var(--text-color-default);
}
</style>
