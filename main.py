import pygame 
from shared import *
from snake import snake_game
from drill import drill_game

def display_text_block(text):
    if not text: return
    start = (310, 120)
    ofs = 20
    title = text[0]
    t_img = pixel_font_small2.render(title, None, "black")
    t_rect = t_img.get_rect(center=(515, 130))
    screen.blit(t_img, t_rect)
    for i in range(1, len(text)):
        t = text[i]
        if (t == ""): continue
        img = pixel_font_small.render(t, None, "black")
        r = img.get_rect(topleft=(start[0], start[1] + i * ofs))
        screen.blit(img, r)
# Text
about_txt = [ 
    "Welcome to 2D Games Collection!",
    "",
    "Navigate the menu with WASD or the arrow keys",
    "and press SPACEBAR or RETURN to play a game.",
    "", 
    "While in a game, press P or ESC to pause.",
    "",
    "Author's note: Thanks for playing!",
    "I've always loved videogames and decided to try",
    "taking up game development as a hobby. This",
    "project is something I started to mess around",
    "with different aspects of game dev, like",
    "sound design and artwork, in an environment",
    "I'm used to.",
    "",
    "While pygame is not the most robust 'engine',", 
    "it certainly allows for a very contained entry",
    "into learning game dev for anyone looking for a",
    "more code-focused path. Would recommend!"
]

g1_txt = [
    "Tapeworm (Snake)",
    "",
    "CONTROLS:",
    "Press WASD or the arrow keys to move.",
    "Collect fruit in order to grow,",
    "but avoid hitting walls or your own body.",
    "",
    "DESCRIPTION:",
    "This game is clone of the classic game 'Snake',",
    "instead playing as a worm."
]

g2_txt = [
    "Drill Rush",
    "",
    "CONTROLS:",
    "Press WASD or the arrow keys to move.",
    "Collect gems and avoid enemies",
    "",
    "DESCRIPTION:",
    "This is an original 'endless runner' game.",
    "Take control of a drill as you mine for",
    "riches, but beware what lurks below.",
    "As you go deeper, the dangers only grow"
]

g3_txt = []
all_text = [about_txt, g1_txt, g2_txt, g3_txt]

# Main Window
m_bg = pygame.surface.Surface(size=(250, 420))
m_bg.fill("darkslategray")
m_bg_rect = m_bg.get_rect(topleft=(20, 100))
title = pixel_font_big.render("2d Games Collection", False, "white")
about = pixel_font.render("About", False, "white")
g1 = pixel_font.render("Tapeworm", False, "white")
g2 = pixel_font.render("Drill Rush", False, "white")
g3 = pixel_font.render("TBD", False, "white")

title_r = title.get_rect(center=(WINDOW_WIDTH/2, 60))
about_r = about.get_rect(topleft=(30, 120))
g1_r = g1.get_rect(topleft=(30, 200))
g2_r = g2.get_rect(topleft=(30, 280))
g3_r = g3.get_rect(topleft=(30, 360))

main_window = [(about, about_r), (title, title_r), (g1, g1_r), (g2, g2_r), (g3, g3_r)]

# Side Window
s_bg = pygame.surface.Surface(size=(450, 420))
s_bg.fill("darkslategray3")
s_bg_r = s_bg.get_rect(topleft=(290, 100))

# Selector
selector = pygame.surface.Surface(size=(230, 50))
selector.fill("gray80")
start_y = 110
selector_r = selector.get_rect(topleft=(25, 110))
select_index = 0
offset = 80

pygame.display.set_caption("2D Games Collection")
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if (select_index > 0): select_index -= 1
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if (select_index < len(main_window) - 2): select_index += 1
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if (select_index == 1):
                    snake_game()
                elif (select_index == 2):
                    drill_game()

    screen.fill("black")
    selector_r.y = start_y + select_index * offset
    screen.blit(m_bg, m_bg_rect)
    screen.blit(s_bg, s_bg_r)
    screen.blit(selector, selector_r)
    for elem in main_window:
            screen.blit(elem[0], elem[1])
    display_text_block(all_text[select_index])
    
    
    pygame.display.update()
    clock.tick(60)