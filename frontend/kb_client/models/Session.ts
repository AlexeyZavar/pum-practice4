import { Player } from '~/kb_client/models/Player'

export interface Session {
  id: string
  players: Player[]
}
