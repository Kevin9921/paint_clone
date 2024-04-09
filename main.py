from tkinter import *
import ttkbootstrap as ttk
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from PIL import Image, ImageDraw
import PIL
from time import time
import os
import tkinter.font as tkfont
import pyautogui

WIDTH, HEIGHT = 700, 500
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
        self.single_line = []

        self.window = ttk.Window()
        #self.window = Tk()
        self.window.title('Better Paint')

        self.window.geometry("800x800")

        self.menu = Menu(self.window)
        #self.window.config()

        self.window.configure(bg='grey',menu=self.menu)

        self.fileMenu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.fileMenu)

        self.editMenu = Menu(self.menu)
        self.menu.add_cascade(label="Edit", menu=self.editMenu)

        self.fileMenu.add_command(label="Save", command=self.save)
        self.fileMenu.add_command(label="Close", command=self.on_closing)



        self.editMenu.add_command(label="Undo", command=self.undo_btn)
        self.editMenu.add_command(label="Redo")

        s = ttk.Style()
        # Create style used by default for all Frames
        s.configure('TFrame', background='#282526')

        self.brush_width = 5

        self.current_color = '#000000'

        self.wrapper = ttk.Frame(self.window)
        self.wrapper.pack(fill="both", expand=True)
        # self.btn_test = Button(self.wrapper, text="test")
        # self.btn_test.place(x=30, y=100)

        # self.btn_frame = Frame(self.window, borderwidth=5, relief=tk.RAISED)
        # self.btn_frame.pack(fill=X)

        self.output_string = ttk.StringVar()
        self.output_string.set(str(self.brush_width))

        # self.output_label.grid(row=2, column=2, sticky=W+E)

        s.configure("Frame4.TFrame", background="light blue")

        self.btn_frame = ttk.Frame(self.wrapper, style="Frame4.TFrame")
        self.btn_frame.pack(fill='both')

        for col in range(9):
            self.btn_frame.columnconfigure(col, weight=1)
        self.btn_frame.rowconfigure(1, weight=1)

        # draw frame
        s.configure("Frame1.TFrame", background="blue")
        s.configure("Frame2.TFrame", background="red")
        s.configure("Frame3.TFrame", background="green")

        # self.draw_frame = ttk.Frame(self.btn_frame, style="Frame1.TFrame")
        # self.draw_frame.grid(row=0,column=0, sticky='ew')

        self.clear_btn = ttk.Button(self.btn_frame, text="Clear", command=self.clear)
        # self.clear_btn.pack(fill ='x', padx=5, pady=5, side=LEFT)
        self.clear_btn.grid(row=0, column=0, sticky='ew', padx=5, pady=5)

        self.undo_btn = ttk.Button(self.btn_frame, text="Undo", command=self.undo_btn)
        # self.undo_btn.pack(fill ='x', padx=5, pady=5)
        self.undo_btn.grid(row=0, column=1, sticky='ew',padx=5, pady=5)

        # Configure the style for the single frame

        # self.single_frame = ttk.Frame(self.btn_frame, style="Frame2.TFrame")
        # self.single_frame.grid(row=0,column=1)
        self.bplus_btn = ttk.Button(self.btn_frame, text="B+", command=self.brush_plus)
        self.bplus_btn.grid(row=0, column=2, sticky='ew', padx=5, pady=5)

        self.bminus_btn = ttk.Button(self.btn_frame, text="B-", command=self.brush_minus)
        self.bminus_btn.grid(row=1, column=2, sticky='ew', padx=5, pady=5)

        self.output_label = ttk.Label(master=self.btn_frame, textvariable=self.output_string, anchor='center', font=tkfont.Font(size=14))
        self.output_label.grid(row=0, column=3, sticky='nsew', rowspan=2, padx=8, pady=8)

        # self.colorshow_btn = ttk.Button(self.btn_frame, text="colorshow_btn", command=self.change_colour)
        # self.colorshow_btn.grid(row=0, column=4, padx=10)


        #self.output_colour.set(str())

        self.label_colour = ttk.Label(self.btn_frame, background=self.current_color)
        self.label_colour.grid(row=0, column=4, sticky="ew",padx=5)



        # self.colour_frame = ttk.Frame(self.btn_frame, style="Frame3.TFrame")
        # self.colour_frame.grid(row=0, column=2, sticky=W + E)

        self.color_btn = ttk.Button(self.btn_frame, text="Choose Colour", command=self.change_colour)
        self.color_btn.grid(row=0, column=5,sticky="ew", padx=10)

        self.color_btn1 = ttk.Button(self.btn_frame, text="Red",
                                     command=lambda: self.change_static_colour("#FF0000"))
        self.color_btn1.grid(row=0, column=6,sticky="ew",padx=2)

        self.color_btn2 = ttk.Button(self.btn_frame, text="Yellow",
                                     command=lambda: self.change_static_colour("#FFFF00"))
        self.color_btn2.grid(row=0, column=7,sticky="ew",padx=2)

        self.color_btn3 = ttk.Button(self.btn_frame, text="Blue",
                                     command=lambda: self.change_static_colour("#006CFF"))
        self.color_btn3.grid(row=0, column=8,sticky="ew",padx=2)

        self.color_btn4 = ttk.Button(self.btn_frame, text="Green",
                                     command=lambda: self.change_static_colour("#2e9134"))
        self.color_btn4.grid(row=1, column=6, sticky="ew", padx=2)

        self.color_btn5 = ttk.Button(self.btn_frame, text="Black",
                                     command=lambda: self.change_static_colour("#000000"))
        self.color_btn5.grid(row=1, column=7, sticky="ew", padx=2)

        self.color_btn6 = ttk.Button(self.btn_frame, text="Purple",
                                     command=lambda: self.change_static_colour("#5300eb"))
        self.color_btn6.grid(row=1, column=8, sticky="ew", padx=2)



        #drawing canvas
        self.cnv = Canvas(self.wrapper, width=WIDTH-10, height=HEIGHT-10, bg='white')
        self.cnv.pack(pady = 50)
        #self.cnv.pack(fill=BOTH, expand=True)
        self.cnv.bind("<B1-Motion>", self.paint)
        self.cnv.bind("<ButtonRelease-1>", self.paint_stop)



        self.image = PIL.Image.new("RGB", (WIDTH, HEIGHT), WHITE)
        self.draw = ImageDraw.Draw(self.image)


        #
        # self.undo_btn = Button(self.btn_frame, text="Undo", command=self.undo_btn)
        # self.undo_btn.grid(row=2, column=0, sticky=W+E)

        self.window.protocol('WM_DELETE_WINDOW', self.on_closing)

    def make_draggable(self, widget):
        widget.bind("<Button-1>", self.on_drag_start)
        widget.bind("<B1-Motion>", self.on_drag_motion)

    def on_drag_start(self, event):
        widget = event.widget
        widget._drag_start_x = event.x
        widget._drag_start_y = event.y

    def on_drag_motion(self, event):
        widget = event.widget
        x = widget.winfo_x() - widget._drag_start_x + event.x
        y = widget.winfo_y() - widget._drag_start_y + event.y
        widget.place(x=x, y=y)

    #used to undo lines in the canvas
    def undo_btn(self):
        if self.single_line:
            line1 = self.single_line.pop()
            line2 = self.Pillow_line.pop()

            print("this is undo", line1)
            for segment in line1:
                self.cnv.delete(segment[0])
                for coord in segment[1]:
                    self.cnv.delete(coord)



    def update_brush_size(self):
        self.output_string.set(self.brush_width)

    def paint_stop(self, event):
        #print("button stop")
        self.single_line.append(self.Canvas_line.copy())
        print("paint stop line",self.Canvas_line)
        print("paint stop line 2", self.single_line)
        self.Canvas_line.clear()

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
        self.Pillow_line.append((pil_line,pil_int_line))

        # Update previous mouse position for next iteration
        self.prev_x, self.prev_y = x2, y2

        # Update last click time
        self.last_click_time = current_time

    def clear(self):
        self.cnv.delete("all")

        self.single_line.clear()
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
        self.update_colour(self.current_color)
        #print(self.current_color)
        #print(type(self.current_color))

    def update_colour(self, colour):
        self.label_colour.config(background=colour)

    def change_static_colour(self, colour):
        self.current_color = colour
        self.update_colour(self.current_color)

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

