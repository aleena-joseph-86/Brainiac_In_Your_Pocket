import time
import tkinter.messagebox
from tkinter import Tk, Frame, Menu, Text, Scrollbar, Button, Entry, Label, PhotoImage
from chatbot import chat
import tensorflow as tf
import numpy as np

DIMS = "500x500"

class ChatInterface(Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.tl_bg = "#EEEEEE"
        self.tl_bg2 = "#EEEEEE"
        self.tl_fg = "#000000"
        self.font = "Verdana 10"
        
        menu = Menu(self.master)
        self.master.config(menu=menu, bd=5)
        
        file = Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file)
        file.add_command(label="Clear Chat", command=self.clear_chat)
        file.add_command(label="Exit", command=self.chatexit)

        options = Menu(menu, tearoff=0)
        menu.add_cascade(label="Preferences", menu=options)
        font = Menu(options, tearoff=0)
        options.add_cascade(label="Font", menu=font)
        font.add_command(label="Default", command=self.font_change_default)
        font.add_command(label="System", command=self.font_change_system)

        color_theme = Menu(options, tearoff=0)
        options.add_cascade(label="Theme", menu=color_theme)
        color_theme.add_command(label="Default", command=self.color_theme_default)
        color_theme.add_command(label="Blue", command=self.color_theme_dark_blue) 
        color_theme.add_command(label="Hacker", command=self.color_theme_hacker)
        
        help_option = Menu(menu, tearoff=0)
        menu.add_cascade(label="About", menu=help_option)
        help_option.add_command(label="About Chatbot", command=self.msg)
        
        self.text_frame = Frame(self.master, bd=6)
        self.text_frame.pack(expand=True, fill="both")
        
        self.text_box_scrollbar = Scrollbar(self.text_frame, bd=0)
        self.text_box_scrollbar.pack(fill="y", side="right")
        
        self.text_box = Text(self.text_frame, yscrollcommand=self.text_box_scrollbar.set, state="disabled",
            bd=1, padx=6, pady=6, spacing3=8, wrap="word", bg=None, font="Verdana 10", relief="groove",
            width=10, height=1)
        self.text_box.pack(expand=True, fill="both")
        self.text_box_scrollbar.config(command=self.text_box.yview)
        
        self.entry_frame = Frame(self.master, bd=1)
        self.entry_frame.pack(side="left", fill="both", expand=True)
        
        self.entry_field = Entry(self.entry_frame, bd=1, justify="left")
        self.entry_field.pack(fill="x", padx=6, pady=6, ipady=3)
        
        self.send_button_frame = Frame(self.master, bd=0)
        self.send_button_frame.pack(fill="both")
        
        self.send_button = Button(self.send_button_frame, text="Send", width=5, relief="groove", bg='white',
            bd=1, command=lambda: self.send_message_insert(None), activebackground="#FFFFFF",
            activeforeground="#000000")
        self.send_button.pack(side="left", ipady=8)
        self.master.bind("<Return>", self.send_message_insert)
        
        self.last_sent_label(date="No messages sent.")

    def last_sent_label(self, date):
        try:
            self.sent_label.destroy()
        except AttributeError:
            pass
        self.sent_label = Label(self.entry_frame, font="Verdana 7", text=date, bg=self.tl_bg2, fg=self.tl_fg)
        self.sent_label.pack(side="left", fill="x", padx=3)

    def clear_chat(self):
        self.text_box.config(state="normal")
        self.last_sent_label(date="No messages sent.")
        self.text_box.delete(1.0, "end")
        self.text_box.delete(1.0, "end")
        self.text_box.config(state="disabled")

    def chatexit(self):
        exit()

    def msg(self):
        tkinter.messagebox.showinfo("NLP - Neural Network based chatbot")

    def send_message_insert(self, message):
        user_input = self.entry_field.get()
        pr1 = "You : " + user_input + "\n"

        self.text_box.configure(state="normal")
        self.text_box.insert("end", pr1)
        self.text_box.configure(state="disabled")
        self.text_box.see("end")
        
        response = chat(user_input)
        pr = "Bot : " + response + "\n"
        
        self.text_box.configure(state="normal")
        self.text_box.insert("end", pr)
        self.text_box.configure(state="disabled")
        self.text_box.see("end")
        self.last_sent_label(str(time.strftime("Last message sent: %B %d, %Y at %I:%M %p")))
        self.entry_field.delete(0, "end")

    def font_change_default(self):
        self.text_box.config(font="Verdana 10")
        self.entry_field.config(font="Verdana 10")
        self.font = "Verdana 10"

    def font_change_system(self):
        self.text_box.config(font="System")
        self.entry_field.config(font="System")
        self.font = "System"

    def color_theme_default(self):
        self.master.config(bg="#EEEEEE")
        self.text_frame.config(bg="#EEEEEE")
        self.entry_frame.config(bg="#EEEEEE")
        self.text_box.config(bg="#FFFFFF", fg="#000000")
        self.entry_field.config(bg="#FFFFFF", fg="#000000", insertbackground="#000000")
        self.send_button_frame.config(bg="#EEEEEE")
        self.send_button.config(bg="#FFFFFF", fg="#000000", activebackground="#FFFFFF", activeforeground="#000000")
        self.sent_label.config(bg="#EEEEEE", fg="#000000")

        self.tl_bg = "#FFFFFF"
        self.tl_bg2 = "#EEEEEE"
        self.tl_fg = "#000000"

    def color_theme_dark_blue(self):
        self.master.config(bg="#263b54")
        self.text_frame.config(bg="#263b54")
        self.text_box.config(bg="#1c2e44", fg="#FFFFFF")
        self.entry_frame.config(bg="#263b54")
        self.entry_field.config(bg="#1c2e44", fg="#FFFFFF", insertbackground="#FFFFFF")
        self.send_button_frame.config(bg="#263b54")
        self.send_button.config(bg="#1c2e44", fg="#FFFFFF", activebackground="#1c2e44", activeforeground="#FFFFFF")
        self.sent_label.config(bg="#263b54", fg="#FFFFFF")

        self.tl_bg = "#1c2e44"
        self.tl_bg2 = "#263b54"
        self.tl_fg = "#FFFFFF"

    def color_theme_hacker(self):
        self.master.config(bg="#0F0F0F")
        self.text_frame.config(bg="#0F0F0F")
        self.entry_frame.config(bg="#0F0F0F")
        self.text_box.config(bg="#0F0F0F", fg="#33FF33")
        self.entry_field.config(bg="#0F0F0F", fg="#33FF33", insertbackground="#33FF33")
        self.send_button_frame.config(bg="#0F0F0F")
        self.send_button.config(bg="#0F0F0F", fg="#FFFFFF", activebackground="#0F0F0F", activeforeground="#FFFFFF")
        self.sent_label.config(bg="#0F0F0F", fg="#33FF33")

        self.tl_bg = "#0F0F0F"
        self.tl_bg2 = "#0F0F0F"
        self.tl_fg = "#33FF33"

root = Tk()
ob = ChatInterface(root)
root.geometry(DIMS)
root.title("Chatbot-NLP")

img = PhotoImage(file='img/bot.png') 
root.iconphoto(False, img)

root.mainloop()
