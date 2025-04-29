
<template>
    <button :class="button" :disabled="disabled" @click="handleClick">
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
        return `btn btn-${this.variant}`;
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
  }
  

  
  .btn:disabled {
 
    cursor: not-allowed;
  }
  </style>