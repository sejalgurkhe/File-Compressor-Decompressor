import tkinter as tk
from tkinter import *

from app.demo_gui import FileCase

# Run the application.
root = Tk()
root.title("Huffman-Compressor and Decompressor")
app = FileCase(root)
root.geometry("1100x500")

while True:
	try:
		root.mainloop()
		break
	except UnicodeDecodeError: # Added to avoid the program crashing when scrolling.
		pass