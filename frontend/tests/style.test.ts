/**
 * SPDX-License-Identifier: AGPL-3.0-only
 * SPDX-FileCopyrightText: 2025 Univention GmbH
 */

import {
  loadThemeStyles,
  loadCustomStyles,
  loadAllStyles,
} from "@/utils/customStyles";

import { vi, describe, test, beforeEach, afterEach, expect } from "vitest";

describe("External CSS Loading", () => {
  beforeEach(() => {
    // Clear the head of the document before each test
    document.head.innerHTML = "";
    vi.spyOn(console, "log").mockImplementation(() => {});
    vi.spyOn(console, "warn").mockImplementation(() => {});
    vi.spyOn(console, "error").mockImplementation(() => {});
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  const simulateLoadEvent = (element: HTMLElement) => {
    const event = new Event("load");
    element.dispatchEvent(event);
  };

  const simulateErrorEvent = (element: HTMLElement) => {
    const event = new Event("error");
    element.dispatchEvent(event);
  };

  describe("loadThemeStyles", () => {
    test("should load theme.css with default path", async () => {
      const promise = loadThemeStyles();
      const link = document.getElementById("theme-styles") as HTMLLinkElement;
      expect(link).not.toBeNull();
      expect(link.href).toBe("http://localhost:3000/univention/theme.css");
      simulateLoadEvent(link);
      await promise;
    });

    test("should load theme.css with custom path", async () => {
      const customPath = "/custom/theme.css";
      const promise = loadThemeStyles(customPath);
      const link = document.getElementById("theme-styles") as HTMLLinkElement;
      expect(link).not.toBeNull();
      expect(link.href).toBe(`http://localhost:3000${customPath}`);
      simulateLoadEvent(link);
      await promise;
    });

    test("should not load theme.css if already loaded", async () => {
      const link = document.createElement("link");
      link.id = "theme-styles";
      document.head.appendChild(link);

      await loadThemeStyles();
      expect(console.log).toHaveBeenCalledWith(
        "CSS already loaded: theme-styles"
      );
    });

    test("should handle theme.css load error gracefully", async () => {
      const promise = loadThemeStyles();
      const link = document.getElementById("theme-styles") as HTMLLinkElement;
      simulateErrorEvent(link);
      await promise;
      expect(console.warn).toHaveBeenCalledWith(
        "Failed to load CSS: /univention/theme.css",
        expect.any(Event)
      );
    });

    test("should insert theme CSS before other stylesheets", async () => {
      const existingStylesheet = document.createElement("link");
      existingStylesheet.rel = "stylesheet";
      document.head.appendChild(existingStylesheet);

      const promise = loadThemeStyles();
      const link = document.getElementById("theme-styles") as HTMLLinkElement;
      expect(link).not.toBeNull();
      expect(document.head.firstChild).toBe(link);
      simulateLoadEvent(link);
      await promise;
    });
  });

  describe("loadCustomStyles", () => {
    test("should load custom.css with default path", async () => {
      const promise = loadCustomStyles();
      const link = document.getElementById("custom-styles") as HTMLLinkElement;
      expect(link).not.toBeNull();
      expect(link.href).toBe(
        "http://localhost:3000/univention/portal/css/custom.css"
      );
      simulateLoadEvent(link);
      await promise;
    });

    test("should load custom.css with custom path", async () => {
      const customPath = "/custom/styles.css";
      const promise = loadCustomStyles(customPath);
      const link = document.getElementById("custom-styles") as HTMLLinkElement;
      expect(link).not.toBeNull();
      expect(link.href).toBe(`http://localhost:3000${customPath}`);
      simulateLoadEvent(link);
      await promise;
    });

    test("should not load custom.css if already loaded", async () => {
      const link = document.createElement("link");
      link.id = "custom-styles";
      document.head.appendChild(link);

      await loadCustomStyles();
      expect(console.log).toHaveBeenCalledWith(
        "CSS already loaded: custom-styles"
      );
    });

    test("should handle custom.css load error gracefully", async () => {
      const promise = loadCustomStyles();
      const link = document.getElementById("custom-styles") as HTMLLinkElement;
      simulateErrorEvent(link);
      await promise;
      expect(console.warn).toHaveBeenCalledWith(
        "Failed to load CSS: /univention/portal/css/custom.css",
        expect.any(Event)
      );
    });

    test("should append custom CSS after other elements", async () => {
      const existingElement = document.createElement("div");
      document.head.appendChild(existingElement);

      const promise = loadCustomStyles();
      const link = document.getElementById("custom-styles") as HTMLLinkElement;
      expect(link).not.toBeNull();
      expect(document.head.lastChild).toBe(link);
      simulateLoadEvent(link);
      await promise;
    });
  });

  describe("loadAllStyles", () => {
    test("should load both theme and custom CSS in correct order", async () => {
      const allStylesPromise = loadAllStyles();

      const themeLink = document.getElementById("theme-styles") as HTMLLinkElement;
      expect(themeLink).not.toBeNull();

      simulateLoadEvent(themeLink);

      // Wait for loadThemeStyles promise to resolve and loadCustomStyles to be called
      await new Promise((resolve) => setTimeout(resolve, 0));

      const customLink = document.getElementById("custom-styles") as HTMLLinkElement;
      expect(customLink).not.toBeNull();

      simulateLoadEvent(customLink);

      await allStylesPromise;

      expect(console.log).toHaveBeenCalledWith(
        "All external styles loaded successfully"
      );
    });

    test("should handle errors gracefully and continue", async () => {
      const allStylesPromise = loadAllStyles();

      const themeLink = document.getElementById("theme-styles") as HTMLLinkElement;
      expect(themeLink).not.toBeNull();

      simulateErrorEvent(themeLink);

      // Wait for loadThemeStyles promise to resolve and loadCustomStyles to be called
      await new Promise((resolve) => setTimeout(resolve, 0));

      const customLink = document.getElementById("custom-styles") as HTMLLinkElement;
      expect(customLink).not.toBeNull();

      simulateLoadEvent(customLink);

      await allStylesPromise;

      expect(console.warn).toHaveBeenCalledWith(
        "Failed to load CSS: /univention/theme.css",
        expect.any(Event)
      );
      expect(console.log).toHaveBeenCalledWith(
        "All external styles loaded successfully"
      );
    });
  });
});
