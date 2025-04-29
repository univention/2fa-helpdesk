<template>
  <button :class="buttonClass" :disabled="disabled" @click="handleClick">
    {{ label }}
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
      default: "primary", // e.g., primary, secondary, danger
    },
    label: {
      type: String,
      default: "Button", // Default label if none is provided
    },
  },
  computed: {
    buttonClass() {
      return `button btn-${this.variant}`;
    },
  },
  methods: {
    handleClick(event) {
      this.$emit("click", event);
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
}

.btn-primary {
  background-color: #4f46e5;
  color: white;
}

.btn-primary:hover {
  background-color: #4338ca;
}

.btn-secondary {
  background-color: #e5e7eb;
  color: #111827;
}

.btn-secondary:hover {
  background-color: #d1d5db;
}

.button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
