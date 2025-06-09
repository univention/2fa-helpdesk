<!--
 SPDX-License-Identifier: AGPL-3.0-only
 SPDX-FileCopyrightText: 2025 Univention GmbH
-->

<template>
  <button
    :class="buttonClass"
    :disabled="disabled || loading"
    @click="handleClick"
  >
    <div class="button-content">
      <span v-if="loading" class="spinner"
        ><svg
          xmlns="http://www.w3.org/2000/svg"
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="feather feather-loader"
        >
          <line x1="12" y1="2" x2="12" y2="6"></line>
          <line x1="12" y1="18" x2="12" y2="22"></line>
          <line x1="4.93" y1="4.93" x2="7.76" y2="7.76"></line>
          <line x1="16.24" y1="16.24" x2="19.07" y2="19.07"></line>
          <line x1="2" y1="12" x2="6" y2="12"></line>
          <line x1="18" y1="12" x2="22" y2="12"></line>
          <line x1="4.93" y1="19.07" x2="7.76" y2="16.24"></line>
          <line x1="16.24" y1="7.76" x2="19.07" y2="4.93"></line></svg
      ></span>
      <span>{{ label }}</span>
    </div>
  </button>
</template>

<script>
export default {
  name: "SimpleButton",
  props: {
    type: {
      type: String,
      default: "button",
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    variant: {
      type: String,
      default: "primary",
    },
    label: {
      type: String,
      default: "Button",
    },
    loading: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    buttonClass() {
      return `button ${this.variant} ${this.loading ? "" : ""}`;
    },
  },
  methods: {
    handleClick(event) {
      if (!this.loading) {
        this.$emit("click", event);
      }
    },
  },
};
</script>

<style scoped>
.button {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  height: 2.25rem;
  line-height: 1.25rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  white-space: nowrap;
  position: relative;
  min-width: 8rem;
  box-sizing: border-box;
}

.button-content {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.primary {
  background-color: var(--button-primary-bgc);
}

.primary:hover {
  background-color: var(--button-primary-bgc-hover);
}

.secondary {
  background-color: var(--button-bgc);
  color: var(--font-color-contrast-high);
}

.secondary:hover {
  background-color: color-mix(
    in srgb,
    var(--button-bgc) 80%,
    var(--font-color-contrast-high) 10%
  );
}

.button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid var(--font-color-contrast-medium);
  border-radius: 50%;
  border-top-color: var(--font-color-contrast-high);
  animation: spin 1.5s linear infinite;
  margin-right: 0.5rem;
  flex-shrink: 0;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.sr-only {
  position: relative;
  width: auto;
  height: auto;
  padding: 0;
  margin: 0;
  overflow: visible;
  clip: auto;
  white-space: normal;
}

.text-with-spinner {
  opacity: 0.8;
}
</style>
