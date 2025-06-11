/**
 * SPDX-License-Identifier: AGPL-3.0-only
 * SPDX-FileCopyrightText: 2025 Univention GmbH
 */

/**
 * Utility to load custom CSS styles provided by customers
 * These styles will override the default theme.css
 */

// Default location for custom CSS file
const DEFAULT_CUSTOM_CSS_PATH = "/ui/css/custom.css";

/**
 * Loads custom CSS styles from the specified path
 * @param path Path to the custom CSS file (defaults to /custom/styles.css)
 */
export function loadCustomStyles(path: string = DEFAULT_CUSTOM_CSS_PATH): void {
  if (document.getElementById("custom-styles")) {
    console.log("Custom styles already loaded");
    return;
  }

  const link = document.createElement("link");
  link.id   = "custom-styles";
  link.rel  = "stylesheet";
  link.type = "text/css";
  link.href = path;

  link.onerror = (err) =>
    console.warn("Failed to load custom CSS; falling back to default:", err);

  document.head.appendChild(link);
}
