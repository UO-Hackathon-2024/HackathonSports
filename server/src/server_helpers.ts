
import { Player } from './interfaces.js';

export const build_player_id = (player_list: Player[]) => { 
    return `${player_list.length + 1}`;
}
