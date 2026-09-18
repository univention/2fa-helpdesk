/**
 * SPDX-License-Identifier: AGPL-3.0-only
 * SPDX-FileCopyrightText: 2026 Univention GmbH
 */

import { ref, computed } from "vue";

export enum Locale {
  DE = "de",
  EN = "en",
}

const translations = {
  [Locale.DE]: {
    // Self-Service Page
    selfServiceTitle: "Self Service",
    resetOwnTokenQuestion: "Wollen Sie ihren eigenen Token zurücksetzen?",
    confirmResetLabel: "Ja, ich möchte meinen Token zurücksetzen.",
    resetTokenButton: "Token zurücksetzen",
    tokenResetSuccess: "Der Token wurde erfolgreich zurückgesetzt.",
    tokenResetError:
      "Fehler beim Zurücksetzen des Tokens. Bitte versuchen Sie es erneut.",

    // User Table
    username: "Benutzername",
    firstname: "Vorname",
    lastname: "Nachname",
    actions: "Aktionen",
    noTotpConfigured: "Kein 2FA-Token konfiguriert",
    loading: "Lädt...",
    noResults: "Keine Ergebnisse gefunden",
    action: "Aktion",
    actionButtonLabel: "Aktion",
    lostTokenTitle: "Verlorener Token von",
    lostTokenMessage: "Das Gerät mit dem Zwei-Faktor-Token von",
    cancelButton: "Abbrechen",
    willBeReported: "wird als verloren gemeldet.",
    searchPlaceholder: "Nach Benutzer suchen",

    // User Overview Page
    adminPageTitle: "Administration Zwei-Faktor-Authentifizierung",
    adminPageDescription:
      "Auf eine Schaltfläche klicken, um einen Token zurückzusetzen.",

    // Table footer
    loadMore: "Mehr laden",
    loadMoreHint: "(oder verfeinern Sie Ihre Suche, um die Liste einzugrenzen)",
    noMoreResults: "Keine weiteren Ergebnisse",
    searchMinChars: "Bitte mindestens 5 Zeichen eingeben",
  },
  [Locale.EN]: {
    // Self-Service Page
    selfServiceTitle: "Self Service",
    resetOwnTokenQuestion: "Do you want to reset your own token?",
    confirmResetLabel: "Yes, I want to reset my token.",
    resetTokenButton: "Reset Token",
    tokenResetSuccess: "The token has been successfully reset.",
    tokenResetError: "Error resetting token. Please try again.",

    // User Table
    username: "Username",
    firstname: "First Name",
    lastname: "Last Name",
    actions: "Actions",
    noTotpConfigured: "No 2FA token configured",
    loading: "Loading...",
    noResults: "No results found",
    action: "Action",
    actionButtonLabel: "Action",
    lostTokenTitle: "Lost token of",
    lostTokenMessage: "The device with the two-factor token of",
    cancelButton: "Cancel",
    willBeReported: "will be reported as lost.",
    searchPlaceholder: "Search for user",

    // User Overview Page
    adminPageTitle: "Two-Factor Authentication Administration",
    adminPageDescription: "Click on one of the buttons to reset a token.",

    // Table footer
    loadMore: "Load more",
    loadMoreHint: "(or refine your search to narrow the list)",
    noMoreResults: "No more results",
    searchMinChars: "Please enter at least 5 characters",
  },
};

const currentLanguage = ref(localStorage.getItem("language") || Locale.DE);

export type Translations = typeof translations;

export function useTranslations() {
  const setLanguage = (lang: string) => {
    currentLanguage.value = lang;
    localStorage.setItem("language", lang);
  };

  const t = computed(() => {
    return (key: keyof Translations[Locale]) => {
      return translations[currentLanguage.value as Locale][key] || key;
    };
  });

  return {
    currentLanguage,
    setLanguage,
    t,
  };
}
