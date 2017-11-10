import cv2
import numpy as np
from Tkinter import *
from PIL import Image
from PIL import ImageTk
import tkFileDialog
import os
import subprocess
import redeye
import enhance

def select_image(func):
    # grab a reference to the image panels
    global panelA, panelB
    maxsize = (512, 512)
    # open a file chooser dialog and allow the user to select an input
    # image
    path = tkFileDialog.askopenfilename()

    # ensure a file path was selected
    if (len(path) > 0):
        # os.system("script2.py "+str(path))
        # subprocess.Popen("script2.py "+str(path), shell=True)
        if(func == "redeye"):
            input,output = redeye.redeye(path)
        if(func == "enhance"):
            input,output = enhance.enhance(path)

        # convert the images to PIL format...

        if(func == "redeye"):
            input_pil = Image.fromarray(cv2.cvtColor(input,cv2.COLOR_BGR2RGB))
            output_pil = Image.fromarray(cv2.cvtColor(output,cv2.COLOR_BGR2RGB))
        if(func == "enhance"):
            input_pil = Image.fromarray(input)
            output_pil = Image.fromarray(output)

        input_pil.thumbnail(maxsize, Image.ANTIALIAS)
        output_pil.thumbnail(maxsize, Image.ANTIALIAS)
        # ...and then to ImageTk format
        input_tk = ImageTk.PhotoImage(input_pil)
        output_tk = ImageTk.PhotoImage(output_pil)

        # if the panels are None, initialize them
        if panelA is None or panelB is None:
            # the first panel will store our original image
            panelA = Label(image=input_tk)
            panelA.image = input_tk
            panelA.pack(side="left", padx=10, pady=10)

            # while the second panel will store the edge map
            panelB = Label(image=output_tk)
            panelB.image = output_tk
            panelB.pack(side="right", padx=10, pady=10)

            # otherwise, update the image panels
        else:
            # update the pannels
            panelA.configure(image=input_tk)
            panelB.configure(image=output_tk)
            panelA.image = input_tk
            panelB.image = output_tk

def select_image_redeye():
    select_image("redeye")

def select_image_enhance():
    select_image("enhance")

# initialize the window toolkit along with the two image panels
root = Tk()
root.title("Assignment 2")
panelA = None
panelB = None

# create a button, then when pressed, will trigger a file chooser
# dialog and allow the user to select an input image; then add the
# button the GUI
btn1 = Button(root, text="Red Eye Correction", command=select_image_redeye)
btn1.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

btn2 = Button(root, text="Image Enhancement", command=select_image_enhance)
btn2.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

# kick off the GUI
root.mainloop()
