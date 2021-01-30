import os
import platform
from tkinter import filedialog
import tkinter as tk

root = tk.Tk()
root.attributes('-topmost', 1)
root.geometry("500x500")
root.withdraw()

system = platform.system()

id3Tags = ['APIC',
           'APIC-1',
           'APIC-2',
           'APIC-3',
           'COMM',
           'GRP1',
           'IPLS',
           'ITNU',
           'MCDI',
           'MVIN',
           'MVNM',
           'OWNE',
           'PCNT',
           'PCST',
           'POPM',
           'PRIV',
           'SYLT',
           'TALB',
           'TBPM',
           'TCAT',
           'TCMP',
           'TCOM',
           'TCON',
           'TCOP',
           'TDAT',
           'TDES',
           'TDLY',
           'TENC',
           'TEXT',
           'TFLT',
           'TGID',
           'TIME',
           'TIT1',
           'TIT2',
           'TIT3',
           'TKEY',
           'TKWD',
           'TLAN',
           'TLEN',
           'TMED',
           'TOAL',
           'TOFN',
           'TOLY',
           'TOPE',
           'TORY',
           'TOWN',
           'TPE1',
           'TPE2',
           'TPE3',
           'TPE4',
           'TPOS',
           'TPUB',
           'TRCK',
           'TRDA',
           'TRSN',
           'TRSO',
           'TSIZ',
           'TSO2',
           'TSOC',
           'TSRC',
           'TSSE',
           'TXXX',
           'TYER',
           'USER',
           'USLT',
           'WCOM',
           'WCOP',
           'WFED',
           'WOAF',
           'WOAR',
           'WOAS',
           'WORS',
           'WPAY',
           'WPUB',
           'WXXX',
           'XDOR',
           'XOLY',
           'XSOA',
           'XSOP',
           'XSOT']


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
    global titleStart
    global nextFrameTag
    global nextTag
    global nextTagText
    nextTag = ""
    songTitleArray = []
    songTitleName = ""
    nextTagText = ""
    titleStart = 0
    nextFrameTag = []

    for s in range(len(parsedFile)):
        if parsedFile[s] == b'\x54':
            if parsedFile[s + 1] == b'\x49':
                if parsedFile[s + 2] == b'\x54':
                    if parsedFile[s + 3] == b'\x32':
                        titleStart = s + 4
                        for i in range(titleStart, len(parsedFile)):
                            if str(parsedFile[i + 1].hex()) == "ff":
                                if str(parsedFile[i + 2].hex()) == "fe":
                                    songTitleIndex = i + 3
                                    for m in range(songTitleIndex, len(parsedFile)):
                                        if parsedFile[m] != b'\x00':
                                            nextFrameTag.append(parsedFile[m].decode(encoding="UTF-8"))
                                            nextFrameTag.append(parsedFile[m + 1].decode(encoding="UTF-8"))
                                            nextFrameTag.append(parsedFile[m + 2].decode(encoding="UTF-8"))
                                            nextFrameTag.append(parsedFile[m + 3].decode(encoding="UTF-8"))
                                            nextTag = nextTagText.join(nextFrameTag)
                                            if nextTag in id3Tags:
                                                break

                                            nextFrameTag.clear()

                                            songTitleArray.append(parsedFile[m].decode(encoding="UTF-8"))
                                break

    print("Title parsing complete, displaying song title...")
    if (songTitleArray):
        songName = songTitleName.join(songTitleArray)
        print("Song Title: " + songName)
        if metadata_text_title != 0:
            metadata_text_title.delete(1.0, tk.END)
        metadata_text_title.insert(tk.END, "Song Title: " + songName)
    else:
        print("Format not recognized or cannot find Song Title tag information")


