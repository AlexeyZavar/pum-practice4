<template>
  <div class="main-container">
    <transition>
      <div v-if="error_visible" class="error-box">
        Что-то не так... Проверь все поля!
      </div>
    </transition>
    <input v-model="form.name" class="inp" placeholder="Юзернейм" type="text">
    <input v-model="form.password" class="inp" placeholder="Пароль" type="password">
    <input v-model="form.avatar" class="inp" placeholder="Аватарка" type="text">
    <div class="p-4 flex flex-col space-y-4 text-center items-center justify-center border rounded-2xl">
      <p>Превью аватарки</p>
      <img :src="form.avatar" alt="" class="avatar">
    </div>
    <button class="btn" @click="register_account">
      Зарегистрироваться
    </button>
    <button class="btn" @click="$router.push('/login')">
      →
    </button>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  name: 'RegisterPage',
  auth: 'guest',
  data () {
    return {
      form: {
        name: '',
        password: '',
        avatar: ''
      },
      error_visible: false
    }
  },
  methods: {
    async register_account () {
      try {
        const res = await this.$axios.post('/rest/register', this.form)
        if (res.data.success) {
          await this.$auth.loginWith('local', {
            data: {
              name: this.form.name,
              password: this.form.password
            }
          })
        }
      } catch (error) {
        this.form.password = ''
        this.error_visible = true
        setTimeout(() => {
          this.error_visible = false
        }, 2000)
      }
    }
  }
})
</script>

<style scoped>

</style>
