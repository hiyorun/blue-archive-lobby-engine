<script setup lang="ts">
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot, Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue'
import { ChevronDownIcon } from '@heroicons/vue/20/solid'
import { useSettings } from '@/stores/settings';
import Models from '@/assets/models.json'
import { onMounted } from 'vue';

const settings = useSettings()

let loop = settings.fetchLoop

onMounted(() => {
  settings.storeModels(Models)
})

defineProps<{
  open?: boolean
}>()

defineEmits<{
  (e: 'close', value: boolean): void
}>()

</script>
<template>
  <TransitionRoot as="template" :show="open">
    <Dialog as="div" class="relative z-10" @close="$emit('close', 'false')">
      <TransitionChild as="template" enter="ease-out duration-300" enter-from="opacity-0" enter-to="opacity-100"
        leave="ease-in duration-200" leave-from="opacity-100" leave-to="opacity-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
      </TransitionChild>

      <div class="fixed inset-0 z-10 overflow-y-auto">
        <div class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
          <TransitionChild as="template" enter="ease-out duration-300"
            enter-from="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
            enter-to="opacity-100 translate-y-0 sm:scale-100" leave="ease-in duration-200"
            leave-from="opacity-100 translate-y-0 sm:scale-100"
            leave-to="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95">
            <DialogPanel
              class="relative transform rounded-lg bg-arisu-400 dark:bg-arisu-700 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg">
              <div class="bg-arisu-400 rounded-lg dark:bg-arisu-700 px-2 pb-2 pt-2 sm:p-6 sm:pb-2">
                <div class="sm:flex sm:items-start">
                  <div class="mt-3 text-center sm:ml-4 sm:mt-0 sm:text-left">
                    <DialogTitle as="h1" class="mb-4 font-bold text-arisu-600 dark:text-arisu-400">
                      Settings
                    </DialogTitle>
                    <div class="mt-2">
                      <span class="mt-2 text-arisu-800 dark:text-arisu-300">Character</span>
                      <p>
                        <Menu as="div" class="relative inline-block text-left">
                          <div>
                            <MenuButton
                              class="inline-flex w-full justify-center gap-x-1.5 rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
                              {{ settings.fetchCurrentModel.name }}
                              <ChevronDownIcon class="-mr-1 h-5 w-5 text-gray-400" aria-hidden="true" />
                            </MenuButton>
                          </div>

                          <transition enter-active-class="transition ease-out duration-100"
                            enter-from-class="transform opacity-0 scale-95"
                            enter-to-class="transform opacity-100 scale-100"
                            leave-active-class="transition ease-in duration-75"
                            leave-from-class="transform opacity-100 scale-100"
                            leave-to-class="transform opacity-0 scale-95">
                            <MenuItems
                              class="absolute left-0 z-10 mt-2 w-56 overflow-scroll max-h-[40vh] origin-top-left rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                              <div class="py-1">
                                <MenuItem v-for="item in settings.fetchModels" v-slot="{ active }"
                                  @click="settings.setModel({ name: item.name, path: item.path })">
                                <a href="#"
                                  :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-2 text-sm']">{{
                                    item.name }}</a>
                                </MenuItem>
                              </div>
                            </MenuItems>
                          </transition>
                        </Menu>
                      </p>
                    </div>
                    <div class="mt-2">
                      <span class="mt-2 text-arisu-800 dark:text-arisu-300">Animation</span>
                      <p class="text-sm text-gray-500">
                        <Menu as="div" class="relative inline-block text-left">
                          <div>
                            <MenuButton
                              class="inline-flex w-full justify-center gap-x-1.5 rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
                              {{ settings.fetchCurrentAnimation }}
                              <ChevronDownIcon class="-mr-1 h-5 w-5 text-gray-400" aria-hidden="true" />
                            </MenuButton>
                          </div>

                          <transition enter-active-class="transition ease-out duration-100"
                            enter-from-class="transform opacity-0 scale-95"
                            enter-to-class="transform opacity-100 scale-100"
                            leave-active-class="transition ease-in duration-75"
                            leave-from-class="transform opacity-100 scale-100"
                            leave-to-class="transform opacity-0 scale-95">
                            <MenuItems
                              class="absolute left-0 z-10 mt-2 w-56 overflow-scroll max-h-[40vh] origin-top-left rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                              <div class="py-1">
                                <MenuItem v-for="item in settings.fetchAnimations" v-slot="{ active }"
                                  @click="settings.setAnimation(item.name)">
                                <a href="#"
                                  :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-2 text-sm']">{{
                                    item.name }}</a>
                                </MenuItem>
                              </div>
                            </MenuItems>
                          </transition>
                        </Menu>
                      </p>
                    </div>
                    <div class="mt-2">
                      <p class="text-sm text-gray-500">
                      <div class="flex gap-x-3">
                        <div class="flex h-6 items-center" @click="settings.setLoop(!loop)">
                          <input v-model="loop" id="loop" name="comments" type="checkbox"
                            class="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-600" />
                        </div>
                        <div class="text-sm leading-6">
                          <label for="loop" class="font-medium text-arisu-900 dark:text-arisu-100">Loop</label>
                        </div>
                      </div>
                      </p>
                    </div>
                  </div>
                </div>
              </div>
              <div class="bg-gray-50 px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6">
                <button type="button"
                  class="inline-flex w-full justify-center rounded-md px-3 py-2 text-sm font-semibold text-arisu-900 dark:text-arisu-100 shadow-sm hover:bg-red-500 sm:ml-3 sm:w-auto"
                  @click="$emit('close', 'false')">Close</button>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>
  