import tkinter as tk
import random


class Minesweeper:
    def __init__(self, cols, rows, mines_quan):
        self.cols = cols
        self.rows = rows
        self.mines = mines_quan
        self.board = {}
        self.flags = set()
        self.revealed = set()
        self.is_first_click = True

    def generate_board(self,first_click_x,first_click_y):
        for j in range(0, self.rows):
            for i in range(0, self.cols ):
                self.board[(j, i)] = 0

        mines_quan_copy = int(self.mines)
        while mines_quan_copy:
            x = random.randint(0, self.rows-1)
            y = random.randint(0, self.cols-1)
            starting_safe_area=1
            is_in_safe_area = abs(x-first_click_x) <= starting_safe_area and abs(y-first_click_y) <= starting_safe_area
            if self.board[(x, y)] == 0 and not is_in_safe_area :
                self.board[(x, y)] = "x"
                mines_quan_copy -= 1
        self.neighbours()
    def neighbours(self):
        for x_cord in range(0, self.rows):
            for y_cord in range(0, self.cols):
                if self.board[(x_cord, y_cord)] == 0:
                    current_neighbour_mines = 0
                    for nx in range(x_cord - 1, x_cord + 2):
                        for ny in range(y_cord - 1, y_cord + 2):
                            if (nx, ny) in self.board and self.board[(nx,ny)] == "x":
                                current_neighbour_mines +=1
                    self.board[(x_cord, y_cord)] = current_neighbour_mines
    def flags_logic(self,x,y):
        if (x, y) in self.revealed:
            return
        if (x, y) in self.flags :
            self.flags.remove((x, y))
        else:
            self.flags.add((x,y))
    def reveal(self, x, y):
        if (x, y) in self.revealed or (x,y) in self.flags:
            return []
        if self.is_first_click:
            self.is_first_click = False
            self.generate_board(x,y)
        self.revealed.add((x,y))
        field = self.board[(x, y)]
        if field == "x":
            return [(x, y)]
        elif field > 0:
            return [(x, y)]
        else:
            newly_revealed = [(x, y)]
            stack = [(x, y)]
            while stack:
                current_x , current_y = stack.pop()
                for nx in range(current_x - 1, current_x + 2):
                    for ny in range(current_y - 1, current_y + 2):
                        if (nx, ny) in self.board and (nx,ny) not in self.flags and (nx,ny) not in self.revealed:
                            self.revealed.add((nx,ny))
                            newly_revealed.append((nx,ny))
                            if self.board[(nx, ny)] == 0:
                                stack.append((nx, ny))
            return newly_revealed
    def reveal_after_all_flags(self,x,y):
        flags_count=0
        this_field_mines=self.board[(x,y)]
        neighbors = []
        for nx in range(x - 1, x + 2):
            for ny in range(y - 1, y + 2):
                if (nx, ny) in self.board and (nx, ny) != (x, y):
                    neighbors.append((nx, ny))
                    if  (nx, ny) in self.flags:
                        flags_count += 1
        newly_revealed = []
        if this_field_mines == flags_count:
            for nx,ny in neighbors:
                if (nx, ny) not in self.flags and (nx, ny) not in self.revealed:
                    newly_revealed.extend(self.reveal(nx, ny))
        return newly_revealed







