import { io, Socket } from 'socket.io-client'
import { GameUpdated, LobbyUpdated } from '~/kb_client/Events'
import { Session } from '~/kb_client/models/Session'
import { GameLobby } from '~/kb_client/models/Lobby'

export class GameManager {
  session: Session
  private socket: Socket

  constructor (socket: Socket) {
    this.socket = socket
    this.session = { id: 'none', players: [] }

    this.socket.on('game_updated', args => this.game_updated(args))
  }

  private game_updated (args: GameUpdated) {
    this.session = args
  }
}

export class LobbyManager {
  lobby: GameLobby
  ready: boolean
  private socket: Socket

  constructor (socket: Socket) {
    this.socket = socket
    this.lobby = { id: 'none', users: [] }
    this.ready = false

    this.socket.on('lobby_updated', args => this.lobby_updated(args))
  }

  join_lobby (id: string) {
    this.socket.emit('join_lobby', { lobby_id: id })
  }

  ready_switch () {
    this.socket.emit('lobby_user_ready_switch')
    this.ready = !this.ready
  }

  private lobby_updated (args: LobbyUpdated) {
    this.lobby = args
  }
}

export class KbClient {
  socket: Socket
  lobby_manager: LobbyManager
  game_manager: GameManager

  constructor (token: string) {
    console.log(this)
    this.socket = io('http://localhost:3001/', { query: { jwt: token } })

    this.lobby_manager = new LobbyManager(this.socket)
    this.game_manager = new GameManager(this.socket)
  }
}
