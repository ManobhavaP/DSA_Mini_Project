import pygame, sys, time
import cmn_func as func


pygame.display.set_caption("Towers of Hanoi")

game_done = False
framerate = 60

# game vars:
steps = 0
n_disks = 3
disks = []
towers_midx = [120, 320, 520]
pointing_at = 0
floating = False
floater = 0
paused = False
WHITE = func.WHITE


def menu_screen():  # to be called before starting actual game loop
    global screen, n_disks, game_done
    menu_done = False
    while not menu_done:  # every screen/scene/level has its own loop
        func.screen.fill(func.BLACK)
        func.screen.blit(func.background_image, (0, 0))
        func.custom_text('Ahoy Hanoi !!', func.SCREEN_WIDTH // 2, (func.SCREEN_HEIGHT // 2)-150,func.BIG_SIZE)
        func.custom_text('Use arrow keys to select difficulty:', func.SCREEN_WIDTH // 2, (func.SCREEN_HEIGHT // 2)-50,func.MEDIUM_SIZE)
        func.custom_text(str(n_disks), func.SCREEN_WIDTH // 2, (func.SCREEN_HEIGHT // 2)+50,func.BIG_SIZE)
        func.custom_text('Press ENTER to continue', func.SCREEN_WIDTH // 2, (func.SCREEN_HEIGHT // 2)+150,func.MEDIUM_SIZE)
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    menu_done = True
                    game_done = True
                if event.key == pygame.K_RETURN:
                    menu_done = True
                if event.key in [pygame.K_RIGHT, pygame.K_UP]:
                    n_disks += 1
                    if n_disks > 6:
                        n_disks = 6
                if event.key in [pygame.K_LEFT, pygame.K_DOWN]:
                    n_disks -= 1
                    if n_disks < 1:
                        n_disks = 1
            if event.type == pygame.QUIT:
                menu_done = True
                game_done = True
        pygame.display.flip()
        func.clock.tick(60)

def game_over(): # game over screen
    global screen, steps
    func.screen.fill(func.BLACK)
    func.screen.blit(func.background_image, (0, 0))
    min_steps = 2**n_disks-1
    func.custom_text('You Won!', func.SCREEN_WIDTH // 2, (func.SCREEN_HEIGHT // 2)-150,func.BIG_SIZE)
    func.custom_text('Your Steps: '+str(steps), func.SCREEN_WIDTH // 2, (func.SCREEN_HEIGHT // 2),func.MEDIUM_SIZE)
    func.custom_text('Minimum Steps: '+str(min_steps), func.SCREEN_WIDTH // 2, (func.SCREEN_HEIGHT // 2)+50,func.MEDIUM_SIZE)
    if min_steps==steps:
        func.custom_text('You finished in minumum steps!',func.SCREEN_WIDTH // 2, (func.SCREEN_HEIGHT // 2)+150,func.MEDIUM_SIZE)
    pygame.display.flip()
    time.sleep(2)   # wait for 2 secs 
    pygame.quit()   #pygame exit
    sys.exit()  #console exit

def draw_towers():
    for xpos in range(40, 460+1, 200):
        pygame.draw.rect(func.screen, func.GREEN, pygame.Rect(xpos, 400, 160 , 20))
        pygame.draw.rect(func.screen, func.GREY, pygame.Rect(xpos+75, 200, 10, 200))
    func.draw_text('Start',func.BLACK,towers_midx[0], 403,func.font_default)
    func.draw_text('Finish',func.BLACK,towers_midx[2], 403,func.font_default)

def make_disks():
    global n_disks, disks
    disks = []
    height = 20
    ypos = 397 - height
    width = n_disks * 23
    for i in range(n_disks):
        disk = {}
        disk['rect'] = pygame.Rect(0, 0, width, height)
        disk['rect'].midtop = (120, ypos)
        disk['val'] = n_disks-i
        disk['tower'] = 0
        disks.append(disk)
        ypos -= height+3
        width -= 23

def draw_disks():
    global screen, disks
    for disk in disks:
        pygame.draw.rect(func.screen, func.NEON_PURPLE, disk['rect'])
    return

def draw_ptr():
    ptr_points = [(towers_midx[pointing_at]-7 ,440), (towers_midx[pointing_at]+7, 440), (towers_midx[pointing_at], 433)]
    pygame.draw.polygon(func.screen, func.RED, ptr_points)
    return

def check_won():
    global disks
    over = True
    for disk in disks:
        if disk['tower'] != 2:
            over = False
    if over:
        time.sleep(0.2)
        game_over()

def reset():
    global steps,pointing_at,floating,floater
    steps = 0
    pointing_at = 0
    floating = False
    floater = 0
    menu_screen()
    make_disks()

def custom_text(text, x, y, size, color=func.YELLOW):
    global screen
    font = func.font_custom
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    func.screen.blit(text_surface, text_rect)

def pause_menu():
    global screen, paused

    background_snapshot = func.screen.copy()

    blurred_screen = pygame.transform.smoothscale(background_snapshot, (func.SCREEN_WIDTH // 10, func.SCREEN_HEIGHT // 10))
    blurred_screen = pygame.transform.smoothscale(blurred_screen, (func.SCREEN_WIDTH, func.SCREEN_HEIGHT))

    overlay = pygame.Surface((func.SCREEN_WIDTH, func.SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))

    #resume_button_rect = pygame.Rect(func.SCREEN_WIDTH // 2 - 50, func.SCREEN_HEIGHT // 2 - 25, 100, 50)
    #menu_button_rect = pygame.Rect(func.SCREEN_WIDTH // 2 - 50, func.SCREEN_HEIGHT // 2 + 25, 100, 50)

    # Initialize the highlighted button
    highlighted_button = "resume"

    func.screen.blit(blurred_screen, (0, 0))
    func.screen.blit(overlay, (0, 0))

    func.custom_text('Game Paused', func.SCREEN_WIDTH // 2, func.SCREEN_HEIGHT // 3, func.BIG_SIZE)
    custom_text('Resume', func.SCREEN_WIDTH // 2, func.SCREEN_HEIGHT // 2, func.MEDIUM_SIZE, color=func.RED if highlighted_button == "resume" else func.YELLOW)
    custom_text('Main Menu', func.SCREEN_WIDTH // 2, func.SCREEN_HEIGHT // 2 + 50, func.MEDIUM_SIZE, color=func.RED if highlighted_button == "menu" else func.YELLOW)

    pygame.display.flip()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Resume the game
                    paused = False
                elif event.key == pygame.K_RETURN:
                    if highlighted_button == "resume":
                        # Resume the game
                        paused = False
                    elif highlighted_button == "menu":
                        # Return to the main menu
                        paused = False
                        reset()
                elif event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    # Toggle the highlighted button
                    highlighted_button = "menu" if highlighted_button == "resume" else "resume"

        func.screen.blit(blurred_screen, (0, 0))
        func.screen.blit(overlay, (0, 0))

        func.custom_text('Game Paused', func.SCREEN_WIDTH // 2, func.SCREEN_HEIGHT // 3, func.BIG_SIZE)
        custom_text('Resume', func.SCREEN_WIDTH // 2, func.SCREEN_HEIGHT // 2, func.MEDIUM_SIZE, color=func.RED if highlighted_button == "resume" else func.YELLOW)
        custom_text('Main Menu', func.SCREEN_WIDTH // 2, func.SCREEN_HEIGHT // 2 + 50, func.MEDIUM_SIZE, color=func.RED if highlighted_button == "menu" else func.YELLOW)

        pygame.display.flip()

        func.clock.tick(60)


# main game loop:
if __name__ == '__main__':
        menu_screen()
        make_disks()
        while not game_done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = True
                        pause_menu()
                    if event.key == pygame.K_q:
                        game_done = True
                    if event.key == pygame.K_RIGHT:
                        pointing_at = (pointing_at+1)%3
                        if floating:
                            disks[floater]['rect'].midtop = (towers_midx[pointing_at], 100)
                            disks[floater]['tower'] = pointing_at
                    if event.key == pygame.K_LEFT:
                        pointing_at = (pointing_at-1)%3
                        if floating:
                            disks[floater]['rect'].midtop = (towers_midx[pointing_at], 100)
                            disks[floater]['tower'] = pointing_at
                    if event.key == pygame.K_UP and not floating:
                        for disk in disks[::-1]:
                            if disk['tower'] == pointing_at:
                                floating = True
                                floater = disks.index(disk)
                                disk['rect'].midtop = (towers_midx[pointing_at], 100)
                                break
                    if event.key == pygame.K_DOWN and floating:
                        for disk in disks[::-1]:
                            if disk['tower'] == pointing_at and disks.index(disk)!=floater:
                                if disk['val']>disks[floater]['val']:
                                    floating = False
                                    disks[floater]['rect'].midtop = (towers_midx[pointing_at], disk['rect'].top-23)
                                    steps += 1
                                break
                        else: 
                            floating = False
                            disks[floater]['rect'].midtop = (towers_midx[pointing_at], 400-23)
                            steps += 1
            if not paused:
                func.screen.fill(func.BLACK)
                func.screen.blit(func.background_image, (0, 0))
                draw_towers()
                draw_disks()
                draw_ptr()
                func.draw_text('Steps: '+str(steps), func.WHITE,func.SCREEN_WIDTH//2, 50,func.font_custom)
                pygame.display.flip()
                if not floating:check_won()
                func.clock.tick(framerate)