import { Session } from '~/kb_client/models/Session'
import { GameLobby } from '~/kb_client/models/Lobby'

export interface LobbyUpdated extends GameLobby {

}

export interface GameUpdated extends Session {

}
