import tkinter as tk
import random



class MinesweeperApp:
    def __init__(self,cols,rows,mines_quan):
        self.mines_label = None
        self.cols = cols
        self.rows = rows
        self.mines = mines_quan
        self.time = 0

        self.window = tk.Tk()
        self.window.geometry("1150x900")
        self.window.title("Minesweeper")
        self.mines_and_numbers = Board(self.cols,self.rows,self.mines)
        self.mines_and_numbers.generate_board()
        self.mines_and_numbers.neighbours()
        self.mouse = Mouse(self,self.mines_and_numbers)
        self.buttons = []
        self.buttons_coordinates = {}
        self.icons = {}
    def photos(self):
        self.icons["puste"] = tk.PhotoImage(file="unnamed.png")
        self.icons["face"] = [tk.PhotoImage(file="buzka" + str(i) + ".png") for i in range(1, 5)]
        self.icons["numbers"] = [tk.PhotoImage(file=str(i) + ".png") for i in range(1, 8)]
        self.icons["mines"] = tk.PhotoImage(file="mina.png")
        self.icons["mines1"] = tk.PhotoImage(file="pierwsza.png")
        self.icons["flag"] = tk.PhotoImage(file="flaga.png")
    def act_time(self):
        self.time = self.time + 1
        self.timer.config(text=str(self.time))
        self.window.after(1000, self.act_time)
    def mines_number(self):
        self.mines_label["text"] = str(self.mines).zfill(3)
    def window_upper_panel(self):
        face = tk.Button(self.window, width=2, height=1)
        face.grid(row=0, column=self.cols // 2 - 1, columnspan=3, pady=30)
        self.timer = tk.Label(self.window, bg="black", fg="red", font=("Arial", 40))
        self.timer.grid(row=0, column=self.cols - 1, columnspan=7, ipadx=10, pady=30)
        self.act_time()
        self.mines_label = tk.Label(self.window, bg="black", fg="white", font=("Arial", 40))
        self.mines_number()
        self.mines_label.grid(row=0, column=0, columnspan=7, ipadx=10, pady=30)
    def buttons_generation(self):
        for i in range(self.cols):
            self.window.columnconfigure(i+1, minsize=35)
        for j in range(self.rows):
            self.window.rowconfigure(j , minsize=35)
        self.window.grid_columnconfigure(0, weight=0, minsize=50)
        for j in range(1, self.rows+1):
            for i in range(1,self.cols+1):
                    b = tk.Button(self.window)
                    b.grid(row=j, column=i, padx=0, pady=0, sticky="nsew")
                    self.buttons.append(b)
                    self.buttons_coordinates[(j,i)] = b
                    b.bind('<Button-1>',lambda event,act_button=b,c=j,z=i:self.mouse.left_click(act_button,c,z))
                    b.bind('<Button-3>', lambda event,act_button=b,c=j,z=i: self.mouse.right_click(act_button,c,z))



class Board:
    def __init__(self,cols,rows,mines_quan):
        self.cols = cols
        self.rows = rows
        self.mines = mines_quan
        self.mines_and_numbers = {}
    def generate_board(self):
        for j in range(1, self.rows + 1):
            for i in range(1, self.cols + 1):
                self.mines_and_numbers[(j, i)] = 0
        l_mines = int(self.mines)
        while l_mines:
            x = random.randint(1, self.rows)
            y = random.randint(1, self.cols)
            if self.mines_and_numbers[(x, y)] == 0:
                self.mines_and_numbers[(x, y)] = "x"
                l_mines -= 1
    def neighbours(self):
        for x_cord in range(1, self.rows + 1):
            for y_cord in range(1, self.cols + 1):
                if self.mines_and_numbers[(x_cord, y_cord)] == 0:
                    cur_mines = 0
                    for m in range(x_cord - 1, x_cord + 2):
                        for z in range(y_cord - 1, y_cord + 2):
                            if (m, z) in self.mines_and_numbers:
                                if self.mines_and_numbers[(m, z)] == "x":
                                    cur_mines = cur_mines + 1
                    self.mines_and_numbers[(x_cord, y_cord)] = cur_mines





class Mouse:
    def __init__(self,minesweeper_app,board):
        self.minesweeper = minesweeper_app
        self.board = board
        self.flags_numbers = None
        self.cols = self.board.cols
        self.rows = self.board.rows
        self.mines = self.board.mines
        self.zeros = []
        self.not_zeros = []
        self.visited = set()
        self.visited_zeros = set()
        self.cliks=0
        self.flags_cords = {}
    def checking_for_zeros(self, x, y, positives_zeros, negative_zeros, visited_zeros, visited_not_zeros):
        for m in range(x - 1, x + 2):
            for z in range(y - 1, y + 2):
                if (m, z) in visited_zeros:
                    continue
                elif (m, z) in self.board.mines_and_numbers:
                    if self.board.mines_and_numbers[(m, z)] == 0:
                        positives_zeros.append((m, z))
                        visited_zeros.add((m, z))
                    else:
                        if (m, z) in self.board.mines_and_numbers and (m, z) not in visited_not_zeros:
                            if self.board.mines_and_numbers[(m, z)] != "x":
                                negative_zeros.append((m, z))
                                visited_not_zeros.add((m, z))
                else:
                    visited_zeros.add((m, z))
    def button_clicking_showing(self, x, y):
        self.flags_numbers = 0
        for m in range(x - 1, x + 2):
            for z in range(y - 1, y + 2):
                if (m, z) in self.flags_cords:
                    if self.flags_cords[(m, z)] == "1":
                        self.flags_numbers += 1
        if self.flags_numbers == self.board.mines_and_numbers[(x, y)] and self.flags_numbers != 0:
            return True
        return None
    def left_click(self,button,x,y):
        if self.cliks == 0:
            for m in range(x - 1, x + 2):
                for z in range(y - 1, y + 2):
                    self.board.mines_and_numbers[(m, z)] = 0
            self.board.neighbours()
            self.cliks = 1
        if self.board.mines_and_numbers[(x, y)] == "x":
            button["image"] = self.minesweeper.icons["mines"]
            return
        else:
            self.checking_for_zeros(x, y, self.zeros, self.not_zeros, self.visited, self.visited_zeros)
            if self.board.mines_and_numbers[(x, y)] == 0:
                button["image"] = self.minesweeper.icons["puste"]
                while self.zeros:
                    self.checking_for_zeros(self.zeros[0][0], self.zeros[0][1], self.zeros, self.not_zeros, self.visited, self.visited_zeros)
                    b = self.minesweeper.buttons_coordinates[self.zeros[0]]
                    b["image"] = self.minesweeper.icons["puste"]
                    del self.zeros[0]
                while self.not_zeros:
                    b1 = self.minesweeper.buttons_coordinates[self.not_zeros[0]]
                    b1["image"] = self.minesweeper.icons["numbers"][self.board.mines_and_numbers[self.not_zeros[0]] - 1]
                    del self.not_zeros[0]
            else:
                button["image"] = self.minesweeper.icons["numbers"][self.board.mines_and_numbers[(x, y)] - 1]
        if self.button_clicking_showing(x, y):
            for m in range(x - 1, x + 2):
                for z in range(y - 1, y + 2):
                    if (m, z) in self.board.mines_and_numbers:
                        if self.board.mines_and_numbers[(m, z)] != "x":
                            b = self.minesweeper.buttons_coordinates[(m, z)]
                            if self.board.mines_and_numbers[(m, z)] == 0:
                                b["image"] = self.minesweeper.icons["puste"]
                            else:
                                b["image"] = self.minesweeper.icons["numbers"][self.board.mines_and_numbers[(m, z)] - 1]

    def right_click(self,button,x,y):
        if button.cget("image") == "":
            button['image'] = self.minesweeper.icons["flag"]
            self.minesweeper.mines =int(self.minesweeper.mines)-1
            self.flags_cords[(x, y)] = "1"

        elif button.cget("image") == self.minesweeper.icons["flag"].name:
            button['image'] = ""
            self.minesweeper.mines =int(self.minesweeper.mines)+1
            self.flags_cords[(x, y)] = ""
        self.minesweeper.mines_number()


if __name__ == '__main__':
    game = MinesweeperApp(cols=30,rows=20,mines_quan="100")
    game.photos()
    game.window_upper_panel()
    game.buttons_generation()




    game.window.mainloop()
