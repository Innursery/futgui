import tkinter as tk
from PIL import ImageTk, Image
from frames.loading import Loading
from frames.playersearch import PlayerSearch
from frames.login import Login
from frames.bid import Bid
from frames.watch import Watch

class Application(tk.Frame):
    def __init__(self, master):
        self.api = None
        self.status = master.status
        tk.Frame.__init__(self, master, bg='#1d93ab')

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self, bg='#1d93ab')
        container.pack(side="top", fill="both", expand=True, padx=15, pady=15)
        container.grid_rowconfigure(0, weight=0)
        container.grid_rowconfigure(1, weight=1)
        container.grid_columnconfigure(0, weight=1)

        fifaImg = ImageTk.PhotoImage(Image.open('images/logo_icon.jpg'))
        fifaLabel = tk.Label(container, bg='#1d93ab', image=fifaImg)
        fifaLabel.grid(column=0, row=0, sticky='w')
        fifaLabel.image = fifaImg

        self.frames = {}
        for F in (Loading, Login, PlayerSearch, Bid, Watch):
            frame = F(container, self)
            self.frames[F] = frame
            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(column=0, row=1, sticky='news')

        self.show_frame(Login)

    def show_frame(self, c, **kwargs):
        '''Show a frame for the given class'''
        frame = self.frames[c]
        frame.set_args(kwargs)
        frame.tkraise()
        frame.active()

    def get_frame(self, c):
        return self.frames[c]
