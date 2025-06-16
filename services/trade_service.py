from model import session, Trade
def propose(from_player, to_player, offered_ids, requested_ids):
    trade = Trade(from_player_id=from_player.id,
                  to_player_id=to_player.id,
                  offered_monsters=",".join(map(str, offered_ids)),
                  requested_monsters=",".join(map(str, requested_ids)))
    session.add(trade); session.commit()
    print(f"Trade #{trade.id} proposed.")
