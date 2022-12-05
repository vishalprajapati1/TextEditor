from tkinter import *
from configuration import *
from functions import removeHighlight, full_spell_check, findWindow, load_words, menuConstructor, openTextFile, replaceWindow, saveFileWindow, textBoxConstruction, toggleModeDark, toggleModeLight

def ToggleModeLight_():
    root.config(menu = menuConstructor(root, mainMenuDarkMode, functionList))
    toggleModeLight(textArea)

def ToggleModeDark_():
    root.config(menu = menuConstructor(root, mainMenuLightMode, functionList))
    toggleModeDark(textArea)

def removeHighlight_():
    removeHighlight(textArea);

def SaveFile_():
    saveFileWindow(root, textArea)
    
def OpenFile_():
    openTextFile(textArea)

def Find_():
    findWindow(root, textArea)

def Replace_():
    replaceWindow(root, textArea)

def SpellCheck_():
    full_spell_check(textArea)

root = Tk()
root.geometry('1100x600')

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

root.title(APP_NAME)
textArea = textBoxConstruction(root, CURRENT_MODE);
textArea.pack()
load_words()

functionList = {
    'File_Open': OpenFile_, 
    'File_Save': SaveFile_, 
    'Edit_Find': Find_,
    'Edit_Replace': Replace_,
    'Edit_Spell check': SpellCheck_,
    'Configure_Dark mode': ToggleModeDark_,
    'Configure_Light mode': ToggleModeLight_,
    'Edit_Remove highlight': removeHighlight_
}

menuBar = menuConstructor(root, mainMenuLightMode, functionList)
root.config(menu = menuBar)

mainloop()