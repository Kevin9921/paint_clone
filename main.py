from tkinter import *
import ttkbootstrap as ttk
from PIL import Image, ImageDraw
import PIL

WIDTH, HEIGHT = 500, 500
CENTER = WIDTH // 2
WHITE = (255,255,255)

class PaintGUI:
    def __init__(self):
        self.window = ttk.Window(themename = 'journal')
        self.window.title('Better Paint')

        self.brush_width = 15
        self.current_color = '#000000'

        self.cnv = Canvas(self.window, width=WIDTH-10, height = HEIGHT-10, bg ='white')
        self.cnv.pack()
        self.cnv.bind("B1-Motion", self.paint)

        self.image = PIL.Image.new("RGB", (WIDTH, HEIGHT), WHITE)
        self.draw = ImageDraw.Draw(self.image)

        self.btn_frame = Frame(self.window)
        self.btn_frame.pack(fill=X)

        self.btn_frame.columnconfigure(0, weight=1)
        self.btn_frame.columnconfigure(1, weight=1)
        self.btn_frame.columnconfigure(2, weight=1)

        self.clear_btn = Button(self.btn_frame, text="Clear", command = self.clear)
        self.clear_btn.grid(row=0, column=0, sticky=W+E)

        self.save_btn = Button(self.btn_frame, text="Save", command=self.save)
        self.save_btn.grid(row=0, column=1, sticky= W+E)

        self.bplus_btn = Button(self.btn_frame, text="B+", command=self.brush_plus)
        self.bplus_btn.grid(row=0, column=2, sticky=W+E)

        self.window.protocol('WM_DELETE_WINDOW', self.on_closing)

    def paint(self):
        pass

    def clear(self):
        pass

    def save(self):
        pass

    def brush_plus(self):
        pass

    def on_closing(self):
        pass

if __name__ == "__main__":
    app = PaintGUI()
    app.window.mainloop()

