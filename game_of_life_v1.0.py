import random
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk

class GameOfLife:
    def __init__(self, rows, cols, cell_size, life_color, death_color):
        # Initialize the simulation with the given number of rows and columns
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        
        # Initialize the colors to be used for drawing the cells
        self.life_color = life_color
        self.death_color = death_color
        
        # Initialize the cells to be a 2D list of rows and columns
        self.cells = [[False for _ in range(cols)] for _ in range(rows)]
        
    def reset(self):
        # Set the state of each cell to either alive or dead randomly, with a probability of 8%
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j] = random.random() < 0.08
    
    def get_life_neighbors(self, i, j):
        # Return the number of live neighbors for the cell at the given row and column
        n = 0
        for x in range(i-1, i+2):
            for y in range(j-1, j+2):
                if x == i and y == j:
                    continue
                x %= self.rows
                y %= self.cols
                if self.cells[x][y]:
                    n += 1
        return n
    
    def update(self):
        # Update the state of each cell using bitwise operations
        new_cells = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                n = self.get_life_neighbors(i, j)
                if self.cells[i][j]:
                    new_cells[i][j] = n == 2 or n == 3
                else:
                    new_cells[i][j] = n == 3
        self.cells = new_cells
    
    def draw(self, canvas):
        # Create an image of the cells
        image = Image.new("RGB", (self.cols*self.cell_size, self.rows*self.cell_size))
        draw = ImageDraw.Draw(image)
        for i in range(self.rows):
            for j in range(self.cols):
                color = self.life_color if self.cells[i][j] else self.death_color
                x1, y1 = j*self.cell_size, i*self.cell_size
                x2, y2 = x1+self.cell_size, y1+self.cell_size
                draw.rectangle((x1, y1, x2, y2), fill=color)
        
        # Convert the image to a PhotoImage object and draw it on the canvas
        photo_image = ImageTk.PhotoImage(image)
        canvas.create_image((0, 0), image=photo_image, anchor=tk.NW)
        canvas.photo_image = photo_image

class GameOfLifeGUI:
    def __init__(self, game):
        # Initialize the GUI with the given game instance
        self.game = game
        
        self.root = tk.Tk()
        self.root.title("Game of Life")
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(self.root, width=self.game.cols*self.game.cell_size, height=self.game.rows*self.game.cell_size)
        self.canvas.pack()
        
        self.root.bind("<Button-1>", self.on_click)
        
        self.update()
    
    def on_click(self, event):
        # Reset the game when the canvas is clicked
        self.game.reset()
        self.update()
    
    def update(self):
        # Update and draw the game, and schedule the next update
        self.game.update()
        self.game.draw(self.canvas)
        self.root.after(1000, self.update)

# Create a new game with 40 rows, 50 columns, and cell size 10 pixels
game = GameOfLife(40, 50, 10, "#6EAE0D", "#DFFF96")
# Create a new GUI for the game
gui = GameOfLifeGUI(game)
# Run the Tkinter event loop
gui.root.mainloop()
