class Cfg:
    APPLICATION_TITLE = "Game of Life"

    # Dimentions of Things
    SCREEN_SIZE = WIDTH, HEIGHT = 800, 600
    MENU_SIZE = MENU_WDITH, MENU_HEIGHT = WIDTH, 50
    MENU_COORDS = MENU_X, MENU_Y = 0, 0
    MENU_BTN_PAD = 10
    MENU_BTN_LEFT = 30
    BOARD_SIZE = BOARD_WIDTH, BOARD_HEIGHT = WIDTH, HEIGHT - MENU_HEIGHT
    BOARD_COORDS = BOARD_X, BOARD_Y = 0, MENU_HEIGHT
    BTN_SIZE = BTN_WIDTH, BTN_HEIGHT = 32, 32

    # Colors: from Chapter 2, Invent With Pygame (online free)
    # --> https://inventwithpython.com/pygame/chapter2.html
    AQUA = (0, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    FUCHSIA = (255, 0, 255)
    GRAY = (128, 128, 128)
    GREEN = (0, 128, 0)
    LIME = (0, 255, 0)
    MAROON = (128, 0, 0)
    NAVY_BLUE = (0, 0, 128)
    OLIVE = (128, 128, 0)
    PURPLE = (128, 0, 128)
    RED = (255, 0, 0)
    SILVER = (192, 192, 192)
    TEAL = (0, 128, 128)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
