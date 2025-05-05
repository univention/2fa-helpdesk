import { ref, computed } from "vue";

const translations = {
  de: {
    // Self-Service Page
    selfServiceTitle: "Self Service",
    resetOwnTokenQuestion: "Wollen Sie ihren eigenen Token zurücksetzen?",
    confirmResetLabel: "Ja, ich möchte meinen Token zurücksetzen.",
    resetTokenButton: "Token zurücksetzen",
    tokenResetSuccess: "Ihr Token wurde erfolgreich zurückgesetzt.",
    tokenResetError:
      "Fehler beim Zurücksetzen des Tokens. Bitte versuchen Sie es erneut.",

    // User Table
    username: "Benutzername",
    firstname: "Vorname",
    lastname: "Nachname",
    loading: "Lädt...",
    noResults: "Keine Ergebnisse gefunden",
    action: "Aktion",
    actionButtonLabel: "Aktion",
    lostTokenTitle: "Verlorener Token von",
    lostTokenMessage: "Das Gerät mit dem Zwei-Faktor-Token von",
    cancelButton: "Abbrechen",
    willBeReported: "wird als verloren gemeldet.",
  },
  en: {
    // Self-Service Page
    selfServiceTitle: "Self Service",
    resetOwnTokenQuestion: "Do you want to reset your own token?",
    confirmResetLabel: "Yes, I want to reset my token.",
    resetTokenButton: "Reset Token",
    tokenResetSuccess: "Your token has been successfully reset.",
    tokenResetError: "Error resetting token. Please try again.",

    // User Table
    username: "Username",
    firstname: "First Name",
    lastname: "Last Name",
    loading: "Loading...",
    noResults: "No results found",
    action: "Action",
    actionButtonLabel: "Action",
    lostTokenTitle: "Lost token of",
    lostTokenMessage: "The device with the two-factor token of",
    cancelButton: "Cancel",
    willBeReported: "will be reported as lost.",
  },
};

const currentLanguage = ref(localStorage.getItem("language") || "de");

export function useTranslations() {
  const setLanguage = (lang: string) => {
    currentLanguage.value = lang;
    localStorage.setItem("language", lang);
  };

  const t = computed(() => {
    return (key: keyof (typeof translations)["de"]) => {
      return translations[currentLanguage.value as "de" | "en"][key] || key;
    };
  });

  return {
    currentLanguage,
    setLanguage,
    t,
  };
}
