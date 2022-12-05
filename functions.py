import tkinter as tk
from tkinter.filedialog import askopenfilename
from configuration import *

dictionary_words = {}


#  this implementation is not efficienty as we've to deal with very large numbers
#  todo: update with a efficient approach
# class RollingHash:
#     def __init__(self, text, sizeWord):
#         self.text = text
#         self.hash = 0
#         self.sizeWord = sizeWord
#         for i in range(0, sizeWord):
#             self.hash = self.hash + (ord(self.text[i]) - ord('a')+1)*(26**(sizeWord-i-1))
#         self.window_start = 0
#         self.window_end = sizeWord
#     def move_window(self):
#         if(self.window_end <= len(self.text) - 1):
#             self.hash = self.hash - (ord(self.text[self.window_start]) - ord("a")+1)*26**(self.sizeWord-1)
#             self.hash = self.hash * 26
#             self.hash = self.hash + ord(self.text[self.window_end])- ord("a")+1
#             self.window_start = self.window_start + 1
#             self.window_end = self.window_end + 1
#     def window_text(self):
#         return self.text[self.window_start:self.window_end]

# dictionary
def load_words():
    global dictionary_words
    with open('words_alpha.txt') as word_file:
        valid_words = set(word_file.read().split())
    
    dictionary_words = valid_words

def search(text, word):
    positions = []
    previous = 0
    while True:
        pos = text.find(word, previous)
        if pos == -1: break
        previous = pos + 1
        position.append(pos)
    return positions

def menuConstructor(root, mainMenuList, functionList):
    menubar = tk.Menu(root)
    for mainMenu in mainMenuList:
        subMenuConstructor(menubar, mainMenu, functionList)
    return menubar

def subMenuConstructor(menubar, mainMenu, functionList):
    menuOption = tk.Menu(menubar, tearoff = 0)
    menubar.add_cascade(label = mainMenu[0], menu = menuOption)
    for subMenu in mainMenu[1]:
            try:
                menuOption.add_command(label = subMenu, command = functionList[mainMenu[0]+'_'+subMenu])
            except:
                print('Function list error')
    return

def textBoxConstruction(root, colorMode):
    textBox = tk.Text(root, 
        font=(DEFAULT_FONT, DEFAULT_FONT_SIZE),
        background = textBoxBg(colorMode),
        foreground = textBoxFg(colorMode),
        insertbackground = textBoxCursor(colorMode),
        wrap = 'word')
    textBox.grid_rowconfigure(0, weight=1)
    textBox.grid_columnconfigure(0, weight=1)
    return textBox

def textBoxBg(colorMode):
    if(colorMode == DARKMODE):
        return DARKMODE_BG
    elif(colorMode == LIGHTMODE):
        return LIGHTMODE_BG 

def textBoxFg(colorMode):
    if(colorMode == DARKMODE):
        return DARKMODE_TEXT
    elif(colorMode == LIGHTMODE):
        return LIGHTMODE_TEXT

def textBoxCursor(colorMode):
    if(colorMode == DARKMODE):
        return DARKMODE_CURSOR
    elif(colorMode == LIGHTMODE):
        return LIGHTMODE_CURSOR

def toggleModeDark(textbox):
    CURRENT_MODE = DARKMODE
    textbox.config(
    background = DARKMODE_BG,
    foreground = DARKMODE_TEXT,
    insertbackground = DARKMODE_CURSOR)
    
    textbox.tag_add('a', '1.0', tk.END)
    textbox.tag_config('a', background = DARKMODE_BG,
    foreground = DARKMODE_TEXT,
    insertbackground = DARKMODE_CURSOR)

def toggleModeLight(textbox):
    CURRENT_MODE = LIGHTMODE
    textbox.config(
    background = LIGHTMODE_BG,
    foreground = LIGHTMODE_TEXT,
    insertbackground = LIGHTMODE_CURSOR)
    textbox.tag_add('a', '1.0', tk.END)
    textbox.tag_config('a', background = LIGHTMODE_BG,
    foreground = LIGHTMODE_TEXT,
    insertbackground = LIGHTMODE_CURSOR)

def openTextFile(textArea):
    filename = askopenfilename()
    with open(filename, 'r') as line:
        for l in line.readlines():
            textArea.insert(tk.END, l)

