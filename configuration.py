# configuration 
# constants
DARKMODE = 0
LIGHTMODE = 1
APP_NAME = 'Notepad'

DARKMODE_BG = 'black'
DARKMODE_TEXT = 'white'
DARKMODE_CURSOR = 'white'

LIGHTMODE_BG = 'white'
LIGHTMODE_TEXT = 'black'
LIGHTMODE_CURSOR = 'black'

DEFAULT_FONT = 'Calibri'
DEFAULT_FONT_SIZE = 24

# default settings
CURRENT_MODE = DARKMODE

falg_isTextHighlighted = False
words_ = None

# menu bar
mainMenuBase = [['File', ['Open', 'Save']], ['Edit', ['Find', 'Replace', 'Spell check', 'Remove highlight']]]
mainMenuDarkMode = mainMenuBase + [['Configure', ['Dark mode']]]
mainMenuLightMode = mainMenuBase + [['Configure', ['Light mode']]]

# functionList name is Menu+'_'+SubMenu, ensure no collision