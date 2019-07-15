# An lossless Image Compression tool
# Author: Onyenanu Princewill
# Copyright: (c) 2019

#Import necessary libraries
import time
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import os
import notify2
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext as st
from PIL import Image
from tkinter.ttk import Progressbar
root = Tk()
root.title("PyCompress 1.0") #  Window Title
#root.geometry("300x50")
#root.resizable(0, 0) # if you want it resizeable, just remove this whole line

# set up variables to store necessary compression data
desiredQuality = ""
quality_sv = tk.IntVar()
allowedExtensions = ['.png', '.jpg', '.jpeg']

# Text for the about about window
aboutTxt = "PyCompress is an Image Compression tool that enables users to reduce sizes of bulky images without significant quality loss. \nThis can be ideal when preparing images for usage on the web.\nPyCompress supports image compression on a file and folder level. \nThus, you can choose to compress a single image file or compress all image files in a selected folder. \nPyCompress is developed by Nigerian Software Developer, Onyenanu Princewill." 

# Text for the How-to-use window
howTxt = "PyCompress supports image compression on a file and folder level. Thus, you can choose to compress a single image file or compress all image files in a selected folder (This could come in handy when trying to compress a bulk of images for use on the web).\nTo Compress a single image fie:\n1. Open PyCompress app and click “Compress File”, a prompt would open for you to browse through your machine and select the image file, once you locate your desired file, click on it to ensure it’s highlighted then click “open”.\n2. A prompt would appear asking if you’d like to keep the original image after compression. Select either “Yes” or “No”. After this another dialog box pops up and requires you to choose a desired compression quality – the default is 10. select your desired quality and click “OK” after that, relax and compression runs in the background .\n3. If successful, you’d get an indication prompt same for failed compressions too. \n\nTo Compress all image files in a folder:\n1. Open PyCompress app and click “Compress Folder”, a prompt would open for you to browse through your machine and select the directory, once you locate your desired directory, click on it to ensure it’s highlighted then click “open”.\n2. A prompt would appear asking if you’d like to keep the original image after compression. Select either “Yes” or “No”. After this another dialog box pops up and requires you to choose a desired compression quality – the default is 10. select your desired quality and click “OK” after that, relax and compression runs in the background .\nNote: Compressing multiple images would usually take a longer time than compressing single images. So, do not freak out if it takes a little time before you get a success prompt. \nIf successful, you’d get an indication prompt same for failed compressions too. "

# Create a Tk menu
def createMenu(*event): # App Menu 
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    settingsMenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=settingsMenu)
    settingsMenu.add_command(label="About", command=about)
    settingsMenu.add_separator()
    settingsMenu.add_command(label="Exit", command=exitWindow)

    helpMenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Help", menu=helpMenu)
    helpMenu.add_command(label="Tutorial", command=helpTutorial)

# Function to ask ser for compression qualtiy
def askQuality(*event):

    rootQuality = tk.Tk()
    rootQuality.title("")
    #rootQuality.geometry("150x0")
    rootQuality.resizable(0, 0)

    def closeQuality():
        setQuality = int(qualityChosen.get())
        print(setQuality)
        global desiredQuality
        desiredQuality = setQuality
        rootQuality.quit()

    tk.Label(rootQuality, text="Set Compression quality:").grid(column=0, row=0)                  
    qualityChosen = ttk.Combobox(rootQuality, width=10, textvariable=quality_sv) 
    qualityChosen['values'] = (10, 20, 30, 40, 50, 60, 70, 80) 
    qualityChosen.current(0)
    qualityChosen.grid(column=0, row=1, padx=10)
    okButton = ttk.Button(rootQuality, text="OK", width=10, command=closeQuality).grid(row=2, column=0, padx=10, pady=10, sticky="")
    rootQuality.mainloop()
    
# Function to perform compression on a single file
def compressFile(path):
    deleteOld = mb.askyesno("Enquiry", "Would you like too keep original Image after compression?")
    askQuality()
    print(desiredQuality)
    try:
        image = Image.open(path)
        fname, fext = os.path.splitext(path) #extract filename
        compressedVersion = image.save(fname+"_compressed_"+str(desiredQuality)+fext, optimize=True, quality=desiredQuality)
        if deleteOld == 0:
            os.remove(path, dir_fd=None)
        return mb.showinfo("Success", "Image Succesfully Compressed And Saved")
    except Exception as e:
        return mb.showerror("Error", e)

# Function to perform compression on a folder 
def compressFolderFile(path, keepFiles):
    try:
        image = Image.open(path)
        fname, fext = os.path.splitext(path) #extract filename
        compressedVersion = image.save(fname+"_compressed_"+str(desiredQuality)+fext, optimize=True, quality=desiredQuality)
        if keepFiles == 0:
            os.remove(path, dir_fd=None)
    except Exception as e:
        return mb.showerror("Error", e)

# Function to browse files
def browseFiles(*event): #Load PDF is now browseFiles
    path = fd.askopenfilename()
    if path == "":
        return
    fname, fext = os.path.splitext(path)
    if fext not in allowedExtensions:
        mb.showerror("Invalid File Type!", "This file extension is not allowed!\nJust *.png, jpg, jpeg are allowed!")
    else:
        compressFile(path)
                   
# Function to browse folders
def browseFolders(*event):
    fileCount = 0
    path = fd.askdirectory()
    if path == "":
        return
    try:
        deleteOld = mb.askyesno("Enquiry", "Would you like to keep original images after compression?")
        askQuality()
        for filename in os.listdir(path):
            if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"):
                newfile = os.path.join(path, filename)
                compressFolderFile(newfile, deleteOld)
                fileCount += 1
            else:
                continue
        if fileCount > 0:
            return mb.showinfo("Success", str(fileCount)+" Images Found, Succesfully Compressed And Saved")
        else:
            return mb.showinfo("Error", "Unable to compress, No image(s) found in specified directory") 
    except Exception as e:
        mb.showerror("Error", e)

# Function to destroy window    
def exitWindow(*event):
    root.destroy()

# Function to render the tutorial screen
def helpTutorial(*event):
    rootHelp = tk.Tk()
    rootHelp.title("How To Use")
    rootHelp.geometry("528x297")
    rootHelp.resizable(0, 0)
    helpText = howTxt
    paper = st.ScrolledText(rootHelp, wrap="word", width=400, height=200, font=("Consolas", 8))
    paper.insert("1.0", helpText)
    paper.configure(state='disabled')
    paper.pack()

# Function to render the about screen
def about(*event):
    rootDocumentary = tk.Tk()
    rootDocumentary.title("About PyCompress")
    rootDocumentary.geometry("350x200")
    rootDocumentary.resizable(0, 0)

    documentaryText = aboutTxt

    paper = st.ScrolledText(rootDocumentary, wrap="word", width=400, height=200, font=("Consolas", 10))
    paper.insert("1.0", documentaryText)
    paper.configure(state='disabled')
    paper.pack()

    rootDocumentary.mainloop()

# Initialize buttons
chooseButton = tk.Button(root, text="Compress File", command=browseFiles).grid(row=0, column=0, padx=10, pady=10, sticky='w')
chooseFolderButton = tk.Button(root, text="Compress Folder", command=browseFolders).grid(row=0, column=1, padx=10, pady=0, sticky='w')


#Create menu and call the mainloop()
createMenu()        
root.mainloop()