def saveFileWindow(root, textArea):
    newWindow = tk.Tk()
    newWindow.resizable(False, False)
    newWindow.eval('tk::PlaceWindow . center')
    fileName = tk.Text(newWindow, height = 1, width = 15)
    fileName.place(x = 25, y = 10)
    newWindow.geometry('170x70')
    def saveFile(event_):
        if(fileName.get('1.0', tk.END)[:-1] == ''):
            return # bad call
        file = open(fileName.get("1.0", tk.END)[:-1], "w+")
        file.write(textArea.get("1.0", tk.END))
        file.close()

    btn = tk.Button(newWindow, text = 'Save', command = newWindow.destroy)
    btn.place(x = 65, y = 35)
    btn.bind("<Button>", saveFile)

def findWindow(root, textArea):
    newWindow = tk.Tk()
    newWindow.resizable(False, False)
    newWindow.eval('tk::PlaceWindow . center')
    fileName = tk.Text(newWindow, height = 1, width = 15)
    fileName.place(x = 25, y = 10)
    newWindow.geometry('170x70')
    def f_(event_):
        textHighlighter(textArea, (len(fileName.get('1.0', tk.END))-1, 
        search(textArea.get('1.0', tk.END), fileName.get('1.0', tk.END))
        ))
        newWindow.destroy
    btn = tk.Button(newWindow, text = 'Find', command = newWindow.destroy)
    btn.place(x = 65, y = 35)
    btn.bind("<Button>", f_)

def replaceWindow(root, textArea):
    newWindow = tk.Tk()
    newWindow.resizable(False, False)
    newWindow.eval('tk::PlaceWindow . center')
    tk.Label(newWindow, text = 'Find what: ').place(x = 15, y = 5)
    fileName = tk.Text(newWindow, height = 1, width = 15)
    fileName.place(x = 15, y = 25)
    tk.Label(newWindow, text = 'Replace what: ').place(x = 15, y = 45)
    rep_ = tk.Text(newWindow, height = 1, width = 15)
    rep_.place(x = 15, y = 65)
    newWindow.geometry('150x120')
    def f_(dummyArgument):
        removeHighlight(textArea)
        textReplace(textArea, (len(fileName.get('1.0', tk.END))-1,
        search(textArea.get('1.0', tk.END), fileName.get('1.0', tk.END))), rep_.get('1.0', tk.END)[:len(rep_.get('1.0', tk.END))-1])

    btn = tk.Button(newWindow, text = 'Replace', command = newWindow.destroy)
    btn.place(x = 50, y = 90)
    btn.bind("<Button>", f_)
    
def textHighlighter(textArea, r_): # r_ is tuple 0 -> length of replaced text, 1-> position tuple
    global falg_isTextHighlighted
    
    for tag in textArea.tag_names():
        textArea.tag_remove(tag, "1.0", "end")

    for endPosition in r_[1]:
        textArea.tag_add('highlight', '1.0'+'+'+str(endPosition)+'c', '1.0'+'+'+str(endPosition+r_[0])+'c')
        textArea.tag_config('highlight', background = 'yellow')
    falg_isTextHighlighted = True
    

def removeHighlight(textArea):
    global falg_isTextHighlighted
    if(falg_isTextHighlighted):
        textArea.tag_add('remove_highlight', '1.0', textArea.index(tk.END))
        textArea.tag_config('remove_highlight', background = textBoxBg(CURRENT_MODE))
        falg_isTextHighlighted = False
        
def textReplace(textArea, r_, stringToReplace):
    offset_ = 0
    for endPosition in r_[1]:
        textArea.delete('1.0+'+str(endPosition+offset_)+'c', '1.0+'+str((endPosition+offset_)+r_[0])+'c')
        textArea.insert('1.0+'+str(endPosition+offset_)+'c', stringToReplace)
        offset_ = offset_ + (len(stringToReplace) - r_[0])

def split_(text):
    seperator_ = (' ', '\n', '.', ',')
    split_pos = []
    isAtSeperator = True
    previous_pos = 0
    for i in range(0, len(text)):
        if(text[i] in seperator_):
            isAtSeperator = True;
            if((i - previous_pos) > 1):
                split_pos.append([previous_pos, i-1])
                previous_pos = i
        elif(isAtSeperator):
            previous_pos = i
            isAtSeperator = False
    return split_pos

def full_spell_check(textArea):
    text = textArea.get('0.0', tk.END)
    for pair in split_(text):
        # O(1) lookup as dictionary is a hash table
        word = text[pair[0]:(pair[1]+1)]
        word = word.lower()
        if(word not in dictionary_words):
            textArea.tag_add('error', '1.0+'+str(pair[0])+'c', '1.0+'+str(pair[1]+1)+'c')
            textArea.tag_config('error', underline = True)
    return

# Program below that are archived #

