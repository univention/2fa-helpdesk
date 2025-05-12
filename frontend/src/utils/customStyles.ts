/**
 * Utility to load custom CSS styles provided by customers
 * These styles will override the default theme.css
 */

// Default location for custom CSS file
const DEFAULT_CUSTOM_CSS_PATH = "/custom/styles.css";

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

    // Create link element
    const link = document.createElement("link");
    link.id = "custom-styles";
    link.rel = "stylesheet";
    link.type = "text/css";
    link.href = path;

    // Set up event listeners
    link.onload = () => {
      console.log("Custom styles loaded successfully");
      resolve();
    };

    link.onerror = (error) => {
      console.warn(
        "Failed to load custom styles, using default theme only:",
        error
      );
      // We resolve instead of reject since this is optional
      // and the app should continue with the default theme
      resolve();
    };

    // Append to head - this will be loaded after theme.css since it's added later
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
    // Continue with the application even if custom styles fail to load
  }
}
