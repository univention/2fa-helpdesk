<template>
  <div v-if="isOpen" class="modal-backdrop" @click.self="closeModal">
    <div class="modal-content">
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
  name: "Modal",
  props: {
    isOpen: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    closeModal() {
      this.$emit("close");
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
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
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
  color: #203257;
  line-height: 1.5;
  margin-top: 12px;
  margin-bottom: 24px;
  text-align: left;
}

.modal-footer {
  padding: 0;
  display: flex;
  justify-content: center;
  gap: 1rem;
}

h3.modal-title {
  color: #4338ca;
  font-size: 1.5rem;
  display: block;
}

/* Add a global style to reset h3 margin within the modal */
:global(.modal-content h3) {
  margin: 0;
  padding: 0;
}
</style>
