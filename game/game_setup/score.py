

def draw_text(text, font, text_color, text_x, text_y, screen):
      img = font.render(text, True, text_color)
      screen.blit(img, (text_x, text_y)) #puts the image onto your screen