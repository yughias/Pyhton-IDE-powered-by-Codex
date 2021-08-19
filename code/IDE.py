from tkinter import *
from EditorFunctions import *
from CustomElements import *
from AI import *
import keyword
import builtins

#list of colored worda
python_keyword = ['[^a-zA-Z]*' + word + '([^a-zA-Z])' for word in keyword.kwlist]
python_variable_names = dir(builtins)
operators = ['+', '-', '/', '=', '*']
brackets = ["''", '""', '()', '[]', '{}', '()']

root = Tk()
root.title('Python Editor')
root.geometry("500x500")

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

root.bind('<F5>', lambda event : Run(editor, output, file_info))
root.bind('<Control-s>', lambda event : Save(editor, file_info))
root.bind('<Control-S>', lambda event : SaveAs(editor, file_info))
root.bind('<Control-o>', lambda event : Open(editor, file_info))
root.bind('<F6>', lambda event : Codex(editor, ['\n\n'], from_begin.get()))
root.bind('<Control-F6>', lambda event : Codex(editor, None, from_begin.get()))


main_window = PanedWindow(orient="horizontal")
main_window.grid(row=0, column=0, sticky='nsew', padx=(4, 4), pady=(4, 4))

left = Frame(main_window)
right = Frame(main_window)
main_window.add(left, stretch="always")
main_window.add(right, stretch="always")

left.grid_columnconfigure(0, weight=1, uniform='left')
left.grid_columnconfigure(1, weight=40, uniform='left')
left.grid_columnconfigure(2, weight=1, uniform='left')
left.rowconfigure(0, weight=1)

right.grid_rowconfigure(0, weight=1, uniform='right')
right.grid_rowconfigure(1, weight=20, uniform='right')
right.grid_columnconfigure(0, weight=1, uniform='right')

editor = CustomText(left, undo=True)
editor.tag_configure("purple", foreground="purple")
editor.tag_configure("blue", foreground="blue")
editor.tag_configure("green", foreground="green")
editor.tag_configure("orange", foreground="orange")
editor.tag_configure("black", foreground="black")

editor.load_list(["\'(.*)\'", "\'\'\'(.*)\'\'\'", "\#(.*)", '\"(.*)\"'], 'green', True)
editor.load_list(["\S*(?=\()"], 'blue', True)
editor.load_list(python_keyword, 'purple', True)
editor.load_list(operators, 'purple', False)
editor.load_list(python_variable_names, 'blue', False)
editor.load_list(['\(', '\)'], 'black', True)

editor.bind("<KeyRelease>", lambda event : editor.update() )
editor.bind("<KeyRelease-Return>", lambda event : add_tab(editor))

for bracket in brackets:
    key = '<KeyRelease-' + bracket[0] + ">"
    editor.bind(key, lambda event : insert_brackets(event, editor, brackets))

editor.grid(row=0, column=1, sticky='nsew')

line = LineNumbers(left, editor, background='#282c34', foreground='gray')
line.grid(row=0, column=0, sticky='nsew', padx=0)

def multiple_yview(*args):
    line.yview(*args)
    editor.yview(*args)

scrollbar = Scrollbar(left, orient=VERTICAL, command=multiple_yview)
scrollbar.grid(row=0, column=2, sticky='nsew')

file_info = Label(right, text="File: None", anchor='w')
file_info.grid(row=0, column=0, sticky='nsew')

output = Text(right)
output.grid(row=1, column=0, sticky='nsew', padx=(0, 0))

menubar = Menu(root)

filemenu = Menu(menubar)
filemenu.add_command(label="Open", command=lambda : Open(editor, file_info))
filemenu.add_command(label="Save", command=lambda : Save(editor, file_info))
filemenu.add_command(label="Save As", command=lambda : SaveAs(editor, file_info))

from_begin = BooleanVar()

codexmenu = Menu(menubar)
codexmenu.add_command(label='Codex One Line', command=lambda : Codex(editor, ['\n'], from_begin.get()))
codexmenu.add_command(label='Codex Function', command=lambda : Codex(editor, ['\n\n'], from_begin.get()))
codexmenu.add_command(label='Codex All', command=lambda : Codex(editor, None, from_begin.get()))
codexmenu.add_checkbutton(label="Codex from begin", onvalue=True, offvalue=False, variable=from_begin)

menubar.add_cascade(label="File", menu=filemenu)
menubar.add_command(label="Run", command=lambda : Run(editor, output, file_info))
menubar.add_cascade(label="Codex", menu=codexmenu)
menubar.add_command(label="GPTJ", command=lambda: GPTJ(editor, True))


root.config(menu=menubar)

open_last_file(editor, file_info)

root.mainloop()
