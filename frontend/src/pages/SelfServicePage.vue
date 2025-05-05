<template>
  <div class="self-service-page">
    <div class="page-header">
      <h1>{{ selfServiceTitle }}</h1>
      <LanguageSelector @change="handleLanguageChange" />
    </div>

    <div class="token-reset-container">
      <div class="token-reset-text">
        {{ resetOwnTokenQuestion }}
      </div>

      <div class="checkbox-container">
        <input
          type="checkbox"
          id="confirm-reset"
          v-model="confirmReset"
          class="reset-checkbox"
        />
        <label for="confirm-reset">{{ confirmResetLabel }}</label>
      </div>

      <SimpleButton
        :label="resetTokenButton"
        variant="primary"
        :disabled="!confirmReset"
        :loading="isResetting"
        @click="resetOwnToken"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import SimpleButton from "../components/Button.vue";
import LanguageSelector from "../components/LanguageSelector.vue";

const confirmReset = ref(false);
const isResetting = ref(false);

const currentLanguage = ref(localStorage.getItem("language") || "de");

const translations = {
  de: {
    selfServiceTitle: "Self Service",
    resetOwnTokenQuestion: "Wollen Sie ihren eigenen Token zurücksetzen?",
    confirmResetLabel: "Ja, ich möchte meinen Token zurücksetzen.",
    resetTokenButton: "Token zurücksetzen",
    tokenResetSuccess: "Ihr Token wurde erfolgreich zurückgesetzt.",
    tokenResetError:
      "Fehler beim Zurücksetzen des Tokens. Bitte versuchen Sie es erneut.",
  },
  en: {
    selfServiceTitle: "Self Service",
    resetOwnTokenQuestion: "Do you want to reset your own token?",
    confirmResetLabel: "Yes, I want to reset my token.",
    resetTokenButton: "Reset Token",
    tokenResetSuccess: "Your token has been successfully reset.",
    tokenResetError: "Error resetting token. Please try again.",
  },
};

const selfServiceTitle = computed(
  () => translations[currentLanguage.value as "de" | "en"].selfServiceTitle
);
const resetOwnTokenQuestion = computed(
  () => translations[currentLanguage.value as "de" | "en"].resetOwnTokenQuestion
);
const confirmResetLabel = computed(
  () => translations[currentLanguage.value as "de" | "en"].confirmResetLabel
);
const resetTokenButton = computed(
  () => translations[currentLanguage.value as "de" | "en"].resetTokenButton
);
const tokenResetSuccess = computed(
  () => translations[currentLanguage.value as "de" | "en"].tokenResetSuccess
);
const tokenResetError = computed(
  () => translations[currentLanguage.value as "de" | "en"].tokenResetError
);

const handleLanguageChange = (lang: string) => {
  currentLanguage.value = lang;
  localStorage.setItem("language", lang);
};

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
      alert(tokenResetSuccess.value);
      confirmReset.value = false;
    })
    .catch((error) => {
      console.error("Error resetting token:", error);
      alert(tokenResetError.value);
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

.page-header {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
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