class MinesweeperInterface:
    def __init__(self, cols, rows, mines_quan):
        self.cols = cols
        self.rows = rows
        self.mines_quan = mines_quan
        self.logic = Minesweeper(cols, rows, mines_quan)
        self.window = tk.Tk()
        self.window.geometry("1050x800")
        self.window.title("Minesweeper")
        self.icons = {}
        self.buttons = {}
        self.time = 0
        self.timer_id= None
        self.game_over = False
        self.top_frame= None
        self.mines_label=None
        self.timer_label=None
        self.reset_button= None
        self.load_photos()
        self.create_top_panel()
        self.grid_generation()
    def load_photos(self):
        self.icons["empty"] = tk.PhotoImage(file="../icons/full_gray.png")
        self.icons["numbers"] = [tk.PhotoImage(file="../icons/"+str(i) + ".png") for i in range(1, 9)]
        self.icons["mine"] = tk.PhotoImage(file="../icons/mine.png")
        self.icons["first_mine"] = tk.PhotoImage(file="../icons/first_mine.png")
        self.icons["flag"] = tk.PhotoImage(file="../icons/flag.png")
    def create_top_panel(self):
        self.top_frame = tk.Frame(self.window, bg="silver", relief="raised", bd=3)
        self.top_frame.grid(row=0, column=0, columnspan=self.cols, sticky="ew")
        self.mines_label = tk.Label(self.top_frame, bg="black", fg="red", font=("Arial", 30, "bold"), width=4)
        self.mines_label.pack(side="left", padx=10, pady=10)
        self.update_mines_display_number()

        self.timer_label = tk.Label(self.top_frame, text="000", bg="black", fg="red", font=("Arial", 30, "bold"),
                                    width=4)
        self.timer_label.pack(side="right", padx=10, pady=10)
        self.reset_button = tk.Button(self.top_frame, text="Reset", font=("Arial", 14, "bold"), command=self.reset_game)
        self.reset_button.pack(side="left", expand=True)

        self.act_time()
    def update_mines_display_number(self):
        self.mines_label.config(text=str(self.logic.mines).zfill(3))
    def act_time(self):
        self.time += 1
        self.timer_label.config(text=str(self.time).zfill(3))
        self.timer_id = self.window.after(1000, self.act_time)

    def grid_generation(self):
        for i in range(self.cols):
            self.window.columnconfigure(i, minsize=35)
        for j in range(self.rows):
            self.window.rowconfigure(j + 1 , minsize=35)
        for row in range(0, self.rows):
            for col in range(0,self.cols):
                button  = tk.Button(self.window, image=self.icons["empty"])
                button.grid(row = row + 1, column=col, sticky="nsew")
                self.buttons[(row, col)] = button
                button.bind('<Button-1>',lambda event,x = row,y=col: self.on_left_click(x, y))
                button.bind('<Button-3>', lambda event,x = row,y =col: self.on_right_click(x, y))
    def on_left_click(self,x,y):
        if self.game_over or (x,y) in self.logic.flags:
            return
        if (x, y) in self.logic.revealed:
            newly_revealed= self.logic.reveal_after_all_flags(x, y)
        else:
            newly_revealed = self.logic.reveal(x, y)
        for (rx, ry) in newly_revealed:
            button = self.buttons[(rx, ry)]
            field_value = self.logic.board[(rx, ry)]
            if field_value == "x":
                button.config(image=self.icons["first_mine"])
                self.game_lost()
            elif field_value > 0:
                button.config(image=self.icons["numbers"][field_value - 1])
            else:
                button.config(image="", relief="sunken", bg="lightgray")
        if not self.game_over:
            self.check_win()
    def on_right_click(self,x,y):
        if self.game_over or (x, y) in self.logic.revealed:
            return

        self.logic.flags_logic(x, y)
        button = self.buttons[(x, y)]

        if (x, y) in self.logic.flags:
            button.config(image=self.icons["flag"])
            self.logic.mines-=1
        else:
            button.config(image=self.icons["empty"])
            self.logic.mines+=1

        self.update_mines_display_number()

    def check_win(self):
        all_safe_fields= (self.rows*self.cols)-int(self.mines_quan)
        if len(self.logic.revealed) == all_safe_fields:
            self.game_won()
    def game_won(self):
        self.game_over=True
        if self.timer_id is not None:
            self.window.after_cancel(self.timer_id)
        self.reset_button.config(text="Wygrana!", bg="lightgreen")
        for (x, y), value in self.logic.board.items():
            if value == "x" and (x, y) not in self.logic.flags:
                self.buttons[(x, y)].config(image=self.icons["flag"])
        self.logic.mines = 0
        self.update_mines_display_number()

    def game_lost(self):
        self.game_over = True

        if self.timer_id is not None:
            self.window.after_cancel(self.timer_id)

        self.reset_button.config(text="Game Over", bg="salmon")


        for (x, y), value in self.logic.board.items():
            if value == "x" and (x, y) not in self.logic.flags:
                if self.buttons[(x, y)].cget("image") != str(self.icons["first_mine"]):
                    self.buttons[(x, y)].config(image=self.icons["mine"])

    def reset_game(self):
        if self.timer_id is not None:
            self.window.after_cancel(self.timer_id)

        self.logic=Minesweeper(self.cols, self.rows, self.mines_quan)


        self.game_over=False
        self.time=0
        self.timer_label.config(text="000")

        self.reset_button.config(text="Reset", bg="SystemButtonFace")
        self.update_mines_display_number()

        for (x, y), btn in self.buttons.items():
            btn.config(image=self.icons["empty"], relief="raised", bg="SystemButtonFace")


        self.act_time()
if __name__ == '__main__':
    game = MinesweeperInterface(cols=30, rows=20, mines_quan=100)
    game.window.mainloop()





