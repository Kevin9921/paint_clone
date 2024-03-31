from tkinter import *
import ttkbootstrap as ttk
#from tkinter import filedialog,
from PIL import Image, ImageDraw
import PIL
from time import time

WIDTH, HEIGHT = 500, 500
CENTER = WIDTH // 2
WHITE = (255,255,255)

class PaintGUI:
    def __init__(self):
        self.last_click_time = 0
        self.interpolation_threshold = 0.05
        self.interpolation_amount = 20

        self.window = ttk.Window(themename = 'journal')
        #self.window = Tk()
        self.window.title('Better Paint')
        self.window.configure(bg = 'grey')
        self. window.geometry("800x800")

        self.brush_width = 5
        self.current_color = '#000000'

        self.cnv = Canvas(self.window, width=WIDTH-10, height = HEIGHT-10, bg ='white')
        self.cnv.pack(pady = 50)
        #self.cnv.pack(fill=BOTH, expand=True)
        self.cnv.bind("<B1-Motion>", self.paint)

        self.image = PIL.Image.new("RGB", (WIDTH, HEIGHT), WHITE)
        self.draw = ImageDraw.Draw(self.image)

        self.btn_frame = Frame(self.window)
        self.btn_frame.pack(fill=X)

        self.btn_frame.columnconfigure(0, weight=1)
        self.btn_frame.columnconfigure(1, weight=1)
        self.btn_frame.columnconfigure(2, weight=1)
        self.btn_frame.columnconfigure(3, weight=1)

        self.clear_btn = Button(self.btn_frame, text="Clear", command = self.clear)
        self.clear_btn.grid(row=0, column=0, sticky=W+E)

        self.save_btn = Button(self.btn_frame, text="Save", command=self.save)
        self.save_btn.grid(row=0, column=1, sticky= W+E)

        self.bplus_btn = Button(self.btn_frame, text="B+", command=self.brush_plus)
        self.bplus_btn.grid(row=0, column=2, sticky=W+E)

        self.bminus_btn = Button(self.btn_frame, text="B-", command=self.brush_minus)
        self.bminus_btn.grid(row=0, column=3, sticky=W+E)

        self.window.protocol('WM_DELETE_WINDOW', self.on_closing)

    def paint(self, event):
        # Get the current time
        current_time = time()

        # Get the current mouse position
        x2, y2 = event.x, event.y

        # Initialize or update previous mouse position
        if not hasattr(self, 'prev_x') or not hasattr(self, 'prev_y'):
            self.prev_x, self.prev_y = x2, y2

        # If the time since the last click is too long, reset the previous mouse position
        if current_time - self.last_click_time > self.interpolation_threshold:
            self.prev_x, self.prev_y = x2, y2

        # Draw a line between the current and previous mouse positions
        self.cnv.create_line(self.prev_x, self.prev_y, x2, y2, fill=self.current_color, width=self.brush_width)
        self.draw.line([self.prev_x, self.prev_y, x2, y2], fill=self.current_color, width=self.brush_width)

        # Interpolate between consecutive mouse positions
        for i in range(1, self.interpolation_amount + 1):
            # Calculate intermediate point coordinates
            interp_x = self.prev_x + (x2 - self.prev_x) * i / (self.interpolation_amount + 1)
            interp_y = self.prev_y + (y2 - self.prev_y) * i / (self.interpolation_amount + 1)

            # Draw a line between the previous and intermediate points
            self.cnv.create_line(self.prev_x, self.prev_y, interp_x, interp_y, fill=self.current_color, width=self.brush_width)
            self.draw.line([self.prev_x, self.prev_y, interp_x, interp_y], fill=self.current_color, width=self.brush_width)

        # Update previous mouse position for next iteration
        self.prev_x, self.prev_y = x2, y2

        # Update last click time
        self.last_click_time = current_time

    def clear(self):
        self.cnv.delete("all")
        self.draw.rectangle([0,0,1000,1000], fill="white")

    def save(self):
        pass

    def brush_plus(self):
        self.brush_width += 1

    def brush_minus(self):
        self.brush_width -= 1

    def on_closing(self):
        pass

if __name__ == "__main__":
    app = PaintGUI()
    app.window.mainloop()

