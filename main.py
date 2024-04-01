from tkinter import *
import ttkbootstrap as ttk
from tkinter import filedialog, messagebox, colorchooser
from PIL import Image, ImageDraw
import PIL
from time import time
import os

WIDTH, HEIGHT = 500, 500
CENTER = WIDTH // 2
WHITE = (255,255,255)

class PaintGUI:
    def __init__(self):
        self.last_click_time = 0
        self.interpolation_threshold = 0.05
        self.interpolation_amount = 15
        self.fileName = ""
        self.fileExt = ""
        self.Canvas_line = []
        self.Pillow_line = []

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
        self.cnv.bind("<ButtonRelease-1>", self.paint_stop)

        self.image = PIL.Image.new("RGB", (WIDTH, HEIGHT), WHITE)
        self.draw = ImageDraw.Draw(self.image)

        self.output_string = ttk.StringVar()
        self.output_string.set(str(self.brush_width))
        self.output_label = ttk.Label(master = self.window, textvariable=self.output_string)
        self.output_label.pack()

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

        self.color_btn = Button(self.btn_frame, text="Colour", command=self.change_colour)
        self.color_btn.grid(row=1, column=1, sticky=W+E)

        self.undo_btn = Button(self.btn_frame, text="Undo", command=self.undo_btn)
        self.undo_btn.grid(row=1, column=0, sticky=W+E)

        self.window.protocol('WM_DELETE_WINDOW', self.on_closing)

    def undo_btn(self):
        line1 = self.Canvas_line.pop()
        line2 = self.Pillow_line.pop()

        print("this is line 1", line1)
        for i in line1:
            print(line1)
            self.cnv.delete(line1[0])
            self.cnv.delete(line1[1])
        #self.cnv.delete(line1[1])



    def update_brush_size(self):
        self.output_string.set(self.brush_width)

    def paint_stop(self, event):

    def paint(self, event):
        # Get the current time
        current_time = time()
        cnv_line = []
        pil_line = []
        cnv_int_line = []
        pil_int_line = []

        # Get the current mouse position
        x2, y2 = event.x, event.y

        # Initialize or update previous mouse position
        if not hasattr(self, 'prev_x') or not hasattr(self, 'prev_y'):
            self.prev_x, self.prev_y = x2, y2

        # If the time since the last click is too long, reset the previous mouse position
        if current_time - self.last_click_time > self.interpolation_threshold:
            self.prev_x, self.prev_y = x2, y2

        # Draw a line between the current and previous mouse positions
        cnv_line.append(self.cnv.create_line(self.prev_x, self.prev_y, x2, y2, fill=self.current_color, width=self.brush_width))
        pil_line.append(self.draw.line([self.prev_x, self.prev_y, x2, y2], fill=self.current_color, width=self.brush_width))

        # Interpolate between consecutive mouse positions
        for i in range(1, self.interpolation_amount + 1):
            # Calculate intermediate point coordinates
            interp_x = self.prev_x + (x2 - self.prev_x) * i / (self.interpolation_amount + 1)
            interp_y = self.prev_y + (y2 - self.prev_y) * i / (self.interpolation_amount + 1)

            # Draw a line between the previous and intermediate points
            cnv_int_line.append(self.cnv.create_line(self.prev_x, self.prev_y, interp_x, interp_y, fill=self.current_color, width=self.brush_width))
            pil_int_line.append(self.draw.line([self.prev_x, self.prev_y, interp_x, interp_y], fill=self.current_color, width=self.brush_width))


        self.Canvas_line.append((cnv_line,cnv_int_line))
        #print(cnv_line)
        print(self.Canvas_line)
        self.Pillow_line.append((pil_line,pil_int_line))

        # Update previous mouse position for next iteration
        self.prev_x, self.prev_y = x2, y2

        # Update last click time
        self.last_click_time = current_time

    def clear(self):
        self.cnv.delete("all")
        self.draw.rectangle([0,0,1000,1000], fill="white")

    def save(self):
        if self.fileName == "":
            filename = filedialog.asksaveasfilename(parent = self.window,
                                                    initialfile="untitled.png",
                                                    defaultextension = "png",
                                                    filetypes=[("PNG", ".png"), ("JPG", ".jpg")])
            self.fileExt = filename
            self.fileName = os.path.basename(filename)
        else:
            filename = filedialog.asksaveasfilename(parent=self.window,
                                                    initialfile=self.fileName,
                                                    defaultextension="png",
                                                    filetypes=[("PNG", ".png"), ("JPG", ".jpg")])
        if filename != "":
            self.image.save(filename)

    def brush_plus(self):
        if self.brush_width < 10:
            self.brush_width += 1
            self.update_brush_size()


    def brush_minus(self):
        if self.brush_width > 1:
            self.brush_width -= 1
            self.update_brush_size()

    def change_colour(self):
        _, self.current_color = colorchooser.askcolor(title="Choose A color")

    def on_closing(self):
        answer = messagebox.askyesnocancel("Quit", "Do you want to save your work", parent=self.window)
        filename = None
        if answer is not None:
            if answer:
                if self.fileName != "":
                    try:
                        self.image.save(self.fileExt)
                        print("Image saved successfully to:", self.fileName)
                    except Exception as e:
                        print("Error saving image:", e)
                else:
                    filename = filedialog.asksaveasfilename(parent=self.window,
                                                            initialfile="untitled.png",
                                                            defaultextension="png",
                                                            filetypes=[("PNG", ".png"), ("JPG", ".jpg")])
                    if filename:
                        self.image.save(filename)
                if filename or self.fileName:
                    self.window.destroy()
                    exit(0)
            else:
                self.window.destroy()
                exit(0)




if __name__ == "__main__":
    app = PaintGUI()
    app.window.mainloop()

