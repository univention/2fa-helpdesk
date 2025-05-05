
<template>
    <div id="swagger-ui" />
  </template>
  
  <script setup lang="ts">
  // eslint-disable-next-line @typescript-eslint/ban-ts-comment
  // @ts-ignore
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