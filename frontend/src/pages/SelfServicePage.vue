<template>
  <div class="self-service-page">
    <div class="page-header">
      <h1>{{ t("selfServiceTitle") }}</h1>
      <LanguageSelector @change="handleLanguageChange" />
    </div>

    <div class="token-reset-container">
      <div class="token-reset-text">
        {{ t("resetOwnTokenQuestion") }}
      </div>

      <div class="checkbox-container">
        <input
          type="checkbox"
          id="confirm-reset"
          v-model="confirmReset"
          class="reset-checkbox"
        />
        <label for="confirm-reset">{{ t("confirmResetLabel") }}</label>
      </div>

      <SimpleButton
        :label="t('resetTokenButton')"
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
import LanguageSelector from "../components/LanguageSelector.vue";
import { useTranslations } from "../composables/useTranslations";
import { Configuration, DefaultApi } from "../../api";

const confirmReset = ref(false);
const isResetting = ref(false);

const { setLanguage, t } = useTranslations();

const handleLanguageChange = (lang: string) => {
  setLanguage(lang);
};

const resetOwnToken = () => {
  if (isResetting.value || !confirmReset.value) {
    return;
  }

  isResetting.value = true;
  const config = new Configuration({
    basePath: import.meta.env.VITE_API_URL,
    accessToken: () => `Bearer ${import.meta.env.VITE_API_TOKEN || ""}`,
  });

  const apiClient = new DefaultApi(config);

  apiClient
    .resetOwnTokenTokenResetOwnPost()
    .then((result) => {
      console.log("Token reset successful:", result);
      alert(t.value("tokenResetSuccess"));
      confirmReset.value = false;
    })
    .catch((error) => {
      console.error("Error resetting token:", error);
      alert(t.value("tokenResetError"));
    })
    .then(() => {
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
