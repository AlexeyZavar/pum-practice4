<template>
  <div class="main-container">
    <div v-for="(user, i) in users" :key="user.id">
      <div class="flex items-center space-x-10">
        <user-avatar :user="user" />
        <p class="text-xl font-bold">
          {{ i + 1 }}. {{ user.name }} (win: {{ user.wins }}, looses: {{ user.looses }})
        </p>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { User } from '~/kb_client/models/User'

export default Vue.extend({
  name: 'ScoreboardPage',
  async asyncData ({ $axios }) {
    const users = await $axios.$get('/rest/scoreboard')

    return { users }
  },
  data () {
    const users: User[] = []

    return {
      users
    }
  }
})
</script>

<style scoped>

</style>
