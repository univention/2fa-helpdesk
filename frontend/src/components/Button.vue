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
      default: "primary",
    },
    label: {
      type: String,
      default: "Button",
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
</style>
