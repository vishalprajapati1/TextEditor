import tkinter as tk
from tkinter.filedialog import askopenfilename
from configuration import *

dictionary_words = {}

# dictionary
def load_words():
    global dictionary_words
    with open('words_alpha.txt') as word_file:
        valid_words = set(word_file.read().split())
    
    dictionary_words = valid_words

def search(text, word):
    # word contain redundant '\n'
    word = word[:-1];
    positions = []
    previous = 0
    while True:
        pos = text.find(word, previous)
        if pos == -1: break
        previous = pos + 1
        positions.append(pos)
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
