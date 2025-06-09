<!--
 SPDX-License-Identifier: AGPL-3.0-only
 SPDX-FileCopyrightText: 2025 Univention GmbH
-->

<template>
  <div v-if="isOpen" class="modal-backdrop" @click.self="closeModal">
    <div
      ref="modalContent"
      class="modal-content"
      tabindex="-1"
      @keydown="handleKeydown"
    >
      <div class="modal-header">
        <slot name="header"></slot>
      </div>
      <div class="modal-body">
        <slot></slot>
      </div>
      <div class="modal-footer">
        <slot name="footer"></slot>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "BaseModal",
  props: {
    isOpen: {
      type: Boolean,
      default: false,
    },
  },
  watch: {
    isOpen(newVal) {
      if (newVal) {
        this.$nextTick(() => {
          this.setFocus();
        });
      }
    },
  },
  methods: {
    closeModal() {
      this.$emit("close");
    },
    setFocus() {
      if (this.$refs.modalContent) {
        this.$refs.modalContent.focus();
      }
    },
    handleKeydown(event) {
      if (event.key === "Escape") {
        this.closeModal();
        return;
      }

      if (event.key === "Tab") {
        this.trapFocus(event);
      }
    },
    trapFocus(event) {
      const modal = this.$refs.modalContent;
      const focusableElements =
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])';
      const focusableNodes = modal.querySelectorAll(focusableElements);

      const focusable = [...focusableNodes].filter(
        (el) => !el.disabled && el.offsetParent !== null
      );

      if (focusable.length === 0) {
        event.preventDefault();
        return;
      }

      const firstFocusable = focusable[0];
      const lastFocusable = focusable[focusable.length - 1];

      if (event.shiftKey && document.activeElement === firstFocusable) {
        event.preventDefault();
        lastFocusable.focus();
      } else if (!event.shiftKey && document.activeElement === lastFocusable) {
        event.preventDefault();
        firstFocusable.focus();
      }
    },
  },
};
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: var(--bgc-underlay);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: var(--bgc-content-container);
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  box-shadow: 0 4px 6px var(--box-shadow);
  overflow: hidden;
  padding: 24px;
}

.modal-header {
  padding: 0;
  text-align: left;
}

.modal-body {
  padding: 0;
  font-size: 1rem;
  color: var(--font-color-contrast-high);
  line-height: 1.5;
  margin-top: 12px;
  margin-bottom: 24px;
  text-align: left;
}

.modal-footer {
  padding: 0;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 1rem;
}

h3.modal-title {
  color: var(--font-color-contrast-high);
  font-size: 1.5rem;
  display: block;
}

:global(.modal-content h3) {
  margin: 0;
  padding: 0;
}
</style>
