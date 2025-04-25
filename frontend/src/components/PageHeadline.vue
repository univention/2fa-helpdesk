<script setup lang="ts">
withDefaults(
  defineProps<{
    text: string;
    level?: 1 | 2 | 3 | 4 | 5 | 6;
    customClass?: string;
    align?: "left" | "center" | "right";
  }>(),
  {
    level: 1,
    align: "left",
  }
);
</script>

<template>
  <component
    :is="`h${level}`"
    :class="['headline', `headline-${level}`, `text-${align}`, customClass]"
  >
    {{ text }}
    <slot></slot>
  </component>
</template>

<style scoped>
.headline {
  margin-bottom: 1.5rem;
  font-weight: 600;
  line-height: 1.2;
  color: inherit;
}

.headline-1 {
  font-size: 1.5rem;
  margin-top: 0;
}

.headline-2 {
  font-size: 1.75rem;
}

.headline-3 {
  font-size: 1.5rem;
}

.headline-4 {
  font-size: 1.25rem;
}

.headline-5 {
  font-size: 1.15rem;
}

.headline-6 {
  font-size: 1rem;
}

.text-left {
  text-align: left;
}

.text-center {
  text-align: center;
}

.text-right {
  text-align: right;
}
</style>