def getartist(parsedFile):
    global artistName
    global artistsName
    global artistArray
    global artistStartingIndex
    global nextTagCheck
    global nextTagText

    artistArray = []
    for s in range(len(parsedFile)):
        if parsedFile[s] == b'T':
            if parsedFile[s + 1] == b'P':
                if parsedFile[s + 2] == b'E':
                    if parsedFile[s + 3] == b'1':
                        artistArray = []
                        artistName = ""
                        artistsName = ""
                        nextTagCheck = []
                        nextTagText = ""
                        ArtistFrameTag = s + 4
                        for i in range(ArtistFrameTag, len(parsedFile)):
                            if str(parsedFile[i].hex()) == "ff":
                                if str(parsedFile[i + 1].hex()) == "fe":
                                    artistStartingIndex = i + 2
                                    for n in range(artistStartingIndex, len(parsedFile)):
                                        if parsedFile[n] != b'\x00':
                                            nextTagCheck.append(parsedFile[n].decode(encoding="UTF-8"))
                                            nextTagCheck.append(parsedFile[n + 1].decode(encoding="UTF-8"))
                                            nextTagCheck.append(parsedFile[n + 2].decode(encoding="UTF-8"))
                                            nextTagCheck.append(parsedFile[n + 3].decode(encoding="UTF-8"))
                                            nextArtistTag = nextTagText.join(nextTagCheck)

                                            if nextArtistTag in id3Tags:
                                                break
                                            nextTagCheck.clear()

                                            artistArray.append(parsedFile[n].decode(encoding="UTF-8"))

                                break
    print("Artist parsing complete, displaying artist information...")
    if artistArray:
        artistsName = artistName.join(artistArray)
        print("Artist Name: " + artistsName)
        if metadata_text_artist != 0:
            metadata_text_artist.delete(1.0, tk.END)
        metadata_text_artist.insert(tk.END, "Artist Name: " + artistsName)
    else:
        print("Format not recognized or cannot find Artist tag information")


def getAlbum(parsedFile):
    global AlbumArrayCombined
    AlbumArrayCombined = ""
    global AlbumNameArray
    for s in range(len(parsedFile)):
        if parsedFile[s] == b'T':
            if parsedFile[s + 1] == b'A':
                if parsedFile[s + 2] == b'L':
                    if parsedFile[s + 3] == b'B':
                        global AlbumFrameTagIndex
                        AlbumFrameTagIndex = s + 4
                        AlbumNextTagCheck = []
                        AlbumNameArray = []
                        AlbumName = ""
                        for i in range(AlbumFrameTagIndex, len(parsedFile)):
                            if str(parsedFile[i].hex()) == "ff":
                                if str(parsedFile[i+1].hex()) == "fe":
                                    AlbumNameStart = i + 2
                                    for k in range(AlbumNameStart, len(parsedFile)):
                                        if parsedFile[k] != b'\x00':
                                            AlbumNextTagCheck.append(parsedFile[k].decode("UTF-8"))
                                            AlbumNextTagCheck.append(parsedFile[k + 1].decode("UTF-8"))
                                            AlbumNextTagCheck.append(parsedFile[k + 2].decode("UTF-8"))
                                            AlbumNextTagCheck.append(parsedFile[k + 3].decode("UTF-8"))
                                            nextAlbumTag = nextTagText.join(AlbumNextTagCheck)

                                            if nextAlbumTag in id3Tags:
                                                break
                                            AlbumNextTagCheck.clear()

                                            AlbumNameArray.append(parsedFile[k].decode("UTF-8"))
                                break
    if AlbumNameArray:
        AlbumName = AlbumArrayCombined.join(AlbumNameArray)
        print("Album parsing complete, displaying ablum information...")
        print("Album Name: " + AlbumName)
        if metadata_text_album != 0:
            metadata_text_album.delete(1.0, tk.END)
        metadata_text_album.insert(tk.END, "Album: " + AlbumName)


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
        getAlbum(parsedFile=parsedFile)

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

metadata_text_album = tk.Text(root, height=1, width=64)
metadata_text_album.pack()

openFile1 = tk.Button(root, text="Open MP3 File...", command=file1)
openFile1.pack()

compare = tk.Button(root, text="Extract", command=extract)
compare.pack()

root.mainloop()
