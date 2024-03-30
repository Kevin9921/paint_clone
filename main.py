from tkinter import *
from PIL import Image, ImageDraw
import PIL

WIDTH, HEIGHT = 500, 500
CENTER = WIDTH // 2
WHITE = (255,255,255)

class PaintGUI:
    def __init__(self):
        self.root = Tk()
        self.root.title('Better Paint')

        self.brush_width = 15
        self.current_color = '#000000'

        self.cnv = Canvas(self.root, width=WIDTH-10, height = HEIGHT-10, bg ='white')
        self.cnv.pack()
        self.cnv.bind("B1-Motion", self.paint)


if __name__ == "__main__":
    app = PaintGUI()
    app.root.mainloop()

