<template>
  <button
    :class="buttonClass"
    :disabled="disabled || loading"
    @click="handleClick"
  >
    <div class="button-content">
      <span v-if="loading" class="spinner"></span>
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
      return `button btn-${this.variant} ${this.loading ? "" : ""}`;
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

.btn-primary {
  background-color: var(--button-primary-bg);
  color: var(--button-primary-text);
}

.btn-primary:hover {
  background-color: var(--button-primary-hover-bg);
}

.btn-secondary {
  background-color: var(--button-secondary-bg);
  color: var(--button-secondary-text);
}

.btn-secondary:hover {
  background-color: var(--button-secondary-hover-bg);
}

.button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #fff;
  animation: spin 1s ease-in-out infinite;
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
