<template>
  <div class="main-container">
    <transition>
      <div v-if="error_visible" class="error-box">
        Что-то не так... Проверь все поля!
      </div>
    </transition>
    <input v-model="form.name" class="inp" placeholder="Юзернейм" type="text">
    <input v-model="form.password" class="inp" placeholder="Пароль" type="password">
    <button class="btn" @click="login_account">
      Авторизироваться
    </button>
    <button class="btn" @click="$router.push('/register')">
      ←
    </button>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  name: 'LoginPage',
  auth: 'guest',
  data () {
    return {
      form: {
        name: '',
        password: ''
      },
      error_visible: false
    }
  },
  methods: {
    async login_account () {
      try {
        await this.$auth.loginWith('local', {
          data: {
            name: this.form.name,
            password: this.form.password
          }
        })
        await this.$router.push('/')
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
