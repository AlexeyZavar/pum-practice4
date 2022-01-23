import { io, Socket } from 'socket.io-client'
import { GameUpdated, LobbyUpdated } from '~/kb_client/Events'
import { Session } from '~/kb_client/models/Session'
import { GameLobby } from '~/kb_client/models/Lobby'
import { Player } from '~/kb_client/models/Player'

export class GameManager {
  session: Session
  private socket: Socket

  constructor (socket: Socket) {
    this.socket = socket
    this.session = {
      id: 'none',
      players: [
        {
          user: {
            id: '1',
            avatar: 'https://avatarfiles.alphacoders.com/307/thumb-1920-307713.jpg',
            name: 'AlexeyZavar'
          },
          money: 10_000_000,
          workshops: 2,
          ore: 4,
          airships: 2
        },
        {
          user: {
            id: '2',
            avatar: 'https://avatarfiles.alphacoders.com/302/thumb-1920-302953.png',
            name: 'Hu Tao'
          },
          money: 20_000_000,
          workshops: 3,
          ore: 1,
          airships: 1
        }
      ],
      market_state: {
        level: 3,
        total_ore: 2,
        airships_demand: 3,
        minimal_price: 300_000,
        maximal_price: 4_500_000
      },
      messages: [
        {
          user_id: '1',
          date: new Date().getTime(),
          text: 'Всем привет!'
        },
        {
          user_id: '2',
          date: new Date().getTime(),
          text: 'Я тебя разнесу..!'
        }
      ]
    }

    this.socket.on('game_updated', args => this.game_updated(args))
    this.socket.on('game_new_message', args => this.game_new_message(args))
  }

  get_player (userId: string): Player | undefined {
    for (const player of this.session.players) {
      if (player.user.id === userId) {
        return player
      }
    }
  }

  private game_updated (args: GameUpdated) {
    this.session = args
  }

  private game_new_message (args: any) {

  }
}

export class LobbyManager {
  lobby: GameLobby
  ready: boolean
  private socket: Socket

  constructor (socket: Socket) {
    this.socket = socket
    this.lobby = {
      id: 'none',
      users: []
    }
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
