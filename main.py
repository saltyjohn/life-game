import pygame
from config import Cfg as cfg
from classes import Area, BlitList, MenuButton, Board

# Game Init, Screen/Display, and Clock
pygame.init()
pygame.display.set_caption(cfg.APPLICATION_TITLE)
screen = pygame.display.set_mode((cfg.WIDTH, cfg.HEIGHT))
clock = pygame.time.Clock()

# Game Blit Objects
menu = Area(size=cfg.MENU_SIZE, coords=cfg.MENU_COORDS, color=cfg.SILVER)
board = Board(size=cfg.BOARD_SIZE, coords=cfg.BOARD_COORDS, color=cfg.WHITE)
play_btn = MenuButton(parent=menu, img_loc="./img/play.png", nth_pos=1)
pause_btn = MenuButton(parent=menu, img_loc="./img/pause.png", nth_pos=2)
trash_bin = MenuButton(parent=menu, img_loc="./img/trash-bin.png", nth_pos=3)

menu_btns = [play_btn, pause_btn, trash_bin]
blit_list = BlitList(objs=[
    menu.main_blit,
    board.main_blit,
    play_btn.main_blit,
    pause_btn.main_blit,
    trash_bin.main_blit,
])


def main():
    app_running = True
    sim_running = False
    sim_rate = 5

    while app_running:
        mouse_pos = pygame.mouse.get_pos()

        if sim_running:
            clock.tick(sim_rate)
            board.run_sim()

        for obj, obj_coords in blit_list.objs:
            screen.blit(obj, obj_coords)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                app_running = False

            blit_list.highlight_updater(menu_btns, mouse_pos)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for btn in menu_btns:
                    if btn.img_rect.collidepoint(mouse_pos):
                        if btn.img_name == 'play':
                            sim_running = True
                            print("Simmulation Running")
                            break
                        if btn.img_name == 'pause':
                            sim_running = False
                            print("Simmulation Stopped")
                            break
                        if btn.img_name == 'trash-bin':
                            sim_running = False
                            print("Simmulation Stopped")
                            board.clear_board()
                            board.update_blit()

                for row in board.squares:
                    for square in row:
                        if square.img_rect.collidepoint(mouse_pos):
                            square.update_square()
                            board.update_blit()

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":

    main()
