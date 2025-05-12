/**
 * Utility to load custom CSS styles provided by customers
 * These styles will override the default theme.css
 */

// Default location for custom CSS file
const DEFAULT_CUSTOM_CSS_PATH = "/ui/css/custom.css";

/**
 * Loads custom CSS styles from the specified path
 * @param path Path to the custom CSS file (defaults to /custom/styles.css)
 * @returns Promise that resolves when the CSS is loaded or rejected if loading fails
 */
export function loadCustomStyles(
  path: string = DEFAULT_CUSTOM_CSS_PATH
): Promise<void> {
  return new Promise((resolve) => {
    // Check if link with custom CSS id already exists
    if (document.getElementById("custom-styles")) {
      console.log("Custom styles already loaded");
      resolve();
      return;
    }

    const link = document.createElement("link");
    link.id = "custom-styles";
    link.rel = "stylesheet";
    link.type = "text/css";
    link.href = path;

    link.onload = () => {
      console.log("Custom styles loaded successfully");
      resolve();
    };

    link.onerror = (error) => {
      console.warn(
        "Failed to load custom styles, using default theme only:",
        error
      );

      resolve();
    };

    document.head.appendChild(link);
  });
}

/**
 * Initialize custom styles
 * This can be called from main.ts
 */
export async function initCustomStyles(): Promise<void> {
  try {
    await loadCustomStyles();
  } catch (error) {
    console.error("Error initializing custom styles:", error);
  }
}
