<template>
    <div id="swagger-ui" />
  </template>
  
  <script setup lang="ts">
  import SwaggerUI from 'swagger-ui'
  import 'swagger-ui/dist/swagger-ui.css'
import { onMounted } from 'vue'
  
  onMounted(() => {
    SwaggerUI({
        dom_id: '#swagger-ui',
        url: '/ui/openapi.json',
    })
})
  </script>