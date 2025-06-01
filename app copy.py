import tkinter as tk
from tkinter import PhotoImage
from shape import *
from eraser_color import *

class ButtonSettings:
    def __init__(self) -> None:
        self.height = 40
        self.width = 50
        
    def getPickerLayout(self):
        picker_layout = [["Line","Pen","Triangle","Rectangle","Oval"]]
        return picker_layout


    def getColorPickerLayout(self):
        color_picker_layout = [["Black","Gray", "Red", "Yellow"],
                               ["Green","Blue","Pink","Brown"]]
        return color_picker_layout
    
    def getImagesLayout(self):
        photos = [[PhotoImage(file="black.png"), PhotoImage(file="gray.png"), PhotoImage(file="red.png"), PhotoImage(file="yellow.png")],
                  [PhotoImage(file="green.png"), PhotoImage(file="blue.png"), PhotoImage(file="pink.png"), PhotoImage(file="brown.png")]]
        return photos


class Application(tk.Frame):
    def __init__(self, window_width, window_height, master=None):
        super().__init__(master)  
        self.master = master
        self.idTracker = [] # Track id to perform undo function
        
        
        self.chosen_color = Color() # Set default color
        self.brush_size = 5 # Set default brush size
        
        # Create a frame and place it in the window
        self.frame = tk.Frame(self.master, width=window_width, height=window_height)
        self.frame.pack()

        
        # Top frame
        self.top_frame = tk.Frame(self.frame, relief="raised", borderwidth=2 )
        self.top_frame.place(width=window_width, height=120, x=0, y=0)

        # Canvas
        self.canvas = tk.Canvas(self.frame, bg="white")
        self.canvas.place(x=0, y=100, width=window_width, height=900)

        
        # Color picker on the left (Frame)
        self.color_picker = tk.Frame(self.top_frame)
        self.color_picker.place(y=3, x=20, width=300, height=105)

        # Eraser and Filler (Frame)
        self.eraser = tk.Frame(self.top_frame)
        self.eraser.place(x=400, y=3, width=80, height=105)

        self.filler = tk.Frame(self.top_frame)
        self.filler.place(x=500, y=3, width=80, height=105)

        # Shapes and Pen (Frame)
        self.picker = tk.Frame(self.top_frame)
        self.picker.place(x=600, y=3, width=370, height=105)

        # Set up layout for Shapes and Pen Frame
        self.picker.grid_rowconfigure(0, weight=1)
        total_columns = 5  # Number of buttons
        for col in range(total_columns):
            self.picker.grid_columnconfigure(col, weight=1)

        # Set up layout for Color Picker Frame
        for r in range(2):  # Two rows
            self.color_picker.grid_rowconfigure(r, weight=1, minsize=50)
        for c in range(4):  # Four columns
            self.color_picker.grid_columnconfigure(c, weight=1, minsize=50)
        
        

        # Start putting in button
        buttonSettings = ButtonSettings()



        
        for r, row in enumerate(buttonSettings.getPickerLayout()):
            for c, val in enumerate(row):
                
            
                button = tk.Button(self.picker, text=f"{val}", command=lambda v=val: self.picker_on_button_click(v))
                
                button.grid(row=r, column=c, padx=1, pady=1, sticky='nsew')

       
        
        images_layout = buttonSettings.getImagesLayout()
        color_picker_layout = buttonSettings.getColorPickerLayout()

        
        for r, row in enumerate(images_layout):
            for c, img in enumerate(row):
                button = tk.Button(self.color_picker, image=img, relief="sunken", borderwidth=2, width=buttonSettings.width, height=buttonSettings.height, compound=tk.TOP, command=lambda color=color_picker_layout[r][c]: self.change_color(color))
                button.grid(row=r, column=c, padx=5, pady=5, sticky='nsew')

        
        self.image_references = images_layout




        # Set up Eraser button
        self.eraserImg=PhotoImage(file="output-onlinepngtools.png")
        self.eraser_button = tk.Button(self.eraser,  image=self.eraserImg,  borderwidth=2, command=self.eraser_action)
        self.eraser_button.place(x=0, y=0, relwidth=1, relheight=1)  # Make the button the same size as the frame

        # Set up Filler button
        self.fillImg = PhotoImage(file="fillFixed.png")
        self.filler_button = tk.Button(self.filler, image=self.fillImg, borderwidth=2, command=self.filler_action)
        self.filler_button.place(x=0, y=0, relwidth=1, relheight=1)        
        
        # Bind buttons
        self.master.bind("<Control-z>", self.undo) # Ctrl Z to undo
        self.master.bind("<Control-=>", self.increase_brush_size)  # Ctrl + to increase size
        self.master.bind("<Control-minus>", self.decrease_brush_size) # Ctrl - to decrease size

        # Cursor 
        self.value_cursor_dict = {"Line":"plus","Triangle":"dotbox", "Pen":"plus", "Rectangle":"dotbox", "Oval":"dotbox","Eraser":"circle", "Filler":"dotbox"}
        
        # Color list 
        self.color_list =  ["Black","Gray", "Red", "Yellow", "Green","Blue","Pink","Brown"]

        # Tools chosen
        self.current_tool= None


    def undo(self, event):
        '''UNDO FUNCTIONALITY'''
        if self.idTracker:
            
            last_line = self.idTracker.pop()
            if isinstance(last_line, list):
                for id in last_line:
                    self.canvas.delete(id)

            else:
                self.canvas.delete(last_line)
        print("Undo finished!")

    def picker_on_button_click(self, value):
        '''PICKING SHAPES AND PEN'''
        
        if value == "Line":
            self.unbind_tool()
            self.current_tool = LineDrawer(self.canvas, self.idTracker, self)
            self.change_cursor(value)
            
        elif value == "Pen":
            self.unbind_tool()
            self.current_tool = Pen(self.canvas, self.idTracker,self)
            self.change_cursor(value)
        elif value == "Triangle":
            self.unbind_tool()
            self.current_tool = Triangle(self.canvas, self.idTracker,self)
            self.change_cursor(value)
        elif value == "Rectangle":
            self.unbind_tool()
            self.current_tool = Rectangle(self.canvas, self.idTracker,self)
            self.change_cursor(value)
        elif value == "Oval":
            self.unbind_tool()
            self.current_tool = Oval(self.canvas, self.idTracker,self)
            self.change_cursor(value)

    def change_cursor(self, value):
        
        '''CHANGE CURSOR BASED ON TOOLS SELECTED'''
        for i in self.value_cursor_dict:
            if i == value:
                self.frame.config(cursor=self.value_cursor_dict.get(i))


    def change_color(self, color):
        '''COLOR CHANGING FOR COLOR PICKER'''
        for i in self.color_list:
            if i == color:
                self.chosen_color.setColor(color)

    def filler_action(self):
        '''INSTANTIATE FILLER'''
        last_key = list(self.value_cursor_dict.keys())[-1]
        self.frame.config(cursor=self.value_cursor_dict.get(last_key))
        self.unbind_tool()
        Filler(self.canvas, self)


    def eraser_action(self):
        '''INSTATIATE ERASER'''
        last_key = list(self.value_cursor_dict.keys())[-2]
        self.frame.config(cursor=self.value_cursor_dict.get(last_key))
        self.unbind_tool()
        Eraser(self.canvas, self)


    def unbind_tool(self):
        '''UNBIND PREVIOUS TOOLS'''
        if self.current_tool is not None:
            self.canvas.unbind("<ButtonPress-1>")
            self.canvas.unbind("<B1-Motion>")
            self.canvas.unbind("<ButtonRelease-1>")
            self.canvas.unbind("<Button-1>")
            self.canvas.unbind("<Motion>")
            

    def increase_brush_size(self, event):
        '''INCREASE BRUSH SIZE'''
        self.brush_size += 1
        print("Brush size:",self.brush_size)

    def decrease_brush_size(self, event):
        '''DECREASE BRUSH SIZE'''
        if self.brush_size > 0:
            self.brush_size -= 1

        print("Brush size:", self.brush_size)


if __name__ == '__main__':
    master = tk.Tk()
    master.title("Paint Simulator")
    window_width = 1000
    window_height = 1000
    # Define window size
    master.geometry(str(window_width) + 'x' + str(window_height))
    app = Application(window_width, window_height, master=master)
    app.mainloop()

    
    