# # get change position
# # def spell_check_position():
# #     return

# ## forward suggestions are archived
# # redsigned forward suggestions functions

# # marker -- markSugg
# def getCurrPos(textArea):
#     return len(textArea.get('1.0', textArea.index('insert')))

# def p_s_(textArea):
#     global previous_insert_position, sp_
#     if(getCurrPos(textArea) != (previous_insert_position+1)):
#         print('c changed')
#     if(textArea.get(textArea.index('insert'), textArea.index('insert')+'+1c') in ('\n', ' ')):
#         if(textArea.get(textArea.index('insert')+'-1c') != '\n'):
#             # mark - was working here
#             None;
#         previous_insert_position = len(textArea.get('1.0', textArea.index('insert')))    
#         return
#     if(textArea.get(textArea.index('insert'), textArea.index('insert')+'+1c') in ('\n', ' ')):
#         if(textArea.get(textArea.index('insert')+'-1c') != '\n'):
#             sp_ = sp_ + textArea.get(textArea.index('insert')+'-1c')
#         previous_insert_position = len(textArea.get('1.0', textArea.index('insert')))
#         print('pos', previous_insert_position)
#     if(textArea.get(textArea.index('insert')+'-1c') == ' '):
#          sp_ = ''
#     print(sp_)
#     return

# def aarchived_p_s_(textArea):
#     #print(getCurrPos(textArea))
#     # it will return partial speeling as we type or change cursor
#     # only when charater after it is a space -- 
#     # if previous position is not known that go back till you find space
#     # or we could create a space matrix -- 
#     #print('.'+textArea.get(textArea.index('insert'), textArea.index('insert')+'+1c')+'.')
#     global previous_insert_position, sp_
#     # #global c_
#     if(getCurrPos(textArea) != (previous_insert_position + 1)):
#         print('w', 'cursor changed to somewhere')
#         return
#     #     previous_insert_position = textArea.index('insert')
#     #     sp_ = ''
#     #     return

#     if(textArea.get(textArea.index('insert'), textArea.index('insert')+'+1c') in ('\n', ' ')):
#     #     # if cursor is changed
#     #     # keep track of the cursor
#     #     # previous_insert_position = textArea.index('insert')
#         if(textArea.get(textArea.index('insert')+'-1c') != '\n'):
#             sp_ = sp_ + textArea.get(textArea.index('insert')+'-1c')
#         previous_insert_position = len(textArea.get('1.0', textArea.index('insert')))
    
#     if(textArea.get(textArea.index('insert')+'-1c') == ' '):
#          sp_ = ''
#     print(sp_)
#     #     #if(textArea.get(textArea.index(previous_insert_position+'+1c'), textArea.index('insert')) == ''):
#     #         # position is not changed
#     #     #    None
#     #     #print(c_, 'a.'+textArea.get(textArea.index(previous_insert_position+'+1c'), textArea.index('insert'))+'.a')
#     #     #previous_insert_position = textArea.index('insert')
#     #     #c_ = c_ + 1
#     #     #print('sugg_', True, '.' + textArea.get(textArea.index('insert'), textArea.index('insert') + '+1c')+'.')
#     return

# # cache cursor position -- if it is as expected that is previous cursor + 1 then do not check back. if it don't then just check back

# # def getSuggestion(partialSpell):
# #     s_ = None

# #     if(partialSpell == 'len'):
# #         s_ = 'ovo'
# #     if(partialSpell == 'leno'):
# #         s_ = 'vo'
# #     if(partialSpell == 'lenov'):
# #         s_ = 'o'
# #     if(partialSpell == 'lenovo'):
# #         s_ = None
    
# #     if(partialSpell == 'vis'):
# #         s_ = 'hal'
# #     if(partialSpell == 'vish'):
# #         s_ = 'al'
# #     if(partialSpell == 'visha'):
# #         s_ = 'l'
# #     if(partialSpell == 'vishal'):
# #         s_ = None 
# #     return s_

# # end

# # # all below are under construction
# # def _getSuggestion(partialSpell):
# #     s_ = None
# #     #print(partialSpell)
# #     if(partialSpell == 'len'):
# #         s_ = 'ovo'
# #     if(partialSpell == 'leno'):
# #         s_ = 'vo'
# #     if(partialSpell == 'lenov'):
# #         s_ = 'o'
# #     if(partialSpell == 'lenovo'):
# #         s_ = None 
# #     # print(partialSpell, s_)
# #     return s_

