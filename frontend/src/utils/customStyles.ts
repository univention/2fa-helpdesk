/**
 * SPDX-License-Identifier: AGPL-3.0-only
 * SPDX-FileCopyrightText: 2025 Univention GmbH
 */
/**
 * Utility to load external CSS styles (theme and custom overrides)
 */

// Default paths for CSS files
const DEFAULT_THEME_CSS_PATH = "/univention/theme.css";
const DEFAULT_CUSTOM_CSS_PATH = "/univention/portal/css/custom.css";

/**
 * Loads a CSS file dynamically with error handling
 * @param id Unique identifier for the link element
 * @param path Path to the CSS file
 * @param insertBefore Whether to insert before existing stylesheets (for theme) or after (for custom)
 * @returns Promise that resolves when CSS is loaded or fails gracefully
 */
function loadCSSFile(
  id: string,
  path: string,
  insertBefore: boolean = false,
): Promise<void> {
  return new Promise((resolve) => {
    // Check if already loaded
    if (document.getElementById(id)) {
      console.log(`CSS already loaded: ${id}`);
      resolve();
      return;
    }

    const link = document.createElement("link");
    link.id = id;
    link.rel = "stylesheet";
    link.type = "text/css";
    link.href = path;

    link.onload = () => {
      console.log(`CSS loaded successfully: ${path}`);
      resolve();
    };

    link.onerror = (err) => {
      console.warn(`Failed to load CSS: ${path}`, err);
      resolve();
    };

    // Insert CSS in correct order
    if (insertBefore) {
      // Theme CSS should load first (before other stylesheets)
      const firstStylesheet = document.querySelector('link[rel="stylesheet"]');
      if (firstStylesheet) {
        document.head.insertBefore(link, firstStylesheet);
      } else {
        document.head.appendChild(link);
      }
    } else {
      // Custom CSS should load last (after other stylesheets)
      document.head.appendChild(link);
    }
  });
}

/**
 * Loads the external theme CSS file
 * @param path Path to the theme CSS file (defaults to /univention/theme.css)
 * @returns Promise that resolves when theme is loaded or fails gracefully
 */
export function loadThemeStyles(
  path: string = DEFAULT_THEME_CSS_PATH,
): Promise<void> {
  return loadCSSFile("theme-styles", path, true);
}

/**
 * Loads custom CSS styles from the specified path
 * @param path Path to the custom CSS file (defaults to /univention/portal/css/custom.css)
 * @returns Promise that resolves when custom styles are loaded or fail gracefully
 */
export function loadCustomStyles(
  path: string = DEFAULT_CUSTOM_CSS_PATH,
): Promise<void> {
  return loadCSSFile("custom-styles", path, false);
}

/**
 * Loads both theme and custom CSS files in the correct order
 * @param themePath Path to the theme CSS file
 * @param customPath Path to the custom CSS file
 * @returns Promise that resolves when both are loaded (or failed gracefully)
 */
export async function loadAllStyles(
  themePath: string = DEFAULT_THEME_CSS_PATH,
  customPath: string = DEFAULT_CUSTOM_CSS_PATH,
): Promise<void> {
  try {
    await loadThemeStyles(themePath);
    await loadCustomStyles(customPath);
    console.log("All external styles loaded successfully");
  } catch (error) {
    console.warn("Error loading external styles:", error);
  }
}
