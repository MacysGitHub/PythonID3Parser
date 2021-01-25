import os
import platform
from tkinter import filedialog
import tkinter as tk
from array import array

root = tk.Tk()
root.attributes('-topmost', 1)
root.geometry("500x500")
root.withdraw()

system = platform.system()

def file1():
    if system != 'Windows':
        global filePath1
        filePath1 = filedialog.askopenfilename(initialdir="~/", title="Select File")
    else:
        filePath1 = filedialog.askopenfilename(initialdir=os.environ['USERPROFILE'] + "\\Downloads\\",
                                                   title="Select File")

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


def gettitle(parsedFile):
    global songTitleIndex
    global songTitleArray
    global songTitleName

    songTitleArray = []
    songTitleName = ""
    for s in range(len(parsedFile)):
        if str(parsedFile[s].hex()) == "ff":
            if str(parsedFile[s + 1].hex()) == "fe":
                songTitleIndex = s + 2
                for m in range(songTitleIndex, len(parsedFile)):
                    if parsedFile[m] != b'\x00':
                        if parsedFile[m] == b'\x54':
                            if parsedFile[m + 1] == b'\x50':
                                if parsedFile[m + 2] == b'\x45':
                                    if parsedFile[m + 3] == b'\x31':
                                        break
                        songTitleArray.append(parsedFile[m].decode(encoding="UTF-8"))

            break

    print("Parsing complete, displaying song information...")
    if (songTitleArray):
        songName = songTitleName.join(songTitleArray)
        print("Song Title:" + songName)
        check_sum_text.insert(tk.END, "Song Title: " + songName)
    else:
        print("Format not recognized or cannot find ID3 tag information")
    # if not songTitleArray:
    #     print("Could not find song title")
    #
    # if songTitleArray:
    #     songName = songTitleName.join(songTitleArray)
    #     print("Song title: " + songName)

    # exit(0)

def extract():
    """"This function returns the SHA-1 hash
    of the file passed into it"""
    print("Building file array for comparison...")

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
        if parsedFile[0] == b'I':
            if parsedFile[1] == b'D':
                if parsedFile[2] == b'3':
                    print("ID3 found, checking Version...")
                    id3 = []
                    id3str = ""
                    s = 0
                    for s in range(3):
                        id3.append(parsedFile[s].decode(encoding="ascii"))
                    print(id3str.join(id3))

                if str(parsedFile[3]).__contains__("x03"):
                    print("ID3v2.3 Identified, Processing Metadata....")
                    if str(parsedFile[10]) == str(b'T'):
                        print("Found Title!")
                        for s in range(len(parsedFile)):
                            if parsedFile[s] == b'T':
                                global titleStart
                                titleStart = s
                                if parsedFile[s + 1] == b'I':
                                    print("First Title Index: " + str(titleStart))
                                    break

                        for s in range(len(parsedFile)):
                            if parsedFile[s] == b'T':
                                if parsedFile[s + 1] == b'P':
                                    if parsedFile[s + 2] == b'E':
                                        if parsedFile[s + 3] == b'1':
                                            global ArtistInfo
                                            ArtistInfo = s
                                            print("Artist Tag at index: " + str(ArtistInfo))
                                    break

                        for s in range(len(parsedFile)):
                            if parsedFile[s] == b'T':
                                if parsedFile[s + 1] == b'A':
                                    if parsedFile[s + 2] == b'L':
                                        if parsedFile[s + 3] == b'B':
                                            global Album
                                            Album = s
                                            print("Album Tag at index: " + str(Album))
                                            check_sum_text.insert(tk.END, "Album Index in file: " + str(Album) + "\n")

        gettitle(parsedFile=parsedFile)

    # print("File 1 Successfully Parsed, Size of File: ")
    # print(len(parsedFile))
    # with open(filePath2, 'rb') as f:
    #     global parsedFile2
    #     parsedFile2 = []
    #     byte = f.read(1)
    #     parsedFile2.append(byte)
    #     while byte:
    #         byte = f.read(1)
    #         parsedFile2.append(byte)
    # print("File 2 Successfully Parsed, Size of File: ")
    # print(len(parsedFile2))
    #
    # with open(filePath3, 'rb') as f:
    #     global parsedFile3
    #     parsedFile3 = []
    #     byte = f.read(1)
    #     parsedFile3.append(byte)
    #     while byte:
    #         byte = f.read(1)
    #         parsedFile3.append(byte)
    # print("File 3 Successfully Parsed, Size of File: ")
    # print(len(parsedFile3))
    #
    # for b in range(len(parsedFile)):
    #     if b < len(parsedFile):
    #         if b < len(parsedFile2):
    #             if parsedFile[b] == parsedFile2[b]:
    #                 if parsedFile[b] == parsedFile3[b]:
    #                     print("Match Found at byte location: " + str(b) + str(parsedFile[b]))


root.deiconify()
root.after_idle(root.attributes, '-topmost', 0)
root.lift()

root.update()

check_sum_text = tk.Text(root, height=10, width=64)
check_sum_text.pack()

openFile1 = tk.Button(root, text="Open MP3 File...", command=file1)
openFile1.pack()

# openFile2 = tk.Button(root, text="Open File 2", command=file2)
# openFile2.pack()
#
# openFile3 = tk.Button(root, text="Open File 3", command=file3)
# openFile3.pack()

compare = tk.Button(root, text="Extract", command=extract)
compare.pack()

root.mainloop()