# # def addSuggestions_(textArea, spell):
# #     global flag_dict, suggestion_, suggestion_start_position, suggestion_end_position, flag_suggesting
# #     # print('l', flag_dict)
# #     if(flag_suggesting):
# #         return
# #     if(getSuggestion(spell) is None):
# #         flag_dict = False
# #         return
    
# #     suggestion_ = getSuggestion(spell)
# #     cursorPosition = textArea.index('insert')
# #     endPosition = textArea.index('end-1c')
# #     # text_one_ = textArea.get('1.0', cursorPosition) 
# #     text_end_ = textArea.get(cursorPosition, endPosition)
# #     # adding suggestion
# #     textArea.delete(cursorPosition, endPosition)
# #     textArea.insert(tk.END, getSuggestion(spell))
# #     # flag_suggesting = True
# #     suggestion_start_position, suggestion_end_position = cursorPosition, textArea.index('end-1c')
# #     #print('s-', suggestion_start_position, suggestion_end_position)
# #     textArea.tag_add('start', cursorPosition, textArea.index("end-1c"))
# #     textArea.tag_config('start', background = "yellow")
# #     textArea.insert(tk.END, text_end_)
# #     textArea.mark_set('insert', cursorPosition)
# #     flag_suggesting = True
# #     flag_dict = False
# #     # flag_cp = True
    
# # def extractSpell(textArea):
# #     #print('spell', textArea.get('1.0', tk.END))
# #     t_ = textArea.get('1.0', textArea.index('insert'))
# #     #print(t_+'.')
# #     return t_
# #     #return t_[0:(len(t_)-1)]

# # def remove_suggestion(textArea):
# #     global removing_sugg_, suggestion_start_position, suggestion_end_position
# #     removing_sugg_ = True
# #     # remove suggestions when cursor is moved
# #     cursorPosition = textArea.index('insert')
# #     endPosition = textArea.index('end-1c')
# #     # text_one_ = textArea.get('1.0', cursorPosition) 
# #     text_end_ = textArea.get(suggestion_end_position, endPosition)
# #     # adding suggestion
# #     textArea.delete(suggestion_end_position, endPosition)
# #     # textArea.insert(tk.END, getSuggestion(spell))
# #     #print('s-', suggestion_start_position, suggestion_end_position)
# #     # textArea.tag_add('start', cursorPosition, textArea.index("end-1c"))
# #     # textArea.tag_config('start', background = "yellow")
# #     textArea.insert(tk.END, text_end_)
# #     textArea.mark_set('insert', cursorPosition)
# #     removing_sugg_ = False
# #     return

# # # archived
# # # def currentSuggestion_f_(textArea):
# # #     global flag_dict, suggestion_end_position, suggestion_, suggestion_start_position
# # #     if(textArea.get(suggestion_start_position, suggestion_start_position + '+1c') == suggestion_[0]):
# # #     # text_one_ = textArea.get('1.0', cursorPosition) 
# # #         flag_dict = True
# # #         cursorPosition = textArea.index('insert')
# # #         endPosition = textArea.index('end-1c')
# # #         text_end_ = textArea.get(cursorPosition, endPosition)
# # #         textArea.delete(cursorPosition, endPosition)
# # #         textArea.insert(tk.END, suggestion_[1:])
# # #         textArea.tag_add('start', cursorPosition, textArea.index("end-1c"))
# # #         textArea.tag_config('start', background = "yellow")
# # #         textArea.insert(tk.END, text_end_)
# # #         textArea.mark_set('insert', cursorPosition)
# # #         flag_dict = False
# # #     return

# # # functions related to suggestions
# # def removeSuggestions(textArea):
# #     # when cursor is moved
# #     textArea.delete(suggestion_start_position, suggestion_end_position)
# #     return

# # def forwardSuggestions(textArea):
# #     global removing_sugg_, flag_dict, flag_suggesting, suggestion_start_position, suggestion_end_position
# #     # Text area get current spelling
# #     # sprint(extractSpell(textArea)+'.')
# #     # print(flag_dict)
# #     # if(flag_dict):
# #     #     return
# #     # if(removing_sugg_):
# #     #     return
# #     # if(flag_suggesting):
# #     #     remove_suggestion(textArea)
# #     #     flag_suggesting = False
# #     #     # removing_sugg_ = False
# #     #     suggestion_start_position, suggestion_end_position = '',''
# #     #     return
# #     #  # it should not work, suggestions are generated
# #     # # if(flag_suggesting):
# #     # #     remove_suggestion(textArea)
# #     # #     return
# #     # flag_dict = True
# #     addSuggestions(textArea, extractSpell(textArea))
# #     return
