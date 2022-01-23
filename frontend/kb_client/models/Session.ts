import { Player } from '~/kb_client/models/Player'
import { MarketState } from '~/kb_client/models/MarketState'
import { Message } from '~/kb_client/models/Message'

export interface Session {
  id: string
  players: Player[]
  market_state: MarketState
  messages: Message[]
}
