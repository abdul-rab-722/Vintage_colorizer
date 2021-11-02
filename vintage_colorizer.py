import tkinter as tk
from tkinter import filedialog
from tkinter import *
from colorizer import add_color
from PIL import ImageTk, Image
import cv2
import os

top=tk.Tk()
top.geometry('1000x600')
top.title('Vintage Colorizer')
top.iconbitmap('.\\images\\icons\\vc_icon.ico')
top.configure(background='white')

def save_colorized(file_path,colorized_img):
    try:
        where=filedialog.asksaveasfilename(filetypes=(('JPEG Files','*.jpg'),('PNG Files','*.png'),('All Files','*.*')),defaultextension=file_path[-4:])
        colorized_img.save(where)
    except:
        pass

def show_save_button(file_path,colorized_img, new):
    save_b=Button(new,text='Save to computer', command=lambda: save_colorized(file_path,colorized_img),padx=10,pady=5)
    save_b.place(relx=0.69,rely=0.86)
    
def convert(file_path, new):
    colorized_img=add_color(file_path)
    colorized_img=cv2.cvtColor(colorized_img,cv2.COLOR_BGR2RGB)
    colorized_img=Image.fromarray(colorized_img)
    colorized_img.thumbnail(((new.winfo_width()/1.8),(new.winfo_height()/1.8)))
    im=ImageTk.PhotoImage(colorized_img)
    label=Label(new,image=im)
    label.image=im
    label.pack(side="right",expand='yes')
    show_save_button(file_path, colorized_img, new)

def show_convert_button(file_path, new):
    convert_b=Button(new,text="Colorize me",command=lambda: convert(file_path, new),padx=10,pady=5)
    convert_b.place(relx=0.79,rely=0.46)

def new_image(im,file_path):
    new=Toplevel()
    new.geometry('1000x600')
    new.title('New Project')
    new.iconbitmap('.\\images\\icons\\vc_icon.ico')
    new.configure(background='white')
    label=Label(new,image=im)
    label.image=im
    label.pack(side="left", expand='yes')
    show_convert_button(file_path, new)

def upload_image(file_path=None,sample_gallery=None):
    if file_path==None: file_path=filedialog.askopenfilename()
    if sample_gallery!=None: sample_gallery.destroy()
    try:
        uploaded=Image.open(file_path)
        uploaded.thumbnail(((top.winfo_width()/2.25),(top.winfo_height()/2.25)))
        im=ImageTk.PhotoImage(uploaded)
        new_image(im,file_path)
    except:
        pass

def upload_sample():
    sample_gallery=Toplevel()
    sample_gallery.geometry('900x470')
    sample_gallery.title('Sample Images')
    sample_gallery.iconbitmap('.\\images\\icons\\vc_icon.ico')
    sample_gallery.configure(background='#05232c')
    sample_text=Label(sample_gallery,text='Pick a sample to colorize')
    sample_text.configure(background='#05232c', foreground='white', font='arial 14 bold underline')
    sample_text.pack(side='top',pady=85)
    samples=os.listdir('.\\images\\samples')
    for sample in range(len(samples)):
        im=Image.open(f'.\\images\\samples\\{samples[sample]}')
        im.thumbnail(((sample_gallery.winfo_width()/6),(sample_gallery.winfo_height()/6)))
        im=ImageTk.PhotoImage(im)
        label=Label(sample_gallery,image=im,cursor="hand2")
        label.image=im
        label.pack(side='left', expand='yes')
        label.bind("<1>",lambda e,s=sample:upload_image(f'.\\images\\samples\\{samples[s]}',sample_gallery))

vc_img=Image.open('.\\images\\others\\Vintage Colorizer.png')
vc_img.thumbnail((top.winfo_width(),top.winfo_height()))
vc_img=ImageTk.PhotoImage(vc_img)
vc_label=Label(top,image=vc_img)
vc_label.image=vc_img
vc_label.pack(side='top',expand='yes')

upload=Button(top,text="Upload an image",command=upload_image,padx=10,pady=5)
upload.configure(background='#05232c',foreground='white',font=('arial',10,'bold'))
upload.place(relx=0.44,rely=0.89)
sample=Button(top,text="Try on a sample image",command=upload_sample,padx=10,pady=5)
sample.configure(background='#107896',foreground='white',font=('arial',10,'bold'))
sample.place(relx=0.68,rely=0.89)

top.mainloop()
