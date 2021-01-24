import os
import platform
from tkinter import filedialog
import tkinter as tk

root = tk.Tk()
root.attributes('-topmost', 1)
root.geometry("500x150")
root.withdraw()

system = platform.system()


def file1():
    if system != 'Windows':
        global filePath1
        filePath1 = filedialog.askopenfilename(initialdir="~/", title="Select File")
    else:
        filePath1 = filedialog.askopenfilename(initialdir=os.environ['USERPROFILE'], title="Select File")


def file2():
    if system != 'Windows':
        global filePath2
        filePath2 = filedialog.askopenfilename(initialdir="~/", title="Select File")
    else:
        filePath2 = filedialog.askopenfilename(initialdir="C:\\Users\\%USERPROFILE%\\", title="Select File")

def file3():
    if system != 'Windows':
        global filePath3
        filePath3 = filedialog.askopenfilename(initialdir="~/", title="Select File")
    else:
        filePath3 = filedialog.askopenfilename(initialdir="C:\\Users\\%USERPROFILE%\\", title="Select File")

def compare():
    """"This function returns the SHA-1 hash
    of the file passed into it"""
    print("Building file differences...")

    # open file for reading in binary mode
    # with open(filePath, 'rb') as file:
    with open(filePath1, "rb") as f:
        global parsedFile
        parsedFile = []
        byte = f.read(1)
        parsedFile.append(byte)
        while byte:
            # Do stuff with byte.
            byte = f.read(1)
            parsedFile.append(byte)
    print("File 1 Successfully Parsed, Size of File: ")
    print(len(parsedFile))
    with open(filePath2, 'rb') as f:
        global parsedFile2
        parsedFile2 = []
        byte = f.read(1)
        parsedFile2.append(byte)
        while byte:
            byte = f.read(1)
            parsedFile2.append(byte)
    print("File 2 Successfully Parsed, Size of File: ")
    print(len(parsedFile2))

    with open(filePath3, 'rb') as f:
        global parsedFile3
        parsedFile3 = []
        byte = f.read(1)
        parsedFile3.append(byte)
        while byte:
            byte = f.read(1)
            parsedFile3.append(byte)
    print("File 3 Successfully Parsed, Size of File: ")
    print(len(parsedFile3))

    for b in range(len(parsedFile)):
        if b < len(parsedFile):
            if b < len(parsedFile2):
                if parsedFile[b] == parsedFile2[b]:
                    if parsedFile[b] == parsedFile3[b]:
                        print("Match Found at byte location: " + str(b) + str(parsedFile[b]))

root.deiconify()
root.after_idle(root.attributes, '-topmost', 0)
root.lift()

root.update()

check_sum_text = tk.Text(root, height=2, width=64)
check_sum_text.pack()

openFile1 = tk.Button(root, text="Open File 1", command=file1)
openFile1.pack()

openFile2 = tk.Button(root, text="Open File 2", command=file2)
openFile2.pack()

openFile3 = tk.Button(root, text="Open File 3", command=file3)
openFile3.pack()

compare = tk.Button(root, text="Compare", command=compare)
compare.pack()

root.mainloop()
