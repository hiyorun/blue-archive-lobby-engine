<script setup lang="ts">
import { ref } from 'vue'
import { Cog6ToothIcon } from '@heroicons/vue/24/solid'
import ModalOptions from './components/ModalOptions.vue'
import LobbyViewer from './components/LobbyViewer.vue'

const open = ref(false)
</script>
<template>
  <Cog6ToothIcon @click="open = true" class="h-6 w-6 m-3 text-arisu-600 dark:text-arisu-400 cursor-pointer">OPEN MODAL
  </Cog6ToothIcon>
  <ModalOptions :open="open" @close="(v) => { open = false }"></ModalOptions>
  <LobbyViewer></LobbyViewer>
</template>