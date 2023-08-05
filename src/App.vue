<script setup lang="ts">
import { ref } from 'vue'
import { Cog6ToothIcon } from '@heroicons/vue/24/solid'
import ModalOptions from './components/ModalOptions.vue'
import LobbyViewer from './components/LobbyViewer.vue'

const open = ref(false)
</script>
<template>
  <Cog6ToothIcon @click="open = true" class="rounded-full bg-arisu-200 dark:bg-arisu-900 absolute h-10 w-10 m-2 p-1 text-arisu-600 dark:text-arisu-400 cursor-pointer">OPEN MODAL
  </Cog6ToothIcon>
  <ModalOptions :open="open" @close="(v) => { open = false }"></ModalOptions>
  <LobbyViewer></LobbyViewer>
</template>