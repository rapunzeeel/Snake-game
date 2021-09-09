import tkinter as tk
from tkinter import Frame, BOTH


class MatrixtableGUI(Frame):
    def __init__(self):
        self.height = 500
        self.width = 450
        self.food = None
        self.rectangles = []
        self.rectangles_coordinates = []
        self.canvas = None
        self.show_window()

    def show_window(self):
        self.window_table = tk.Tk()
        self.window_table.title("Snake game")
        self.canvas = tk.Canvas(self.window_table, height=self.height, width=self.width)
        self.draw_table(0)

    def draw_table(self, score):
        for i in range(1, 450, 15):
            for j in range(1, 460, 15):
                self.canvas.create_line(i, j, 460, j)  # crtanje horizontalnih linija
                self.canvas.create_line(i, j, i, 450)  # crtanje vertikanih linija

        self.show_score(score)
        self.canvas.pack(fill=BOTH, expand=1)

    def show_score(self, score):
        labela = tk.Label(text="SCORE: " + str(score))
        labela.place(relx=0.62, rely=0.95, relwidth=0.2, relheight=0.05)
