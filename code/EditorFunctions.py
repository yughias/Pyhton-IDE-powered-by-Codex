from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox
import subprocess

file_path = None
def setFileInfo(file_info):
    file_info.config(text='File: ' + file_path)

    with open('last_open.txt', 'w') as f:
        f.write(file_path)

def open_last_file(editor, file_info):
    global file_path
    try:
        with open('last_open.txt', 'r') as f:
            file_path = f.read()
        with open(file_path, 'r') as f:
            file = f.read()
            editor.delete(1.0, END)
            editor.insert(1.0, file)

        setFileInfo(file_info)
        editor.update()
    except:
        pass
def Save(editor, file_info):
    global file_path
    if file_path == None:
        answer = messagebox.askyesno("Question","No file selected. Save as new file?")
        if answer == True:
            SaveAs(editor, file_info)
        return

    with open(file_path, "w") as f:
        f.write(editor.get(1.0, 'end-1c'))

def SaveAs(editor, file_info):
    global file_path
    file_path = filedialog.asksaveasfilename(title = "Save File",
                                             filetypes = [("Python files",
                                                           "*.py*")] )

    Save(editor, file_info)
    setFileInfo(file_info)

def Run(editor, output, file_info):
    if file_path == None:
        answer = messagebox.askyesno("Question","You need to save the file first. Save?")
        if answer == True:
            SaveAs(editor, file_info)
        else:
            return
    else:
        Save(editor, file_info)
    output.delete(1.0, END)
    command = 'python ' + file_path

    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    while True:
        outResult = p.stdout.readline()
        output.insert(END, outResult)
        if not outResult:
            break

def Open(editor, file_info):
    global file_path
    file_path = filedialog.askopenfilename(title = "Select a File",
                                          filetypes = (("Python files",
                                                        "*.py*"),
                                                       ("all files",
                                                        "*.*")))

    with open(file_path, 'r') as f:
        file = f.read()
        editor.delete(1.0, END)
        editor.insert(1.0, file)

    setFileInfo(file_info)
    editor.update()

def add_tab(editor):
    tab_n = 0
    lines = editor.get(1.0, editor.index(INSERT)).splitlines()
    if lines[-1][-1] == ':' :
        tab_n = 1;

    tab_n += lines[-1].count("\t")
    editor.insert(editor.index(INSERT), '\t'*tab_n)

def insert_brackets(key, editor, brackets):
    start_b = brackets[0]
    end_b = brackets[1]
    text = editor.get(1.0, 'end')
    for bracket in brackets:
        if key.char in bracket:
            start_count = text.count(bracket[0])
            end_count = text.count(bracket[1])
            if start_count > end_count:
                index = editor.index(INSERT)
                editor.insert(index, bracket[1])
                editor.mark_set("insert", index)
            return
