<template>
  <div class="w-screen h-screen flex flex-col justify-center items-center">
    <particles id="background-particles" url="particlesjs-config.json" />
    <div class="backdrop-blur w-full md:w-1/2 2xl:w-1/4 p-8 shadow-lg border rounded-2xl">
      <div class="border-b">
        <p class="font-bold text-xl text-center">
          💸 КБ ПУМ ✈️
        </p>
      </div>
      <nuxt />
      <div v-if="$auth.loggedIn" class="pt-4 border-t">
        <p class="text-center">
          Добро пожаловать, <span class="font-bold">{{ $auth.user.name }} ~</span>
        </p>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  name: 'DefaultLayout'
})
</script>
