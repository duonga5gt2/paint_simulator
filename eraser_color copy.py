class Eraser:
    def __init__(self, canvas, app):
        self.canvas = canvas
        self.app = app # Pass in the app the get the brush size

        
        self.canvas.bind("<B1-Motion>", self.track_erase)
        self.current_shape = None 
        self.shape_id = None
        
    def track_erase(self, event):
        try:
            self.shape_id = self.canvas.find_overlapping(event.x - self.app.brush_size, event.y - self.app.brush_size, event.x + self.app.brush_size, event.y + self.app.brush_size)[0]
            
            self.canvas.delete(self.shape_id)
        except IndexError:
            pass

    
        


# Backend for the color picker
class Color:
    def __init__(self, color='black') -> None:
        self.default_color = color

        
    def getColor(self):
        return self.default_color
    
    def setColor(self, color):
        self.default_color = color


#Backend for the Filler
class Filler:
    def __init__(self, canvas, app) -> None:
        self.canvas = canvas
        self.color = app # Pass in the app to use the same color picker

        self.canvas.bind("<Motion>", self.track)
        self.canvas.bind("<Button-1>", self.paint)
        self.current_shape = None 
        self.shape_id = None

    def track(self, event):
    
        try:
            self.shape_id = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)[0]
            
        except IndexError:
            pass

    
    def paint(self, event):
        if self.shape_id:
            self.canvas.itemconfig(self.shape_id, fill=self.color.chosen_color.getColor())