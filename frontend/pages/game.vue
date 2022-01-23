<template>
  <div class="flex flex-row">
    <!-- CHAT -->
    <div class="w-1/5 h-screen border-r flex flex-col">
      <div class="shrink-0 h-24 p-4 bg-poetry-600 flex justify-center items-center">
        <p class="text-center text-white uppercase text-2xl">
          Чат
        </p>
      </div>
      <div class="h-full overflow-y-scroll scrollbar scrollbar-thin scrollbar-thumb-rounded-full scrollbar-track-rounded-full scrollbar-thumb-poetry-600 divide-y">
        <chat-message v-for="(message, i) in $game.game_manager.session.messages" :key="i" :message="message" />
      </div>
      <input class="p-4 border-y outline-none" type="text">
    </div>
    <!-- GAME -->
    <div class="w-4/5 h-screen flex flex-col">
      <!-- QUEUE -->
      <div class="h-24 p-4 border-b flex flex-row space-x-4">
        <user-avatar v-for="player in $game.game_manager.session.players" :key="player.user.id" :user="player.user" />
      </div>
      <div class="p-8 h-full grid grid-cols-2 gap-8">
        <div class="card">
          <div class="flex flex-row justify-center space-x-4">
            <p>Статистика</p>
            <select v-model="selectedPlayer" name="stats_player" class="w-auto">
              <option v-for="player in $game.game_manager.session.players" :key="player.user.id" :value="player">
                {{ player.user.name }}
              </option>
            </select>
          </div>
          <div class="mt-16 p-4 flex justify-center">
            <user-avatar :user="selectedPlayer.user" size="medium" />
          </div>
          <div class="flex justify-center">
            <div class="flex flex-col">
              <p><span class="font-bold">Баланс:</span> {{ selectedPlayer.money }} ₽</p>
              <p><span class="font-bold">Мастерских:</span> {{ selectedPlayer.workshops }} шт.</p>
              <p><span class="font-bold">Руды:</span> {{ selectedPlayer.ore }} шт.</p>
              <p><span class="font-bold">Самолётов:</span> {{ selectedPlayer.airships }} шт.</p>
            </div>
          </div>
        </div>
        <div class="card">
          <div class="flex flex-row justify-center space-x-4">
            <p>Ситуация на рынке</p>
          </div>
          <div class="mt-40 flex justify-center">
            <div class="flex flex-col">
              <p><span class="font-bold">Уровень:</span> {{ $game.game_manager.session.market_state.level }} (символ звезды)</p>
              <p><span class="font-bold">Доступно руды:</span> {{ $game.game_manager.session.market_state.total_ore }} шт.</p>
              <p><span class="font-bold">Спрос на самолёты:</span> {{ $game.game_manager.session.market_state.airships_demand }} шт.</p>
              <p><span class="font-bold">Мин. цена покупки руды:</span> {{ $game.game_manager.session.market_state.minimal_price }} ₽</p>
              <p><span class="font-bold">Макс. цена продажи самолётов:</span> {{ $game.game_manager.session.market_state.maximal_price }} ₽</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { Player } from '~/kb_client/models/Player'

export default Vue.extend({
  name: 'GamePage',
  layout: 'game',
  data () {
    const selectedPlayer: Player = this.$game.game_manager.session.players[0]

    return {
      selectedPlayer
    }
  }
})
</script>

<style scoped>
.card {
  @apply p-8;
  @apply bg-poetry-300 shadow-lg;
  @apply text-2xl;
}

select {
  @apply outline-none;
  @apply px-2 rounded-2xl;
}
</style>
