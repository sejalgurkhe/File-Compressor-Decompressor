import tkinter as tk
from tkinter import *
import tkinter.font as font
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter.messagebox import showerror
from tkinter.messagebox import showinfo

from app.huffman import HuffmanCoder
from app.utils import *

from docx import *

import os
import pickle

class FileCase:
    def __init__(self, master):
        self.filename = ""
        self.file_ext = ""
        self.filepath = ""
        self.destination_path = ""
        self.data_dir = ""
        self.master = master
        master.title("Huffman-Compressor and Decompressor")


        self.label = Label(master, text="HUFFMAN COMPRESSOR and DECOMPRESSOR",height="4",width="112",fg = "lightblue1",bg = "dodgerblue4", font = ("Helvetica", 16))
        self.label.pack()
        self.label1 = Label(master, text="", height="4", width="112", font=("Helvetica", 16))
        self.label1.pack()

        self.load_label = Label(master,text="Click Here to Load a File: ",height="4",font=("Helvetica", 18))
        self.load_label.place(x=150,y=130)
        self.load_button = Button(master, text="Load File", command = self.load_file,height="2",width="20",bg="lightblue1",fg="black",font=("Helvetica", 16),borderwidth=2, relief="solid")
        self.load_button.place(x=500,y=150)


        self.filenameLabel = Label(master, text="You have not selected a file yet.", font=("Helvetica", 18))
        self.filenameLabel.place(x=500,y=250)

        self.procedure_Label = Label(master, text="Select Your Choice: ", font=("Helvetica", 18))
        self.procedure_Label.place(x=150, y=350)

        self.compressButton = Button(master, text="Compress File", font=("Helvetica", 16),height="2",width="20",bg="lightblue1",fg="black",borderwidth=2, relief="solid", command=self.compress_file)
        self.compressButton.place(x=400,y=350)

        self.decompressButton = Button(master, text="Decompress File", font=("Helvetica", 16),height="2",width="20", bg="lightblue1",fg="black",borderwidth=2, relief="solid", command=self.decompress_file)
        self.decompressButton.place(x=700, y=350)

    def load_file(self):
        self.filepath = askopenfilename(title="Choose a file to compress.",
                                        filetypes=(
                                        ("bin files", "*.bin"), ("text files", "*.txt"), ("doc files", "*.docx")))

        if self.filepath == "" or None:
            showinfo("Error", "Please select a valid file.")
            self.filenameLabel['text'] = "You have not selected a file yet."
            return

        showinfo("",
                 "Please select a destination folder to save your compressed/decompressed file to.")
        self.destination_path = askdirectory()

        if self.destination_path == "" or None:
            showinfo("Error", "Please select a valid destination directory.")
            self.filepath == ""
            self.filenameLabel['text'] = "You have not selected a file yet."
            return

        self.filename = self.filepath.split("/")[-1]
        self.file_ext = os.path.splitext(self.filepath)[1]

        if self.file_ext == ".docx":
            showinfo("Warning",
                     "You have selected a Word document. Please make sure the file does not contain any images.")
            self.updateFilenameLabel()
            return

        self.updateFilenameLabel()
        return


    def updateFilenameLabel(self):
        self.filenameLabel['text'] = self.filename
        return

    """Create a new instance of HuffmanCoder and compress the file located at self.filepath to self.destination_path."""

    def compress_file(self):
        if self.file_ext == ".bin":
            showinfo("Error", "That file is already compressed. Cannot compress it any further.")
            return


        if containsDirectory(os.getcwd() + "/app/data", self.filename):
            self.data_dir = os.getcwd() + "/app/data/" + self.filename

        else:
            os.makedirs(os.getcwd() + "/app/data/" + self.filename)
            self.data_dir = os.getcwd() + "/app/data/" + self.filename

        if self.filepath == "" or None:
            showinfo("Compression Error", "Please load a file first.")
            return

        huffmanCoder = HuffmanCoder(self.filepath, self.destination_path)

        try:
            compressed_filepath = huffmanCoder.compress()
            showinfo("Success",
                     "Successfully compressed " + self.filename + " to " + compressed_filepath + ". Please do not change the compressed file name.")

            with open(self.data_dir + "/" + self.filename + "-coder.pickle", 'wb') as coder:
                pickle.dump(huffmanCoder, coder, protocol=pickle.HIGHEST_PROTOCOL)

        except:
            showinfo("Error", "Huffman Coding Error.")
            return

        return


    def decompress_file(self):
        # Check if the loaded file isn't a .bin file. If True, then it cannot be decompressed.
        if self.filepath == "":
            showinfo("Please select a file to decompress first.")
            return

        if self.file_ext != ".bin":
            showinfo("Error", "That file is not a .bin file. It cannot be decompressed.")
            return

        # File type to decompress to.
        filetype = self.filepath.split("-")[-1].split(".")[0]


        if filetype == "txt" :
            filename = self.filepath.split("/")[-1][0:-8]
            data_dir_name = filename + "." + filetype

            if not containsDirectory(os.getcwd() + "/app/data", data_dir_name):
                showinfo(
                    "Decompression Error: Cannot Find Appropriate Huffman Tree. If you changed the file name, please restore it to its original name.")
                return

            with open(os.getcwd() + "/app/data/" + data_dir_name + "/" + data_dir_name + "-coder.pickle",
                      'rb') as coder:
                huffmanCoder = pickle.load(coder)


        elif filetype == "docx":
            filename = self.filepath.split("/")[-1][0:-9]
            data_dir_name = filename + "." + filetype

            if not containsDirectory(os.getcwd() + "/app/data", data_dir_name):
                showinfo(
                    "Decompression Error: Cannot Find Appropriate Huffman Tree. If you changed the file name, please restore it to its original name.")
                return

            with open(os.getcwd() + "/app/data/" + data_dir_name + "/" + data_dir_name + "-coder.pickle",
                      'rb') as coder:
                huffmanCoder = pickle.load(coder)

        try:
            decompressed_file = huffmanCoder.decompress(compressed_filepath=self.filepath,
                                                        decompression_path=self.destination_path)
        except:
            showinfo("Error", "HuffmanCoder Decompression Error ")
            return

        showinfo("Success", "Successfully decompressed file to " + decompressed_file)
        return



