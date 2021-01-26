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
                        # if parsedFile[m] != b'\x54':
                        #     if parsedFile[m + 1] != b'\x50':
                        #         if parsedFile[m + 2] != b'\x45':
                        #             if parsedFile[m + 3] != b'\x31':
                        songTitleArray.append(parsedFile[m].decode(encoding="UTF-8"))

            break

    print("Title parsing complete, displaying song title...")
    if (songTitleArray):
        songName = songTitleName.join(songTitleArray)
        print("Song Title:" + songName)
        if metadata_text_title != 0:
            metadata_text_title.delete(1.0, tk.END)
        metadata_text_title.insert(tk.END, "Song Title: " + songName + "\n")
    else:
        print("Format not recognized or cannot find Song Title tag information")


def getartist(parsedFile):
    global artistName
    global ArtistInfo
    global artistArray
    global artistStartingIndex
    artistArray = []
    for s in range(len(parsedFile)):
        if parsedFile[s] == b'T':
            if parsedFile[s + 1] == b'P':
                if parsedFile[s + 2] == b'E':
                    if parsedFile[s + 3] == b'1':
                        artistArray = []
                        artistName = ""
                        ArtistFrameTag = s + 4
                        for i in range(ArtistFrameTag, len(parsedFile)):
                            if str(parsedFile[i].hex()) == "ff":
                                if str(parsedFile[i + 1].hex()) == "fe":
                                    artistStartingIndex = i + 2
                                    for n in range(artistStartingIndex, len(parsedFile)):
                                        if parsedFile[n] != b'\x00':
                                            if parsedFile[n] == b'\x54':
                                                if parsedFile[n + 1] == b'\x50':
                                                    if parsedFile[n + 2] == b'\x45':
                                                        if parsedFile[n + 3] == b'\x32':
                                                            break

                                            # if parsedFile[n] != b'\x54':
                                            #     if parsedFile[n + 1] != b'\x50':
                                            #         if parsedFile[n + 2] != b'\x45':
                                            #             if parsedFile[n + 3] != b'\x32':
                                            artistArray.append(parsedFile[n].decode(encoding="UTF-8"))
                                break
    print("Artist parsing complete, displaying artist information...")
    if (artistArray):
        artistsName = artistName.join(artistArray)
        print("Artist Name:" + artistsName)
        if metadata_text_artist != 0:
            metadata_text_artist.delete(1.0, tk.END)
        metadata_text_artist.insert(tk.END, "Artist Name: " + artistsName + "\n")
    else:
        print("Format not recognized or cannot find Artist tag information")


def getAlbum():
    for s in range(len(parsedFile)):
        if parsedFile[s] == b'T':
            if parsedFile[s + 1] == b'A':
                if parsedFile[s + 2] == b'L':
                    if parsedFile[s + 3] == b'B':
                        global Album
                        Album = s
                        print("Album Tag at index: " + str(Album))
                        #metadata_text.insert(tk.END, "Album Index in file: " + str(Album) + "\n")


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

        gettitle(parsedFile=parsedFile)
        getartist(parsedFile=parsedFile)

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

metadata_text_title = tk.Text(root, height=1, width=64)
metadata_text_title.pack()

metadata_text_artist = tk.Text(root, height=1, width=64)
metadata_text_artist.pack()

openFile1 = tk.Button(root, text="Open MP3 File...", command=file1)
openFile1.pack()

compare = tk.Button(root, text="Extract", command=extract)
compare.pack()

root.mainloop()
