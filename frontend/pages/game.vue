<template>
  <div class="flex flex-row">
    <!-- CHAT -->
    <div class="w-1/5 h-screen border-r flex flex-col">
      <div class="shrink-0 h-24 p-4 bg-poetry-600 flex justify-center items-center">
        <p class="text-center text-white uppercase text-2xl">
          Чат
        </p>
      </div>
      <div class="h-full overflow-y-scroll scrollbar scrollbar-thin scrollbar-thumb-rounded-full scrollbar-track-rounded-full scrollbar-thumb-poetry-600">
        <chat-message v-for="i in 20" :key="i" />
      </div>
      <input class="p-4 border-y outline-none" type="text">
    </div>
    <!-- GAME -->
    <div class="w-4/5 h-screen flex flex-col">
      <!-- QUEUE -->
      <div class="h-24 p-4 border-b flex flex-row space-x-4">
        <img class="avatar" src="https://avatarfiles.alphacoders.com/307/thumb-1920-307713.jpg" alt="">
        <img class="avatar" src="https://avatarfiles.alphacoders.com/307/thumb-1920-307713.jpg" alt="">
        <img class="avatar" src="https://avatarfiles.alphacoders.com/307/thumb-1920-307713.jpg" alt="">
      </div>
      <div class="p-8 h-full grid grid-cols-2 gap-8">
        <div class="card">
          <div class="flex flex-row justify-center space-x-4">
            <p>Статистика</p>
            <select name="stats_player" class="w-auto">
              <option value="AlexeyZavar">
                AlexeyZavar
              </option>
            </select>
          </div>
          <div class="p-4 flex justify-center">
            <img class="avatar" src="https://avatarfiles.alphacoders.com/307/thumb-1920-307713.jpg" alt="">
          </div>
          <div class="flex justify-center">
            <div class="flex flex-col">
              <p><span class="font-bold">Баланс:</span> 1 916 000 ₽</p>
              <p><span class="font-bold">Мастерских:</span> 4 шт.</p>
              <p><span class="font-bold">Руды:</span> 10 шт.</p>
              <p><span class="font-bold">Самолётов:</span> 6 шт.</p>
            </div>
          </div>
        </div>
        <div class="card">
          <div class="flex flex-row justify-center space-x-4">
            <p>Ситуация на рынке</p>
          </div>
          <div class="mt-16 flex justify-center">
            <div class="flex flex-col">
              <p><span class="font-bold">Уровень:</span> 5 (символ звезды)</p>
              <p><span class="font-bold">Доступно руды:</span> 30 шт.</p>
              <p><span class="font-bold">Спрос на самолёты:</span> 20 шт.</p>
              <p><span class="font-bold">Мин. цена покупки руды:</span> 300 000 ₽</p>
              <p><span class="font-bold">Макс. цена продажи самолётов:</span> 4 500 000 ₽</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  name: 'GamePage',
  layout: 'game'
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
