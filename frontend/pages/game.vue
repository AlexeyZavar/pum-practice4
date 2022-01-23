<template>
  <div class="flex flex-row">
    <!-- CHAT -->
    <div class="w-1/5 h-screen border-r flex flex-col">
      <div class="shrink-0 h-24 p-4 bg-poetry-600 flex justify-center items-center">
        <p class="text-center text-white uppercase text-2xl">
          Чат
        </p>
      </div>
      <div
        class="h-full overflow-y-scroll scrollbar scrollbar-thin scrollbar-thumb-rounded-full scrollbar-track-rounded-full scrollbar-thumb-poetry-600 divide-y"
      >
        <chat-message v-for="(message, i) in $game.game_manager.messages" :key="i" :message="message" />
      </div>
      <input v-model="chatMessage" class="p-4 border-y outline-none" type="text" @keydown.enter="send_message">
    </div>
    <!-- GAME -->
    <div class="w-4/5 h-screen flex flex-col">
      <!-- QUEUE -->
      <div class="h-24 p-4 border-b flex flex-row space-x-4">
        <user-avatar
          v-for="id in $game.game_manager.session.queue"
          :key="id"
          :user="$game.game_manager.get_player(id).user"
        />
      </div>
      <div class="h-full grid grid-cols-2">
        <div class="card">
          <div class="flex flex-row justify-center space-x-4">
            <p>Статистика</p>
            <select v-model="selectedPlayer" class="w-auto" name="stats_player">
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
              <div class="flex flex-row space-x-4">
                <img alt="" src="~/assets/images/money.svg" width="24">
                <p>
                  <span class="font-bold">Баланс:</span> {{ selectedPlayer.money }} ₽
                </p>
              </div>
              <div class="flex flex-row space-x-4">
                <img alt="" src="~/assets/images/workshop.svg" width="24">
                <p><span class="font-bold">Мастерских:</span> {{ selectedPlayer.workshops }} шт.</p>
              </div>
              <div class="flex flex-row space-x-4">
                <img alt="" src="~/assets/images/ore.svg" width="24">
                <p><span class="font-bold">Руды:</span> {{ selectedPlayer.ore }} шт.</p>
              </div>
              <div class="flex flex-row space-x-4">
                <img alt="" src="~/assets/images/airship.svg" width="24">
                <p><span class="font-bold">Самолётов:</span> {{ selectedPlayer.airships }} шт.</p>
              </div>
            </div>
          </div>
        </div>
        <div class="card">
          <div class="flex flex-row justify-center space-x-4">
            <p>Ситуация на рынке</p>
          </div>
          <div class="mt-40 flex justify-center">
            <div class="flex flex-col">
              <div class="flex flex-row space-x-4">
                <img alt="" src="~/assets/images/level.svg" width="24">
                <p><span class="font-bold">Уровень:</span> {{ $game.game_manager.session.market_state.level }} ★</p>
              </div>
              <div class="flex flex-row space-x-4">
                <img alt="" src="~/assets/images/ore.svg" width="24">
                <p>
                  <span class="font-bold">Доступно руды:</span> {{ $game.game_manager.session.market_state.total_ore }}
                  шт.
                </p>
              </div>
              <div class="flex flex-row space-x-4">
                <img alt="" src="~/assets/images/airship.svg" width="24">
                <p>
                  <span class="font-bold">Спрос на самолёты:</span>
                  {{ $game.game_manager.session.market_state.airships_demand }} шт.
                </p>
              </div>
              <div class="flex flex-row space-x-4">
                <img alt="" src="~/assets/images/buy.svg" width="24">
                <p>
                  <span class="font-bold">Мин. цена покупки руды:</span>
                  {{ $game.game_manager.session.market_state.minimal_price }} ₽
                </p>
              </div>
              <div class="flex flex-row space-x-4">
                <img alt="" src="~/assets/images/sell.svg" width="24">
                <p>
                  <span class="font-bold">Макс. цена продажи самолётов:</span>
                  {{ $game.game_manager.session.market_state.maximal_price }} ₽
                </p>
              </div>
            </div>
          </div>
        </div>
        <!-- PLAYER MOVE MODAL -->
        <div :class="{'hidden': !modalShown}" class="w-full h-full fixed z-10 overflow-auto bg-black/40">
          <div class="mt-[10%] w-4/5 bg-white">
            <div class="w-full p-8 flex flex-col space-y-4 text-2xl justify-center items-center">
              <p class="uppercase font-bold">
                Твой ход!
              </p>
              <div class="w-2/5 flex flex-col space-y-4">
                <div class="flex flex-row space-x-4 justify-between">
                  <p class="w-20">
                    Купить
                  </p>
                  <div class="flex flex-row space-x-2">
                    <input
                      v-model="move.ore_request_amount"
                      class="w-20 px-2 border rounded-2xl outline-none"
                      min="0"
                      type="number"
                    >
                    <img alt="" src="~/assets/images/ore.svg" width="24">
                  </div>
                  <p>за</p>
                  <div class="flex flex-row space-x-2">
                    <input
                      v-model="move.ore_request_price"
                      class="w-20 px-2 border rounded-2xl outline-none"
                      min="0"
                      type="number"
                    >
                    <img alt="" src="~/assets/images/money.svg" width="24">
                  </div>
                </div>
                <div class="flex flex-row space-x-4 justify-between">
                  <p class="w-20">
                    Продать
                  </p>
                  <div class="flex flex-row space-x-2">
                    <input
                      v-model="move.sell_request_amount"
                      class="w-20 px-2 border rounded-2xl outline-none"
                      min="0"
                      type="number"
                    >
                    <img alt="" src="~/assets/images/airship.svg" width="24">
                  </div>
                  <p>за</p>
                  <div class="flex flex-row space-x-2">
                    <input
                      v-model="move.sell_request_price"
                      class="w-20 px-2 border rounded-2xl outline-none"
                      min="0"
                      type="number"
                    >
                    <img alt="" src="~/assets/images/money.svg" width="24">
                  </div>
                </div>
                <div class="flex flex-row space-x-4 justify-between">
                  <p class="w-20">
                    Изготовить
                  </p>
                  <div class="flex flex-row space-x-2">
                    <input
                      v-model="move.airships_amount"
                      class="w-20 px-2 border rounded-2xl outline-none"
                      min="0"
                      type="number"
                    >
                    <img alt="" src="~/assets/images/airship.svg" width="24">
                  </div>
                </div>
                <div class="flex flex-row space-x-4 justify-between items-center">
                  <div class="flex flex-row space-x-2">
                    <p>Построить новый цех</p>
                    <img alt="" src="~/assets/images/workshop.svg" width="24">
                  </div>
                  <input v-model="move.build_workshop" type="checkbox">
                </div>
                <button class="uppercase btn" @click="make_move">
                  Готово
                </button>
              </div>
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
      selectedPlayer,
      chatMessage: '',
      move: {
        ore_request_amount: 0,
        ore_request_price: 0,
        airships_amount: 0,
        sell_request_amount: 0,
        sell_request_price: 0,
        build_workshop: false
      }
    }
  },
  computed: {
    modalShown () {
      console.log(this.$auth.loggedIn, this.$game.game_manager.session?.queue, this.$game.game_manager.session?.queue[0], this.$auth.user?.id, this.$auth.user)
      return this.$game.game_manager.session?.queue[0] === this.$auth.user?.id
    },
    moveValid () {

    }
  },
  methods: {
    send_message () {
      if (this.chatMessage && this.chatMessage.length > 0) {
        this.$game.game_manager.send_message(this.chatMessage)
        this.chatMessage = ''
      }
    },
    make_move () {
      this.$game.game_manager.make_move(this.move)
    }
  }
})
</script>

<style scoped>
.card {
  @apply m-8 p-8;
  @apply bg-poetry-300 shadow-lg;
  @apply text-2xl;
}

select {
  @apply outline-none;
  @apply px-2 rounded-2xl;
}
</style>
