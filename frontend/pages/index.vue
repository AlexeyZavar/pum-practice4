<template>
  <div class="main-container">
    <button class="btn" @click="create_lobby">
      Создать лобби
    </button>
    <button class="btn" @click="join_lobby">
      Присоединиться к лобби
    </button>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

interface LobbyCreated {
  lobby_id: string
}

export default Vue.extend({
  name: 'IndexPage',
  mounted () {
    this.$socket.on('lobby_created', this.lobby_created)

    if (this.$game.token === '') {
      location.reload()
    }
  },
  beforeDestroy () {
    this.$socket.offAny(this.lobby_created)
  },
  methods: {
    create_lobby () {
      this.$socket.emit('create_lobby')
    },
    join_lobby () {
      this.$router.push('join')
    },
    lobby_created (args: LobbyCreated) {
      this.$router.push('lobby')
    }
  }
})
</script>
