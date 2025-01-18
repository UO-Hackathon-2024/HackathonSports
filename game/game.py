import pygame

def auto_move(player, ball):
    if player.x < ball.x:
        player.x += player.speed
    elif player.x > ball.x:
        player.x -= player.speed
