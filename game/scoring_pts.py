P1_score = 0
P2_score = 0
max_score = 11


#animations after whichever person wins
def update_scores(player):
    global score_player_1, score_player_2
    if player == 1:
        score_player_1 += 1
    elif player == 2:
        score_player_2 += 1

def get_scores():
    return score_player_1, score_player_2

