class Oval:
    def __init__(self, canvas, idTracker, app) -> None:
        self.canvas = canvas 
        self.idTracker = idTracker # Pass in to use the same id tracking list
        
        self.startX = None
        self.startY = None
        self.circle = None
        self.app = app # Pass in the app to use the same color picker
        self.canvas.bind("<ButtonPress-1>", self.mouse_left_button_press)
        self.canvas.bind("<B1-Motion>", self.mouse_move_left_button_press)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_left_release)


    def mouse_left_button_press(self, event):
        self.startX = event.x
        self.startY = event.y


        self.circle = self.canvas.create_oval(self.startX , self.startY , event.x , event.y , fill='', outline=self.app.chosen_color.getColor(), width=self.app.brush_size)


    def mouse_move_left_button_press(self,event):

        if self.circle:
            # Modify the existing oval without deleting it
            self.canvas.coords(self.circle, self.startX, self.startY, event.x, event.y)



    def mouse_left_release(self, event):
        if self.circle:
            self.idTracker.append(self.circle)
            self.circle = None

class Rectangle: 
    def __init__(self, canvas, idTracker, app):
        self.canvas = canvas
        self.idTracker = idTracker # Pass in to use the same id tracking list
        
        self.startX = None
        self.startY = None
        self.app = app # Pass in the app to use the same color picker
        self.rec = None
        self.canvas.bind("<ButtonPress-1>", self.mouse_left_button_press)
        self.canvas.bind("<B1-Motion>", self.mouse_move_left_button_press)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_left_release)
    def mouse_left_button_press(self, event):
        self.startX = event.x
        self.startY = event.y


        self.rec = self.canvas.create_rectangle(self.startX, self.startY, event.x, event.y, fill='', width=self.app.brush_size)

    def mouse_move_left_button_press(self,event):

        if self.rec:
            self.canvas.delete(self.rec)
            self.rec = self.canvas.create_rectangle(self.startX, self.startY, event.x, event.y, fill='', outline=self.app.chosen_color.getColor(), width = self.app.brush_size)


    def mouse_left_release(self, event):
        if self.rec:
            self.idTracker.append(self.rec)
            self.rec = None
            


       




class Triangle:
    def __init__(self, canvas, idTracker, app) -> None:
        self.pointID = []
        self.triangleID = []
        self.point_coordinate = []
        
        self.idTracker = idTracker # Pass in to use the same id tracking list
        self.canvas = canvas
        self.startX = None
        self.startY = None
        self.dot = None
        self.triangle = None

        self.app = app # Pass in the app to use the same color picker
        self.canvas.bind("<ButtonPress-1>", self.mouse_left_button_press)
        

    def mouse_left_button_press(self, event):
        self.startX = event.x
        self.startY = event.y

        self.point_coordinate.append(self.startX)
        self.point_coordinate.append(self.startY)

        
        

        if len(self.pointID) <= 1:
            self.dot = self.canvas.create_oval(self.startX - 2, self.startY - 2, event.x + 2, event.y + 2, fill = 'yellow')
            self.pointID.append(self.dot)
            
        else:
            for i in self.pointID:
                self.canvas.delete(i)
            
            self.pointID = []    

            self.triangle = self.canvas.create_polygon(self.point_coordinate[0], self.point_coordinate[1], self.point_coordinate[2], self.point_coordinate[3], self.point_coordinate[4], self.point_coordinate[5], fill = '', outline = self.app.chosen_color.getColor(), width=self.app.brush_size)
            
            self.point_coordinate = []

            self.triangleID.append(self.triangle)
            
            self.startX = None
            self.startY = None
            self.dot = None
            self.triangle = None

            self.idTracker.append(self.triangleID)
            self.triangleID = []



class LineDrawer:
    def __init__(self, canvas, idTracker, app):
        self.canvas = canvas
        self.startX = None
        self.startY = None
        self.current_line = None
        self.idTracker = idTracker # Pass in to use the same id tracking list
        self.app = app # Pass in the app to use the same color picker
        
        self.canvas.bind("<ButtonPress-1>", self.mouse_left_button_press)
        self.canvas.bind("<B1-Motion>", self.mouse_move_left_button_press)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_left_release)

    def mouse_left_button_press(self, event):
        self.startX = event.x
        self.startY = event.y

        self.current_line = self.canvas.create_line(self.startX, self.startY, event.x, event.y,fill=self.app.chosen_color.getColor(), width=self.app.brush_size)

        

    def mouse_move_left_button_press(self, event):
        if self.current_line:
            self.canvas.delete(self.current_line)
            self.current_line = self.canvas.create_line(self.startX, self.startY, event.x, event.y, fill=self.app.chosen_color.getColor(), width=self.app.brush_size)

        

    def mouse_left_release(self, event):
        if self.current_line:
            self.idTracker.append(self.current_line)
            self.current_line = None

        



class Pen:
    def __init__(self, canvas, idTracker, app):
        self.canvas = canvas
        self.startX = None
        self.startY = None
        self.current_line = None
        self.idTracker = idTracker # Pass in to use the same id tracking list
        self.id = []
        

        self.app = app # Pass in the app to use the same color picker
        # Bind mouse events to canvas for line drawing
        self.canvas.bind("<ButtonPress-1>", self.mouse_left_button_press)
        self.canvas.bind("<B1-Motion>", self.mouse_move_left_button_press)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_left_release)

    def mouse_left_button_press(self, event):

        self.id = []
        self.startX = event.x
        self.startY = event.y

        

        

    def mouse_move_left_button_press(self, event):
        
        if self.startX is not None and self.startY is not None:
            # Create line segments between previous and current mouse position
            self.current_line = self.canvas.create_line(self.startX, self.startY, event.x, event.y, fill = self.app.chosen_color.getColor(), width=self.app.brush_size)
            
            
            # Track the line segment
            self.id.append(self.current_line)
            

            
            # Update startX and startY to current position for continuous drawing
            self.startX = event.x
            self.startY = event.y

            

    def mouse_left_release(self, event):
        self.startX = None
        self.startY = None
       


        self.idTracker.append(self.id)

        