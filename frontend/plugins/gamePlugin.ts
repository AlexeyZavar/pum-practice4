import { Plugin } from '@nuxt/types'
import { Socket } from 'socket.io-client'
import Vue from 'vue'
import { KbClient } from '~/kb_client/KbClient'

declare module 'vue/types/vue' {
  interface Vue {
    $socket: Socket
    $game: KbClient
  }
}

declare module '@nuxt/types' {
  interface Context {
    $socket: Socket
    $game: KbClient
  }
}

const socket: Plugin = (_, inject) => {
  const value = `; ${document.cookie}`
  const parts = value.split('; auth._token.local=')

  let token = ''
  if (parts && parts.length === 2) {
    token = parts.pop()!.split(';').shift()!.replace('Bearer%20', '')
  }

  const client = Vue.observable(new KbClient(token))

  inject('socket', client.socket)
  inject('game', client)
}

export default socket
